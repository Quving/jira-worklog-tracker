# Jira Worklog Tracker
[![Build Status](https://drone.quving.com/api/badges/Quving/jira-worklog-tracker/status.svg)](https://drone.quving.com/Quving/jira-worklog-tracker)

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
docker run --rm quving/jira-worklog-tracker:latest \
    -u "johndoe@hexample.com" \
    -t "3PHwqURul2qB3DjhDp0TAD3F" \
    -s "https://miao.atlassian.net/"  \
    -p "customer mobile app" \
    -df "06.06.2021" \
    -dt "09.06.2021"
```

### Sample Output
```
Retrieve projects...
Retrieve issues...
Retrieve worklogs...
=================================================================
                           SUMMARY

    Interval:	  2021-06-08 to 2021-06-09
    Time spent:	  670.0 min

=================================================================
```
