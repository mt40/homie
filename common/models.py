from typing import Optional

from django.core.exceptions import ValidationError
from django.db import models
from django.forms import CharField
from pendulum import DateTime

from portfolio import time_util


class IntDateTimeField(models.Field):
    def __init__(self, auto_now: bool = False, auto_now_add: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add

    def db_type(self, connection):
        return "integer"

    def from_db_value(self, value, expression, connection) -> Optional[DateTime]:
        if value is None:
            return value
        try:
            return time_util.from_unix_timestamp(value)
        except TypeError as err:
            raise ValidationError(str(err))

    def to_python(self, value):
        try:
            return time_util.parse(value)
        except TypeError as err:
            raise ValidationError(str(err))

    def get_prep_value(self, value: DateTime):
        if isinstance(value, int) or value is None:  # already a timestamp
            return value

        return value.int_timestamp

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            now = time_util.now()
            setattr(model_instance, self.attname, now)
            return now

        return super().pre_save(model_instance, add)

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': CharField,
            **kwargs,
        })

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return str(self.get_prep_value(value))


class BaseModel(models.Model):
    class Meta:
        abstract = True

    create_time = IntDateTimeField(auto_now_add=True)
    update_time = IntDateTimeField(auto_now=True)