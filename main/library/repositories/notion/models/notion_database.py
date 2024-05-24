import sys, os

sys.path.insert(0, os.path.abspath("."))
from main.library.repositories.notion.models.notion_property import NotionProperty


class NotionDatabase:
    def __init__(
        self, name: str, properties: list[NotionProperty], database_id: str = None
    ):
        self.id = database_id
        self.name = name
        self.properties = properties

    def __str__(self):
        return f"{self.name}: {self.properties}"

    def __repr__(self):
        return f"{self.name}: {self.properties}"

    def __eq__(self, other):
        return self.name == other.name and self.properties == other.properties

    def __hash__(self):
        return hash((self.name, self.properties))

    def get_property(self, name: str) -> NotionProperty:
        for prop in self.properties:
            if prop.name == name:
                return prop
        return None
