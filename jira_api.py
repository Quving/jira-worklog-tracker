# This code sample uses the 'requests' library:
# http://docs.python-requests.org
from datetime import datetime

import arrow
import requests
from requests.auth import HTTPBasicAuth


class JiraApi:
    MAX_RESULTS = 10000
    REQUEST_HEADER = {"Accept": "application/json"}

    def __init__(self, username, token, jira_server):
        self.username = username
        self.jira_server = jira_server
        self.token = token
        self.auth = HTTPBasicAuth(username, token)

    def get_all_projects(self):
        url = "{}/rest/api/3/project".format(self.jira_server)

        response = requests.request("GET", url, headers=JiraApi.REQUEST_HEADER, auth=self.auth)
        return response.json()

    def get_all_issues_by_current_user(self, project_id):

        search_jql = 'project={} and assignee = currentUser()'.format(project_id)
        url = "{}/rest/api/3/search".format(self.jira_server)
        params = (
            ('jql', search_jql),
            ('maxResults', JiraApi.MAX_RESULTS),
        )
        response = requests.request("GET", url, headers=JiraApi.REQUEST_HEADER, auth=self.auth, params=params)
        return response.json()['issues']

    def get_all_worklogs_from_issues(self, issues: list):
        """
        Get all worklog objects to given issues.
        :param issues:
        :return: A dict {'<issue_id' : <worklog_obj>, ...}
        """
        worklogs = {}
        for issue in issues:
            url = "{}/rest/api/3/issue/{}/worklog".format(self.jira_server, issue['id'])
            response = requests.request("GET", url, headers=JiraApi.REQUEST_HEADER, auth=self.auth)
            if response.status_code != 200:
                print(response.status_code)
            worklogs[issue['id']] = response.json()['worklogs']
        return worklogs

    def get_all_worklogs_from_issues_between(self, issues: list, from_dt: datetime, to_dt: datetime):
        def is_between(time: datetime, from_dt: datetime, to_dt: datetime):
            # add offset-aware
            from_dt1 = from_dt.replace(tzinfo=None)
            to_dt1 = to_dt.replace(tzinfo=None)
            time1 = time.replace(tzinfo=None)

            # from_dt must be before to_dt
            if from_dt1 < to_dt1:
                return from_dt1 <= time1 and to_dt1 >= time1
            else:
                raise ValueError('Value Error: from_dt must be before to_dt.')

        worklogs_detail = self.get_all_worklogs_from_issues(issues=issues)

        wl_filtered = {}
        for issue_id, worklogs in worklogs_detail.items():
            for worklog in worklogs:
                dt = arrow.get(worklog['started']).datetime
                if is_between(time=dt, from_dt=from_dt, to_dt=to_dt):
                    if issue_id not in wl_filtered:
                        wl_filtered[issue_id] = []

                    wl_filtered[issue_id].append(worklog)

        return wl_filtered
