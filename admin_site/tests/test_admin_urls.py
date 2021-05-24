from django.test import TestCase
from django.urls import reverse


class AdminUrlsTests(TestCase):
    def test_reverse(self):
        reverse('homie_admin:calculator')