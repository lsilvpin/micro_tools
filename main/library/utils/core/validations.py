import datetime
import os, sys
from typing import Any

sys.path.insert(0, os.path.abspath("."))


def is_primitive(value: Any) -> bool:
    is_datetime: bool = type(datetime.datetime.now()) == type(value)
    return value is None or isinstance(value, (str, int, float, bool)) or is_datetime


def is_list(value: Any) -> bool:
    return isinstance(value, list)


def is_object(value: Any) -> bool:
    return not is_primitive(value) and not is_list(value)
