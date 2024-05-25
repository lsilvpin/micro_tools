import traceback
from dependency_injector.wiring import inject, Provide
from fastapi.responses import JSONResponse
from main.library.di_container import Container
from main.library.repositories.notion.core.notion_database_manager import (
    NotionDatabaseManager,
)
from main.library.repositories.notion.core.notion_page_manager import NotionPageManager
from main.library.repositories.notion.core.notion_searcher import NotionSearcher
from main.library.repositories.notion.models.notion_custom_icon import NotionIcon
from main.library.repositories.notion.models.notion_database import NotionDatabase
from main.library.repositories.notion.models.notion_page import NotionPage
from main.library.repositories.notion.models.notion_page_block import NotionPageBlock
from main.library.repositories.notion.models.notion_property import NotionProperty
from main.library.repositories.notion.models.notion_search_result import (
    NotionSearchResult,
)
from main.library.tools.core.log_tool import LogTool
from fastapi import APIRouter, Body, Depends, Path
from main.library.tools.core.settings_tool import SettingsTool
from main.library.utils.core.settings_helper import get
from main.library.utils.models.validation_exception import ValidationException

router = APIRouter()


@router.post(
    "/search",
    tags=["Notion Searcher"],
    responses={
        200: {
            "description": "Success",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "6f48b54c-094d-4339-aa90-89f9985fb6c7",
                            "title": "Página de teste",
                            "url": "https://www.notion.so/6f48b54c094d4339aa9089f9985fb6c7",
                            "archived": False,
                        }
                    ]
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
async def search(
    query: dict = Body(
        ...,
        example={
            "query": "",
            "sort": {"direction": "ascending", "timestamp": "last_edited_time"},
            "page_size": 10,
        },
        title="Query",
        description="Termo de busca",
    ),
    log_tool: LogTool = Depends(Provide[Container.log_tool]),
    notion_searcher: NotionSearcher = Depends(Provide[Container.notion_searcher]),
):
    """
    Busca uma página no Notion.
    """
    try:
        log_tool.info("Buscando página no Notion.")
        assert query is not None, "Query não pode ser nula."
        result: NotionSearchResult = notion_searcher.search(query)
        log_tool.info(f"Páginas retornadas: \n{result}")
        return result
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
        log_tool.error(f"Erro ao buscar página: {error_msg}")
        stack_trace: str = traceback.format_exc()
        log_tool.error(f"Traceback: {stack_trace}")
        return JSONResponse(
            content={
                "Message": error_msg,
                "StackTrace": stack_trace,
            },
            status_code=500,
        )
