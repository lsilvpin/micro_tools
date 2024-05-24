import sys, os
from typing import Any

sys.path.insert(0, os.path.abspath("."))
from main.library.repositories.notion.models.notion_custom_icon import NotionIcon
from main.library.repositories.notion.models.notion_page_block import NotionPageBlock
from main.library.repositories.notion.models.notion_property import NotionProperty


class NotionPage:
    def __init__(
        self,
        icon: NotionIcon,
        properties: list[NotionProperty],
        blocks: list[NotionPageBlock],
        page_id: str = None,
    ):
        self.id = page_id
        self.icon = icon
        self.properties = properties
        self.blocks = blocks

    def __str__(self):
        return f"{self.icon}, {self.properties}, {self.blocks}"

    def __repr__(self):
        return f"{self.icon}, {self.properties}, {self.blocks}"

    def __eq__(self, other):
        return (
            self.icon == other.icon
            and self.properties == other.properties
            and self.blocks == other.blocks
        )

    def __hash__(self):
        return hash((self.icon, self.properties, self.blocks))
