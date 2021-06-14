import csv
import os
import time


def csv_export(worklogs: dict, issues: list, jira_server):
    export_dir = 'exports'
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    filename = "{}/{}.csv".format(export_dir, time.time())

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Issue-ID', 'Issue-Key', 'Issue-Name', 'Issue-Link', 'Worklog Spent in Minutes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for issue_id, worklog in worklogs.items():
            issue = list(filter(lambda x: x['id'] == issue_id, issues))[0]
            writer.writerow({
                fieldnames[0]: issue_id,
                fieldnames[1]: issue['key'],
                fieldnames[2]: issue['fields']['summary'],
                fieldnames[3]: os.path.join(jira_server, 'browse', issue['key'].lower()),
                fieldnames[4]: int(sum([x['timeSpentSeconds'] / 60 for x in worklog]))
            })
