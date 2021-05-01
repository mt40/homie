import pendulum
from django.conf import settings
from pendulum import DateTime


pendulum.DateTime.__str__ = lambda self: self.to_datetime_string()


def now() -> DateTime:
    return pendulum.now(tz=settings.TIME_ZONE)


def from_unix_timestamp(ts: int) -> DateTime:
    return pendulum.from_timestamp(ts, tz=settings.TIME_ZONE)


def parse(date_time_str: str) -> DateTime:
    return pendulum.parse(date_time_str, tz=settings.TIME_ZONE)
