from typing import List

from app.core.configs import TelegramNotifierConfig
from app.core.exceptions import NetworkConnectionError
from app.core.models import BaseAnswer
from app.notifier import Notifier
from app.utils.requesting import make_request


class TelegramNotifier(Notifier):

    def __init__(self, config: TelegramNotifierConfig):
        self.config: TelegramNotifierConfig = config
        self.send_message_endpoint = f"https://api.telegram.org/bot{self.config.bot_token}/sendMessage"

    def notify(self, message: BaseAnswer):
        for known_user in self.config.known_users:
            try:
                make_request('POST', self.send_message_endpoint, data={'chat_id': known_user,
                                                                       'text': f'<pre>{message.to_string()}</pre>',
                                                                       'parse_mode': 'html'})
            except (NetworkConnectionError, BaseException) as e:
                print(f"NetworkConnectionError: cannot send message to bot")


class EmailNotifier:
    pass
