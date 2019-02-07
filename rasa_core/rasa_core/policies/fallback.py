import json
import logging
import os
from typing import Any, List, Text

from rasa_core import utils
from rasa_core.constants import FALLBACK_SCORE
from rasa_core.domain import Domain
from rasa_core.policies.policy import Policy
from rasa_core.trackers import DialogueStateTracker

logger = logging.getLogger(__name__)


class FallbackPolicy(Policy):
    """Policy which predicts fallback actions.

    A fallback can be triggered by a low confidence score on a
    NLU prediction or by a low confidence score on an action
    prediction. """

    @staticmethod
    def _standard_featurizer():
        return None

    def __init__(self,
                 nlu_threshold: float = 0.3,
                 core_threshold: float = 0.3,
                 fallback_action_name: Text = "action_default_fallback"
                 ) -> None:
        """Create a new Fallback policy.

        Args:
            core_threshold: if NLU confidence threshold is met,
                predict fallback action with confidence `core_threshold`.
                If this is the highest confidence in the ensemble,
                the fallback action will be executed.
            nlu_threshold: minimum threshold for NLU confidence.
                If intent prediction confidence is lower than this,
                predict fallback action with confidence 1.0.
            fallback_action_name: name of the action to execute as a fallback
        """

        super(FallbackPolicy, self).__init__()

        self.nlu_threshold = nlu_threshold
        self.core_threshold = core_threshold
        self.fallback_action_name = fallback_action_name

    def train(self,
              training_trackers: List[DialogueStateTracker],
              domain: Domain,
              **kwargs: Any
              ) -> None:
        """Does nothing. This policy is deterministic."""

        pass

    def should_fallback(self,
                        nlu_confidence: float,
                        last_action_name: Text
                        ) -> bool:
        """It should predict fallback action only if
        a. predicted NLU confidence is lower than ``nlu_threshold`` &&
        b. last action is NOT fallback action
        """
        return (nlu_confidence < self.nlu_threshold and
                last_action_name != self.fallback_action_name)

    def fallback_scores(self, domain, fallback_score=FALLBACK_SCORE):
        """Prediction scores used if a fallback is necessary."""

        result = [0.0] * domain.num_actions
        idx = domain.index_for_action(self.fallback_action_name)
        result[idx] = fallback_score
        return result

    def predict_action_probabilities(self,
                                     tracker: DialogueStateTracker,
                                     domain: Domain) -> List[float]:
        """Predicts a fallback action if NLU confidence is low
            or no other policy has a high-confidence prediction"""

        nlu_data = tracker.latest_message.parse_data

        # if NLU interpreter does not provide confidence score,
        # it is set to 1.0 here in order
        # to not override standard behaviour
        nlu_confidence = nlu_data["intent"].get("confidence", 1.0)

        if tracker.latest_action_name == self.fallback_action_name:
            result = [0.0] * domain.num_actions
            idx = domain.index_for_action('action_listen')
            result[idx] = FALLBACK_SCORE

        elif self.should_fallback(nlu_confidence, tracker.latest_action_name):
            logger.debug("NLU confidence {} is lower "
                         "than NLU threshold {}. "
                         "Predicting fallback action: {}"
                         "".format(nlu_confidence, self.nlu_threshold,
                                   self.fallback_action_name))
            # we set this to 1.1 to make sure fallback overrides
            # the memoization policy
            result = self.fallback_scores(domain)
        else:
            # NLU confidence threshold is met, so
            # predict fallback action with confidence `core_threshold`
            # if this is the highest confidence in the ensemble,
            # the fallback action will be executed.
            result = self.fallback_scores(domain, self.core_threshold)

        return result

    def persist(self, path: Text) -> None:
        """Persists the policy to storage."""
        config_file = os.path.join(path, 'fallback_policy.json')
        meta = {
            "nlu_threshold": self.nlu_threshold,
            "core_threshold": self.core_threshold,
            "fallback_action_name": self.fallback_action_name
        }
        utils.create_dir_for_file(config_file)
        utils.dump_obj_as_json_to_file(config_file, meta)

    @classmethod
    def load(cls, path: Text) -> 'FallbackPolicy':
        meta = {}
        if os.path.exists(path):
            meta_path = os.path.join(path, "fallback_policy.json")
            if os.path.isfile(meta_path):
                meta = json.loads(utils.read_file(meta_path))

        return cls(**meta)
