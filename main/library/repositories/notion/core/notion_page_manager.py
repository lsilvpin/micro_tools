import sys, os, http.client, json

from main.library.repositories.notion.core.notion_block_manager import (
    NotionBlockManager,
)
from main.library.repositories.notion.models.notion_page_block import NotionPageBlock
from main.library.repositories.notion.utils.notion_factory import (
    build_blocks_for_request,
    build_icon_for_request,
    build_page_from_response,
    build_properties_for_request,
)
from main.library.repositories.notion.utils.notion_validations import (
    validate_http_response,
)

sys.path.insert(0, os.path.abspath("."))
from main.library.repositories.notion.models.notion_page import NotionPage
from main.library.tools.core.log_tool import LogTool
from main.library.tools.core.settings_tool import SettingsTool


class NotionPageManager:
    def __init__(
        self,
        settings_tool: SettingsTool,
        log_tool: LogTool,
        notion_block_manager: NotionBlockManager,
    ):
        self.settings_tool: SettingsTool = settings_tool
        self.log_tool: LogTool = log_tool
        self.notion_block_manager: NotionBlockManager = notion_block_manager

    def create_page(self, page: NotionPage, database_id: str):
        assert page is not None, "Page cannot be None"
        assert database_id is not None, "Database ID cannot be None"
        assert page.properties is not None, "Page properties cannot be None"
        assert len(page.properties) > 0, "Page properties cannot be empty"
        assert page.blocks is not None, "Page blocks cannot be None"
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
        notion_database_uri: str = f"/v1/pages"
        headers: dict = {
            "Authorization": f"Bearer {notion_api_key}",
            "Content-Type": "application/json",
            "Notion-Version": notion_version,
        }
        icon: dict = build_icon_for_request(page)
        properties: dict = build_properties_for_request(page)
        blocks: list = build_blocks_for_request(page)
        body: dict = {
            "parent": {"database_id": database_id},
            "icon": icon,
            "properties": properties,
            "children": blocks,
        }
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
        return response_dict

    def read_page_properties_by_page_id(self, page_id: str) -> NotionPage:
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
        notion_database_uri: str = f"/v1/pages/{page_id}"
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
        response_page: NotionPage = build_page_from_response(response_dict)
        return response_page

    def read_page_by_id(self, page_id: str) -> NotionPage:
        assert page_id is not None, "Page ID cannot be None"
        notionPage: NotionPage = self.read_page_properties_by_page_id(page_id)
        blocks: list[NotionPageBlock] = []
        has_more: bool = True
        next_cursor: str = None
        while has_more:
            response: dict = self.notion_block_manager.read_page_blocks_by_page_id(
                page_id, page_size=100, start_cursor=next_cursor
            )
            blocks.extend(response["blocks"])
            has_more = response["has_more"]
            next_cursor = response["next_cursor"]
        notionPage.blocks = blocks
        return notionPage
    
    def update_page_by_id(self, page_id: str, page: NotionPage) -> dict:
        assert page_id is not None, "Page ID cannot be None"
        assert page is not None, "Page cannot be None"
        assert page.properties is not None, "Page properties cannot be None"
        assert len(page.properties) > 0, "Page properties cannot be empty"
        assert page.blocks is not None, "Page blocks cannot be None"
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
        notion_database_uri: str = f"/v1/pages/{page_id}"
        headers: dict = {
            "Authorization": f"Bearer {notion_api_key}",
            "Content-Type": "application/json",
            "Notion-Version": notion_version,
        }
        properties: dict = build_properties_for_request(page)
        blocks: list = build_blocks_for_request(page)
        body: dict = {
            "icon": {"type": "emoji", "emoji": "👩🏻‍💻"},
            "properties": properties,
            "children": blocks,
        }
        body_json: str = json.dumps(body)
        isHttps: bool = notion_protocol == "https"
        conn: http.client.HTTPSConnection = (
            http.client.HTTPSConnection(notion_host, notion_port)
            if isHttps
            else http.client.HTTPConnection(notion_host, notion_port)
        )
        assert conn is not None, "Connection cannot be None"
        conn.request("PATCH", notion_database_uri, body_json, headers)
        response: http.client.HTTPResponse = conn.getresponse()
        assert response is not None, "Response cannot be None"
        response_status: int = response.status
        response_data: bytes = response.read()
        validate_http_response(response_status, response.reason, response_data)
        response_str: str = response_data.decode("utf-8")
        response_dict: dict = json.loads(response_str)
        return response_dict

    def archive_page_by_id(self, page_id: str) -> dict:
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
        notion_database_uri: str = f"/v1/pages/{page_id}"
        headers: dict = {
            "Authorization": f"Bearer {notion_api_key}",
            "Content-Type": "application/json",
            "Notion-Version": notion_version,
        }
        body: dict = {"archived": True}
        body_json: str = json.dumps(body)
        isHttps: bool = notion_protocol == "https"
        conn: http.client.HTTPSConnection = (
            http.client.HTTPSConnection(notion_host, notion_port)
            if isHttps
            else http.client.HTTPConnection(notion_host, notion_port)
        )
        assert conn is not None, "Connection cannot be None"
        conn.request("PATCH", notion_database_uri, body_json, headers)
        response: http.client.HTTPResponse = conn.getresponse()
        assert response is not None, "Response cannot be None"
        response_status: int = response.status
        response_data: bytes = response.read()
        validate_http_response(response_status, response.reason, response_data)
        response_str: str = response_data.decode("utf-8")
        response_dict: dict = json.loads(response_str)
        return response_dict

    def unarchive_page_by_id(self, page_id: str) -> dict:
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
        notion_database_uri: str = f"/v1/pages/{page_id}"
        headers: dict = {
            "Authorization": f"Bearer {notion_api_key}",
            "Content-Type": "application/json",
            "Notion-Version": notion_version,
        }
        body: dict = {"archived": False}
        body_json: str = json.dumps(body)
        isHttps: bool = notion_protocol == "https"
        conn: http.client.HTTPSConnection = (
            http.client.HTTPSConnection(notion_host, notion_port)
            if isHttps
            else http.client.HTTPConnection(notion_host, notion_port)
        )
        assert conn is not None, "Connection cannot be None"
        conn.request("PATCH", notion_database_uri, body_json, headers)
        response: http.client.HTTPResponse = conn.getresponse()
        assert response is not None, "Response cannot be None"
        response_status: int = response.status
        response_data: bytes = response.read()
        validate_http_response(response_status, response.reason, response_data)
        response_str: str = response_data.decode("utf-8")
        response_dict: dict = json.loads(response_str)
        return response_dict