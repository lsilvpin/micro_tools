import sys, os

sys.path.insert(0, os.path.abspath("."))
from typing import Any


class NotionPageBlock:
    def __init__(self, block_type: str, value: Any, block_id: str = None):
        self.id = block_id
        self.type = block_type
        self.value = value

    def __str__(self):
        return f"{self.type}: {self.value}"

    def __repr__(self):
        return f"{self.type}: {self.value}"

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value
