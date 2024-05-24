import sys, os, http.client, json

from main.library.repositories.notion.models.notion_page_block import NotionPageBlock
from main.library.repositories.notion.models.notion_property import NotionProperty
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
        response_page: NotionPage = self.__build_page_from_response(response_dict)
        return response_page
    
    def __build_page_from_response(self, response: dict) -> NotionPage:
        assert response is not None, "Response cannot be None"
        assert "object" in response, "Response object cannot be None"
        assert response["object"] == "page", "Response object must be a page"
        assert "properties" in response, "Response properties cannot be None"
        assert response["properties"] is not None, "Response properties cannot be None"
        page_id: str = response["id"]
        properties: dict = response["properties"]
        notionProperties: list = []
        notionBlocks: list = []
        for prop in properties:
            name: str = prop
            prop_type: str = properties[prop]["type"]
            value: str = self.__get_prop_value_from_response(properties[prop])
            notionProperties.append(NotionProperty(name, prop_type, value))
        return NotionPage(notionProperties, notionBlocks, page_id)
    
    def __get_block_value_from_response(self, block: dict) -> str:
        assert block is not None, "Block cannot be None"
        assert "type" in block, "Block type cannot be None"
        block_type: str = block["type"]
        if block_type == "paragraph":
            return block["paragraph"]["text"][0]["text"]["content"]
        elif block_type == "heading_1":
            return block["heading_1"]["text"][0]["text"]["content"]
        elif block_type == "heading_2":
            return block["heading_2"]["text"][0]["text"]["content"]
        elif block_type == "heading_3":
            return block["heading_3"]["text"][0]["text"]["content"]
        elif block_type == "bulleted_list":
            return block["bulleted_list"]["text"][0]["text"]["content"]
        elif block_type == "numbered_list":
            return block["numbered_list"]["text"][0]["text"]["content"]
        elif block_type == "to_do":
            return block["to_do"]["text"][0]["text"]["content"]
        elif block_type == "toggle":
            return block["toggle"]["text"][0]["text"]["content"]
        elif block_type == "image":
            return block["image"]["external"]["url"]
        elif block_type == "video":
            return block["video"]["external"]["url"]
        elif block_type == "file":
            return block["file"]["external"]["url"]
        elif block_type == "code":
            return block["code"]["text"]
        elif block_type == "quote":
            return block["quote"]["text"][0]["text"]["content"]
        else:
            raise Exception(f"Invalid block type: {block_type}")
    
    def __get_prop_value_from_response(self, prop: dict) -> str:
        assert prop is not None, "Property cannot be None"
        assert "type" in prop, "Property type cannot be None"
        prop_type: str = prop["type"]
        if prop_type == "title":
            return prop["title"][0]["plain_text"]
        elif prop_type == "rich_text":
            return prop["rich_text"][0]["plain_text"]
        elif prop_type == "number":
            return str(prop["number"])
        elif prop_type == "select":
            return prop["select"]["name"]
        elif prop_type == "multi_select":
            return prop["multi_select"][0]["name"]
        elif prop_type == "date":
            return prop["date"]["start"]
        elif prop_type == "people":
            return prop["people"][0]["id"]
        elif prop_type == "files":
            return prop["files"][0]["id"]
        elif prop_type == "checkbox":
            return str(prop["checkbox"])
        elif prop_type == "url":
            return prop["url"]
        elif prop_type == "email":
            return prop["email"]
        elif prop_type == "phone_number":
            return prop["phone_number"]
        elif prop_type == "formula":
            return prop["formula"]["expression"]
        elif prop_type == "relation":
            return prop["relation"][0]["id"]
        elif prop_type == "rollup":
            return prop["rollup"]["array"][0]["id"]
        elif prop_type == "created_time":
            return prop["created_time"]
        elif prop_type == "last_edited_time":
            return prop["last_edited_time"]
        elif prop_type == "last_edited_by":
            return prop["last_edited_by"]["id"]
        elif prop_type == "created_by":
            return prop["created_by"]["id"]
        else:
            raise Exception(f"Invalid property type: {prop_type}")

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
