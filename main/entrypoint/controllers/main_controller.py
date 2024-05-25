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
        name = "Micro Tools Api"
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
