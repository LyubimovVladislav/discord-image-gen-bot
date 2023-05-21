import re as regex
import random
import sys


class Parser:
    @staticmethod
    def is_int(s: str) -> bool:
        if not s:
            return False
        return s.isdigit()

    @staticmethod
    def is_float(s: str) -> bool:
        if not s:
            return False
        return not regex.match(r'^[+-]?\d+\.\d*$', s) is None

    @staticmethod
    def in_maxsize_range(s: str) -> bool:
        return len(s) <= len(str(sys.maxsize))

    @staticmethod
    def is_proper_int(s: str) -> bool:
        # As seed, torch accepts only long int, so it's required to parse string to int but not exceed the long range
        # -9300000000000000000 already throws an exception(19 digits + sign) while 9999999999999999999 not(19 digits)
        # for long int type
        if not Parser.in_maxsize_range(s):
            return False
        if s[0] in ('-', '+'):
            return s[1:].isdigit()
        return s.isdigit()

    @staticmethod
    def get_seed(s: str) -> int:
        if not s:
            raise ValueError('get_seed() exception: argument cant be empty')
        if Parser.is_proper_int(s):
            return int(s)
        random.seed(s)
        return random.randrange(int('-' + '9' * (len(str(sys.maxsize)) - 1)), int('9' * len(str(sys.maxsize))))
