# this builtin is needed so we can overwrite in test
from builtins import input

import json
import requests

from rasa_core import utils
from rasa_core.channels import UserMessage
from rasa_core.channels.channel import button_to_string, RestInput
from rasa_core.constants import DEFAULT_SERVER_URL
from rasa_core.interpreter import INTENT_MESSAGE_PREFIX


def print_bot_output(message, color=utils.bcolors.OKBLUE):
    if "text" in message:
        utils.print_color(message.get("text"), color)

    if "image" in message:
        utils.print_color("Image: " + message.get("image"), color)

    if "attachment" in message:
        utils.print_color("Attachment: " + message.get("attachment"), color)

    if "buttons" in message:
        for idx, button in enumerate(message.get("buttons")):
            button_str = button_to_string(button, idx)
            utils.print_color(button_str, color)


def get_cmd_input():
    return input().strip()


def send_message_receive_block(server_url, auth_token, sender_id, message):
    payload = {
        "sender": sender_id,
        "message": message
    }

    response = requests.post("{}/webhooks/rest/webhook?token={}".format(
        server_url, auth_token),
        json=payload)
    response.raise_for_status()
    return response.json()


def send_message_receive_stream(server_url, auth_token, sender_id, message):
    payload = {
        "sender": sender_id,
        "message": message
    }

    url = "{}/webhooks/rest/webhook?stream=true&token={}".format(
        server_url, auth_token)

    with requests.post(url, json=payload, stream=True) as r:

        r.raise_for_status()

        if r.encoding is None:
            r.encoding = 'utf-8'

        for line in r.iter_lines(decode_unicode=True):
            if line:
                yield json.loads(line)


def record_messages(server_url=DEFAULT_SERVER_URL,
                    auth_token=None,
                    sender_id=UserMessage.DEFAULT_SENDER_ID,
                    max_message_limit=None,
                    use_response_stream=True,
                    on_finish=None):
    """Read messages from the command line and print bot responses."""

    auth_token = auth_token if auth_token else ""

    exit_text = INTENT_MESSAGE_PREFIX + 'stop'

    utils.print_color("Bot loaded. Type a message and press enter "
                      "(use '{}' to exit): ".format(exit_text),
                      utils.bcolors.OKGREEN)

    num_messages = 0
    while not utils.is_limit_reached(num_messages, max_message_limit):
        text = get_cmd_input()
        if text == exit_text:
            break

        if use_response_stream:
            bot_responses = send_message_receive_stream(server_url,
                                                        auth_token,
                                                        sender_id, text)
        else:
            bot_responses = send_message_receive_block(server_url,
                                                       auth_token,
                                                       sender_id, text)

        for response in bot_responses:
            print_bot_output(response)

        num_messages += 1

    if on_finish:
        on_finish()


class CmdlineInput(RestInput):

    @classmethod
    def name(cls):
        return "cmdline"

    def url_prefix(self):
        return RestInput.name()
