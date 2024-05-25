import json
import sys, os
from typing import Any

sys.path.insert(0, os.path.abspath("."))
from main.library.repositories.notion.models.notion_custom_icon import NotionIcon
from main.library.repositories.notion.models.notion_property import NotionProperty


class NotionDatabase:
    def __init__(
        self,
        icon: NotionIcon,
        title: dict,
        properties: list[NotionProperty],
        description: dict,
        is_inline: bool,
        parent_id: dict | None = None,
        id: str | None = None,
        archived: bool | None = None,
        url: str | None = None,
        request_id: str | None = None,
    ):
        self.is_inline = is_inline
        self.parent_id = parent_id
        self.icon = icon
        self.title = title
        self.description = description
        self.properties = properties
        self.id = id
        self.archived = archived
        self.url = url
        self.request_id = request_id

    def __str__(self):
        return f"NotionDatabase(is_inline={self.is_inline}, parent={self.parent_id}, icon={self.icon}, title={self.title}, description={self.description}, properties={self.properties}, database_id={self.id}, archived={self.archived}, url={self.url}, request_id={self.request_id})"

    def __repr__(self):
        return self.__str__()

    def from_json(self, data: str):
        return self.from_dict(json.loads(data))

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_create_payload(self) -> dict:
        assert self.is_inline is not None, "is_inline cannot be None"
        assert self.parent_id is not None, "parent cannot be None"
        assert self.icon is not None, "icon cannot be None"
        assert self.title is not None, "title cannot be None"
        assert self.description is not None, "description cannot be None"
        assert self.properties is not None, "properties cannot be None"
        assert len(self.properties) > 0, "properties cannot be empty"
        payload: dict = {
            "is_inline": bool(self.is_inline),
            "parent": {"type": "page_id", "page_id": str(self.parent_id)},
            "icon": self.icon.to_payload(),
            "title": [{"text": {"content": str(self.title)}}],
            "description": [{"text": {"content": str(self.description)}}],
            "properties": {},
        }
        for prop in self.properties:
            assert prop.name is not None, "Property name cannot be None"
            assert prop.type is not None, "Property type cannot be None"
            payload["properties"][prop.name] = (
                self.__get_prop_options_to_create_db_payload(prop)
            )
        return payload

    def to_update_payload(self) -> dict:
        assert self.is_inline is not None, "is_inline cannot be None"
        assert self.icon is not None, "icon cannot be None"
        assert self.title is not None, "title cannot be None"
        assert self.description is not None, "description cannot be None"
        assert self.properties is not None, "properties cannot be None"
        assert len(self.properties) > 0, "properties cannot be empty"
        payload: dict = {
            "is_inline": bool(self.is_inline),
            "icon": self.icon.to_payload(),
            "title": [{"text": {"content": str(self.title)}}],
            "description": [{"text": {"content": str(self.description)}}],
            "properties": {},
        }
        for prop in self.properties:
            assert prop.name is not None, "Property name cannot be None"
            assert prop.type is not None, "Property type cannot be None"
            payload["properties"][prop.name] = (
                self.__get_prop_options_to_create_db_payload(prop)
            )
        return payload

    def to_archive_or_unarchive_payload(self) -> dict:
        assert self.archived is not None, "archived cannot be None"
        return {"archived": self.archived}

    @staticmethod
    def from_dict(data: dict):
        assert data is not None, "Database Data should not be None"
        assert "is_inline" in data, "Database Data should have an is_inline"
        assert "icon" in data, "Database Data should have an icon"
        assert "title" in data, "Database Data should have a title"
        assert "description" in data, "Database Data should have a description"
        assert "properties" in data, "Database Data should have properties"
        assert (
            len(data["properties"]) > 0
        ), "Database Data should have at least one property"
        database_id: str | None = None
        if "id" in data:
            database_id = str(data["id"])
        parent_id: str | None = None
        if "parent_id" in data:
            parent_id = str(data["parent_id"])
        is_inline: bool = bool(data["is_inline"])
        icon: NotionIcon = NotionIcon.from_dict(data["icon"])
        title: str = str(data["title"])
        description: str = str(data["description"])
        properties: list[NotionProperty] = []
        for p in data["properties"]:
            prop = NotionProperty.from_dict(p)
            properties.append(prop)
        archived: bool = True
        if "archived" in data:
            archived = bool(data["archived"])
        url: str | None = None
        if "url" in data:
            url = str(data["url"])
        request_id: str | None = None
        if "request_id" in data:
            request_id = str(data["request_id"])
        db: NotionDatabase = NotionDatabase(
            icon,
            title,
            properties,
            description,
            is_inline,
            parent_id,
            database_id,
            archived,
            url,
            request_id,
        )
        return db

    @staticmethod
    def from_read_response(data: dict):
        assert data is not None, "Database Data from read response should not be None"
        assert "id" in data, "Database Data from read response should have an id"
        assert (
            "is_inline" in data
        ), "Database Data from read response should have an is_inline"
        assert "parent" in data, "Database Data from read response should have a parent"
        assert "icon" in data, "Database Data from read response should have an icon"
        assert "title" in data, "Database Data from read response should have a title"
        assert (
            "description" in data
        ), "Database Data from read response should have a description"
        assert (
            "properties" in data
        ), "Database Data from read response should have properties"
        assert (
            len(data["properties"]) > 0
        ), "Database Data from read response should have at least one property"
        assert (
            "archived" in data
        ), "Database Data from read response should have an archived"
        assert "url" in data, "Database Data from read response should have an url"
        database_id: str = str(data["id"])
        is_inline: bool = bool(data["is_inline"])
        parent_id: str = NotionDatabase.get_parent_from_response(data["parent"])
        icon: NotionIcon = NotionIcon.from_response(data["icon"])
        title: str = str(data["title"][0]["plain_text"])
        description: str | None = None
        if "description" in data and len(data["description"]) > 0:
            description = str(data["description"][0]["plain_text"])
        properties: list[NotionProperty] = NotionDatabase.get_properties_from_response(
            data["properties"]
        )
        archived: bool = bool(data["archived"])
        url: str = str(data["url"])
        request_id: str | None = None
        if "request_id" in data:
            request_id = str(data["request_id"])
        db: NotionDatabase = NotionDatabase(
            icon,
            title,
            properties,
            description,
            is_inline,
            parent_id,
            database_id,
            archived,
            url,
            request_id,
        )
        return db

    @staticmethod
    def get_properties_from_response(properties_data: dict) -> list[NotionProperty]:
        properties: list[NotionProperty] = []
        for key, value in properties_data.items():
            prop = dict(value)
            prop_name: str = key
            prop_type: str = prop["type"]
            prop_options: Any = None
            if prop_type == "number":
                prop_options = prop["number"]
            elif prop_type == "select":
                prop_options = prop["select"]
            elif prop_type == "multi_select":
                prop_options = prop["multi_select"]
            else:
                prop_options = prop[prop_type]
            properties.append(NotionProperty(prop_name, prop_type, None, prop_options))
        return properties

    @staticmethod
    def get_parent_from_response(parent_data: dict) -> str:
        assert parent_data is not None, "Parent Data should not be None"
        assert "type" in parent_data, "Parent Data should have a type"
        assert "page_id" in parent_data, "Parent Data should have a page_id"
        return str(parent_data["page_id"])

    def __get_prop_options_to_create_db_payload(self, prop: NotionProperty) -> dict:
        prop_options: Any = prop.options
        if prop.type == "number":
            assert (
                prop_options is not None
            ), "When type is number, property options cannot be None"
            return {"number": {"format": prop_options["format"]}}
        elif prop.type == "select":
            assert (
                prop_options is not None
            ), "When type is select, property options cannot be None"
            return {"select": {"options": prop_options["options"]}}
        elif prop.type == "multi_select":
            return {"multi_select": {"options": prop_options["options"]}}
        else:
            return {f"{prop.type}": {}}
