import sys, os

sys.path.insert(0, os.path.abspath("."))
from typing import Any


class NotionProperty:
    def __init__(
        self, name: str, prop_type: str, value: Any, options: Any | None = None
    ):
        self.name = name
        self.type = prop_type
        self.value = value
        self.options = options

    def __str__(self) -> str:
        return f"{self.name} ({self.type}): {self.value}"

    @staticmethod
    def from_dict(data: dict) -> "NotionProperty":
        return NotionProperty(
            name=data["name"],
            prop_type=data["type"],
            value=data.get("value"),
            options=data.get("options"),
        )