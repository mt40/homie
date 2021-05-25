from enum import Enum, unique
from django.db import models


_admin_name = 'homie_admin'

class UrlName(models.TextChoices):
    CALCULATOR = f'{_admin_name}:calculator'
    CALCULATOR_RESULT = f'{_admin_name}:calculator_result'