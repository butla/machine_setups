from datetime import datetime

import pytest

from python_scripts_for_machine import transferwise_statements


@pytest.mark.parametrize(
    "year, month, expected_start, expected_end",
    [
        (2022, 1, "2022-01-01T00:00:00Z", "2022-02-01T00:00:00Z"),
        (2022, 2, "2022-02-01T00:00:00Z", "2022-03-01T00:00:00Z"),
        (2022, 12, "2022-12-01T00:00:00Z", "2023-01-01T00:00:00Z"),
    ],
)
def test_get_month_ends(year, month, expected_start, expected_end):
    start, end = transferwise_statements.get_month_ends(
        datetime(year=year, month=month, day=1)
    )
    assert start == expected_start
    assert end == expected_end
