#!/usr/bin/env python3

# TODO
# - put in dropbox
# - cron
from datetime import datetime
import itertools
from pathlib import Path
import shlex
import subprocess
from typing import List, Tuple

from dateutil.relativedelta import relativedelta
import pytz
import requests

token = None


def main():
    global token
    token = Path("~/.credentials/transferwise_token").expanduser().read_text().strip()
    # TODO always take previous month, unless I pass "-c"
    # statements_month = int(sys.argv[1])

    last_month = datetime.now() - relativedelta(months=1)
    statements_month = last_month

    start_time, end_time = get_month_ends(statements_month)
    profile_id = get_profile_id()
    account_id = get_account_id(profile_id)

    statements_url_template = (
        "https://api.transferwise.com/v3/profiles/{profile_id}/borderless-accounts/"
        "{account_id}/statement.{file_format}?"
        "currency={currency}&intervalStart={start_time}&intervalEnd={end_time}"
    )

    for file_format, currency in itertools.product(["csv", "pdf"], ["GBP", "USD"]):
        statements_url = statements_url_template.format(
            profile_id=profile_id,
            account_id=account_id,
            file_format=file_format,
            currency=currency,
            start_time=start_time,
            end_time=end_time,
        )
        print("Will request:\n", statements_url)
        # TODO this needs to get 403 with a challenge and then make the actual request now...
        subprocess.run(
            shlex.split(
                f'wget --header="Authorization: Bearer {token}" --content-disposition {statements_url}'
            )
        )
    print("\nPulled all statements.")


def get_profile_id() -> int:
    resp = requests.get(
        "https://api.transferwise.com/v1/profiles",
        headers={"Authorization": f"Bearer {token}"},
    )
    resp.raise_for_status()

    profiles: List[dict] = resp.json()
    business_profile = next(
        profile for profile in profiles if profile["type"] == "business"
    )
    return business_profile["id"]


def get_account_id(profile_id: int) -> int:
    resp = requests.get(
        f"https://api.transferwise.com/v1/borderless-accounts?profileId={profile_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    resp.raise_for_status()

    accounts: List[dict] = resp.json()
    business_account = accounts[0]
    return business_account["id"]


def get_month_ends(date_in_month: datetime) -> Tuple[str, str]:
    def to_utc_string(date: datetime) -> str:
        as_utc = date.astimezone(pytz.utc)
        return as_utc.isoformat().replace("+00:00", "Z")

    gb_timezone = pytz.timezone("Europe/London")
    start_date = gb_timezone.localize(
        datetime(year=date_in_month.year, month=date_in_month.month, day=1)
    )

    end_date = start_date + relativedelta(months=1)
    return to_utc_string(start_date), to_utc_string(end_date)


if __name__ == "__main__":
    main()
