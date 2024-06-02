import sys, os
from typing import Any

from main.library.repositories.notion.models.notion_custom_icon import NotionIcon
from main.library.repositories.notion.utils.notion_icon_types import NOTION_ICON_TYPES

sys.path.insert(0, os.path.abspath("."))

from main.library.repositories.notion.models.notion_page import NotionPage
from main.library.repositories.notion.models.notion_page_block import NotionPageBlock
from main.library.repositories.notion.models.notion_property import NotionProperty


def build_block_from_response(block: dict) -> NotionPageBlock:
    assert block is not None, "Block cannot be None"
    assert "object" in block, "Block object cannot be None"
    assert block["object"] == "block", "Block object must be a block"
    assert "type" in block, "Block type cannot be None"
    block_type: str = block["type"]
    value: str = get_block_value_from_response(block)
    block_id: str = block["id"]
    return NotionPageBlock(block_type, value, block_id)


def build_page_from_response(response: dict) -> NotionPage:
    assert response is not None, "Response cannot be None"
    assert "object" in response, "Response object cannot be None"
    assert response["object"] == "page", "Response object must be a page"
    assert "properties" in response, "Response properties cannot be None"
    assert response["properties"] is not None, "Response properties cannot be None"
    page_id: str = response["id"]
    created_time: str = response["created_time"]
    last_edited_time: str = response["last_edited_time"]
    created_by: str = response["created_by"]["id"]
    last_edited_by: str = response["last_edited_by"]["id"]
    parent: dict = response["parent"]
    archived: bool = response["archived"]
    url: str = response["url"]
    request_id: str = ""
    if "request_id" in response:
        request_id: str = response["request_id"]
    page_icon: NotionIcon = get_icon_from_response(response)
    properties: dict = response["properties"]
    notionProperties: list = []
    notionBlocks: list = []
    for prop in properties:
        name: str = prop
        prop_type: str = properties[prop]["type"]
        value: str = get_prop_value_from_response(properties[prop])
        notionProperties.append(NotionProperty(name, prop_type, value))
    return NotionPage(
        page_icon,
        notionProperties,
        notionBlocks,
        page_id,
        parent,
        url,
        request_id,
        archived,
        created_time,
        last_edited_time,
        created_by,
        last_edited_by,
    )


def get_icon_from_response(response: dict) -> NotionIcon | None:
    assert response is not None, "Response cannot be None"
    assert "object" in response, "Response object cannot be None"
    assert response["object"] == "page", "Response object must be a page"
    if "icon" in response and response["icon"] is not None:
        assert response["icon"] is not None, "Response icon cannot be None"
        icon: dict = response["icon"]
        assert "type" in icon, "Icon type cannot be None"
        icon_type: str = icon["type"]
        if icon_type == NOTION_ICON_TYPES["emoji"]:
            return NotionIcon(icon_type, icon["emoji"])
        elif icon_type == NOTION_ICON_TYPES["external"]:
            return NotionIcon(icon_type, icon["external"]["url"])
        elif icon_type == NOTION_ICON_TYPES["file"]:
            return NotionIcon(icon_type, icon["file"]["url"])
        else:
            raise Exception(f"Invalid icon type: {icon_type}")
    else:
        return None


def get_block_value_from_response(block: dict) -> Any:
    assert block is not None, "Block cannot be None"
    assert "type" in block, "Block type cannot be None"
    block_type: str = block["type"]
    if block_type == "paragraph":
        return str(block["paragraph"]["rich_text"][0]["plain_text"])
    elif block_type == "heading_1":
        return str(block["heading_1"]["rich_text"][0]["plain_text"])
    elif block_type == "heading_2":
        return str(block["heading_2"]["rich_text"][0]["plain_text"])
    elif block_type == "heading_3":
        return str(block["heading_3"]["rich_text"][0]["plain_text"])
    elif block_type == "bulleted_list_item":
        return str(block["bulleted_list_item"]["rich_text"][0]["plain_text"])
    elif block_type == "numbered_list_item":
        return str(block["numbered_list_item"]["rich_text"][0]["plain_text"])
    elif block_type == "to_do":
        return str(block["to_do"]["rich_text"][0]["plain_text"])
    elif block_type == "toggle":
        return str(block["toggle"]["rich_text"][0]["plain_text"])
    elif block_type == "image":
        return str(block["image"]["external"]["url"])
    elif block_type == "video":
        return str(block["video"]["external"]["url"])
    elif block_type == "file":
        return {
            "name": str(block["file"]["name"]),
            "url": str(block["file"]["external"]["url"]),
        }
    elif block_type == "code":
        return {
            "content": str(block["code"]["rich_text"][0]["plain_text"]),
            "language": str(block["code"]["language"]),
        }
    elif block_type == "quote":
        return str(block["quote"]["rich_text"][0]["plain_text"])
    else:
        raise Exception(f"Invalid block type: {block_type}")


def get_prop_value_from_response(prop: dict) -> Any:
    assert prop is not None, "Property cannot be None"
    assert "type" in prop, "Property type cannot be None"
    prop_type: str = prop["type"]
    if prop_type == "title":
        return str(prop["title"][0]["plain_text"])
    elif prop_type == "rich_text":
        return str(prop["rich_text"][0]["plain_text"])
    elif prop_type == "number":
        return float(prop["number"])
    elif prop_type == "select":
        return {
            "name": str(prop["select"]["name"] if "name" in prop["select"] else ""),
            "color": str(prop["select"]["color"] if "color" in prop["select"] else ""),
        }
    elif prop_type == "multi_select":
        options: list[dict] = prop["multi_select"]
        return [
            {"name": str(option["name"]), "color": str(option["color"])}
            for option in options
        ]
    elif prop_type == "date":
        return str(prop["date"]["start"])
    elif prop_type == "people":
        people_ids: list[str] = [str(person["id"]) for person in prop["people"]]
        return people_ids
    elif prop_type == "files":
        files: list[dict] = prop["files"]
        files_to_return: list[dict] = []
        for file in files:
            file_obj: dict = {}
            if "external" in file:
                file_obj["name"] = str(file["name"])
                file_obj["url"] = str(file["external"]["url"] if "url" in file["external"] else "")
            elif "file" in file:
                file_obj["name"] = str(file["name"])
                file_obj["url"] = str(file["file"]["url"] if "url" in file["file"] else "")
            else:
                raise Exception(f"Unrecognized file object: {file}")
            files_to_return.append(file_obj)
        return files_to_return
    elif prop_type == "checkbox":
        return bool(prop["checkbox"])
    elif prop_type == "url":
        return str(prop["url"])
    elif prop_type == "email":
        return str(prop["email"])
    elif prop_type == "phone_number":
        return str(prop["phone_number"])
    elif prop_type == "formula":
        return dict(prop["formula"])
    elif prop_type == "relation":
        relation_list: list[dict] = prop["relation"]
        return [str(relation["id"]) for relation in relation_list]
    elif prop_type == "rollup":
        return dict(prop["rollup"])
    elif prop_type == "created_time":
        return str(prop["created_time"])
    elif prop_type == "last_edited_time":
        return str(prop["last_edited_time"])
    elif prop_type == "last_edited_by":
        return str(prop["last_edited_by"]["id"] if "id" in prop["last_edited_by"] else "")
    elif prop_type == "created_by":
        return str(prop["created_by"]["id"] if "id" in prop["created_by"] else "")
    else:
        raise Exception(f"Invalid property type: {prop_type}")


def build_blocks_for_request(page: NotionPage) -> list:
    assert page is not None, "Page cannot be None"
    assert page.blocks is not None, "Blocks cannot be None"
    assert len(page.blocks) >= 0, "Blocks cannot be empty"
    blocks: list = []
    for notionBlock in page.blocks:
        if notionBlock.type == "paragraph":
            assert isinstance(
                notionBlock.value, str
            ), "When type is paragraph, value must be a string"
            paragraph_content: str = notionBlock.value
            blocks.append(
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": paragraph_content,
                                },
                            }
                        ]
                    },
                }
            )
        elif notionBlock.type == "heading_1":
            assert isinstance(
                notionBlock.value, str
            ), "When type is heading_1, value must be a string"
            heading_1_content: str = notionBlock.value
            blocks.append(
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": heading_1_content,
                                },
                            }
                        ]
                    },
                }
            )
        elif notionBlock.type == "heading_2":
            assert isinstance(
                notionBlock.value, str
            ), "When type is heading_2, value must be a string"
            heading_2_content: str = notionBlock.value
            blocks.append(
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": heading_2_content,
                                },
                            }
                        ]
                    },
                }
            )
        elif notionBlock.type == "heading_3":
            assert isinstance(
                notionBlock.value, str
            ), "When type is heading_3, value must be a string"
            heading_3_content: str = notionBlock.value
            blocks.append(
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": heading_3_content,
                                },
                            }
                        ]
                    },
                }
            )
        elif notionBlock.type == "bulleted_list_item":
            assert isinstance(
                notionBlock.value, str
            ), "When type is bulleted_list_item, value must be a string"
            bulleted_single_item_content: str = notionBlock.value
            blocks.append(
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": bulleted_single_item_content,
                                },
                            }
                        ]
                    },
                }
            )
        elif notionBlock.type == "numbered_list_item":
            assert isinstance(
                notionBlock.value, str
            ), "When type is numbered_list_item, value must be a string"
            numbered_single_item_content: str = notionBlock.value
            blocks.append(
                {
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": numbered_single_item_content,
                                },
                            }
                        ]
                    },
                }
            )
        elif notionBlock.type == "to_do":
            assert isinstance(
                notionBlock.value, str
            ), "When type is to_do, value must be a string"
            todo_single_item_content: str = notionBlock.value
            blocks.append(
                {
                    "object": "block",
                    "type": "to_do",
                    "to_do": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": todo_single_item_content,
                                },
                            }
                        ]
                    },
                }
            )
        elif notionBlock.type == "toggle":
            assert isinstance(
                notionBlock.value, str
            ), "When type is toggle, value must be a string"
            toggle_single_item_content: str = notionBlock.value
            blocks.append(
                {
                    "object": "block",
                    "type": "toggle",
                    "toggle": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": toggle_single_item_content,
                                },
                            }
                        ]
                    },
                }
            )
        elif notionBlock.type == "image":
            assert isinstance(
                notionBlock.value, str
            ), "When type is image, value must be a string"
            image_url: str = notionBlock.value
            blocks.append(
                {
                    "object": "block",
                    "type": "image",
                    "image": {
                        "caption": [],
                        "type": "external",
                        "external": {
                            "url": image_url,
                        },
                    },
                }
            )
        elif notionBlock.type == "video":
            assert isinstance(
                notionBlock.value, str
            ), "When type is video, value must be a string"
            video_url: str = notionBlock.value
            blocks.append(
                {
                    "object": "block",
                    "type": "video",
                    "video": {
                        "caption": [],
                        "type": "external",
                        "external": {
                            "url": video_url,
                        },
                    },
                }
            )
        elif notionBlock.type == "file":
            assert isinstance(
                notionBlock.value, dict
            ), "When type is file, value must be a dictionary"
            file: dict = notionBlock.value
            file_name: str = file["name"]
            file_url: str = file["url"]
            blocks.append(
                {
                    "object": "block",
                    "type": "file",
                    "file": {
                        "caption": [],
                        "type": "external",
                        "external": {
                            "url": file_url,
                        },
                        "name": file_name,
                    },
                }
            )
        elif notionBlock.type == "code":
            assert isinstance(
                notionBlock.value, dict
            ), "When type is code, value must be a dictionary"
            code: dict = notionBlock.value
            code_content: str = code["content"]
            code_language: str = code["language"]
            blocks.append(
                {
                    "object": "block",
                    "type": "code",
                    "code": {
                        "caption": [],
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": code_content,
                                },
                            }
                        ],
                        "language": code_language,
                    },
                }
            )
        elif notionBlock.type == "quote":
            assert isinstance(
                notionBlock.value, str
            ), "When type is quote, value must be a string"
            quote_content: str = notionBlock.value
            blocks.append(
                {
                    "object": "block",
                    "type": "quote",
                    "quote": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": quote_content,
                                },
                            }
                        ]
                    },
                }
            )
        else:
            raise Exception(f"Invalid Notion block type: {notionBlock.type}")
    return blocks


def build_properties_for_request(page: NotionPage) -> dict:
    assert page is not None, "Page cannot be None"
    assert page.properties is not None, "Properties cannot be None"
    assert len(page.properties) > 0, "Properties cannot be empty"
    properties: dict = {}
    for notionProperty in page.properties:
        if notionProperty.type == "title":
            assert isinstance(
                notionProperty.value, str
            ), "When type is title, value must be a string"
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
            assert isinstance(
                notionProperty.value, str
            ), "When type is rich_text, value must be a string"
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
            assert isinstance(
                notionProperty.value, float
            ), "When type is number, value must be a float"
            properties[notionProperty.name] = {
                "number": notionProperty.value,
            }
        elif notionProperty.type == "select":
            assert isinstance(
                notionProperty.value, dict
            ), "When type is select, value must be a dictionary"
            selection_value: str = notionProperty.value["name"]
            selection_color: str = notionProperty.value["color"]
            properties[notionProperty.name] = {
                "select": {"name": selection_value, "color": selection_color}
            }
        elif notionProperty.type == "multi_select":
            assert isinstance(
                notionProperty.value, list
            ), "When type is multi_select, value must be a list of dictionaries"
            selection_list: list[dict] = notionProperty.value
            selections: list[dict] = [
                {"name": selection["name"], "color": selection["color"]}
                for selection in selection_list
            ]
            properties[notionProperty.name] = {"multi_select": selections}
        elif notionProperty.type == "date":
            assert isinstance(
                notionProperty.value, str
            ), "When type is date, value must be a string"
            properties[notionProperty.name] = {
                "date": {
                    "start": notionProperty.value,
                }
            }
        elif notionProperty.type == "people":
            assert isinstance(
                notionProperty.value, list
            ), "When type is people, value must be a list of strings"
            persons: list[str] = notionProperty.value
            person_ids: list[str] = [
                {"object": "user", "id": person_id} for person_id in persons
            ]
            properties[notionProperty.name] = {"people": person_ids}
        elif notionProperty.type == "files":
            assert isinstance(
                notionProperty.value, list
            ), "When type is files, value must be a list of strings"
            files: list[dict] = notionProperty.value
            files_obj: list[str] = [
                {"name": file["name"], "external": {"url": file["url"]}}
                for file in files
            ]
            properties[notionProperty.name] = {"files": files_obj}
        elif notionProperty.type == "checkbox":
            assert isinstance(
                notionProperty.value, bool
            ), "When type is checkbox, value must be a boolean"
            properties[notionProperty.name] = {
                "checkbox": notionProperty.value,
            }
        elif notionProperty.type == "url":
            assert isinstance(
                notionProperty.value, str
            ), "When type is url, value must be a string"
            properties[notionProperty.name] = {
                "url": notionProperty.value,
            }
        elif notionProperty.type == "email":
            assert isinstance(
                notionProperty.value, str
            ), "When type is email, value must be a string"
            properties[notionProperty.name] = {
                "email": notionProperty.value,
            }
        elif notionProperty.type == "phone_number":
            assert isinstance(
                notionProperty.value, str
            ), "When type is phone_number, value must be a string"
            properties[notionProperty.name] = {
                "phone_number": notionProperty.value,
            }
        elif notionProperty.type == "formula":
            raise Exception("Formulas are not supported for now")
        elif notionProperty.type == "relation":
            assert isinstance(
                notionProperty.value, list
            ), "When type is relation, value must be a list of strings"
            ids: list[str] = notionProperty.value
            relation: list[dict] = [{"id": id} for id in ids]
            properties[notionProperty.name] = {"relation": relation}
        elif notionProperty.type == "rollup":
            raise Exception("Rollups are not supported for now")
        elif notionProperty.type == "created_time":
            raise Exception("Created time should not be set manually")
        elif notionProperty.type == "last_edited_time":
            raise Exception("Last edited time should not be set manually")
        elif notionProperty.type == "last_edited_by":
            raise Exception("Last edited by should not be set manually")
        elif notionProperty.type == "created_by":
            raise Exception("Created by should not be set manually")
        else:
            raise Exception(f"Invalid Notion property type: {notionProperty.type}")
    return properties


def build_icon_for_request(page: NotionPage) -> dict:
    assert page is not None, "Page cannot be None"
    assert page.icon is not None, "Icon cannot be None"
    if page.icon.type == NOTION_ICON_TYPES["emoji"]:
        return {
            "type": NOTION_ICON_TYPES["emoji"],
            "emoji": page.icon.value,
        }
    elif page.icon.type == NOTION_ICON_TYPES["external"]:
        return {
            "type": NOTION_ICON_TYPES["external"],
            "external": {
                "url": page.icon.value,
            },
        }
    elif page.icon.type == NOTION_ICON_TYPES["file"]:
        return {
            "type": NOTION_ICON_TYPES["file"],
            "file": {
                "url": page.icon.value,
            },
        }
    else:
        raise Exception(f"Invalid Notion icon type: {page.icon.type}")
