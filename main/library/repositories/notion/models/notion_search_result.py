import sys, os
from typing import Any

from main.library.repositories.notion.models.notion_database import NotionDatabase
from main.library.repositories.notion.models.notion_page import NotionPage
from main.library.repositories.notion.utils.notion_factory import (
    build_page_from_response,
)

sys.path.insert(0, os.path.abspath("."))


class NotionSearchResult:
    def __init__(
        self,
        pages: list[NotionPage] | None = None,
        databases: list[NotionDatabase] | None = None,
        has_more: bool = False,
        next_cursor: str | None = None,
        request_id: str | None = None,
    ):
        self.has_more = has_more
        self.next_cursor = next_cursor
        self.pages = pages
        self.databases = databases
        self.request_id = request_id

    def __str__(self):
        return f"{self.has_more}, {self.next_cursor}"

    def count(self):
        return len(self.pages) + len(self.databases)

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "NotionSearchResult":
        pages_from_dict: list[dict] = [
            page for page in data["results"] if page["object"] == "page"
        ]
        databases_from_dict: list[dict] = [
            database for database in data["results"] if database["object"] == "database"
        ]
        pages = [build_page_from_response(page) for page in pages_from_dict]
        databases = [
            NotionDatabase.from_read_response(database)
            for database in databases_from_dict
        ]
        return NotionSearchResult(
            pages=pages,
            databases=databases,
            has_more=data.get("has_more", False),
            next_cursor=data.get("next_cursor", None),
            request_id=data.get("request_id"),
        )
