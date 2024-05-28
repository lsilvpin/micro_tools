import http.client
import json
import os, sys

from main.library.repositories.notion.models.notion_search_result import (
    NotionSearchResult,
)
from main.library.repositories.notion.utils.notion_validations import (
    validate_http_response,
)

sys.path.insert(0, os.path.abspath("."))
from main.library.repositories.notion.models.notion_database import NotionDatabase
from main.library.tools.core.log_tool import LogTool
from main.library.tools.core.settings_tool import SettingsTool


class NotionSearcher:
    def __init__(self, settings_tool: SettingsTool, log_tool: LogTool):
        self.settings_tool = settings_tool
        self.log_tool = log_tool

    def search(
        self,
        token: str,
        search_obj: dict,
        page_size: int = 100,
        start_cursor: str | None = None,
    ) -> NotionSearchResult:
        assert token is not None, "Token cannot be None"
        assert search_obj is not None, "Search object cannot be None"
        notion_protocol: str = self.settings_tool.get("NOTION_PROTOCOL")
        assert notion_protocol is not None, "NOTION_PROTOCOL cannot be None"
        notion_host: str = self.settings_tool.get("NOTION_HOST")
        assert notion_host is not None, "NOTION_HOST cannot be None"
        notion_port: str = self.settings_tool.get("NOTION_PORT")
        assert notion_port is not None, "NOTION_PORT cannot be None"
        notion_version: str = self.settings_tool.get("NOTION_VERSION")
        assert notion_version is not None, "NOTION_VERSION cannot be None"
        notion_database_uri: str = f"/v1/search"
        headers: dict = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": notion_version,
        }
        body: dict = search_obj
        if "page_size" not in body or body["page_size"] is None:
            body["page_size"] = page_size
        if (
            "start_cursor" not in body or body["start_cursor"] is None
        ) and start_cursor is not None:
            body["start_cursor"] = start_cursor
        body_json: str = json.dumps(body)
        isHttps: bool = notion_protocol == "https"
        conn: http.client.HTTPSConnection = (
            http.client.HTTPSConnection(notion_host, notion_port)
            if isHttps
            else http.client.HTTPConnection(notion_host, notion_port)
        )
        assert conn is not None, "Connection cannot be None"
        conn.request("POST", notion_database_uri, body_json, headers)
        response: http.client.HTTPResponse = conn.getresponse()
        assert response is not None, "Response cannot be None"
        response_status: int = response.status
        response_data: bytes = response.read()
        validate_http_response(response_status, response.reason, response_data)
        response_str: str = response_data.decode("utf-8")
        response_dict: dict = json.loads(response_str)
        search_result: NotionSearchResult = NotionSearchResult.from_dict(response_dict)
        return search_result
