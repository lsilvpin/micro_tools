import sys, os

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
notion_page_manager: NotionPageManager = container.notion_page_manager()


def test_should_create_agent_page(mocker):
    # Mocks
    successResponse = mocker.Mock()
    successResponse.status = 200
    sample: str = (
        '{"object":"page","id":"c5353a8c-a89c-4dd0-96c5-e3e2d19a0387","created_time":"2024-05-24T14:23:00.000Z","last_edited_time":"2024-05-24T14:23:00.000Z","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"cover":null,"icon":{"type":"emoji","emoji":"👩🏻‍💻"},"parent":{"type":"database_id","database_id":"6301f640-e21c-4526-a72e-d96e7d4ba71d"},"archived":false,"in_trash":false,"properties":{"Papel":{"id":"PqtR","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Exemplo de Papel","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de Papel","href":null}]},"Objetivo":{"id":"TF%7BM","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Exemplo de objetivo","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de objetivo","href":null}]},"Nome":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Exemplo de nome","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de nome","href":null}]}},"url":"https://www.notion.so/Exemplo-de-nome-c5353a8ca89c4dd096c5e3e2d19a0387","public_url":null,"developer_survey":"https://notionup.typeform.com/to/bllBsoI4?utm_source=postman","request_id":"50003c9b-16bb-4409-86b4-96f02d25a24e"}'
    )
    successResponse.read.return_value = sample.encode("utf-8")
    conn = mocker.Mock()
    conn.getresponse.return_value = successResponse
    mocker.patch("http.client.HTTPSConnection", return_value=conn)

    # Arrange
    database_id: str = "6301f640e21c4526a72ed96e7d4ba71d"
    nome: NotionProperty = NotionProperty(
        "Nome", NOTION_PROPERTY_TYPES["title"], "Exemplo de nome"
    )
    papel: NotionProperty = NotionProperty(
        "Papel", NOTION_PROPERTY_TYPES["rich_text"], "Exemplo de Papel"
    )
    objetivo: NotionProperty = NotionProperty(
        "Objetivo", NOTION_PROPERTY_TYPES["rich_text"], "Exemplo de objetivo"
    )
    image: NotionPageBlock = NotionPageBlock(
        NOTION_BLOCK_TYPES["image"],
        "https://images.unsplash.com/photo-1513097633097-329a3a64e0d4?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb",
    )
    page: NotionPage = NotionPage([nome, papel, objetivo], [image])

    # Act
    response_data: dict = notion_page_manager.create_page(page, database_id)

    # Assert
    assert response_data is not None
    assert "object" in response_data
    assert response_data["object"] == "page"
    assert "Nome" in response_data["properties"]
    assert "Objetivo" in response_data["properties"]
    assert "Papel" in response_data["properties"]
    assert (
        response_data["properties"]["Nome"]["title"][0]["text"]["content"] == nome.value
    )
    assert (
        response_data["properties"]["Objetivo"]["rich_text"][0]["text"]["content"]
        == objetivo.value
    )
    assert (
        response_data["properties"]["Papel"]["rich_text"][0]["text"]["content"]
        == papel.value
    )


def test_should_read_page_properties_by_page_id(mocker):
    # Mocks
    successResponse = mocker.Mock()
    successResponse.status = 200
    sample: str = (
        '{"object":"page","id":"48a4c8b5-8c75-43ee-8863-505c38ffa20e","created_time":"2024-05-24T01:47:00.000Z","last_edited_time":"2024-05-24T02:04:00.000Z","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"cover":null,"icon":{"type":"emoji","emoji":"👩🏻‍💻"},"parent":{"type":"database_id","database_id":"6301f640-e21c-4526-a72e-d96e7d4ba71d"},"archived":false,"in_trash":false,"properties":{"Papel":{"id":"PqtR","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Exemplo de Papel","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de Papel","href":null}]},"Objetivo":{"id":"TF%7BM","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Exemplo de objetivo","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de objetivo","href":null}]},"Nome":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Exemplo de nome 3","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de nome 3","href":null}]}},"url":"https://www.notion.so/Exemplo-de-nome-3-48a4c8b58c7543ee8863505c38ffa20e","public_url":null,"developer_survey":"https://notionup.typeform.com/to/bllBsoI4?utm_source=postman","request_id":"e0f3a17f-5281-470a-960f-369392eec3a7"}'
    )
    successResponse.read.return_value = sample.encode("utf-8")
    conn = mocker.Mock()
    conn.getresponse.return_value = successResponse
    mocker.patch("http.client.HTTPSConnection", return_value=conn)

    # Arrange
    page_id: str = "c5353a8c-a89c-4dd0-96c5-e3e2d19a0387"

    # Act
    response_page: NotionPage = notion_page_manager.read_page_properties_by_page_id(
        page_id
    )

    # Assert
    assert response_page is not None, "Page not found"
    assert response_page.properties is not None, "Page properties are empty"


def test_should_read_page_by_id(mocker):
    # Mocks
    successResponse = mocker.Mock()
    successResponse.status = 200
    sample: str = (
        '{"object":"page","id":"48a4c8b5-8c75-43ee-8863-505c38ffa20e","created_time":"2024-05-24T01:47:00.000Z","last_edited_time":"2024-05-24T02:04:00.000Z","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"cover":null,"icon":{"type":"emoji","emoji":"👩🏻‍💻"},"parent":{"type":"database_id","database_id":"6301f640-e21c-4526-a72e-d96e7d4ba71d"},"archived":false,"in_trash":false,"properties":{"Papel":{"id":"PqtR","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Exemplo de Papel","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de Papel","href":null}]},"Objetivo":{"id":"TF%7BM","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Exemplo de objetivo","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de objetivo","href":null}]},"Nome":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Exemplo de nome 3","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de nome 3","href":null}]}},"url":"https://www.notion.so/Exemplo-de-nome-3-48a4c8b58c7543ee8863505c38ffa20e","public_url":null,"developer_survey":"https://notionup.typeform.com/to/bllBsoI4?utm_source=postman","request_id":"e0f3a17f-5281-470a-960f-369392eec3a7"}'
    )
    successResponse.read.return_value = sample.encode("utf-8")
    conn = mocker.Mock()
    conn.getresponse.return_value = successResponse
    mocker.patch("http.client.HTTPSConnection", return_value=conn)
    notion_block_manager_mock = mocker.patch(
        "main.library.repositories.notion.core.notion_block_manager.NotionBlockManager"
    )
    notion_block_manager_mock.read_page_blocks_by_page_id.return_value = {
        "has_more": False,
        "next_cursor": None,
        "blocks": [
            NotionPageBlock(NOTION_BLOCK_TYPES["paragraph"], "This is a test 1"),
            NotionPageBlock(NOTION_BLOCK_TYPES["paragraph"], "This is a test 2"),
            NotionPageBlock(NOTION_BLOCK_TYPES["paragraph"], "This is a test 3"),
        ],
    }

    # Arrange
    notion_page_manager_with_mocks = NotionPageManager(
        settings_tool, log_tool, notion_block_manager_mock
    )
    page_id: str = "c5353a8c-a89c-4dd0-96c5-e3e2d19a0387"

    # Act
    response_page: NotionPage = notion_page_manager_with_mocks.read_page_by_id(page_id)

    # Assert
    assert response_page is not None, "Page not found"
    assert response_page.properties is not None, "Page properties are empty"
    assert len(response_page.properties) > 0, "Page properties are empty"
    assert response_page.blocks is not None, "Page blocks are empty"
    assert len(response_page.blocks) > 0, "Page blocks are empty"

def test_should_archive_page_by_id(mocker):
    # Mocks
    successResponse = mocker.Mock()
    successResponse.status = 200
    sample: str = (
        '{"object":"page","id":"b278bdba-2484-4976-a2fc-36414c73d73d","created_time":"2024-05-24T01:40:00.000Z","last_edited_time":"2024-05-24T17:56:00.000Z","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"cover":null,"icon":{"type":"external","external":{"url":"https://www.notion.so/icons/document_gray.svg"}},"parent":{"type":"database_id","database_id":"6301f640-e21c-4526-a72e-d96e7d4ba71d"},"archived":true,"in_trash":true,"properties":{"Papel":{"id":"PqtR","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Exemplo de Papel","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de Papel","href":null}]},"Objetivo":{"id":"TF%7BM","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Exemplo de objetivo","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de objetivo","href":null}]},"Nome":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Exemplo de nome","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de nome","href":null}]}},"url":"https://www.notion.so/Exemplo-de-nome-b278bdba24844976a2fc36414c73d73d","public_url":null,"developer_survey":"https://notionup.typeform.com/to/bllBsoI4?utm_source=postman","request_id":"ce90d097-14b7-424c-9ace-d87e91875795"}'
    )
    successResponse.read.return_value = sample.encode("utf-8")
    conn = mocker.Mock()
    conn.getresponse.return_value = successResponse
    mocker.patch("http.client.HTTPSConnection", return_value=conn)
    
    # Arrange
    page_id: str = "c5353a8c-a89c-4dd0-96c5-e3e2d19a0387"
    
    # Act
    response_data: dict = notion_page_manager.archive_page_by_id(page_id)
    
    # Assert
    assert response_data is not None
    assert "object" in response_data
    assert response_data["object"] == "page"
    assert "archived" in response_data
    assert response_data["archived"] == True

def test_should_unarchive_page_by_id(mocker):
     # Mocks
    successResponse = mocker.Mock()
    successResponse.status = 200
    sample: str = (
        '{"object":"page","id":"b278bdba-2484-4976-a2fc-36414c73d73d","created_time":"2024-05-24T01:40:00.000Z","last_edited_time":"2024-05-24T17:56:00.000Z","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"cover":null,"icon":{"type":"external","external":{"url":"https://www.notion.so/icons/document_gray.svg"}},"parent":{"type":"database_id","database_id":"6301f640-e21c-4526-a72e-d96e7d4ba71d"},"archived":false,"in_trash":false,"properties":{"Papel":{"id":"PqtR","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Exemplo de Papel","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de Papel","href":null}]},"Objetivo":{"id":"TF%7BM","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Exemplo de objetivo","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de objetivo","href":null}]},"Nome":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Exemplo de nome","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de nome","href":null}]}},"url":"https://www.notion.so/Exemplo-de-nome-b278bdba24844976a2fc36414c73d73d","public_url":null,"developer_survey":"https://notionup.typeform.com/to/bllBsoI4?utm_source=postman","request_id":"e5bf8292-2f15-4a38-b913-eed4d6a1325b"}'
    )
    successResponse.read.return_value = sample.encode("utf-8")
    conn = mocker.Mock()
    conn.getresponse.return_value = successResponse
    mocker.patch("http.client.HTTPSConnection", return_value=conn)
    
    # Arrange
    page_id: str = "c5353a8c-a89c-4dd0-96c5-e3e2d19a0387"
    
    # Act
    response_data: dict = notion_page_manager.archive_page_by_id(page_id)
    
    # Assert
    assert response_data is not None
    assert "object" in response_data
    assert response_data["object"] == "page"
    assert "archived" in response_data
    assert response_data["archived"] == False
   