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


@router.get(
    "/info",
    tags=["Information"],
    responses={
        200: {"description": "Success", "content": {"application/json": {}}},
        500: {
            "description": "Internal Server Error",
            "content": {"application/json": {}},
        },
    },
)
@inject
async def get_info(logger: LogTool = Depends(Provide[Container.log_tool])):
    """
    Retorna informações básicas deste micro-serviço.

    Retorna um objeto JSON com o nome, a versão e outras informações úteis do micro-serviço.

    Retorna:
        - 200: Sucesso com as informações básicas do micro-serviço.
        - 500: Erro interno do servidor com a mensagem de erro.
    """
    try:
        name = "Meu Micro-serviço"
        version = "1.0.0"
        system = platform.system()
        machine = platform.machine()
        processor = platform.processor()
        python_version = platform.python_version()
        environment = get("environment")
        logger.info(
            "Informações sobre a API foram requisitadas e retornadas com sucesso."
        )
        return {
            "name": name,
            "version": version,
            "system": system,
            "machine": machine,
            "processor": processor,
            "python_version": python_version,
            "environment": environment,
        }
    except Exception as e:
        logger.error(f"Erro ao obter informações sobre a API: {str(e)}")
        return {"error": str(e)}, 500


@router.post(
    "/create",
    tags=["Sample Management"],
    responses={
        200: {
            "description": "Success",
            "content": {"application/json": {"example": {"CreatedId": "123456"}}},
        },
        422: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "ErrorTag": "Unprocessable Entity",
                        "ErrorMessage": "Invalid request",
                        "ErrorCode": "422",
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "ErrorTag": "Internal Server Error",
                        "ErrorMessage": "Internal Server Error",
                        "ErrorCode": "500",
                    }
                }
            },
        },
    },
)
@inject
async def create_sample(
    body: dict = Body(
        ...,
        example={
            "ThingName": "My Thing",
            "ThingDescription": "This is a thing.",
            "ThingValue": 123.45,
            "ThingStatus": "Active",
            "ThingCreatedAt": "2021-01-01T00:00:00",
            "ThingUpdatedAt": "2021-01-01T00:00:00",
        },
    ),
    logger: LogTool = Depends(Provide[Container.log_tool]),
):
    """
    Cria um objeto de exemplo.
    """
    try:
        logger.info("Objeto de exemplo criado com sucesso.")
        logger.info(f"Objeto de exemplo: {body}")
        return {"CreatedId": "123456"}
    except ValidationException as e:
        logger.error(f"Erro ao validar os dados da requisição: {str(e)}")
        return 400, {
            "ErrorTag": "Bad Request",
            "ErrorMessage": "Invalid request",
            "ErrorCode": "400",
        }
    except Exception as e:
        logger.error(f"Erro ao criar objeto de exemplo: {str(e)}")
        return 500, {
            "ErrorTag": "Internal Server Error",
            "ErrorMessage": "Internal Server Error",
            "ErrorCode": "500",
        }


@router.get(
    "/read/{id}",
    tags=["Sample Management"],
    responses={
        200: {
            "description": "Success",
            "content": {
                "application/json": {
                    "example": {
                        "ThingName": "My Thing",
                        "ThingDescription": "This is a thing.",
                        "ThingValue": 123.45,
                        "ThingStatus": "Active",
                        "ThingCreatedAt": "2021-01-01T00:00:00",
                        "ThingUpdatedAt": "2021-01-01T00:00:00",
                    }
                }
            },
        },
        422: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "ErrorTag": "Unprocessable Entity",
                        "ErrorMessage": "Invalid request",
                        "ErrorCode": "422",
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "ErrorTag": "Internal Server Error",
                        "ErrorMessage": "Internal Server Error",
                        "ErrorCode": "500",
                    }
                }
            },
        },
    },
)
@inject
async def read_sample(
    id: str = Path(
        ..., title="ID", description="ID do objeto de exemplo", example="123456"
    ),
    logger: LogTool = Depends(Provide[Container.log_tool]),
):
    """
    Lê um objeto de exemplo.
    """
    try:
        logger.info(f"Objeto de exemplo lido com sucesso. ID: {id}")
        return {
            "ThingName": "My Thing",
            "ThingDescription": "This is a thing.",
            "ThingValue": 123.45,
            "ThingStatus": "Active",
            "ThingCreatedAt": "2021-01-01T00:00:00",
            "ThingUpdatedAt": "2021-01-01T00:00:00",
        }
    except ValidationException as ve:
        logger.error(f"Erro ao validar os dados da requisição: {str(ve)}")
        return 400, {
            "ErrorTag": "Bad Request",
            "ErrorMessage": "Invalid request",
            "ErrorCode": "400",
        }
    except Exception as e:
        logger.error(f"Erro ao ler objeto de exemplo: {str(e)}")
        return 500, {
            "ErrorTag": "Internal Server Error",
            "ErrorMessage": "Internal Server Error",
            "ErrorCode": "500",
        }


@router.put(
    "/update/{id}",
    tags=["Sample Management"],
    responses={
        200: {
            "description": "Success",
            "content": {"application/json": {"example": {"UpdatedId": "123456"}}},
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "ErrorTag": "Bad Request",
                        "ErrorMessage": "Invalid request",
                        "ErrorCode": "400",
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "ErrorTag": "Internal Server Error",
                        "ErrorMessage": "Internal Server Error",
                        "ErrorCode": "500",
                    }
                }
            },
        },
    },
)
@inject
async def update_sample(
    id: str = Path(
        ..., title="ID", description="ID do objeto de exemplo", example="123456"
    ),
    body: dict = Body(
        ...,
        example={
            "ThingName": "My Thing",
            "ThingDescription": "This is a thing.",
            "ThingValue": 123.45,
            "ThingStatus": "Active",
            "ThingCreatedAt": "2021-01-01T00:00:00",
            "ThingUpdatedAt": "2021-01-01T00:00:00",
        },
    ),
    logger: LogTool = Depends(Provide[Container.log_tool]),
):
    """
    Atualiza um objeto de exemplo.
    """
    try:
        logger.info(f"Objeto de exemplo atualizado com sucesso. ID: {id}")
        logger.info(f"Objeto de exemplo atualizado: {body}")
        return {"UpdatedId": "123456"}
    except ValidationException as ve:
        logger.error(f"Erro ao validar os dados da requisição: {str(ve)}")
        return 400, {
            "ErrorTag": "Bad Request",
            "ErrorMessage": "Invalid request",
            "ErrorCode": "400",
        }
    except Exception as e:
        logger.error(f"Erro ao atualizar objeto de exemplo: {str(e)}")
        return 500, {
            "ErrorTag": "Internal Server Error",
            "ErrorMessage": "Internal Server Error",
            "ErrorCode": "500",
        }


@router.delete(
    "/delete/{id}",
    tags=["Sample Management"],
    responses={
        200: {
            "description": "Success",
            "content": {"application/json": {"example": {"DeletedId": "123456"}}},
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "ErrorTag": "Bad Request",
                        "ErrorMessage": "Invalid request",
                        "ErrorCode": "400",
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "ErrorTag": "Internal Server Error",
                        "ErrorMessage": "Internal Server Error",
                        "ErrorCode": "500",
                    }
                }
            },
        },
    },
)
@inject
async def delete_sample(
    id: str = Path(
        ..., title="ID", description="ID do objeto de exemplo", example="123456"
    ),
    logger: LogTool = Depends(Provide[Container.log_tool]),
):
    """
    Deleta um objeto de exemplo.
    """
    try:
        logger.info(f"Objeto de exemplo deletado com sucesso. ID: {id}")
        return {"DeletedId": "123456"}
    except ValidationException as ve:
        logger.error(f"Erro ao validar os dados da requisição: {str(ve)}")
        return 400, {
            "ErrorTag": "Bad Request",
            "ErrorMessage": "Invalid request",
            "ErrorCode": "400",
        }
    except Exception as e:
        logger.error(f"Erro ao deletar objeto de exemplo: {str(e)}")
        return 500, {
            "ErrorTag": "Internal Server Error",
            "ErrorMessage": "Internal Server Error",
            "ErrorCode": "500",
        }


@router.post(
    "/pages/{database_id}",
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
            "icon": {"type": "emoji", "emoji": "🚀"},
            "properties": [
                {"name": "Name", "type": "title", "value": "My Page"},
                {"name": "Description", "type": "rich_text", "value": "This is a description"},
                {"name": "Number", "type": "number", "value": 123.45},
                {"name": "Select", "type": "select", "value": {"name": "Option 1", "color": "gray"}},
                {"name": "Tags", "type": "multi_select", "value": [{"name": "Tag 1", "color": "gray"}, {"name": "Tag 2", "color": "blue"}]},
                {"name": "Data", "type": "date", "value": "2024-05-24"},
                {"name": "IsTrue", "type": "checkbox", "value": True},
                {"name": "Pessoa", "type": "people", "value": ["6595192e-1c62-4f33-801c-84424f2ffa9c"]},
                {"name": "Arquivo", "type": "files", "value": [{"name": "MeninaBonita.jpeg", "url": "https://images.unsplash.com/photo-1513097633097-329a3a64e0d4?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb"}]},
                {"name": "URL", "type": "url", "value": "https://www.google.com"},
                {"name": "Email", "type": "email", "value": "fulano@email.com"},
                {"name": "Número Telefone", "type": "phone_number", "value": "+5511999999999"},
                {"name": "TB_MICRO_TOOLS_AGENTS", "type": "relation", "value": ["4c65fc9c-2ff4-462e-9493-71ebb14c22cb"]},
            ],
            "blocks": [
                {"type": "image", "value": "https://images.unsplash.com/photo-1513097633097-329a3a64e0d4?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb"},
                {"type": "heading_1", "value": "Título 1"},
                {"type": "heading_2", "value": "Título 2"},
                {"type": "heading_3", "value": "Título 3"},
                {"type": "paragraph", "value": "Este é um parágrafo."},
                {"type": "video", "value": "https://www.youtube.com/watch?v=wVL6z7lWvjQ&list=RDwVL6z7lWvjQ&start_radio=1"},
                {"type": "bulleted_list_item", "value": "Item de lista"},
                {"type": "numbered_list_item", "value": "Item de lista numerada"},
                {"type": "to_do", "value": "Tarefa a fazer"},
                {"type": "toggle", "value": "Alternar"},
                {"type": "file", "value": {"name": "MeninaBonita.jpeg", "url": "https://images.unsplash.com/photo-1513097633097-329a3a64e0d4?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb"}},
                {"type": "code", "value": {"content": "print('Hello, World!')", "language": "python"}},
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
            icon_type=body["icon"]["type"], icon_value=body["icon"]["emoji"]
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
            page_blocks.append(NotionPageBlock(block_type=block["type"], value=block["value"]))
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
