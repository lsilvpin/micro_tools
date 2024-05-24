import sys, os, http.client, json

from main.library.repositories.notion.utils.notion_validations import (
    validate_http_response,
)

sys.path.insert(0, os.path.abspath("."))
from main.library.repositories.notion.models.notion_page import NotionPage
from main.library.tools.core.log_tool import LogTool
from main.library.tools.core.settings_tool import SettingsTool


class NotionPageManager:
    def __init__(self, settings_tool: SettingsTool, log_tool: LogTool):
        self.settings_tool: SettingsTool = settings_tool
        self.log_tool: LogTool = log_tool

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
        properties: dict = self.__build_properties(page)
        blocks: list = self.__build_blocks(page)
        body: dict = {
            "parent": {"database_id": database_id},
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
        conn.request("POST", notion_database_uri, body_json, headers)
        response: http.client.HTTPResponse = conn.getresponse()
        assert response is not None, "Response cannot be None"
        response_status: int = response.status
        response_data: bytes = response.read()
        validate_http_response(response_status, response.reason, response_data)
        response_str: str = response_data.decode("utf-8")
        response_dict: dict = json.loads(response_str)
        return response_dict

    def __build_blocks(self, page: NotionPage) -> list:
        assert page is not None, "Page cannot be None"
        assert page.blocks is not None, "Blocks cannot be None"
        assert len(page.blocks) >= 0, "Blocks cannot be empty"
        blocks: list = []
        for notionBlock in page.blocks:
            if notionBlock.type == "paragraph":
                blocks.append(
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": notionBlock.value,
                                    },
                                }
                            ]
                        },
                    }
                )
            elif notionBlock.type == "heading_1":
                blocks.append(
                    {
                        "object": "block",
                        "type": "heading_1",
                        "heading_1": {
                            "text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": notionBlock.value,
                                    },
                                }
                            ]
                        },
                    }
                )
            elif notionBlock.type == "heading_2":
                blocks.append(
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": notionBlock.value,
                                    },
                                }
                            ]
                        },
                    }
                )
            elif notionBlock.type == "heading_3":
                blocks.append(
                    {
                        "object": "block",
                        "type": "heading_3",
                        "heading_3": {
                            "text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": notionBlock.value,
                                    },
                                }
                            ]
                        },
                    }
                )
            elif notionBlock.type == "bulleted_list":
                blocks.append(
                    {
                        "object": "block",
                        "type": "bulleted_list",
                        "bulleted_list": {
                            "text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": notionBlock.value,
                                    },
                                }
                            ]
                        },
                    }
                )
            elif notionBlock.type == "numbered_list":
                blocks.append(
                    {
                        "object": "block",
                        "type": "numbered_list",
                        "numbered_list": {
                            "text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": notionBlock.value,
                                    },
                                }
                            ]
                        },
                    }
                )
            elif notionBlock.type == "to_do":
                blocks.append(
                    {
                        "object": "block",
                        "type": "to_do",
                        "to_do": {
                            "text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": notionBlock.value,
                                    },
                                }
                            ]
                        },
                    }
                )
            elif notionBlock.type == "toggle":
                blocks.append(
                    {
                        "object": "block",
                        "type": "toggle",
                        "toggle": {
                            "text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": notionBlock.value,
                                    },
                                }
                            ]
                        },
                    }
                )
            elif notionBlock.type == "image":
                blocks.append(
                    {
                        "object": "block",
                        "type": "image",
                        "image": {
                            "caption": [],
                            "type": "external",
                            "external": {
                                "url": notionBlock.value,
                            },
                        },
                    }
                )
            elif notionBlock.type == "video":
                blocks.append(
                    {
                        "object": "block",
                        "type": "video",
                        "video": {
                            "caption": [],
                            "type": "external",
                            "external": {
                                "url": notionBlock.value,
                            },
                        },
                    }
                )
            elif notionBlock.type == "file":
                blocks.append(
                    {
                        "object": "block",
                        "type": "file",
                        "file": {
                            "caption": [],
                            "type": "external",
                            "external": {
                                "url": notionBlock.value,
                            },
                        },
                    }
                )
            elif notionBlock.type == "code":
                blocks.append(
                    {
                        "object": "block",
                        "type": "code",
                        "code": {
                            "text": notionBlock.value,
                        },
                    }
                )
            elif notionBlock.type == "quote":
                blocks.append(
                    {
                        "object": "block",
                        "type": "quote",
                        "quote": {
                            "text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": notionBlock.value,
                                    },
                                }
                            ]
                        },
                    }
                )
            else:
                raise Exception(f"Invalid Notion block type: {notionBlock.type}")
        return blocks

    def __build_properties(self, page: NotionPage) -> dict:
        assert page is not None, "Page cannot be None"
        assert page.properties is not None, "Properties cannot be None"
        assert len(page.properties) > 0, "Properties cannot be empty"
        properties: dict = {}
        for notionProperty in page.properties:
            if notionProperty.type == "title":
                properties[notionProperty.name] = {
                    "title": [
                        {
                            "text": {
                                "content": notionProperty.value,
                            }
                        }
                    ]
                }
            elif notionProperty.type == "rich_text":
                properties[notionProperty.name] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": notionProperty.value,
                            }
                        }
                    ]
                }
            elif notionProperty.type == "number":
                properties[notionProperty.name] = {
                    "number": notionProperty.value,
                }
            elif notionProperty.type == "select":
                properties[notionProperty.name] = {
                    "select": {
                        "name": notionProperty.value,
                    }
                }
            elif notionProperty.type == "multi_select":
                properties[notionProperty.name] = {
                    "multi_select": [
                        {
                            "name": notionProperty.value,
                        }
                    ]
                }
            elif notionProperty.type == "date":
                properties[notionProperty.name] = {
                    "date": {
                        "start": notionProperty.value,
                    }
                }
            elif notionProperty.type == "people":
                properties[notionProperty.name] = {
                    "people": [
                        {
                            "object": "user",
                            "id": notionProperty.value,
                        }
                    ]
                }
            elif notionProperty.type == "files":
                properties[notionProperty.name] = {
                    "files": [
                        {
                            "object": "file",
                            "id": notionProperty.value,
                        }
                    ]
                }
            elif notionProperty.type == "checkbox":
                properties[notionProperty.name] = {
                    "checkbox": notionProperty.value,
                }
            elif notionProperty.type == "url":
                properties[notionProperty.name] = {
                    "url": notionProperty.value,
                }
            elif notionProperty.type == "email":
                properties[notionProperty.name] = {
                    "email": notionProperty.value,
                }
            elif notionProperty.type == "phone_number":
                properties[notionProperty.name] = {
                    "phone_number": notionProperty.value,
                }
            elif notionProperty.type == "formula":
                properties[notionProperty.name] = {
                    "formula": {
                        "expression": notionProperty.value,
                    }
                }
            elif notionProperty.type == "relation":
                properties[notionProperty.name] = {
                    "relation": [
                        {
                            "id": notionProperty.value,
                        }
                    ]
                }
            elif notionProperty.type == "rollup":
                properties[notionProperty.name] = {
                    "rollup": {
                        "array": [
                            {
                                "id": notionProperty.value,
                            }
                        ]
                    }
                }
            elif notionProperty.type == "created_time":
                properties[notionProperty.name] = {
                    "created_time": notionProperty.value,
                }
            elif notionProperty.type == "last_edited_time":
                properties[notionProperty.name] = {
                    "last_edited_time": notionProperty.value,
                }
            elif notionProperty.type == "last_edited_by":
                properties[notionProperty.name] = {
                    "last_edited_by": {
                        "object": "user",
                        "id": notionProperty.value,
                    }
                }
            elif notionProperty.type == "created_by":
                properties[notionProperty.name] = {
                    "created_by": {
                        "object": "user",
                        "id": notionProperty.value,
                    }
                }
            else:
                raise Exception(f"Invalid Notion property type: {notionProperty.type}")
        return properties
