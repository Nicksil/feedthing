import datetime

from django.test import TestCase
from django.utils import timezone

from ..utils import ensure_aware


class CoreUtilsTestCase(TestCase):
    def test_ensure_aware_returns_aware_datetime_when_given_naive_datetime(self):
        # Naive
        _datetime = datetime.datetime.now()
        _initial_id = id(_datetime)
        self.assertIsNone(_datetime.utcoffset())

        # Aware
        _datetime = ensure_aware(_datetime)
        _final_id = id(_datetime)
        self.assertIsNotNone(_datetime.utcoffset())

        # Confirm discrete objects
        self.assertNotEqual(_initial_id, _final_id)

    def test_ensure_aware_returns_aware_datetime_when_given_aware_datetime(self):
        # Aware
        _datetime = timezone.make_aware(datetime.datetime.now())
        _initial_id = id(_datetime)
        self.assertIsNotNone(_datetime.utcoffset())

        # Aware (Same object)
        _datetime = ensure_aware(_datetime)
        _final_id = id(_datetime)
        self.assertIsNotNone(_datetime.utcoffset())

        # Confirm same object
        self.assertEqual(_initial_id, _final_id)