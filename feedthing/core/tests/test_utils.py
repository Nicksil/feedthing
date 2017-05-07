import datetime
import time

from django.test import TestCase
from django.utils import timezone

from ..utils import ensure_aware, struct_time_to_datetime, FriendlyID


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

    def test_FriendlyID_encode_classmethod_returns_string_ID(self):
        str_id = FriendlyID.encode(1)

        self.assertIsInstance(str_id, str)
        self.assertEqual(str_id, 'TTH9R')

    def test_FriendlyID_encode_classmethod_returns_None_when_given_number_greater_than_SIZE(self):
        none_id = FriendlyID.encode(FriendlyID.SIZE + 1)
        self.assertIsNone(none_id)

    def test_FriendlyID_encode_classmethod_returns_None_when_given_number_less_than_zero(self):
        none_id = FriendlyID.encode(-1)
        self.assertIsNone(none_id)
