import sys, os
from typing import Any

sys.path.insert(0, os.path.abspath("."))


class NotionIcon:
    def __init__(self, icon_type: str, icon_value: Any):
        self.type = icon_type
        self.value = icon_value

    def __str__(self):
        return f"{self.type}: {self.value}"

    def __repr__(self):
        return f"{self.type}: {self.value}"

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __hash__(self):
        return hash((self.type, self.value))
