import pendulum
from django.conf import settings
from pendulum import DateTime


def now() -> DateTime:
    return pendulum.now(tz=settings.TIME_ZONE)


def from_unix_timestamp(ts: int) -> DateTime:
    return pendulum.from_timestamp(ts, tz=settings.TIME_ZONE)
