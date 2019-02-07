from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import warnings

from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.policies.fallback import FallbackPolicy

logger = logging.getLogger(__name__)


def train_nlu():

    training_data = load_data('data/nlu/nlu.json')
    trainer = Trainer(config.load("config/config_tensorflow.yml"))
    trainer.train(training_data)
    model_directory = trainer.persist('./models/nlu/',
                                      fixed_model_name="current")
    return model_directory


def train_dialogue(domain_file="domain.yml",
                   model_path="models/dialogue",
                   training_data_file="data/core/stories.md"):

    fallback = FallbackPolicy(
        fallback_action_name="action_default_fallback",
        nlu_threshold=0.5,
        core_threshold=0.3
    )

    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(), KerasPolicy(), fallback])

    training_data = agent.load_data(training_data_file)
    agent.train(
        training_data
    )

    agent.persist(model_path)
    return agent


if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")
    if task == "train-nlu":
        train_nlu()
    elif task == "train-dialogue":
        train_dialogue()
