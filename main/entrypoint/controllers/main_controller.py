import platform
from dependency_injector.wiring import inject, Provide
from main.library.di_container import Container
from main.library.tools.core.log_tool import LogTool
from fastapi import APIRouter, Body, Depends, Path
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
        logger.info("Informações sobre a API foram requisitadas e retornadas com sucesso.")
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
            "content": {
                "application/json": {
                    "example": {
                        "CreatedId": "123456"
                    }
                }
            }
        },
        422: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "ErrorTag": "Unprocessable Entity",
                        "ErrorMessage": "Invalid request",
                        "ErrorCode": "422"
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
                        "ErrorCode": "500"
                    }
                }
            },
        },
    }
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
        }
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
            }
        },
        422: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "ErrorTag": "Unprocessable Entity",
                        "ErrorMessage": "Invalid request",
                        "ErrorCode": "422"
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
                        "ErrorCode": "500"
                    }
                }
            },
        },
    }
)
@inject
async def read_sample(
    id: str = Path(
        ...,
        title="ID",
        description="ID do objeto de exemplo",
        example="123456"
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
            "content": {
                "application/json": {
                    "example": {
                        "UpdatedId": "123456"
                    }
                }
            }
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "ErrorTag": "Bad Request",
                        "ErrorMessage": "Invalid request",
                        "ErrorCode": "400"
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
                        "ErrorCode": "500"
                    }
                }
            },
        },
    }
)
@inject
async def update_sample(
    id: str = Path(
        ...,
        title="ID",
        description="ID do objeto de exemplo",
        example="123456"
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
        }
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
            "content": {
                "application/json": {
                    "example": {
                        "DeletedId": "123456"
                    }
                }
            }
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "ErrorTag": "Bad Request",
                        "ErrorMessage": "Invalid request",
                        "ErrorCode": "400"
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
                        "ErrorCode": "500"
                    }
                }
            },
        },
    }
)
@inject
async def delete_sample(
    id: str = Path(
        ...,
        title="ID",
        description="ID do objeto de exemplo",
        example="123456"
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