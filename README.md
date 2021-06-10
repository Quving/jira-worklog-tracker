# Jira Worklog Tracker

[![Build Status](https://drone.quving.com/api/badges/Quving/jira-worklog-tracker/status.svg)](https://drone.quving.com/Quving/jira-worklog-tracker)
![](https://img.shields.io/github/languages/top/Quving/jira-worklog-tracker)
![](https://img.shields.io/github/v/tag/Quving/jira-worklog-tracker)
![](https://img.shields.io/github/issues/Quving/jira-worklog-tracker)

## Motivation
This repository contains small scripts to determine the recorded working time in Jira tickets between two specific dates.

## Setup

## Jira Personal Access Token
Create your own personal access token in Jira.
Reference: https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html


## Installation
```
pip install -r requirements.txt
```

## Usage

### Example
```
python tracker.py \
    -u "johndoe@hexample.com" \
    -t "3PHwqURul2qB3DjhDp0TAD3F" \
    -s "https://miao.atlassian.net/"  \
    -p "customer mobile app" \
    -df "06.06.2021" \
    -dt "09.06.2021"
```

or using Docker


```
docker run --rm -it -v $(pwd)/exports:/app/exports quving/jira-worklog-tracker:v1.0.0 \
    -u "johndoe@hexample.com" \
    -t "3PHwqURul2qB3DjhDp0TAD3F" \
    -s "https://miao.atlassian.net/"  \
    -p "customer mobile app" \
    -df "08.06.2021"     \
    -dt "09.06.2021"
```

### Sample Output
## CSV
![](https://i.imgur.com/haq0KsG.png)

## Console
```
Retrieve projects...	1 projects found.
Retrieve issues...	45 issues found.
Retrieve worklogs...	7 worklogs found.
=================================================================
			SUMMARY

	Interval:	2021-06-08 to 2021-06-10
	Time spent:	260.0 min

	Days:   	0
	Hours:  	4
	Minutes:	20
	Seconds:	0

=================================================================
```

