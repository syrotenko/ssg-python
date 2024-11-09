import requests
import json

import DotDict


DEFAULT_TELEGRAM_CREDS_FILE = './resources/telegram-creds.txt'


_default_creds = None
@property
def default_creds():
    global _default_creds
    if not _default_creds:
        with open(DEFAULT_TELEGRAM_CREDS_FILE, 'r') as f:
            _default_creds = DotDict(json.load(f))
    return _default_creds


def get_creds_from_file(path):
    with open(path, 'r') as f:
        creds = json.load(f)
    return DotDict(creds)


def send_message(message, creds=default_creds):
    url = f"https://api.telegram.org/bot{creds.t_bot_token}/sendMessage?chat_id={creds.t_chat_id}&text={message}"
    requests.get(url).json()
