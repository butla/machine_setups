#!/usr/bin/env python3
from datetime import datetime, timedelta


def count_work_days(start, stop):
    count = 0
    current_day = start
    while current_day <= stop:
        if current_day.weekday() not in (5, 6):
            count += 1
        current_day += timedelta(days=1)
    return count


leave_days = [
    '2018-12-17',
    '2018-12-20',
    '2018-12-21',
    '2018-12-24',
    '2018-12-25',
    '2018-12-26',
    '2018-12-31',
    '2019-01-01',
    '2019-01-02',
    '2019-03-25',
    '2019-05-03',
    '2019-05-06',
    '2019-07-05',
    '2019-08-09',
    '2019-08-15',
    '2019-08-16',
    '2019-08-20',
    '2019-08-26',
    '2019-10-15',
    '2019-10-31',
    '2019-11-01',
]

additional_days = [
    '2018-12-16',
]

d1 = datetime(year=2018, month=11, day=15)
d2 = datetime(year=2019, month=11, day=10)
print(count_work_days(d1, d2) - len(leave_days) + len(additional_days))
