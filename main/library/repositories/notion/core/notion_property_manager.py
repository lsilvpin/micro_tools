from typing import Any

from main.library.repositories.notion.models.notion_property import NotionProperty


class NotionPropertyManager:
    def create(self, notionProperty: NotionProperty, page_id: str):
        assert notionProperty is not None
        assert notionProperty.name is not None
        assert notionProperty.type is not None
        assert notionProperty.value is not None
        assert page_id is not None
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
        notion_database_id: str = self.settings_tool.get("NOTION_AGENTS_DB_ID")
        assert notion_database_id is not None, "NOTION_DATABASE_ID cannot be None"
        notion_database_uri: str = f"/v1/pages"
        headers: dict = {
            "Authorization": f"Bearer {notion_api_key}",
            "Content-Type": "application/json",
            "Notion-Version": notion_version,
        }
        body: dict = {
            "parent": {"database_id": notion_database_id},
            "icon": {"type": "emoji", "emoji": "👩🏻‍💻"},
            "properties": {
                "Nome": {
                    "title": [
                        {
                            "text": {
                                "content": nome,
                            }
                        }
                    ]
                },
                "Papel": {
                    "rich_text": [
                        {
                            "text": {
                                "content": papel,
                            }
                        }
                    ]
                },
                "Objetivo": {
                    "rich_text": [
                        {
                            "text": {
                                "content": objetivo,
                            }
                        }
                    ]
                },
            },
            "children": [
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
            ],
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
        self.__validate_response(response_status, response.reason, response_data)
        response_str: str = response_data.decode("utf-8")
        response_dict: dict = json.loads(response_str)
        return response_dict

