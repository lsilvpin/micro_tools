import sys, os
from typing import Any

sys.path.insert(0, os.path.abspath("."))
from main.library.repositories.notion.models.notion_page_block import NotionPageBlock
from main.library.repositories.notion.models.notion_property import NotionProperty


class NotionPage:
    def __init__(
        self,
        properties: list[NotionProperty],
        blocks: list[NotionPageBlock],
        page_id: str = None,
    ):
        self.id = page_id
        self.properties = properties
        self.blocks = blocks

    def __str__(self):
        return f"{self.properties}"

    def __repr__(self):
        return f"{self.title}: {self.properties}"

    def __eq__(self, other):
        return self.title == other.title and self.properties == other.properties

    def __hash__(self):
        return hash((self.title, self.properties))

    def get_property(self, name: str) -> NotionProperty:
        for prop in self.properties:
            if prop.name == name:
                return prop
        return None

    def get_block(self, block_id: str) -> NotionPageBlock:
        for block in self.blocks:
            if block.id == block_id:
                return block
        return None

    def get_blocks_by_type(self, block_type: str) -> list[NotionPageBlock]:
        return [block for block in self.blocks if block.type == block_type]

    def get_property_value(self, name: str) -> Any:
        prop = self.get_property(name)
        if prop:
            return prop.value
        return None

    def get_block_value(self, block_id: str) -> Any:
        block = self.get_block(block_id)
        if block:
            return block.value
        return None
    
    def get_block_values_by_type(self, block_type: str) -> list[Any]:
        blocks = self.get_blocks_by_type(block_type)
        return [block.value for block in blocks]