import datetime
from itertools import takewhile
from typing import Iterator


DATE_FORMAT = "%Y-%m-%d"


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


def first_date_of(year: int, month: int) -> datetime.date:
    return today().replace(year=year, month=month, day=1)


def last_date_of(year: int, month: int) -> datetime.date:
    next_month = (first_date_of(year, month) + datetime.timedelta(days=31))
    return first_date_of(next_month.year, next_month.month) - datetime.timedelta(days=1)


def same_date_in(year: int, month: int, target: datetime.date) -> datetime.date:
    """
    Returns the same date as `target` in the given month.
    If the given month doesn't have the target day, the last day is selected.
    """
    last_date = last_date_of(year, month)
    if target.day > last_date.day:
        return last_date
    return last_date.replace(day=target.day)
