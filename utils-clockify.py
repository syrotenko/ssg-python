import requests
import datetime
import json

import DotDict


DEFAULT_CLOCKIFY_CREDS_FILE = './resources/clockify-creds.txt'


_default_creds = None
@property
def default_creds():
    global _default_creds
    if not _default_creds:
        with open(DEFAULT_CLOCKIFY_CREDS_FILE, 'r') as f:
            _default_creds = DotDict(json.load(f))
    return _default_creds


def get_creds_from_file(path):
    with open(path, 'r') as f:
        creds = json.load(f)
    return DotDict(creds)


def get_times(creds=default_creds):
    """ Example get and process time entries from clockify """

    url = f"https://api.clockify.me/api/v1/workspaces/{creds.c_workspace_id}/user/{creds.c_user_id}/time-entries"
    headers = {"x-api-key": creds.c_api_key}
    res = requests.get(url, headers).json()

    report = {}
    for r in res:
        description = r['description']
        timeInterval = r['timeInterval']

        start = datetime.datetime.fromisoformat(timeInterval['start'])
        now = datetime.datetime.now()
        if not (start.year == now.year and start.isocalendar()[1] == now.isocalendar()[1]):
            continue

        durationStr = timeInterval['duration'].lower()

        durationFormat = 'pt'
        if 'h' in durationStr:
            durationFormat += '%Hh'
        if 'm' in durationStr:
            durationFormat += '%Mm'
        if 's' in durationStr:
            durationFormat += '%Ss'

        duration = datetime.datetime.strptime(durationStr, durationFormat)
        report[description] = report.get(description, 0) + \
                              (duration.hour * 60 * 60) + (duration.minute * 60) + duration.second
