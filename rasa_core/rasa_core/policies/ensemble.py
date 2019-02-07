import sys
from collections import defaultdict

import json
import logging
import numpy as np
import os
from datetime import datetime
from typing import Text, Optional, Any, List, Dict, Tuple

import rasa_core
from rasa_core import utils, training, constants
from rasa_core.actions.action import ACTION_LISTEN_NAME
from rasa_core.domain import Domain
from rasa_core.events import SlotSet, ActionExecuted, ActionExecutionRejected
from rasa_core.exceptions import UnsupportedDialogueModelError
from rasa_core.featurizers import MaxHistoryTrackerFeaturizer
from rasa_core.policies import Policy
from rasa_core.policies.fallback import FallbackPolicy
from rasa_core.policies.memoization import (
    MemoizationPolicy,
    AugmentedMemoizationPolicy)
from rasa_core.trackers import DialogueStateTracker

logger = logging.getLogger(__name__)


class PolicyEnsemble(object):
    def __init__(self,
                 policies: List[Policy],
                 action_fingerprints: Optional[Dict] = None) -> None:
        self.policies = policies
        self.training_trackers = None
        self.date_trained = None

        if action_fingerprints:
            self.action_fingerprints = action_fingerprints
        else:
            self.action_fingerprints = {}

    @staticmethod
    def _training_events_from_trackers(training_trackers):
        events_metadata = defaultdict(set)

        for t in training_trackers:
            tracker = t.init_copy()
            for event in t.events:
                tracker.update(event)
                if not isinstance(event, ActionExecuted):
                    action_name = tracker.latest_action_name
                    events_metadata[action_name].add(event)

        return events_metadata

    def train(self,
              training_trackers: List[DialogueStateTracker],
              domain: Domain, **kwargs: Any) -> None:
        if training_trackers:
            for policy in self.policies:
                policy.train(training_trackers, domain, **kwargs)
        else:
            logger.info("Skipped training, because there are no "
                        "training samples.")
        self.training_trackers = training_trackers
        self.date_trained = datetime.now().strftime('%Y%m%d-%H%M%S')

    def probabilities_using_best_policy(self,
                                        tracker: DialogueStateTracker,
                                        domain: Domain
                                        ) -> Tuple[List[float], Text]:
        raise NotImplementedError

    def _max_histories(self):
        # type: () -> List[Optional[int]]
        """Return max history."""

        max_histories = []
        for p in self.policies:
            if isinstance(p.featurizer, MaxHistoryTrackerFeaturizer):
                max_histories.append(p.featurizer.max_history)
            else:
                max_histories.append(None)
        return max_histories

    @staticmethod
    def _create_action_fingerprints(training_events):
        """Fingerprint each action using the events it created during train.

        This allows us to emit warnings when the model is used
        if an action does things it hasn't done during training."""
        if not training_events:
            return None

        action_fingerprints = {}
        for k, vs in training_events.items():
            slots = list({v.key for v in vs if isinstance(v, SlotSet)})
            action_fingerprints[k] = {"slots": slots}
        return action_fingerprints

    def _persist_metadata(self,
                          path: Text,
                          dump_flattened_stories: bool = False) -> None:
        """Persists the domain specification to storage."""

        # make sure the directory we persist to exists
        domain_spec_path = os.path.join(path, 'policy_metadata.json')
        training_data_path = os.path.join(path, 'stories.md')
        utils.create_dir_for_file(domain_spec_path)

        policy_names = [utils.module_path_from_instance(p)
                        for p in self.policies]

        training_events = self._training_events_from_trackers(
            self.training_trackers)

        action_fingerprints = self._create_action_fingerprints(training_events)

        metadata = {
            "action_fingerprints": action_fingerprints,
            "rasa_core": rasa_core.__version__,
            "python": ".".join([str(s) for s in sys.version_info[:3]]),
            "max_histories": self._max_histories(),
            "ensemble_name": self.__module__ + "." + self.__class__.__name__,
            "policy_names": policy_names,
            "trained_at": self.date_trained
        }

        utils.dump_obj_as_json_to_file(domain_spec_path, metadata)

        # if there are lots of stories, saving flattened stories takes a long
        # time, so this is turned off by default
        if dump_flattened_stories:
            training.persist_data(self.training_trackers, training_data_path)

    def persist(self, path: Text, dump_flattened_stories: bool = False) -> None:
        """Persists the policy to storage."""

        self._persist_metadata(path, dump_flattened_stories)

        for i, policy in enumerate(self.policies):
            dir_name = 'policy_{}_{}'.format(i, type(policy).__name__)
            policy_path = os.path.join(path, dir_name)
            policy.persist(policy_path)

    @classmethod
    def load_metadata(cls, path):
        metadata_path = os.path.join(path, 'policy_metadata.json')
        metadata = json.loads(utils.read_file(os.path.abspath(metadata_path)))
        return metadata

    @staticmethod
    def ensure_model_compatibility(metadata, version_to_check=None):
        from packaging import version

        if version_to_check is None:
            version_to_check = constants.MINIMUM_COMPATIBLE_VERSION

        model_version = metadata.get("rasa_core", "0.0.0")
        if version.parse(model_version) < version.parse(version_to_check):
            raise UnsupportedDialogueModelError(
                "The model version is to old to be "
                "loaded by this Rasa Core instance. "
                "Either retrain the model, or run with"
                "an older version. "
                "Model version: {} Instance version: {} "
                "Minimal compatible version: {}"
                "".format(model_version, rasa_core.__version__,
                          version_to_check),
                model_version)

    @classmethod
    def load(cls, path: Text) -> 'PolicyEnsemble':
        """Loads policy and domain specification from storage"""

        metadata = cls.load_metadata(path)
        cls.ensure_model_compatibility(metadata)
        policies = []
        for i, policy_name in enumerate(metadata["policy_names"]):
            policy_cls = utils.class_from_module_path(policy_name)
            dir_name = 'policy_{}_{}'.format(i, policy_cls.__name__)
            policy_path = os.path.join(path, dir_name)
            policy = policy_cls.load(policy_path)
            policies.append(policy)
        ensemble_cls = utils.class_from_module_path(
            metadata["ensemble_name"])
        fingerprints = metadata.get("action_fingerprints", {})
        ensemble = ensemble_cls(policies, fingerprints)
        return ensemble

    @classmethod
    def from_dict(cls, dictionary: Dict[Text, Any]) -> List[Policy]:

        policies = []

        for policy in dictionary.get('policies', []):

            policy_name = policy.pop('name')
            if policy.get('featurizer'):
                featurizer_func, featurizer_config = \
                    cls.get_featurizer_from_dict(policy)

                if featurizer_config.get('state_featurizer'):
                    state_featurizer_func, state_featurizer_config = \
                        cls.get_state_featurizer_from_dict(
                            featurizer_config)

                    # override featurizer's state_featurizer
                    # with real state_featurizer class
                    featurizer_config['state_featurizer'] = (
                        state_featurizer_func(**state_featurizer_config)
                    )

                # override policy's featurizer with real featurizer class
                policy['featurizer'] = featurizer_func(**featurizer_config)

            constr_func = utils.class_from_module_path(policy_name)
            policy_object = constr_func(**policy)

            policies.append(policy_object)

        return policies

    @classmethod
    def get_featurizer_from_dict(cls, policy):
        # policy can have only 1 featurizer
        if len(policy['featurizer']) > 1:
            raise InvalidPolicyConfig(
                "policy can have only 1 featurizer")
        featurizer_config = policy['featurizer'][0]
        featurizer_name = featurizer_config.pop('name')
        featurizer_func = utils.class_from_module_path(featurizer_name)

        return featurizer_func, featurizer_config

    @classmethod
    def get_state_featurizer_from_dict(cls, featurizer_config):
        # featurizer can have only 1 state featurizer
        if len(featurizer_config['state_featurizer']) > 1:
            raise InvalidPolicyConfig(
                "featurizer can have only 1 state featurizer")
        state_featurizer_config = (
            featurizer_config['state_featurizer'][0]
        )
        state_featurizer_name = state_featurizer_config.pop('name')
        state_featurizer_func = utils.class_from_module_path(
            state_featurizer_name)

        return state_featurizer_func, state_featurizer_config

    def continue_training(self,
                          trackers: List[DialogueStateTracker],
                          domain: Domain,
                          **kwargs: Any) -> None:

        self.training_trackers.extend(trackers)
        for p in self.policies:
            p.continue_training(self.training_trackers, domain, **kwargs)


class SimplePolicyEnsemble(PolicyEnsemble):

    @staticmethod
    def is_not_memo_policy(best_policy_name):
        is_memo = best_policy_name.endswith(
            "_" + MemoizationPolicy.__name__)
        is_augmented = best_policy_name.endswith(
            "_" + AugmentedMemoizationPolicy.__name__)
        return not (is_memo or is_augmented)

    def probabilities_using_best_policy(self,
                                        tracker: DialogueStateTracker,
                                        domain: Domain
                                        ) -> Tuple[List[float], Text]:
        result = None
        max_confidence = -1
        best_policy_name = None

        for i, p in enumerate(self.policies):
            probabilities = p.predict_action_probabilities(tracker, domain)
            if isinstance(tracker.events[-1], ActionExecutionRejected):
                probabilities[domain.index_for_action(
                    tracker.events[-1].action_name)] = 0.0
            confidence = np.max(probabilities)
            if confidence > max_confidence:
                max_confidence = confidence
                result = probabilities
                best_policy_name = 'policy_{}_{}'.format(i, type(p).__name__)

        if (result.index(max_confidence) ==
                domain.index_for_action(ACTION_LISTEN_NAME) and
                tracker.latest_action_name == ACTION_LISTEN_NAME and
                self.is_not_memo_policy(best_policy_name)):
            # Trigger the fallback policy when ActionListen is predicted after
            # a user utterance. This is done on the condition that:
            # - a fallback policy is present,
            # - there was just a user message and the predicted
            #   action is action_listen by a policy
            #   other than the MemoizationPolicy

            fallback_idx_policy = [(i, p) for i, p in enumerate(self.policies)
                                   if isinstance(p, FallbackPolicy)]

            if fallback_idx_policy:
                fallback_idx, fallback_policy = fallback_idx_policy[0]

                logger.debug("Action 'action_listen' was predicted after "
                             "a user message using {}. "
                             "Predicting fallback action: {}"
                             "".format(best_policy_name,
                                       fallback_policy.fallback_action_name))

                result = fallback_policy.fallback_scores(domain)
                best_policy_name = 'policy_{}_{}'.format(
                    fallback_idx,
                    type(fallback_policy).__name__)

        # normalize probablilities
        if np.sum(result) != 0:
            result = result / np.nansum(result)

        logger.debug("Predicted next action using {}"
                     "".format(best_policy_name))
        return result, best_policy_name


class InvalidPolicyConfig(Exception):
    """Exception that can be raised when policy config is not valid."""
    pass
