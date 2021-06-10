# This code sample uses the 'requests' library:
# http://docs.python-requests.org
from datetime import datetime

import arrow
import requests
from requests.auth import HTTPBasicAuth


class JiraApi:
    def __init__(self, username, token, jira_server):
        self.username = username
        self.jira_server = jira_server
        self.token = token
        self.auth = HTTPBasicAuth(username, token)

        self.headers = {"Accept": "application/json"}

    def get_all_worklogs_from_issues(self, issues: list):
        """
        Get all worklog objects to given issues.
        :param issues:
        :return: A dict {'<issue_id' : <worklog_obj>, ...}
        """
        worklogs = {}
        for issue in issues:
            url = "{}/rest/api/3/issue/{}/worklog".format(self.jira_server, issue.id)
            response = requests.request("GET", url, headers=self.headers, auth=self.auth)
            worklogs[issue.id] = response.json()
        return worklogs

    def get_all_worklogs_from_issues_between(self, issues: list, from_dt: datetime, to_dt: datetime):

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

        worklogs = self.get_all_worklogs_from_issues(issues=issues)
        wl_filtered = []
        for issue_id, worklog in worklogs.items():
            for wl in worklog['worklogs']:
                dt = arrow.get(wl['started']).datetime
                if is_between(time=dt, from_dt=from_dt, to_dt=to_dt):
                    wl_filtered.append(worklog)

        return wl_filtered
