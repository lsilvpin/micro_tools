import sys, os

from main.library.repositories.notion.models.notion_custom_icon import NotionIcon
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
    image: NotionPageBlock = NotionPageBlock(
        NOTION_BLOCK_TYPES["image"],
        "https://images.unsplash.com/photo-1513097633097-329a3a64e0d4?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb",
    )
    page: NotionPage = NotionPage(icon, [nome, papel, objetivo], [image])

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


def test_should_query_pages_by_database_id(mocker):
    # Mocks
    successResponse = mocker.Mock()
    successResponse.status = 200
    sample: str = (
        '{"object":"list","results":[{"object":"page","id":"6f48b54c-094d-4339-aa90-89f9985fb6c7","created_time":"2024-05-24T22:43:00.000Z","last_edited_time":"2024-05-25T02:10:00.000Z","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"cover":null,"icon":{"type":"emoji","emoji":"🚀"},"parent":{"type":"database_id","database_id":"c7c1007a-d112-4b8c-a621-a769adaf7dda"},"archived":false,"in_trash":false,"properties":{"Criado por":{"id":"%3BHF%7B","type":"created_by","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af","name":"lsilvpin_integration","avatar_url":null,"type":"bot","bot":{}}},"Rollup":{"id":"%3FE%3DX","type":"rollup","rollup":{"type":"array","array":[{"type":"rich_text","rich_text":[{"type":"text","text":{"content":"Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso","href":null}]}],"function":"show_original"}},"Data":{"id":"%3Ftz%7C","type":"date","date":{"start":"2024-05-24","end":null,"time_zone":null}},"Number":{"id":"%3FuPt","type":"number","number":123.45},"TB_MICRO_TOOLS_AGENTS":{"id":"BBeA","type":"relation","relation":[{"id":"4c65fc9c-2ff4-462e-9493-71ebb14c22cb"}],"has_more":false},"Arquivo":{"id":"RhQY","type":"files","files":[{"name":"MeninaBonita.jpeg","type":"external","external":{"url":"https://images.unsplash.com/photo-1513097633097-329a3a64e0d4?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb"}}]},"Última edição":{"id":"VJ%7BH","type":"last_edited_time","last_edited_time":"2024-05-25T02:10:00.000Z"},"Número Telefone":{"id":"%5CUE%5D","type":"phone_number","phone_number":"+5511999999999"},"URL":{"id":"%5DB%5Br","type":"url","url":"https://www.google.com"},"Criado em":{"id":"_UYD","type":"created_time","created_time":"2024-05-24T22:43:00.000Z"},"Description":{"id":"cFut","type":"rich_text","rich_text":[{"type":"text","text":{"content":"This is a description","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"This is a description","href":null}]},"Select":{"id":"h%7DHj","type":"select","select":{"id":"4742d912-2063-4da5-b84e-b8d1a7a4bcab","name":"Option 1","color":"gray"}},"Soma":{"id":"l%3D%7CU","type":"formula","formula":{"type":"boolean","boolean":false}},"IsTrue":{"id":"mWc%7B","type":"checkbox","checkbox":true},"Pessoa":{"id":"m~%3F%5B","type":"people","people":[{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c","name":"Luís Henrique da Silva Pinheiro","avatar_url":"https://lh3.googleusercontent.com/a/AAcHTtcnTtIpmU5cSjZvseJMEdyEqNV8Xj3OhPFNxAmH=s100","type":"person","person":{"email":"lsilvpin@gmail.com"}}]},"Tags":{"id":"n%3FtV","type":"multi_select","multi_select":[{"id":"b64cc08c-61ac-410c-9bf2-6e86f26f0c9f","name":"Tag 1","color":"gray"},{"id":"a5bccd0b-30e7-4dc7-a3d1-fefad1ed875c","name":"Tag 2","color":"blue"}]},"Email":{"id":"nql~","type":"email","email":"fulano@email.com"},"Última edição por":{"id":"plkg","type":"last_edited_by","last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af","name":"lsilvpin_integration","avatar_url":null,"type":"bot","bot":{}}},"Name":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Minha Página","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Minha Página","href":null}]}},"url":"https://www.notion.so/Minha-P-gina-6f48b54c094d4339aa9089f9985fb6c7","public_url":null},{"object":"page","id":"f08a40ba-7f45-4a2a-ba60-e0b1f1e3a6bb","created_time":"2024-05-24T22:30:00.000Z","last_edited_time":"2024-05-24T22:30:00.000Z","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"cover":null,"icon":{"type":"emoji","emoji":"🚀"},"parent":{"type":"database_id","database_id":"c7c1007a-d112-4b8c-a621-a769adaf7dda"},"archived":false,"in_trash":false,"properties":{"Criado por":{"id":"%3BHF%7B","type":"created_by","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af","name":"lsilvpin_integration","avatar_url":null,"type":"bot","bot":{}}},"Rollup":{"id":"%3FE%3DX","type":"rollup","rollup":{"type":"array","array":[{"type":"rich_text","rich_text":[{"type":"text","text":{"content":"Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso","href":null}]}],"function":"show_original"}},"Data":{"id":"%3Ftz%7C","type":"date","date":{"start":"2024-05-24","end":null,"time_zone":null}},"Number":{"id":"%3FuPt","type":"number","number":123.45},"TB_MICRO_TOOLS_AGENTS":{"id":"BBeA","type":"relation","relation":[{"id":"4c65fc9c-2ff4-462e-9493-71ebb14c22cb"}],"has_more":false},"Arquivo":{"id":"RhQY","type":"files","files":[{"name":"MeninaBonita.jpeg","type":"external","external":{"url":"https://images.unsplash.com/photo-1513097633097-329a3a64e0d4?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb"}}]},"Última edição":{"id":"VJ%7BH","type":"last_edited_time","last_edited_time":"2024-05-24T22:30:00.000Z"},"Número Telefone":{"id":"%5CUE%5D","type":"phone_number","phone_number":"+5511999999999"},"URL":{"id":"%5DB%5Br","type":"url","url":"https://www.google.com"},"Criado em":{"id":"_UYD","type":"created_time","created_time":"2024-05-24T22:30:00.000Z"},"Description":{"id":"cFut","type":"rich_text","rich_text":[{"type":"text","text":{"content":"This is a description","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"This is a description","href":null}]},"Select":{"id":"h%7DHj","type":"select","select":{"id":"4742d912-2063-4da5-b84e-b8d1a7a4bcab","name":"Option 1","color":"gray"}},"Soma":{"id":"l%3D%7CU","type":"formula","formula":{"type":"boolean","boolean":false}},"IsTrue":{"id":"mWc%7B","type":"checkbox","checkbox":true},"Pessoa":{"id":"m~%3F%5B","type":"people","people":[{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c","name":"Luís Henrique da Silva Pinheiro","avatar_url":"https://lh3.googleusercontent.com/a/AAcHTtcnTtIpmU5cSjZvseJMEdyEqNV8Xj3OhPFNxAmH=s100","type":"person","person":{"email":"lsilvpin@gmail.com"}}]},"Tags":{"id":"n%3FtV","type":"multi_select","multi_select":[{"id":"b64cc08c-61ac-410c-9bf2-6e86f26f0c9f","name":"Tag 1","color":"gray"},{"id":"a5bccd0b-30e7-4dc7-a3d1-fefad1ed875c","name":"Tag 2","color":"blue"}]},"Email":{"id":"nql~","type":"email","email":"fulano@email.com"},"Última edição por":{"id":"plkg","type":"last_edited_by","last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af","name":"lsilvpin_integration","avatar_url":null,"type":"bot","bot":{}}},"Name":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"My Page","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"My Page","href":null}]}},"url":"https://www.notion.so/My-Page-f08a40ba7f454a2aba60e0b1f1e3a6bb","public_url":null},{"object":"page","id":"6a11ae1e-8e2d-4799-a5dc-cb80c3de1e35","created_time":"2024-05-24T22:20:00.000Z","last_edited_time":"2024-05-24T22:20:00.000Z","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"cover":null,"icon":{"type":"emoji","emoji":"🚀"},"parent":{"type":"database_id","database_id":"c7c1007a-d112-4b8c-a621-a769adaf7dda"},"archived":false,"in_trash":false,"properties":{"Criado por":{"id":"%3BHF%7B","type":"created_by","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af","name":"lsilvpin_integration","avatar_url":null,"type":"bot","bot":{}}},"Rollup":{"id":"%3FE%3DX","type":"rollup","rollup":{"type":"array","array":[{"type":"rich_text","rich_text":[{"type":"text","text":{"content":"Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso","href":null}]}],"function":"show_original"}},"Data":{"id":"%3Ftz%7C","type":"date","date":{"start":"2024-05-24","end":null,"time_zone":null}},"Number":{"id":"%3FuPt","type":"number","number":123.45},"TB_MICRO_TOOLS_AGENTS":{"id":"BBeA","type":"relation","relation":[{"id":"4c65fc9c-2ff4-462e-9493-71ebb14c22cb"}],"has_more":false},"Arquivo":{"id":"RhQY","type":"files","files":[]},"Última edição":{"id":"VJ%7BH","type":"last_edited_time","last_edited_time":"2024-05-24T22:20:00.000Z"},"Número Telefone":{"id":"%5CUE%5D","type":"phone_number","phone_number":"+5511999999999"},"URL":{"id":"%5DB%5Br","type":"url","url":"https://www.google.com"},"Criado em":{"id":"_UYD","type":"created_time","created_time":"2024-05-24T22:20:00.000Z"},"Description":{"id":"cFut","type":"rich_text","rich_text":[{"type":"text","text":{"content":"This is a description","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"This is a description","href":null}]},"Select":{"id":"h%7DHj","type":"select","select":{"id":"4742d912-2063-4da5-b84e-b8d1a7a4bcab","name":"Option 1","color":"gray"}},"Soma":{"id":"l%3D%7CU","type":"formula","formula":{"type":"boolean","boolean":false}},"IsTrue":{"id":"mWc%7B","type":"checkbox","checkbox":true},"Pessoa":{"id":"m~%3F%5B","type":"people","people":[{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c","name":"Luís Henrique da Silva Pinheiro","avatar_url":"https://lh3.googleusercontent.com/a/AAcHTtcnTtIpmU5cSjZvseJMEdyEqNV8Xj3OhPFNxAmH=s100","type":"person","person":{"email":"lsilvpin@gmail.com"}}]},"Tags":{"id":"n%3FtV","type":"multi_select","multi_select":[{"id":"b64cc08c-61ac-410c-9bf2-6e86f26f0c9f","name":"Tag 1","color":"gray"},{"id":"a5bccd0b-30e7-4dc7-a3d1-fefad1ed875c","name":"Tag 2","color":"blue"}]},"Email":{"id":"nql~","type":"email","email":"fulano@email.com"},"Última edição por":{"id":"plkg","type":"last_edited_by","last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af","name":"lsilvpin_integration","avatar_url":null,"type":"bot","bot":{}}},"Name":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"My Page","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"My Page","href":null}]}},"url":"https://www.notion.so/My-Page-6a11ae1e8e2d4799a5dccb80c3de1e35","public_url":null},{"object":"page","id":"e11f16c4-71d2-4a35-92e2-96b86ac22cb9","created_time":"2024-05-24T21:58:00.000Z","last_edited_time":"2024-05-24T21:58:00.000Z","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"cover":null,"icon":{"type":"external","external":{"url":"https://www.notion.so/icons/document_gray.svg"}},"parent":{"type":"database_id","database_id":"c7c1007a-d112-4b8c-a621-a769adaf7dda"},"archived":false,"in_trash":false,"properties":{"Criado por":{"id":"%3BHF%7B","type":"created_by","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af","name":"lsilvpin_integration","avatar_url":null,"type":"bot","bot":{}}},"Rollup":{"id":"%3FE%3DX","type":"rollup","rollup":{"type":"array","array":[{"type":"rich_text","rich_text":[{"type":"text","text":{"content":"Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso","href":null}]}],"function":"show_original"}},"Data":{"id":"%3Ftz%7C","type":"date","date":{"start":"2024-05-14","end":null,"time_zone":null}},"Number":{"id":"%3FuPt","type":"number","number":1},"TB_MICRO_TOOLS_AGENTS":{"id":"BBeA","type":"relation","relation":[{"id":"4c65fc9c-2ff4-462e-9493-71ebb14c22cb"}],"has_more":false},"Arquivo":{"id":"RhQY","type":"files","files":[]},"Última edição":{"id":"VJ%7BH","type":"last_edited_time","last_edited_time":"2024-05-24T21:58:00.000Z"},"Número Telefone":{"id":"%5CUE%5D","type":"phone_number","phone_number":"35928760099"},"URL":{"id":"%5DB%5Br","type":"url","url":"https://jsonformatter.curiousconcept.com/#"},"Criado em":{"id":"_UYD","type":"created_time","created_time":"2024-05-24T21:58:00.000Z"},"Description":{"id":"cFut","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Descrição 1","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Descrição 1","href":null}]},"Select":{"id":"h%7DHj","type":"select","select":{"id":"67cdf6ee-d834-45e7-b905-5820666a7247","name":"Alface","color":"green"}},"Soma":{"id":"l%3D%7CU","type":"formula","formula":{"type":"boolean","boolean":false}},"IsTrue":{"id":"mWc%7B","type":"checkbox","checkbox":true},"Pessoa":{"id":"m~%3F%5B","type":"people","people":[{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c","name":"Luís Henrique da Silva Pinheiro","avatar_url":"https://lh3.googleusercontent.com/a/AAcHTtcnTtIpmU5cSjZvseJMEdyEqNV8Xj3OhPFNxAmH=s100","type":"person","person":{"email":"lsilvpin@gmail.com"}}]},"Tags":{"id":"n%3FtV","type":"multi_select","multi_select":[{"id":"0e6e51c7-af87-4031-bb4a-ea4da3731069","name":"Tag A","color":"orange"},{"id":"f473d51d-e1f4-4a8c-b119-25eb5f14a179","name":"Tag B","color":"blue"}]},"Email":{"id":"nql~","type":"email","email":"fulano@email.com"},"Última edição por":{"id":"plkg","type":"last_edited_by","last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af","name":"lsilvpin_integration","avatar_url":null,"type":"bot","bot":{}}},"Name":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Nome 1","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Nome 1","href":null}]}},"url":"https://www.notion.so/Nome-1-e11f16c471d24a3592e296b86ac22cb9","public_url":null},{"object":"page","id":"9151da24-9e26-432c-8d33-51e58b9f68c0","created_time":"2024-05-24T21:56:00.000Z","last_edited_time":"2024-05-24T21:56:00.000Z","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"cover":null,"icon":{"type":"external","external":{"url":"https://www.notion.so/icons/document_gray.svg"}},"parent":{"type":"database_id","database_id":"c7c1007a-d112-4b8c-a621-a769adaf7dda"},"archived":false,"in_trash":false,"properties":{"Criado por":{"id":"%3BHF%7B","type":"created_by","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af","name":"lsilvpin_integration","avatar_url":null,"type":"bot","bot":{}}},"Rollup":{"id":"%3FE%3DX","type":"rollup","rollup":{"type":"array","array":[{"type":"rich_text","rich_text":[{"type":"text","text":{"content":"Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso","href":null}]}],"function":"show_original"}},"Data":{"id":"%3Ftz%7C","type":"date","date":{"start":"2024-05-14","end":null,"time_zone":null}},"Number":{"id":"%3FuPt","type":"number","number":1},"TB_MICRO_TOOLS_AGENTS":{"id":"BBeA","type":"relation","relation":[{"id":"4c65fc9c-2ff4-462e-9493-71ebb14c22cb"}],"has_more":false},"Arquivo":{"id":"RhQY","type":"files","files":[]},"Última edição":{"id":"VJ%7BH","type":"last_edited_time","last_edited_time":"2024-05-24T21:56:00.000Z"},"Número Telefone":{"id":"%5CUE%5D","type":"phone_number","phone_number":"35928760099"},"URL":{"id":"%5DB%5Br","type":"url","url":"https://jsonformatter.curiousconcept.com/#"},"Criado em":{"id":"_UYD","type":"created_time","created_time":"2024-05-24T21:56:00.000Z"},"Description":{"id":"cFut","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Descrição 1","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Descrição 1","href":null}]},"Select":{"id":"h%7DHj","type":"select","select":{"id":"67cdf6ee-d834-45e7-b905-5820666a7247","name":"Alface","color":"green"}},"Soma":{"id":"l%3D%7CU","type":"formula","formula":{"type":"boolean","boolean":false}},"IsTrue":{"id":"mWc%7B","type":"checkbox","checkbox":true},"Pessoa":{"id":"m~%3F%5B","type":"people","people":[{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c","name":"Luís Henrique da Silva Pinheiro","avatar_url":"https://lh3.googleusercontent.com/a/AAcHTtcnTtIpmU5cSjZvseJMEdyEqNV8Xj3OhPFNxAmH=s100","type":"person","person":{"email":"lsilvpin@gmail.com"}}]},"Tags":{"id":"n%3FtV","type":"multi_select","multi_select":[{"id":"0e6e51c7-af87-4031-bb4a-ea4da3731069","name":"Tag A","color":"orange"},{"id":"f473d51d-e1f4-4a8c-b119-25eb5f14a179","name":"Tag B","color":"blue"}]},"Email":{"id":"nql~","type":"email","email":"fulano@email.com"},"Última edição por":{"id":"plkg","type":"last_edited_by","last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af","name":"lsilvpin_integration","avatar_url":null,"type":"bot","bot":{}}},"Name":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Nome 1","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Nome 1","href":null}]}},"url":"https://www.notion.so/Nome-1-9151da249e26432c8d3351e58b9f68c0","public_url":null},{"object":"page","id":"56ae651b-8149-48fe-9aa4-8d7dac1ce2f8","created_time":"2024-05-24T21:53:00.000Z","last_edited_time":"2024-05-24T21:53:00.000Z","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"cover":null,"icon":{"type":"external","external":{"url":"https://www.notion.so/icons/document_gray.svg"}},"parent":{"type":"database_id","database_id":"c7c1007a-d112-4b8c-a621-a769adaf7dda"},"archived":false,"in_trash":false,"properties":{"Criado por":{"id":"%3BHF%7B","type":"created_by","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af","name":"lsilvpin_integration","avatar_url":null,"type":"bot","bot":{}}},"Rollup":{"id":"%3FE%3DX","type":"rollup","rollup":{"type":"array","array":[{"type":"rich_text","rich_text":[{"type":"text","text":{"content":"Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso","href":null}]}],"function":"show_original"}},"Data":{"id":"%3Ftz%7C","type":"date","date":{"start":"2024-05-14","end":null,"time_zone":null}},"Number":{"id":"%3FuPt","type":"number","number":1},"TB_MICRO_TOOLS_AGENTS":{"id":"BBeA","type":"relation","relation":[{"id":"4c65fc9c-2ff4-462e-9493-71ebb14c22cb"}],"has_more":false},"Arquivo":{"id":"RhQY","type":"files","files":[]},"Última edição":{"id":"VJ%7BH","type":"last_edited_time","last_edited_time":"2024-05-24T21:53:00.000Z"},"Número Telefone":{"id":"%5CUE%5D","type":"phone_number","phone_number":"35928760099"},"URL":{"id":"%5DB%5Br","type":"url","url":"https://jsonformatter.curiousconcept.com/#"},"Criado em":{"id":"_UYD","type":"created_time","created_time":"2024-05-24T21:53:00.000Z"},"Description":{"id":"cFut","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Descrição 1","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Descrição 1","href":null}]},"Select":{"id":"h%7DHj","type":"select","select":{"id":"67cdf6ee-d834-45e7-b905-5820666a7247","name":"Alface","color":"green"}},"Soma":{"id":"l%3D%7CU","type":"formula","formula":{"type":"boolean","boolean":false}},"IsTrue":{"id":"mWc%7B","type":"checkbox","checkbox":true},"Pessoa":{"id":"m~%3F%5B","type":"people","people":[{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c","name":"Luís Henrique da Silva Pinheiro","avatar_url":"https://lh3.googleusercontent.com/a/AAcHTtcnTtIpmU5cSjZvseJMEdyEqNV8Xj3OhPFNxAmH=s100","type":"person","person":{"email":"lsilvpin@gmail.com"}}]},"Tags":{"id":"n%3FtV","type":"multi_select","multi_select":[{"id":"0e6e51c7-af87-4031-bb4a-ea4da3731069","name":"Tag A","color":"orange"},{"id":"f473d51d-e1f4-4a8c-b119-25eb5f14a179","name":"Tag B","color":"blue"}]},"Email":{"id":"nql~","type":"email","email":"fulano@email.com"},"Última edição por":{"id":"plkg","type":"last_edited_by","last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af","name":"lsilvpin_integration","avatar_url":null,"type":"bot","bot":{}}},"Name":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Nome 1","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Nome 1","href":null}]}},"url":"https://www.notion.so/Nome-1-56ae651b814948fe9aa48d7dac1ce2f8","public_url":null},{"object":"page","id":"cd3eacc0-498e-49b9-851e-79b9199f3e62","created_time":"2024-05-24T21:43:00.000Z","last_edited_time":"2024-05-24T21:57:00.000Z","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"last_edited_by":{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c"},"cover":null,"icon":{"type":"external","external":{"url":"https://www.notion.so/icons/document_gray.svg"}},"parent":{"type":"database_id","database_id":"c7c1007a-d112-4b8c-a621-a769adaf7dda"},"archived":false,"in_trash":false,"properties":{"Criado por":{"id":"%3BHF%7B","type":"created_by","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af","name":"lsilvpin_integration","avatar_url":null,"type":"bot","bot":{}}},"Rollup":{"id":"%3FE%3DX","type":"rollup","rollup":{"type":"array","array":[{"type":"rich_text","rich_text":[{"type":"text","text":{"content":"Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso","href":null}]}],"function":"show_original"}},"Data":{"id":"%3Ftz%7C","type":"date","date":{"start":"2024-05-14","end":null,"time_zone":null}},"Number":{"id":"%3FuPt","type":"number","number":1},"TB_MICRO_TOOLS_AGENTS":{"id":"BBeA","type":"relation","relation":[{"id":"4c65fc9c-2ff4-462e-9493-71ebb14c22cb"}],"has_more":false},"Arquivo":{"id":"RhQY","type":"files","files":[{"name":"Belial.jpeg","type":"file","file":{"url":"https://prod-files-secure.s3.us-west-2.amazonaws.com/9e5c8bff-440c-423c-a6e4-9cea461b34ee/f46aba42-1a83-45b3-b81a-b229c7971770/Belial.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45HZZMZUHI%2F20240525%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20240525T022545Z&X-Amz-Expires=3600&X-Amz-Signature=4eb1dfc0f83cdf29bc0d55aa76295788d45525b83cbfaba004b4c6a2a1e98b3e&X-Amz-SignedHeaders=host&x-id=GetObject","expiry_time":"2024-05-25T03:25:45.780Z"}}]},"Última edição":{"id":"VJ%7BH","type":"last_edited_time","last_edited_time":"2024-05-24T21:57:00.000Z"},"Número Telefone":{"id":"%5CUE%5D","type":"phone_number","phone_number":"35928760099"},"URL":{"id":"%5DB%5Br","type":"url","url":"https://jsonformatter.curiousconcept.com/#"},"Criado em":{"id":"_UYD","type":"created_time","created_time":"2024-05-24T21:43:00.000Z"},"Description":{"id":"cFut","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Descrição 1","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Descrição 1","href":null}]},"Select":{"id":"h%7DHj","type":"select","select":{"id":"67cdf6ee-d834-45e7-b905-5820666a7247","name":"Alface","color":"green"}},"Soma":{"id":"l%3D%7CU","type":"formula","formula":{"type":"boolean","boolean":false}},"IsTrue":{"id":"mWc%7B","type":"checkbox","checkbox":true},"Pessoa":{"id":"m~%3F%5B","type":"people","people":[{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c","name":"Luís Henrique da Silva Pinheiro","avatar_url":"https://lh3.googleusercontent.com/a/AAcHTtcnTtIpmU5cSjZvseJMEdyEqNV8Xj3OhPFNxAmH=s100","type":"person","person":{"email":"lsilvpin@gmail.com"}}]},"Tags":{"id":"n%3FtV","type":"multi_select","multi_select":[{"id":"0e6e51c7-af87-4031-bb4a-ea4da3731069","name":"Tag A","color":"orange"},{"id":"f473d51d-e1f4-4a8c-b119-25eb5f14a179","name":"Tag B","color":"blue"}]},"Email":{"id":"nql~","type":"email","email":"fulano@email.com"},"Última edição por":{"id":"plkg","type":"last_edited_by","last_edited_by":{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c","name":"Luís Henrique da Silva Pinheiro","avatar_url":"https://lh3.googleusercontent.com/a/AAcHTtcnTtIpmU5cSjZvseJMEdyEqNV8Xj3OhPFNxAmH=s100","type":"person","person":{"email":"lsilvpin@gmail.com"}}},"Name":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Nome 1","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Nome 1","href":null}]}},"url":"https://www.notion.so/Nome-1-cd3eacc0498e49b9851e79b9199f3e62","public_url":null},{"object":"page","id":"5fa23dbe-28c8-42f0-9415-2b43f284b153","created_time":"2024-05-24T20:03:00.000Z","last_edited_time":"2024-05-24T20:15:00.000Z","created_by":{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c"},"last_edited_by":{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c"},"cover":null,"icon":null,"parent":{"type":"database_id","database_id":"c7c1007a-d112-4b8c-a621-a769adaf7dda"},"archived":false,"in_trash":false,"properties":{"Criado por":{"id":"%3BHF%7B","type":"created_by","created_by":{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c","name":"Luís Henrique da Silva Pinheiro","avatar_url":"https://lh3.googleusercontent.com/a/AAcHTtcnTtIpmU5cSjZvseJMEdyEqNV8Xj3OhPFNxAmH=s100","type":"person","person":{"email":"lsilvpin@gmail.com"}}},"Rollup":{"id":"%3FE%3DX","type":"rollup","rollup":{"type":"array","array":[{"type":"rich_text","rich_text":[{"type":"text","text":{"content":"Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso","href":null}]}],"function":"show_original"}},"Data":{"id":"%3Ftz%7C","type":"date","date":{"start":"2024-05-14","end":null,"time_zone":null}},"Number":{"id":"%3FuPt","type":"number","number":1},"TB_MICRO_TOOLS_AGENTS":{"id":"BBeA","type":"relation","relation":[{"id":"4c65fc9c-2ff4-462e-9493-71ebb14c22cb"}],"has_more":false},"Arquivo":{"id":"RhQY","type":"files","files":[{"name":"Belial.jpeg","type":"file","file":{"url":"https://prod-files-secure.s3.us-west-2.amazonaws.com/9e5c8bff-440c-423c-a6e4-9cea461b34ee/f46aba42-1a83-45b3-b81a-b229c7971770/Belial.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45HZZMZUHI%2F20240525%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20240525T022545Z&X-Amz-Expires=3600&X-Amz-Signature=4eb1dfc0f83cdf29bc0d55aa76295788d45525b83cbfaba004b4c6a2a1e98b3e&X-Amz-SignedHeaders=host&x-id=GetObject","expiry_time":"2024-05-25T03:25:45.781Z"}}]},"Última edição":{"id":"VJ%7BH","type":"last_edited_time","last_edited_time":"2024-05-24T20:15:00.000Z"},"Número Telefone":{"id":"%5CUE%5D","type":"phone_number","phone_number":"35928760099"},"URL":{"id":"%5DB%5Br","type":"url","url":"https://jsonformatter.curiousconcept.com/#"},"Criado em":{"id":"_UYD","type":"created_time","created_time":"2024-05-24T20:03:00.000Z"},"Description":{"id":"cFut","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Descrição 1","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Descrição 1","href":null}]},"Select":{"id":"h%7DHj","type":"select","select":{"id":"67cdf6ee-d834-45e7-b905-5820666a7247","name":"Alface","color":"green"}},"Soma":{"id":"l%3D%7CU","type":"formula","formula":{"type":"boolean","boolean":false}},"IsTrue":{"id":"mWc%7B","type":"checkbox","checkbox":true},"Pessoa":{"id":"m~%3F%5B","type":"people","people":[{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c","name":"Luís Henrique da Silva Pinheiro","avatar_url":"https://lh3.googleusercontent.com/a/AAcHTtcnTtIpmU5cSjZvseJMEdyEqNV8Xj3OhPFNxAmH=s100","type":"person","person":{"email":"lsilvpin@gmail.com"}}]},"Tags":{"id":"n%3FtV","type":"multi_select","multi_select":[{"id":"0e6e51c7-af87-4031-bb4a-ea4da3731069","name":"Tag A","color":"orange"},{"id":"f473d51d-e1f4-4a8c-b119-25eb5f14a179","name":"Tag B","color":"blue"}]},"Email":{"id":"nql~","type":"email","email":"fulano@email.com"},"Última edição por":{"id":"plkg","type":"last_edited_by","last_edited_by":{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c","name":"Luís Henrique da Silva Pinheiro","avatar_url":"https://lh3.googleusercontent.com/a/AAcHTtcnTtIpmU5cSjZvseJMEdyEqNV8Xj3OhPFNxAmH=s100","type":"person","person":{"email":"lsilvpin@gmail.com"}}},"Name":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Nome 1","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Nome 1","href":null}]}},"url":"https://www.notion.so/Nome-1-5fa23dbe28c842f094152b43f284b153","public_url":null},{"object":"page","id":"254d6af9-11da-44ac-8ea9-a41d23c0d443","created_time":"2024-05-24T20:03:00.000Z","last_edited_time":"2024-05-24T20:12:00.000Z","created_by":{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c"},"last_edited_by":{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c"},"cover":null,"icon":null,"parent":{"type":"database_id","database_id":"c7c1007a-d112-4b8c-a621-a769adaf7dda"},"archived":false,"in_trash":false,"properties":{"Criado por":{"id":"%3BHF%7B","type":"created_by","created_by":{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c","name":"Luís Henrique da Silva Pinheiro","avatar_url":"https://lh3.googleusercontent.com/a/AAcHTtcnTtIpmU5cSjZvseJMEdyEqNV8Xj3OhPFNxAmH=s100","type":"person","person":{"email":"lsilvpin@gmail.com"}}},"Rollup":{"id":"%3FE%3DX","type":"rollup","rollup":{"type":"array","array":[{"type":"rich_text","rich_text":[{"type":"text","text":{"content":"Exemplo de objetivo","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de objetivo","href":null}]},{"type":"rich_text","rich_text":[{"type":"text","text":{"content":"Exemplo de objetivo","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de objetivo","href":null}]}],"function":"show_original"}},"Data":{"id":"%3Ftz%7C","type":"date","date":{"start":"2024-05-27","end":null,"time_zone":null}},"Number":{"id":"%3FuPt","type":"number","number":3},"TB_MICRO_TOOLS_AGENTS":{"id":"BBeA","type":"relation","relation":[{"id":"10ba095b-36bd-44f1-b91c-6748e9510943"},{"id":"945cda42-8c7a-496c-9eb6-cf195f41ee3f"}],"has_more":false},"Arquivo":{"id":"RhQY","type":"files","files":[{"name":"BiduiaCorrompida.jpeg","type":"file","file":{"url":"https://prod-files-secure.s3.us-west-2.amazonaws.com/9e5c8bff-440c-423c-a6e4-9cea461b34ee/ef7d2cc7-856a-4e0d-9611-4e9db2bcf9d5/BiduiaCorrompida.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45HZZMZUHI%2F20240525%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20240525T022545Z&X-Amz-Expires=3600&X-Amz-Signature=b050721982bb7c431f064d576e683f49038b2e010718b03f601d89cf2f72662e&X-Amz-SignedHeaders=host&x-id=GetObject","expiry_time":"2024-05-25T03:25:45.780Z"}}]},"Última edição":{"id":"VJ%7BH","type":"last_edited_time","last_edited_time":"2024-05-24T20:12:00.000Z"},"Número Telefone":{"id":"%5CUE%5D","type":"phone_number","phone_number":"34920009266"},"URL":{"id":"%5DB%5Br","type":"url","url":"https://www.primevideo.com/region/na/detail/0LAF7TR58P2GOJPXU8S66IFQUE/ref=atv_dp_amz_c_TS5124c5_1_4?jic=16%7CCgNhbGwSA2FsbA%3D%3D"},"Criado em":{"id":"_UYD","type":"created_time","created_time":"2024-05-24T20:03:00.000Z"},"Description":{"id":"cFut","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Descrição 3","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Descrição 3","href":null}]},"Select":{"id":"h%7DHj","type":"select","select":{"id":"4cd7fb06-e7a3-4025-8fa7-747048c132fd","name":"Kacto","color":"yellow"}},"Soma":{"id":"l%3D%7CU","type":"formula","formula":{"type":"boolean","boolean":false}},"IsTrue":{"id":"mWc%7B","type":"checkbox","checkbox":true},"Pessoa":{"id":"m~%3F%5B","type":"people","people":[{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c","name":"Luís Henrique da Silva Pinheiro","avatar_url":"https://lh3.googleusercontent.com/a/AAcHTtcnTtIpmU5cSjZvseJMEdyEqNV8Xj3OhPFNxAmH=s100","type":"person","person":{"email":"lsilvpin@gmail.com"}}]},"Tags":{"id":"n%3FtV","type":"multi_select","multi_select":[{"id":"a44827ec-71e6-4241-8b43-780c3cb32f0f","name":"Tag D","color":"yellow"}]},"Email":{"id":"nql~","type":"email","email":"lsilvpin@gmail.com"},"Última edição por":{"id":"plkg","type":"last_edited_by","last_edited_by":{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c","name":"Luís Henrique da Silva Pinheiro","avatar_url":"https://lh3.googleusercontent.com/a/AAcHTtcnTtIpmU5cSjZvseJMEdyEqNV8Xj3OhPFNxAmH=s100","type":"person","person":{"email":"lsilvpin@gmail.com"}}},"Name":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Nome 3","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Nome 3","href":null}]}},"url":"https://www.notion.so/Nome-3-254d6af911da44ac8ea9a41d23c0d443","public_url":null},{"object":"page","id":"2071ec0c-9c34-4ef3-afed-72267fb7accd","created_time":"2024-05-24T20:03:00.000Z","last_edited_time":"2024-05-24T20:09:00.000Z","created_by":{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c"},"last_edited_by":{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c"},"cover":null,"icon":null,"parent":{"type":"database_id","database_id":"c7c1007a-d112-4b8c-a621-a769adaf7dda"},"archived":false,"in_trash":false,"properties":{"Criado por":{"id":"%3BHF%7B","type":"created_by","created_by":{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c","name":"Luís Henrique da Silva Pinheiro","avatar_url":"https://lh3.googleusercontent.com/a/AAcHTtcnTtIpmU5cSjZvseJMEdyEqNV8Xj3OhPFNxAmH=s100","type":"person","person":{"email":"lsilvpin@gmail.com"}}},"Rollup":{"id":"%3FE%3DX","type":"rollup","rollup":{"type":"array","array":[],"function":"show_original"}},"Data":{"id":"%3Ftz%7C","type":"date","date":{"start":"2024-05-10","end":null,"time_zone":null}},"Number":{"id":"%3FuPt","type":"number","number":2},"TB_MICRO_TOOLS_AGENTS":{"id":"BBeA","type":"relation","relation":[],"has_more":false},"Arquivo":{"id":"RhQY","type":"files","files":[]},"Última edição":{"id":"VJ%7BH","type":"last_edited_time","last_edited_time":"2024-05-24T20:09:00.000Z"},"Número Telefone":{"id":"%5CUE%5D","type":"phone_number","phone_number":null},"URL":{"id":"%5DB%5Br","type":"url","url":null},"Criado em":{"id":"_UYD","type":"created_time","created_time":"2024-05-24T20:03:00.000Z"},"Description":{"id":"cFut","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Descrição 2","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Descrição 2","href":null}]},"Select":{"id":"h%7DHj","type":"select","select":{"id":"fb744b25-edc2-48e3-9305-14fbae13a2d9","name":"Cebola","color":"pink"}},"Soma":{"id":"l%3D%7CU","type":"formula","formula":{"type":"boolean","boolean":false}},"IsTrue":{"id":"mWc%7B","type":"checkbox","checkbox":false},"Pessoa":{"id":"m~%3F%5B","type":"people","people":[]},"Tags":{"id":"n%3FtV","type":"multi_select","multi_select":[{"id":"0e6e51c7-af87-4031-bb4a-ea4da3731069","name":"Tag A","color":"orange"},{"id":"bca795ce-4f7d-45fa-a690-870bc7f4a15b","name":"Tag C","color":"gray"}]},"Email":{"id":"nql~","type":"email","email":null},"Última edição por":{"id":"plkg","type":"last_edited_by","last_edited_by":{"object":"user","id":"6595192e-1c62-4f33-801c-84424f2ffa9c","name":"Luís Henrique da Silva Pinheiro","avatar_url":"https://lh3.googleusercontent.com/a/AAcHTtcnTtIpmU5cSjZvseJMEdyEqNV8Xj3OhPFNxAmH=s100","type":"person","person":{"email":"lsilvpin@gmail.com"}}},"Name":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Nome 2","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Nome 2","href":null}]}},"url":"https://www.notion.so/Nome-2-2071ec0c9c344ef3afed72267fb7accd","public_url":null}],"next_cursor":null,"has_more":false,"type":"page_or_database","page_or_database":{},"developer_survey":"https://notionup.typeform.com/to/bllBsoI4?utm_source=postman","request_id":"ee81d9b7-0e28-4de3-a6c9-e60201c11980"}'
    )
    successResponse.read.return_value = sample.encode("utf-8")
    conn = mocker.Mock()
    conn.getresponse.return_value = successResponse
    mocker.patch("http.client.HTTPSConnection", return_value=conn)

    # Arrange
    database_id: str = "c7c1007a-d112-4b8c-a621-a769adaf7dda"
    filter: dict = {"property": "Name", "title": {"contains": ""}}

    # Act
    response_data: list[NotionPage] = notion_page_manager.query_pages_by_database_id(
        database_id, filter
    )

    # Assert
    assert response_data is not None
    assert len(response_data) > 0
    for page in response_data:
        assert page is not None
        assert page.id is not None
        assert page.created_time is not None
        assert page.last_edited_time is not None
        assert page.created_by is not None
        assert page.last_edited_by is not None
        if page.icon is not None:
            assert page.icon.type in NOTION_ICON_TYPES.values()
            assert page.icon.value in [
                "🚀",
                "https://www.notion.so/icons/document_gray.svg",
            ]
        assert page.parent is not None
        assert page.parent["type"] == "database_id"
        assert page.parent["database_id"] == database_id
        assert page.archived is False
        assert page.properties is not None
        assert page.url is not None
        assert page.request_id is not None


def test_should_update_page_by_id(mocker):
    # Mocks
    successResponse = mocker.Mock()
    successResponse.status = 200
    sample: str = (
        '{"object":"page","id":"b278bdba-2484-4976-a2fc-36414c73d73d","created_time":"2024-05-24T01:40:00.000Z","last_edited_time":"2024-05-24T18:39:00.000Z","created_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"last_edited_by":{"object":"user","id":"27910b45-ae07-403c-b7e9-35b5adc896af"},"cover":null,"icon":{"type":"emoji","emoji":"👩🏻‍💻"},"parent":{"type":"database_id","database_id":"6301f640-e21c-4526-a72e-d96e7d4ba71d"},"archived":false,"in_trash":false,"properties":{"Papel":{"id":"PqtR","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Exemplo de Papel","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de Papel","href":null}]},"Objetivo":{"id":"TF%7BM","type":"rich_text","rich_text":[{"type":"text","text":{"content":"Exemplo de objetivo","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de objetivo","href":null}]},"Nome":{"id":"title","type":"title","title":[{"type":"text","text":{"content":"Exemplo de nome 3","link":null},"annotations":{"bold":false,"italic":false,"strikethrough":false,"underline":false,"code":false,"color":"default"},"plain_text":"Exemplo de nome 3","href":null}]}},"url":"https://www.notion.so/Exemplo-de-nome-3-b278bdba24844976a2fc36414c73d73d","public_url":null,"developer_survey":"https://notionup.typeform.com/to/bllBsoI4?utm_source=postman","request_id":"4161f203-ee7c-433c-a20a-f40620d5e8fb"}'
    )
    successResponse.read.return_value = sample.encode("utf-8")
    conn = mocker.Mock()
    conn.getresponse.return_value = successResponse
    mocker.patch("http.client.HTTPSConnection", return_value=conn)

    # Arrange
    page_id: str = "b278bdba-2484-4976-a2fc-36414c73d73d"
    icon: NotionIcon = NotionIcon("emoji", "👩🏻‍💻")
    properties: list[NotionProperty] = [
        NotionProperty("Nome", NOTION_PROPERTY_TYPES["title"], "Exemplo de nome 3"),
        NotionProperty("Papel", NOTION_PROPERTY_TYPES["rich_text"], "Exemplo de Papel"),
        NotionProperty(
            "Objetivo", NOTION_PROPERTY_TYPES["rich_text"], "Exemplo de objetivo"
        ),
    ]
    page: NotionPage = NotionPage(icon, properties, [])

    # Act
    response_data: dict = notion_page_manager.update_page_by_id(page_id, page)

    # Assert
    assert response_data is not None
    assert "object" in response_data
    assert response_data["object"] == "page"
    assert "id" in response_data
    assert response_data["id"] == page_id
    assert "icon" in response_data
    assert response_data["icon"]["type"] == icon.type
    assert response_data["icon"]["emoji"] == icon.value
    assert "properties" in response_data
    assert "Nome" in response_data["properties"]
    assert "Papel" in response_data["properties"]
    assert "Objetivo" in response_data["properties"]
    assert (
        response_data["properties"]["Nome"]["title"][0]["text"]["content"]
        == "Exemplo de nome 3"
    )
    assert (
        response_data["properties"]["Papel"]["rich_text"][0]["text"]["content"]
        == "Exemplo de Papel"
    )
    assert (
        response_data["properties"]["Objetivo"]["rich_text"][0]["text"]["content"]
        == "Exemplo de objetivo"
    )


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
