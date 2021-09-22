from datetime import datetime

import pytest

import work_days_between


def _date(day):
    return datetime(year=2019, month=8, day=day)


@pytest.mark.parametrize('start, end, expected_count', [
    (_date(1), _date(1), 1),
    (_date(1), _date(2), 2),
    (_date(1), _date(3), 2),
    (_date(1), _date(5), 3),
])
def test_work_days(start, end, expected_count):
    assert work_days_between.count_work_days(start, end) == expected_count
