#!/usr/bin/env
# python -*- coding: utf-8 -*-
import argparse
import datetime

from jira import JIRA

from jira_api import JiraApi


def track(username, token, server, projects, date_from, date_to):
    jira = JIRA(server=server, basic_auth=(username, token))
    jira_api = JiraApi(username=username, token=token, jira_server=server)

    print("Retrieve projects...")
    all_projects = jira.projects()
    relevant_projects = list(filter(lambda x: x.name.lower() in projects, all_projects))

    print("Retrieve issues...")
    issues = []
    for project in relevant_projects:
        issues += jira.search_issues('project={} and assignee = currentUser()'.format(project.id), maxResults=10000)

    print("Retrieve worklogs...")

    # with open("worklogs.json", "w") as file:
    #     json.dump(worklogs, file, indent=4)

    # with open('worklogs.json', 'r') as file:
    #     worklogs = json.load(file)

    date_from = datetime.datetime.strptime(date_from, '%d.%m.%Y')
    date_to = datetime.datetime.strptime(date_to, '%d.%m.%Y')

    worklogs = jira_api.get_all_worklogs_from_issues_between(
        issues=issues,
        from_dt=datetime.datetime.combine(date_from, datetime.datetime.min.time()),
        to_dt=datetime.datetime.combine(date_to, datetime.datetime.min.time())
    )

    worklog_time_spent = 0
    for worklog in worklogs:
        for wl2 in worklog['worklogs']:
            worklog_time_spent += wl2['timeSpentSeconds']

    # Print summary output
    print("=================================================================")
    print("\t\t\t\tSUMMARY\n")
    print("\tInterval:\t{} to {}".format(date_from.date(), date_to.date()))
    print("\tTime spent:\t{} min".format(worklog_time_spent / 60))
    print()
    print("=================================================================")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='How to use Jira-Worklog-Tracker')
    parser.add_argument('-u', '--username', help='Jira Email', required=True)
    parser.add_argument('-t', '--token', help='Personal Access Token', required=True)
    parser.add_argument('-s', '--server', help='Jira Server (e.g. "https://myproject.atlassian.net")', required=True)
    parser.add_argument('-p', '--projects', nargs='+', help='Projects to track.', required=True)
    parser.add_argument('-df', '--date_from', help='Date from (e.g. "tt.mm.yyy")', required=True)
    parser.add_argument('-dt', '--date_to', help='Date to (e.g. "tt.mm.yyy")', required=True)

    args = parser.parse_args()
    track(
        username=args.username,
        token=args.token,
        server=args.server,
        projects=args.projects,
        date_from=args.date_from,
        date_to=args.date_to,
    )
