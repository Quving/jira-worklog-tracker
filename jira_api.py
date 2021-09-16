# This code sample uses the 'requests' library:
# http://docs.python-requests.org
from datetime import datetime, timedelta

import arrow
import requests
from requests.auth import HTTPBasicAuth


class JiraApi:
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

    def get_all_issues_by_current_user(self, project_id) -> list:
        """
        Return all tickets of the current user in the given project as list.
        :param project_id:
        :return:
        """
        search_jql = 'project={} and assignee = currentUser()'.format(project_id)
        url = "{}/rest/api/3/search".format(self.jira_server)
        issues = []

        # Start querying issues until all issues are queried.
        start_at = 0
        items_total = 1
        while start_at <= items_total:
            params = (
                ('jql', search_jql),
                ('startAt', start_at),
                ('maxResults', 100),
            )

            response = requests.request("GET", url, headers=JiraApi.REQUEST_HEADER, auth=self.auth, params=params)
            if response.status_code != 200:
                print("Wrong request. Cancel!")
                return []

            # Update condition
            items_total = response.json()['total']
            start_at += response.json()['maxResults']

            # Join results
            issues += response.json()['issues']

        return issues

    def get_all_worklogs_from_issues(self, issues: list):
        """
        Get all worklog objects to given issues.
        :param issues:
        :return: A dict {'<issue_id' : <worklog_obj>, ...}
        """
        worklogs_dict = {}
        for issue in issues:
            url = "{}/rest/api/3/issue/{}/worklog".format(self.jira_server, issue['id'])
            worklogs = []
            # Start querying issues until all issues are queried.
            start_at = 0
            items_total = 1
            while start_at <= items_total:
                response = requests.request("GET", url, headers=JiraApi.REQUEST_HEADER, auth=self.auth)

                if response.status_code != 200:
                    print(response.status_code)

                # Update condition
                items_total = response.json()['total']
                start_at += response.json()['maxResults']

                # Join results
                worklogs += response.json()['worklogs']

            worklogs_dict[issue['id']] = worklogs
        return worklogs_dict

    def get_all_worklogs_from_issues_between(self, issues: list, from_dt: datetime, to_dt: datetime):
        def is_between(time: datetime, from_dt: datetime, to_dt: datetime):
            # add offset-aware
            from_dt1 = from_dt.replace(tzinfo=None)
            to_dt1 = to_dt.replace(tzinfo=None) + timedelta(days=1)
            time1 = time.replace(tzinfo=None)

            # from_dt must be before to_dt
            if from_dt1 < to_dt1:
                return from_dt1 <= time1 <= to_dt1
            else:
                raise ValueError('Value Error: from_dt must be before to_dt.')

        worklogs_dict = self.get_all_worklogs_from_issues(issues=issues)

        wl_filtered = {}
        for issue_id, worklogs in worklogs_dict.items():
            for worklog in worklogs:
                dt = arrow.get(worklog['started']).datetime
                if is_between(time=dt, from_dt=from_dt, to_dt=to_dt):
                    if issue_id not in wl_filtered:
                        wl_filtered[issue_id] = []

                    wl_filtered[issue_id].append(worklog)

        return wl_filtered
