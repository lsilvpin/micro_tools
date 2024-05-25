import traceback
from dependency_injector.wiring import inject, Provide
from fastapi.responses import JSONResponse
from main.library.di_container import Container
from main.library.repositories.notion.core.notion_database_manager import (
    NotionDatabaseManager,
)
from main.library.repositories.notion.core.notion_page_manager import NotionPageManager
from main.library.repositories.notion.models.notion_custom_icon import NotionIcon
from main.library.repositories.notion.models.notion_database import NotionDatabase
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
    "/databases/{page_id}/create",
    tags=["Notion Database Management"],
    responses={
        200: {
            "description": "Success",
            "content": {
                "application/json": {
                    "example": {"database_id": "6301f640e21c4526a72ed96e7d4ba71d"}
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
async def create_database(
    page_id: str = Path(
        ...,
        title="Page ID",
        description="ID da página do Notion",
        example="6f48b54c-094d-4339-aa90-89f9985fb6c7",
    ),
    body: dict = Body(
        ...,
        example={
            "is_inline": True,
            "icon": {"type": "emoji", "value": "🚀"},
            "title": "Banco de dados",
            "description": "Descrição do db",
            "properties": [
                {"name": "Arquivo", "type": "files", "value": None, "options": {}},
                {
                    "name": "Número Telefone",
                    "type": "phone_number",
                    "value": None,
                    "options": {},
                },
                {
                    "name": "Select",
                    "type": "select",
                    "value": None,
                    "options": {
                        "options": [
                            {
                                "name": "Alface",
                                "color": "green",
                            },
                            {
                                "name": "Cebola",
                                "color": "pink",
                            },
                            {
                                "name": "Kacto",
                                "color": "yellow",
                            },
                            {
                                "name": "Option 1",
                                "color": "gray",
                            },
                        ]
                    },
                },
                {"name": "URL", "type": "url", "value": None, "options": {}},
                {
                    "name": "Criado por",
                    "type": "created_by",
                    "value": None,
                    "options": {},
                },
                {
                    "name": "Última edição",
                    "type": "last_edited_time",
                    "value": None,
                    "options": {},
                },
                {
                    "name": "Tags",
                    "type": "multi_select",
                    "value": None,
                    "options": {
                        "options": [
                            {
                                "name": "Tag A",
                                "color": "orange",
                            },
                            {
                                "name": "Tag B",
                                "color": "blue",
                            },
                            {
                                "name": "Tag C",
                                "color": "gray",
                            },
                            {
                                "name": "Tag D",
                                "color": "yellow",
                            },
                            {
                                "name": "Tag 1",
                                "color": "gray",
                            },
                            {
                                "name": "Tag 2",
                                "color": "blue",
                            },
                        ]
                    },
                },
                {
                    "name": "Última edição por",
                    "type": "last_edited_by",
                    "value": None,
                    "options": {},
                },
                {"name": "Data", "type": "date", "value": None, "options": {}},
                {
                    "name": "Number",
                    "type": "number",
                    "value": None,
                    "options": {"format": "number"},
                },
                {
                    "name": "Criado em",
                    "type": "created_time",
                    "value": None,
                    "options": {},
                },
                {"name": "Email", "type": "email", "value": None, "options": {}},
                {"name": "Pessoa", "type": "people", "value": None, "options": {}},
                {
                    "name": "Description",
                    "type": "rich_text",
                    "value": None,
                    "options": {},
                },
                {"name": "IsTrue", "type": "checkbox", "value": None, "options": {}},
                {"name": "Name", "type": "title", "value": None, "options": {}},
            ],
        },
    ),
    log_tool: LogTool = Depends(Provide[Container.log_tool]),
    notion_database_manager: NotionDatabaseManager = Depends(
        Provide[Container.notion_database_manager]
    ),
):
    """
    Cria um banco de dados no Notion.
    """
    try:
        log_tool.info("Criando banco de dados no Notion.")
        database: NotionDatabase = NotionDatabase.from_dict(body)
        response: dict = notion_database_manager.create_database(page_id, database)
        log_tool.info(f"Resposta da API do Notion: {response}")
        database_id: str = response["id"]
        return {"database_id": database_id}
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
    "/databases/{database_id}/read",
    tags=["Notion Database Management"],
    responses={
        200: {
            "description": "Success",
            "content": {"application/json": {"example": {"temp": "temp"}}},
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
async def read_database(
    database_id: str = Path(
        ...,
        title="Database ID",
        description="ID do banco de dados do Notion",
        example="c7c1007a-d112-4b8c-a621-a769adaf7dda",
    ),
    log_tool: LogTool = Depends(Provide[Container.log_tool]),
    notion_database_manager: NotionDatabaseManager = Depends(
        Provide[Container.notion_database_manager]
    ),
):
    """
    Lê um banco de dados no Notion.
    """
    try:
        log_tool.info("Lendo banco de dados no Notion.")
        assert database_id is not None, "ID do banco de dados não pode ser nulo."
        db: NotionDatabase = notion_database_manager.read_database_by_id(database_id)
        log_tool.info(f"Banco de dados retornado: \n{db}")
        return db
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
        log_tool.error(f"Erro ao ler banco de dados: {error_msg}")
        stack_trace: str = traceback.format_exc()
        log_tool.error(f"Traceback: {stack_trace}")
        return JSONResponse(
            content={
                "Message": error_msg,
                "StackTrace": stack_trace,
            },
            status_code=500,
        )
