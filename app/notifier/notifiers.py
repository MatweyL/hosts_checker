from typing import List

from app.core.exceptions import NetworkConnectionError
from app.core.models import BaseAnswer
from app.notifier import Notifier
from app.utils.requesting import make_request


class TelegramNotifier(Notifier):

    def __init__(self, bot_token: str, known_users: List[int]):
        self.bot_token = bot_token
        self.known_users = known_users
        self.send_message_endpoint = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    def notify(self, message: BaseAnswer):
        for known_user in self.known_users:
            try:
                make_request('POST', self.send_message_endpoint, data={'chat_id': known_user,
                                                                       'text': message.to_string()})
            except NetworkConnectionError as e:
                print(f"NetworkConnectionError: cannot send message to bot: {e}")


class EmailNotifier:
    pass
