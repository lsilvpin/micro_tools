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
        parent: dict[str, str] = None,
        url: str = None,
        request_id: str = None,
        archived: bool = False,
        created_time: str = None,
        last_edited_time: str = None,
        created_by: str = None,
        last_edited_by: str = None,
    ):
        self.id = page_id
        self.parent = parent
        self.url = url
        self.request_id = request_id
        self.archived = archived
        self.created_time = created_time
        self.last_edited_time = last_edited_time
        self.created_by = created_by
        self.last_edited_by = last_edited_by
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
