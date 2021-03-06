import datetime
import time

from django.test import TestCase
from django.utils import timezone

from ..utils import ensure_aware
from ..utils import now
from ..utils import struct_time_to_datetime
from ..utils import time_since


class CoreUtilsTestCase(TestCase):
    def test_ensure_aware_returns_aware_datetime_when_given_naive_datetime(self):
        # Naive
        _datetime = datetime.datetime.now()
        initial_id = id(_datetime)
        self.assertIsNone(_datetime.utcoffset())

        # Aware
        _datetime = ensure_aware(_datetime)
        final_id = id(_datetime)
        self.assertIsNotNone(_datetime.utcoffset())

        # Confirm discrete objects
        self.assertNotEqual(initial_id, final_id)

    def test_ensure_aware_returns_aware_datetime_when_given_aware_datetime(self):
        # Aware
        _datetime = timezone.make_aware(datetime.datetime.now())
        initial_id = id(_datetime)
        self.assertIsNotNone(_datetime.utcoffset())

        # Aware (Same object)
        _datetime = ensure_aware(_datetime)
        final_id = id(_datetime)
        self.assertIsNotNone(_datetime.utcoffset())

        # Confirm same object
        self.assertEqual(initial_id, final_id)

    def test_struct_time_to_datetime_returns_aware_datetime_object(self):
        s_time = time.localtime()
        _datetime = struct_time_to_datetime(s_time)

        self.assertIsInstance(_datetime, datetime.datetime)
        self.assertIsNotNone(_datetime.utcoffset())

    def test_struct_time_to_datetime_returns_naive_datetime_object(self):
        s_time = time.localtime()
        _datetime = struct_time_to_datetime(s_time, aware=False)

        self.assertIsInstance(_datetime, datetime.datetime)
        self.assertIsNone(_datetime.utcoffset())

    def test_now_returns_aware_datetime_object(self):
        _now = now()
        self.assertIsNotNone(_now.utcoffset())

    def test_now_returns_naive_datetime_object(self):
        _now = now(aware=False)
        self.assertIsNone(_now.utcoffset())

    def test_time_since_returns_correct_string_for_hours_elapsed(self):
        then = datetime.datetime.now() - datetime.timedelta(hours=3)
        result = time_since(then)
        self.assertEqual(result, '3h')

    def test_time_since_returns_correct_string_for_days_elapsed(self):
        then = datetime.datetime.now() - datetime.timedelta(days=3)
        result = time_since(then)
        self.assertEqual(result, '3d')
