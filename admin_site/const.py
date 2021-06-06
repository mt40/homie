from enum import Enum, unique
from django.db import models


_admin_name = 'homie_admin'

class UrlName(models.TextChoices):
    ADMIN_INDEX = f"{_admin_name}:index"
    APP_INDEX = f"{_admin_name}:app_list"
    CALCULATOR = f'{_admin_name}:calculator'
    CALCULATOR_RESULT = f'{_admin_name}:calculator_result'