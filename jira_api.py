# This code sample uses the 'requests' library:
# http://docs.python-requests.org
from datetime import datetime

import arrow
import requests
from requests.auth import HTTPBasicAuth


def get_worklogs(issues: list, SERVER, USERNAME, PERSONAL_ACCESS_TOKEN):
    auth = HTTPBasicAuth(USERNAME, PERSONAL_ACCESS_TOKEN)
    headers = {"Accept": "application/json"}
    worklogs = {}

    for issue in issues:
        url = "{}/rest/api/3/issue/{}/worklog".format(SERVER, issue.id)

        response = requests.request("GET", url, headers=headers, auth=auth)
        worklogs[issue.id] = response.json()
    return worklogs


def filter_worklogs_from_to(worklogs: dict, from_dt: datetime, to_dt: datetime):
    def is_between(time: datetime, from_dt: datetime, to_dt: datetime):
        # add offset-aware
        from_dt = from_dt.replace(tzinfo=None)
        to_dt = to_dt.replace(tzinfo=None)
        time = time.replace(tzinfo=None)

        # from_dt must be before to_dt
        if from_dt < to_dt:
            return from_dt <= time and to_dt >= time
        else:
            raise Exception('Value Error: from_dt must be before to_dt.')

    wl_filtered = []
    for issue_id, worklog in worklogs.items():
        for wl in worklog['worklogs']:
            dt = arrow.get(wl['started']).datetime
            if is_between(time=dt, from_dt=from_dt, to_dt=to_dt):
                wl_filtered.append(worklog)

    return wl_filtered
