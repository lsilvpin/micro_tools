import sys, os

from main.library.tools.core.log_tool import LogTool

sys.path.insert(0, os.path.abspath("."))
import http.client, json

from main.library.repositories.notion.utils.notion_factory import (
    build_block_from_response,
)
from main.library.repositories.notion.models.notion_page_block import NotionPageBlock
from main.library.repositories.notion.utils.notion_validations import (
    validate_http_response,
)
from main.library.tools.core.settings_tool import SettingsTool


class NotionBlockManager:
    def __init__(self, settings_tool: SettingsTool, log_tool: LogTool):
        self.settings_tool: SettingsTool = settings_tool
        self.log_tool: LogTool = log_tool

    def read_page_blocks_by_page_id(
        self, page_id: str, page_size: int = 100, start_cursor: str = None
    ) -> dict:
        assert page_id is not None, "Page ID cannot be None"
        notion_protocol: str = self.settings_tool.get("NOTION_PROTOCOL")
        assert notion_protocol is not None, "NOTION_PROTOCOL cannot be None"
        notion_host: str = self.settings_tool.get("NOTION_HOST")
        assert notion_host is not None, "NOTION_HOST cannot be None"
        notion_port: str = self.settings_tool.get("NOTION_PORT")
        assert notion_port is not None, "NOTION_PORT cannot be None"
        notion_version: str = self.settings_tool.get("NOTION_VERSION")
        assert notion_version is not None, "NOTION_VERSION cannot be None"
        notion_api_key: str = self.settings_tool.get("NOTION_API_KEY")
        assert notion_api_key is not None, "NOTION_API_KEY cannot be None"
        notion_database_uri: str = (
            f"/v1/blocks/{page_id}/children?page_size={page_size}"
        )
        if start_cursor is not None:
            notion_database_uri += f"&start_cursor={start_cursor}"
        headers: dict = {
            "Authorization": f"Bearer {notion_api_key}",
            "Content-Type": "application/json",
            "Notion-Version": notion_version,
        }
        isHttps: bool = notion_protocol == "https"
        conn: http.client.HTTPSConnection = (
            http.client.HTTPSConnection(notion_host, notion_port)
            if isHttps
            else http.client.HTTPConnection(notion_host, notion_port)
        )
        assert conn is not None, "Connection cannot be None"
        conn.request("GET", notion_database_uri, headers=headers)
        response: http.client.HTTPResponse = conn.getresponse()
        assert response is not None, "Response cannot be None"
        response_status: int = response.status
        response_data: bytes = response.read()
        validate_http_response(response_status, response.reason, response_data)
        response_str: str = response_data.decode("utf-8")
        response_dict: dict = json.loads(response_str)
        assert "results" in response_dict, "Results cannot be None"
        assert response_dict["results"] is not None, "Results cannot be None"
        assert len(response_dict["results"]) > 0, "Results cannot be empty"
        blocks: list[NotionPageBlock] = []
        for block in response_dict["results"]:
            notionPageBlock: NotionPageBlock = build_block_from_response(block)
            blocks.append(notionPageBlock)
        blocks_response: dict = {
            "has_more": response_dict["has_more"],
            "next_cursor": response_dict["next_cursor"],
            "blocks": blocks,
        }
        return blocks_response
