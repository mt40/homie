from django.test import TestCase
from django.urls import reverse

from admin_site.const import UrlName


class AdminUrlsTests(TestCase):
    def test_reverse_calculator(self):
        reverse(UrlName.CALCULATOR.value)

    def test_reverse_calculator_result(self):
        reverse(UrlName.CALCULATOR_RESULT.value, kwargs={
            'result': 1
        })