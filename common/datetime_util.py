import datetime
from itertools import takewhile
from typing import Iterator


def today() -> datetime.date:
    return datetime.date.today()


def tmr() -> datetime.date:
    return datetime.date.today() + datetime.timedelta(days=1)


def first_date_current_month() -> datetime.date:
    return today().replace(day=1)


def last_date_current_month() -> datetime.date:
    this_month = first_date_current_month()
    next_month = this_month.replace(month=this_month.month + 1)
    return next_month - datetime.timedelta(days=1)


def get_date_iterator(
    start_date: datetime.date, end_date: datetime.date
) -> Iterator[datetime.date]:
    """
    Returns an iterator whose each element is a date.
    Returns no element if start_date is later than end_date.

    Args:
        start_date: inclusive
        end_date: inclusive
    """
    for days in takewhile(
        lambda d: start_date + datetime.timedelta(days=d) <= end_date,
        range(0, 31)
    ):
        yield start_date + datetime.timedelta(days=days)
