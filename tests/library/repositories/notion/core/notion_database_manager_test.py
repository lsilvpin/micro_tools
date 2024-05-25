import sys, os

from main.library.repositories.notion.core.notion_database_manager import (
    NotionDatabaseManager,
)
from main.library.repositories.notion.models.notion_custom_icon import NotionIcon
from main.library.repositories.notion.models.notion_database import NotionDatabase
from main.library.repositories.notion.utils.notion_icon_types import NOTION_ICON_TYPES
from main.library.tools.core.log_tool import LogTool
from main.library.tools.core.settings_tool import SettingsTool

sys.path.insert(0, os.path.abspath("."))

from main.library.di_container import Container
from main.library.repositories.notion.core.notion_page_manager import NotionPageManager
from main.library.repositories.notion.models.notion_page import NotionPage
from main.library.repositories.notion.models.notion_page_block import NotionPageBlock
from main.library.repositories.notion.models.notion_property import NotionProperty
from main.library.repositories.notion.utils.notion_block_types import NOTION_BLOCK_TYPES
from main.library.repositories.notion.utils.notion_property_types import (
    NOTION_PROPERTY_TYPES,
)

container: Container = Container()
settings_tool: SettingsTool = container.settings_tool()
log_tool: LogTool = container.log_tool()
notion_database_manager: NotionDatabaseManager = container.notion_database_manager()


def test_should_create_database(mocker):
    # Mocks
    successResponse = mocker.Mock()
    successResponse.status = 200
    sample: str = (
        '{"object":"database","id":"1c62e8a0-bb82-46d9-8000-71c3679e840e","cover":null,"icon":{"type":"emoji","emoji":"🚀"},"created_time":"2024-05-25T10:45:00.000Z","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"last_edited_time":"2024-05-25T10:49:00.000Z","title":[{"type":"text","text":{"content":"Banco de dados","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Banco de dados","href":null}],"description":[{"type":"text","text":{"content":"Descrição do db","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Descrição do db","href":null}],"is_inline":true,"properties":{"Criado por":{"id":"%3DtzW","name":"Criado por","type":"created_by","created_by":{}},"Description":{"id":"GjYQ","name":"Description","type":"rich_text","rich_text":{}},"Pessoa":{"id":"I%3CHo","name":"Pessoa","type":"people","people":{}},"IsTrue":{"id":"S%7BCr","name":"IsTrue","type":"checkbox","checkbox":{}},"Criado em":{"id":"VGNJ","name":"Criado em","type":"created_time","created_time":{}},"Última edição":{"id":"b%3DU%5E","name":"Última edição","type":"last_edited_time","last_edited_time":{}},"URL":{"id":"bSXz","name":"URL","type":"url","url":{}},"Tags":{"id":"ey%5CV","name":"Tags","type":"multi_select","multi_select":{"options":[{"id":"936c9256-25b5-4136-9b8a-395b6a28fbbe","name":"Tag A","color":"orange","description":null},{"id":"d4c1753a-3d76-4d37-b09a-1000cdc38e26","name":"Tag B","color":"blue","description":null},{"id":"eeecfecb-38ea-445b-adf9-01cfd3e0b0b9","name":"Tag C","color":"gray","description":null},{"id":"06f416c3-ecb2-4d92-bd6d-f6ce17b645d7","name":"Tag D","color":"yellow","description":null},{"id":"18113695-d4de-47f2-ac75-36113cd20d5f","name":"Tag 1","color":"gray","description":null},{"id":"026cfaef-68f1-4c92-8673-7cb80793b606","name":"Tag 2","color":"blue","description":null}]}},"Email":{"id":"goDM","name":"Email","type":"email","email":{}},"Data":{"id":"jPYm","name":"Data","type":"date","date":{}},"Arquivo":{"id":"syp%7B","name":"Arquivo","type":"files","files":{}},"Number":{"id":"wu%5Ep","name":"Number","type":"number","number":{"format":"number"}},"Select":{"id":"%7B%40lO","name":"Select","type":"select","select":{"options":[{"id":"b12d6d48-c142-429e-843e-2449f7af7926","name":"Alface","color":"green","description":null},{"id":"3b9b9c16-4ae4-43c3-9892-ba97117f9913","name":"Cebola","color":"pink","description":null},{"id":"8707be84-4a20-411b-8601-23f989729211","name":"Kacto","color":"yellow","description":null},{"id":"67a4e6aa-9f04-4052-ace2-30ff5584d877","name":"Option 1","color":"gray","description":null}]}},"Última edição por":{"id":"~IgL","name":"Última edição por","type":"last_edited_by","last_edited_by":{}},"Número Telefone":{"id":"~V%5C%7B","name":"Número Telefone","type":"phone_number","phone_number":{}},"Name":{"id":"title","name":"Name","type":"title","title":{}}},"parent":{"type":"page_id","page_id":"6f48b54c-094d-4339-aa90-89f9985fb6c7"},"url":"https://www.notion.so/1c62e8a0bb8246d9800071c3679e840e","public_url":null,"archived":false,"in_trash":false,"developer_survey":"https://notionup.typeform.com/to/bllBsoI4?utm_source=postman","request_id":"f5f68e21-08a3-4b39-98a7-ab0f1b489f4b"}'
    )
    successResponse.read.return_value = sample.encode("utf-8")
    conn = mocker.Mock()
    conn.getresponse.return_value = successResponse
    mocker.patch("http.client.HTTPSConnection", return_value=conn)

    # Arrange
    page_id: str = "6f48b54c-094d-4339-aa90-89f9985fb6c7"
    icon: NotionIcon = NotionIcon("emoji", "👩🏻‍💻")
    nome: NotionProperty = NotionProperty(
        "Nome", NOTION_PROPERTY_TYPES["title"], "Exemplo de nome"
    )
    papel: NotionProperty = NotionProperty(
        "Papel", NOTION_PROPERTY_TYPES["rich_text"], "Exemplo de Papel"
    )
    objetivo: NotionProperty = NotionProperty(
        "Objetivo", NOTION_PROPERTY_TYPES["rich_text"], "Exemplo de objetivo"
    )
    is_inline: bool = True
    database: NotionDatabase = NotionDatabase(
        icon,
        "Meu Banco de Dados",
        [nome, papel, objetivo],
        "Descrição do banco de dados",
        is_inline,
    )

    # Act
    response_data: dict = notion_database_manager.create_database(page_id, database)

    # Assert
    assert response_data is not None
    assert response_data["object"] == "database"
    assert response_data["id"] is not None
    assert response_data["cover"] is None
    assert response_data["icon"] is not None
    assert response_data["created_time"] is not None
    assert response_data["created_by"] is not None
    assert response_data["last_edited_by"] is not None
    assert response_data["last_edited_time"] is not None
    assert response_data["title"] is not None
    assert response_data["description"] is not None
    assert response_data["is_inline"] is True
    assert response_data["properties"] is not None
    assert response_data["parent"] is not None
    assert response_data["url"] is not None
    assert response_data["public_url"] is None
    assert response_data["archived"] is False
    assert response_data["in_trash"] is False
    assert response_data["developer_survey"] is not None
    assert response_data["request_id"] is not None
