# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import csv
import os
import time
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
            worklogs[issue['id']] = response.json()['worklogs']
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

        def csv_export(worklogs: dict, issues: list):
            export_dir = 'exports'
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)

            filename = "{}/{}.csv".format(export_dir, time.time())

            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['Issue-ID', 'Issue-Key', 'Issue-Link', 'Worklog Spent in Minutes']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for issue_id, worklog in worklogs.items():
                    issue = list(filter(lambda x: x['id'] == issue_id, issues))[0]
                    writer.writerow({
                        fieldnames[0]: issue_id,
                        fieldnames[1]: issue['key'],
                        fieldnames[2]: os.path.join(self.jira_server, 'browse', issue['key'].lower()),
                        fieldnames[3]: sum([x['timeSpentSeconds'] / 60 for x in worklog])
                    })

        worklogs = self.get_all_worklogs_from_issues(issues=issues)
        wl_filtered = {}
        for issue_id, worklog in worklogs.items():
            for wl in worklog:
                dt = arrow.get(wl['started']).datetime
                if is_between(time=dt, from_dt=from_dt, to_dt=to_dt):
                    if issue_id in wl_filtered:
                        wl_filtered[issue_id] += worklog
                    else:
                        wl_filtered[issue_id] = worklog

        # CSV Export
        csv_export(wl_filtered, issues)

        return wl_filtered
