import sys, os
sys.path.insert(0, os.path.abspath("."))
from typing import Any


class NotionProperty:
    def __init__(self, name: str, prop_type: str, value: Any):
        self.name = name
        self.type = prop_type
        self.value = value

    def __str__(self):
        return f"{self.name}: {self.value}"

    def __repr__(self):
        return f"{self.name}: {self.value}"

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.type == other.type
            and self.value == other.value
        )

    def __hash__(self):
        return hash((self.name, self.type, self.value))
