"""
core.utils
~~~~~~~~~~
"""
from typing import Optional
import datetime
import math
import time

from django.utils import timezone


def ensure_aware(dt):
    """Will convert datetime.datetime instance from naive into aware,
    or return if instance is already aware.
    """
    if timezone.is_aware(dt):
        return dt

    return timezone.make_aware(dt)


def struct_time_to_datetime(s_time: time.struct_time, aware: bool = True) -> datetime.datetime:
    """Will convert time.struct_time instance to datetime.datetime object. Will return
    aware datetime object unless aware = False (default is True).
    """
    dt = datetime.datetime.fromtimestamp(
        time.mktime(s_time)
    )

    if aware:
        return ensure_aware(dt)

    return dt


class FriendlyID:
    """
    CREDIT:
        - django-invoice
        - https://github.com/simonluijk/django-invoice/blob/master/invoice/utils/friendly_id.py
    LICENCE:
        - Copyright (c) 2014, Simon Luijk. All rights reserved.
    """
    SIZE = 10000000
    VALID_CHARS = '3456789ACDEFGHJKLQRSTUVWXY'

    def __init__(self, num):
        self.num = num

    @classmethod
    def encode(cls, num: int) -> Optional[str]:
        """
        Encode a simple number, using a perfect hash and converting to a
        more user friendly string of characters.
        """
        if num > cls.SIZE or num < 0:
            return None

        instance = cls(num)
        _hash = instance.perfect_hash()

        return instance.friendly_number(_hash)

    def find_suitable_period(self) -> int:
        """
        Automatically find a suitable period to use.
        Factors are best, because they will have 1 left over when
        dividing SIZE+1.
        This only needs to be run once, on import.
        """
        # The highest acceptable factor will be the square root of the size.
        highest_acceptable_factor = int(math.sqrt(self.SIZE))

        # Too high a factor (eg SIZE/2) and the interval is too small, too
        # low (eg 2) and the period is too small.
        # We would prefer it to be lower than the number of VALID_CHARS, but more
        # than say 4.
        starting_point = len(self.VALID_CHARS) > 14 and len(self.VALID_CHARS) // 2 or 13
        list_a = list(range(starting_point, 7, -1))
        list_b = list(range(highest_acceptable_factor, starting_point + 1, -1))
        list_c = [6, 5, 4, 3, 2]

        for p in list_a + list_b + list_c:
            if self.SIZE % p == 0:
                return p

        raise Exception('No valid period could be found for SIZE={}.\nTry avoiding prime numbers :-)'.format(self.SIZE))

    def friendly_number(self, num: int) -> str:
        """
        Convert a base 10 number to a base X string.
        Characters from VALID_CHARS are chosen, to convert the number
        to eg base 24, if there are 24 characters to choose from.
        Use valid chars to choose characters that are friendly, avoiding
        ones that could be confused in print or over the phone.
        """
        string = ''

        # The length of the string is determined by how many characters are necessary
        # to present a base 30 representation of SIZE.
        while len(self.VALID_CHARS) ** len(string) <= self.SIZE:
            # PREpend string (to remove all obvious signs of order)
            string = self.VALID_CHARS[num % len(self.VALID_CHARS)] + string
            num //= len(self.VALID_CHARS)

        return string

    def perfect_hash(self) -> int:
        """
        Translate a number to another unique number, using a perfect hash function.
        Only meaningful where 0 <= num <= SIZE.
        """
        _num = self.num
        _offset = self.SIZE / 2 - 1
        _period = self.find_suitable_period()

        return int(((_num + _offset) * (self.SIZE // _period)) % (self.SIZE + 1) + 1)
