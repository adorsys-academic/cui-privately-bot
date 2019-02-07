from rasa_core.agent import Agent
from rasa_core.channels.socketio import SocketIOInput
from rasa_core.tracker_store import MongoTrackerStore
from rasa_core.domain import TemplateDomain
from rasa_core.interpreter import (
    NaturalLanguageInterpreter, RasaNLUInterpreter)
from rasa_core.utils import EndpointConfig

import os
import sys

domain = TemplateDomain.load(os.path.join("../models/dialogue", "domain.yml"))

interpreter = RasaNLUInterpreter("../models/nlu/default/current/")

action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")

tracker_store = MongoTrackerStore(domain,
                                  host="mongodb://<MONGO_URL>")

agent = Agent.load("../models/dialogue",
                   interpreter=interpreter,
                   tracker_store=tracker_store,
                   action_endpoint=action_endpoint)

input_channel = SocketIOInput(
    # event name for messages sent from the user
    user_message_evt="user_uttered",
    # event name for messages sent from the bot
    bot_message_evt="bot_uttered",
    # socket.io namespace to use for the messages
    namespace=None
)

agent.handle_channels([input_channel], 5005)
