import sys, os
from typing import Any

from main.library.repositories.notion.utils.notion_icon_types import NOTION_ICON_TYPES

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

    def to_payload(self) -> dict:
        payload: dict = {"type": self.type}
        if self.type == NOTION_ICON_TYPES["emoji"]:
            payload["emoji"] = self.value
        elif self.type == NOTION_ICON_TYPES["external"]:
            payload["external"] = {"url": self.value}
        elif self.type == NOTION_ICON_TYPES["file"]:
            payload["file"] = {"url": self.value}
        else:
            raise ValueError(f"Invalid icon type: {self.type}")
        return payload

    @staticmethod
    def from_response(data: dict):
        assert data is not None, "Icon data should not be None"
        assert "type" in data, "Icon data should have a type"
        icon_type: str = data["type"]
        icon_value: Any | None = None
        if icon_type == NOTION_ICON_TYPES["emoji"]:
            icon_value: str = data["emoji"]
        elif icon_type == NOTION_ICON_TYPES["external"]:
            icon_value: str = data["external"]["url"]
        elif icon_type == NOTION_ICON_TYPES["file"]:
            icon_value: str = data["file"]["url"]
        else:
            raise ValueError(f"Invalid icon type: {icon_type}")
        icon: NotionIcon = NotionIcon(icon_type, icon_value)
        return icon
