import platform
import traceback
from dependency_injector.wiring import inject, Provide
from fastapi.responses import JSONResponse
from main.library.di_container import Container
from main.library.repositories.notion.core.notion_page_manager import NotionPageManager
from main.library.repositories.notion.models.notion_custom_icon import NotionIcon
from main.library.repositories.notion.models.notion_page import NotionPage
from main.library.repositories.notion.models.notion_page_block import NotionPageBlock
from main.library.repositories.notion.models.notion_property import NotionProperty
from main.library.tools.core.log_tool import LogTool
from fastapi import APIRouter, Body, Depends, Path
from main.library.tools.core.settings_tool import SettingsTool
from main.library.utils.core.settings_helper import get
from main.library.utils.models.validation_exception import ValidationException

router = APIRouter()


@router.post(
    "/pages/{database_id}/create",
    tags=["Notion Management"],
    responses={
        200: {
            "description": "Success",
            "content": {
                "application/json": {
                    "example": {"page_id": "6301f640e21c4526a72ed96e7d4ba71d"}
                }
            },
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "Message": "Invalid request",
                        "StackTrace": "Traceback...",
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "Message": "Internal Server Error",
                        "StackTrace": "Traceback...",
                    }
                }
            },
        },
    },
)
@inject
async def create_page(
    database_id: str = Path(
        ...,
        title="Database ID",
        description="ID do banco de dados do Notion",
        example="c7c1007a-d112-4b8c-a621-a769adaf7dda",
    ),
    body: dict = Body(
        ...,
        example={
            "icon": {"type": "emoji", "value": "🚀"},
            "properties": [
                {"name": "Name", "type": "title", "value": "My Page"},
                {
                    "name": "Description",
                    "type": "rich_text",
                    "value": "This is a description",
                },
                {"name": "Number", "type": "number", "value": 123.45},
                {
                    "name": "Select",
                    "type": "select",
                    "value": {"name": "Option 1", "color": "gray"},
                },
                {
                    "name": "Tags",
                    "type": "multi_select",
                    "value": [
                        {"name": "Tag 1", "color": "gray"},
                        {"name": "Tag 2", "color": "blue"},
                    ],
                },
                {"name": "Data", "type": "date", "value": "2024-05-24"},
                {"name": "IsTrue", "type": "checkbox", "value": True},
                {
                    "name": "Pessoa",
                    "type": "people",
                    "value": ["6595192e-1c62-4f33-801c-84424f2ffa9c"],
                },
                {
                    "name": "Arquivo",
                    "type": "files",
                    "value": [
                        {
                            "name": "MeninaBonita.jpeg",
                            "url": "https://images.unsplash.com/photo-1513097633097-329a3a64e0d4?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb",
                        }
                    ],
                },
                {"name": "URL", "type": "url", "value": "https://www.google.com"},
                {"name": "Email", "type": "email", "value": "fulano@email.com"},
                {
                    "name": "Número Telefone",
                    "type": "phone_number",
                    "value": "+5511999999999",
                },
                {
                    "name": "TB_MICRO_TOOLS_AGENTS",
                    "type": "relation",
                    "value": ["4c65fc9c-2ff4-462e-9493-71ebb14c22cb"],
                },
            ],
            "blocks": [
                {
                    "type": "image",
                    "value": "https://images.unsplash.com/photo-1513097633097-329a3a64e0d4?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb",
                },
                {"type": "heading_1", "value": "Título 1"},
                {"type": "heading_2", "value": "Título 2"},
                {"type": "heading_3", "value": "Título 3"},
                {"type": "paragraph", "value": "Este é um parágrafo."},
                {
                    "type": "video",
                    "value": "https://www.youtube.com/watch?v=wVL6z7lWvjQ&list=RDwVL6z7lWvjQ&start_radio=1",
                },
                {"type": "bulleted_list_item", "value": "Item de lista"},
                {"type": "numbered_list_item", "value": "Item de lista numerada"},
                {"type": "to_do", "value": "Tarefa a fazer"},
                {"type": "toggle", "value": "Alternar"},
                {
                    "type": "file",
                    "value": {
                        "name": "MeninaBonita.jpeg",
                        "url": "https://images.unsplash.com/photo-1513097633097-329a3a64e0d4?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb",
                    },
                },
                {
                    "type": "code",
                    "value": {
                        "content": "print('Hello, World!')",
                        "language": "python",
                    },
                },
                {"type": "quote", "value": "Citação"},
            ],
        },
    ),
    log_tool: LogTool = Depends(Provide[Container.log_tool]),
    notion_page_manager: NotionPageManager = Depends(
        Provide[Container.notion_page_manager]
    ),
):
    """
    Cria uma página no Notion.
    """
    try:
        log_tool.info("Criando página no Notion.")
        assert database_id is not None, "ID do banco de dados não pode ser nulo."
        notion_icon: NotionIcon = NotionIcon(
            icon_type=body["icon"]["type"], icon_value=body["icon"]["value"]
        )
        page_properties: list[NotionProperty] = []
        for prop in body["properties"]:
            page_properties.append(
                NotionProperty(
                    name=prop["name"], prop_type=prop["type"], value=prop["value"]
                )
            )
        page_blocks: list[NotionPageBlock] = []
        for block in body["blocks"]:
            page_blocks.append(
                NotionPageBlock(block_type=block["type"], value=block["value"])
            )
        notion_page: NotionPage = NotionPage(notion_icon, page_properties, page_blocks)
        log_tool.info(f"Payload: {notion_page}")
        response_obj: dict = notion_page_manager.create_page(notion_page, database_id)
        log_tool.info(f"Objeto retornado pela API do Notion: {response_obj}")
        created_id: str = response_obj["id"]
        log_tool.info(f"Página criada com sucesso. ID: {created_id}")
        return {"page_id": created_id}
    except ValidationException as ve:
        error_msg: str = ve.args[0]
        log_tool.error(f"Erro ao validar os dados da requisição: {error_msg}")
        stack_trace: str = traceback.format_exc()
        log_tool.error(f"Traceback: {stack_trace}")
        return JSONResponse(
            content={
                "Message": error_msg,
                "StackTrace": stack_trace,
            },
            status_code=400,
        )
    except Exception as e:
        error_msg: str = e.args[0]
        log_tool.error(f"Erro ao criar página: {error_msg}")
        stack_trace: str = traceback.format_exc()
        log_tool.error(f"Traceback: {stack_trace}")
        return JSONResponse(
            content={
                "Message": error_msg,
                "StackTrace": stack_trace,
            },
            status_code=500,
        )


@router.get(
    "/pages/{page_id}/read",
    tags=["Notion Management"],
    responses={
        200: {
            "description": "Success",
            "content": {
                "application/json": {
                    "example": {
                        "id": "6f48b54c-094d-4339-aa90-89f9985fb6c7",
                        "parent": {
                            "type": "database_id",
                            "database_id": "c7c1007a-d112-4b8c-a621-a769adaf7dda",
                        },
                        "url": "https://www.notion.so/My-Page-6f48b54c094d4339aa9089f9985fb6c7",
                        "request_id": "239e5628-f003-41b2-a4c6-4916f11f24d2",
                        "archived": False,
                        "created_time": "2024-05-24T22:43:00.000Z",
                        "last_edited_time": "2024-05-24T22:43:00.000Z",
                        "created_by": "27910b45-ae07-403c-b7e9-35b5adc896af",
                        "last_edited_by": "27910b45-ae07-403c-b7e9-35b5adc896af",
                        "icon": {"type": "emoji", "value": "🚀"},
                        "properties": [
                            {
                                "name": "Criado por",
                                "type": "created_by",
                                "value": "27910b45-ae07-403c-b7e9-35b5adc896af",
                            },
                            {
                                "name": "Rollup",
                                "type": "rollup",
                                "value": {
                                    "type": "array",
                                    "array": [
                                        {
                                            "type": "rich_text",
                                            "rich_text": [
                                                {
                                                    "type": "text",
                                                    "text": {
                                                        "content": "Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso",
                                                        "link": None,
                                                    },
                                                    "annotations": {
                                                        "bold": False,
                                                        "italic": False,
                                                        "strikethrough": False,
                                                        "underline": False,
                                                        "code": False,
                                                        "color": "default",
                                                    },
                                                    "plain_text": "Desenvolver códigos para solucionar problemas utilizando as tecnologias mais adequadas para cada caso",
                                                    "href": None,
                                                }
                                            ],
                                        }
                                    ],
                                    "function": "show_original",
                                },
                            },
                            {"name": "Data", "type": "date", "value": "2024-05-24"},
                            {"name": "Number", "type": "number", "value": 123.45},
                            {
                                "name": "TB_MICRO_TOOLS_AGENTS",
                                "type": "relation",
                                "value": ["4c65fc9c-2ff4-462e-9493-71ebb14c22cb"],
                            },
                            {
                                "name": "Arquivo",
                                "type": "files",
                                "value": [
                                    {
                                        "name": "MeninaBonita.jpeg",
                                        "url": "https://images.unsplash.com/photo-1513097633097-329a3a64e0d4?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb",
                                    }
                                ],
                            },
                            {
                                "name": "Última edição",
                                "type": "last_edited_time",
                                "value": "2024-05-24T22:43:00.000Z",
                            },
                            {
                                "name": "Número Telefone",
                                "type": "phone_number",
                                "value": "+5511999999999",
                            },
                            {
                                "name": "URL",
                                "type": "url",
                                "value": "https://www.google.com",
                            },
                            {
                                "name": "Criado em",
                                "type": "created_time",
                                "value": "2024-05-24T22:43:00.000Z",
                            },
                            {
                                "name": "Description",
                                "type": "rich_text",
                                "value": "This is a description",
                            },
                            {
                                "name": "Select",
                                "type": "select",
                                "value": {"name": "Option 1", "color": "gray"},
                            },
                            {
                                "name": "Soma",
                                "type": "formula",
                                "value": {"type": "boolean", "boolean": False},
                            },
                            {"name": "IsTrue", "type": "checkbox", "value": True},
                            {
                                "name": "Pessoa",
                                "type": "people",
                                "value": ["6595192e-1c62-4f33-801c-84424f2ffa9c"],
                            },
                            {
                                "name": "Tags",
                                "type": "multi_select",
                                "value": [
                                    {"name": "Tag 1", "color": "gray"},
                                    {"name": "Tag 2", "color": "blue"},
                                ],
                            },
                            {
                                "name": "Email",
                                "type": "email",
                                "value": "fulano@email.com",
                            },
                            {
                                "name": "Última edição por",
                                "type": "last_edited_by",
                                "value": "27910b45-ae07-403c-b7e9-35b5adc896af",
                            },
                            {"name": "Name", "type": "title", "value": "My Page"},
                        ],
                        "blocks": [
                            {
                                "id": "7114b603-c0fe-4f6d-a09b-7556f6c1e2e5",
                                "type": "image",
                                "value": "https://images.unsplash.com/photo-1513097633097-329a3a64e0d4?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb",
                            },
                            {
                                "id": "86e0df54-07e2-4ab7-ad33-0924fcf8c895",
                                "type": "heading_1",
                                "value": "Título 1",
                            },
                            {
                                "id": "b5214a04-59da-445d-87fe-e51f42edda74",
                                "type": "heading_2",
                                "value": "Título 2",
                            },
                            {
                                "id": "f131668c-3cf0-443c-bbcd-8b0dbde03842",
                                "type": "heading_3",
                                "value": "Título 3",
                            },
                            {
                                "id": "eed1c385-599b-4057-b560-e68c6a9955b3",
                                "type": "paragraph",
                                "value": "Este é um parágrafo.",
                            },
                            {
                                "id": "7d6627e8-b5a3-4bfb-b763-d2ac4d2da88f",
                                "type": "video",
                                "value": "https://www.youtube.com/watch?v=wVL6z7lWvjQ&list=RDwVL6z7lWvjQ&start_radio=1",
                            },
                            {
                                "id": "74e9a35b-b820-4800-9429-cabf864fc0a8",
                                "type": "bulleted_list_item",
                                "value": "Item de lista",
                            },
                            {
                                "id": "85119090-5ad5-4a7e-a6ba-6ca44d11b2de",
                                "type": "numbered_list_item",
                                "value": "Item de lista numerada",
                            },
                            {
                                "id": "36099b18-8d64-4240-9ce7-4af4e4deedfe",
                                "type": "to_do",
                                "value": "Tarefa a fazer",
                            },
                            {
                                "id": "3af89dcb-4873-43c6-99af-d82155cc0e60",
                                "type": "toggle",
                                "value": "Alternar",
                            },
                            {
                                "id": "319e8ad8-d839-4610-b2f7-7f37b4ab44e6",
                                "type": "file",
                                "value": {
                                    "name": "MeninaBonita.jpeg",
                                    "url": "https://images.unsplash.com/photo-1513097633097-329a3a64e0d4?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb",
                                },
                            },
                            {
                                "id": "89244ef0-605f-4307-805f-2c3d901f2f62",
                                "type": "code",
                                "value": {
                                    "content": "print('Hello, World!')",
                                    "language": "python",
                                },
                            },
                            {
                                "id": "c03a6c36-f57b-4a00-84cf-79e97e277805",
                                "type": "quote",
                                "value": "Citação",
                            },
                        ],
                    }
                }
            },
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "Message": "Invalid request",
                        "StackTrace": "Traceback...",
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "Message": "Internal Server Error",
                        "StackTrace": "Traceback...",
                    }
                }
            },
        },
    },
)
@inject
async def read_page(
    page_id: str = Path(
        ...,
        title="Page ID",
        description="ID da página do Notion",
        example="6f48b54c-094d-4339-aa90-89f9985fb6c7",
    ),
    log_tool: LogTool = Depends(Provide[Container.log_tool]),
    notion_page_manager: NotionPageManager = Depends(
        Provide[Container.notion_page_manager]
    ),
):
    """
    Lê uma página no Notion.
    """
    try:
        log_tool.info("Lendo página no Notion.")
        assert page_id is not None, "ID da página não pode ser nulo."
        response_obj: NotionPage = notion_page_manager.read_page_by_id(page_id)
        log_tool.info(f"Página retornada: \n{response_obj}")
        return response_obj
    except ValidationException as ve:
        error_msg: str = ve.args[0]
        log_tool.error(f"Erro ao validar os dados da requisição: {error_msg}")
        stack_trace: str = traceback.format_exc()
        log_tool.error(f"Traceback: {stack_trace}")
        return JSONResponse(
            content={
                "Message": error_msg,
                "StackTrace": stack_trace,
            },
            status_code=400,
        )
    except Exception as e:
        error_msg: str = e.args[0]
        log_tool.error(f"Erro ao ler página: {error_msg}")
        stack_trace: str = traceback.format_exc()
        log_tool.error(f"Traceback: {stack_trace}")
        return JSONResponse(
            content={
                "Message": error_msg,
                "StackTrace": stack_trace,
            },
            status_code=500,
        )


@router.put(
    "/pages/{page_id}/archive",
    tags=["Notion Management"],
    responses={
        200: {
            "description": "Success",
            "content": {
                "application/json": {
                    "example": {
                        "Message": "Página 6f48b54c-094d-4339-aa90-89f9985fb6c7 arquivada com sucesso."
                    }
                }
            },
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "Message": "Invalid request",
                        "StackTrace": "Traceback...",
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "Message": "Internal Server Error",
                        "StackTrace": "Traceback...",
                    }
                }
            },
        },
    },
)
@inject
async def archive_page(
    page_id: str = Path(
        ...,
        title="Page ID",
        description="ID da página do Notion",
        example="6f48b54c-094d-4339-aa90-89f9985fb6c7",
    ),
    log_tool: LogTool = Depends(Provide[Container.log_tool]),
    notion_page_manager: NotionPageManager = Depends(
        Provide[Container.notion_page_manager]
    ),
):
    """
    Atualiza uma página no Notion.
    """
    try:
        log_tool.info("Atualizando página no Notion.")
        assert page_id is not None, "ID da página não pode ser nulo."
        response: dict = notion_page_manager.archive_page_by_id(page_id)
        log_tool.info(f"Resposta da API do Notion: {response}")
        return {"Message": f"Página {page_id} arquivada com sucesso."}
    except ValidationException as ve:
        error_msg: str = ve.args[0]
        log_tool.error(f"Erro ao validar os dados da requisição: {error_msg}")
        stack_trace: str = traceback.format_exc()
        log_tool.error(f"Traceback: {stack_trace}")
        return JSONResponse(
            content={
                "Message": error_msg,
                "StackTrace": stack_trace,
            },
            status_code=400,
        )
    except Exception as e:
        error_msg: str = e.args[0]
        log_tool.error(f"Erro ao atualizar página: {error_msg}")
        stack_trace: str = traceback.format_exc()
        log_tool.error(f"Traceback: {stack_trace}")
        return JSONResponse(
            content={
                "Message": error_msg,
                "StackTrace": stack_trace,
            },
            status_code=500,
        )


@router.put(
    "/pages/{page_id}/unarchive",
    tags=["Notion Management"],
    responses={
        200: {
            "description": "Success",
            "content": {
                "application/json": {
                    "example": {
                        "Message": "Página 6f48b54c-094d-4339-aa90-89f9985fb6c7 recuperada com sucesso."
                    }
                }
            },
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "Message": "Invalid request",
                        "StackTrace": "Traceback...",
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "Message": "Internal Server Error",
                        "StackTrace": "Traceback...",
                    }
                }
            },
        },
    },
)
@inject
async def unarchive_page(
    page_id: str = Path(
        ...,
        title="Page ID",
        description="ID da página do Notion",
        example="6f48b54c-094d-4339-aa90-89f9985fb6c7",
    ),
    log_tool: LogTool = Depends(Provide[Container.log_tool]),
    notion_page_manager: NotionPageManager = Depends(
        Provide[Container.notion_page_manager]
    ),
):
    """
    Desarquiva uma página no Notion.
    """
    try:
        log_tool.info("Desarquivando página no Notion.")
        assert page_id is not None, "ID da página não pode ser nulo."
        response: dict = notion_page_manager.unarchive_page_by_id(page_id)
        log_tool.info(f"Resposta da API do Notion: {response}")
        return {"Message": f"Página {page_id} recuperada com sucesso."}
    except ValidationException as ve:
        error_msg: str = ve.args[0]
        log_tool.error(f"Erro ao validar os dados da requisição: {error_msg}")
        stack_trace: str = traceback.format_exc()
        log_tool.error(f"Traceback: {stack_trace}")
        return JSONResponse(
            content={
                "Message": error_msg,
                "StackTrace": stack_trace,
            },
            status_code=400,
        )
    except Exception as e:
        error_msg: str = e.args[0]
        log_tool.error(f"Erro ao desarquivar página: {error_msg}")
        stack_trace: str = traceback.format_exc()
        log_tool.error(f"Traceback: {stack_trace}")
        return JSONResponse(
            content={
                "Message": error_msg,
                "StackTrace": stack_trace,
            },
            status_code=500,
        )
