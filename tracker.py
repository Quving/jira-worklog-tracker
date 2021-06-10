#!/usr/bin/env
# python -*- coding: utf-8 -*-
import argparse
import datetime

from jira_api import JiraApi


def track(username, token, server, projects, date_from, date_to):
    jira_api = JiraApi(username=username, token=token, jira_server=server)

    print("Retrieve projects...\t", end="", flush=True)
    all_projects = jira_api.get_all_projects()
    # all_projects = jira.projects()
    projects = list(filter(lambda x: x['name'].lower() in projects, all_projects))
    print("{} projects found.".format(len(projects)))

    print("Retrieve issues...\t", end="", flush=True)
    issues = []
    for project in projects:
        issues += jira_api.get_all_issues_by_current_user(project_id=project['id'])
    print("{} issues found.".format(len(issues)))

    print("Retrieve worklogs...\t", end="", flush=True)
    date_from = datetime.datetime.strptime(date_from, '%d.%m.%Y')
    date_to = datetime.datetime.strptime(date_to, '%d.%m.%Y')

    worklogs = jira_api.get_all_worklogs_from_issues_between(
        issues=issues,
        from_dt=datetime.datetime.combine(date_from, datetime.datetime.min.time()),
        to_dt=datetime.datetime.combine(date_to, datetime.datetime.min.time())
    )
    print("{} worklogs found.".format(len(worklogs)))

    worklog_time_spent = 0
    for worklog in worklogs:
        for wl2 in worklog['worklogs']:
            worklog_time_spent += wl2['timeSpentSeconds']

    # Print summary output
    print("=================================================================")
    print("\t\t\tSUMMARY\n")
    print("\tInterval:\t{} to {}".format(date_from.date(), date_to.date()))
    print("\tTime spent:\t{} min".format(worklog_time_spent / 60))
    days = worklog_time_spent // 86400
    hours = worklog_time_spent // 3600 % 24
    minutes = worklog_time_spent // 60 % 60
    seconds = worklog_time_spent % 60
    print("\n\tDays:   \t{}\n\tHours:  \t{}\n\tMinutes:\t{}\n\tSeconds:\t{}\n".format(days, hours, minutes, seconds))
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
