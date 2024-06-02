import traceback
from dependency_injector.wiring import inject, Provide
from fastapi.responses import JSONResponse
from main.entrypoint.middleware.core.auth_middleware import get_token
from main.library.di_container import Container
from main.library.tools.core.character_ai_tool import CharacterAiTool
from main.library.tools.core.log_tool import LogTool
from fastapi import APIRouter, Body, Depends, Path, Query
from main.library.tools.models.character_ai_response import CharacterAiResponse
from main.library.utils.models.validation_exception import ValidationException

router = APIRouter()


@router.post(
    "/characterai/{char_id}/chat",
    tags=["Character AI"],
    responses={
        200: {
            "description": "Success",
            "content": {
                "application/json": {
                    "example": {
                        "created_at": "27/05/2024 22:10:23",
                        "session": {
                            "chat_id": "0f3e34b0-df45-40d2-8be3-b0d5bffd1377",
                            "turn_id": "78c30aad-bbbb-4bb5-b39e-30fff8cd0440",
                        },
                        "character": {
                            "id": "amhBBampjntDRr_RjHdjyrwvAxOqklHwItldIsqsjLU",
                            "name": "Chat GPT",
                        },
                        "candidates": [
                            {
                                "candidate_id": "79f9354d-7147-45bc-994d-29590641101b",
                                "message": 'Como Lorde Dart Vader, eu digo com determinação: "Luke Skywalker, seus poderes são fracos comparados aos meus. Logo, destruirei qualquer oposição e dominarei o universo, independentemente do seu intento. Prepare-se para minha vingança."',
                            }
                        ],
                        "primary_candidate_id": "79f9354d-7147-45bc-994d-29590641101b",
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
        403: {
            "description": "Forbidden",
            "content": {
                "application/json": {"example": {"detail": "Not authenticated"}}
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
async def chat(
    token: str = Depends(get_token),
    char_id: str = Path(
        ...,
        title="Character ID",
        description="Identificador do personagem",
        example="amhBBampjntDRr_RjHdjyrwvAxOqklHwItldIsqsjLU",
    ),
    chat_id: str = Query(
        None,
        title="Chat ID",
        description="Identificador do chat",
        example="0f3e34b0-df45-40d2-8be3-b0d5bffd1377",
    ),
    body: dict = Body(
        ...,
        title="Body",
        description="Texto a ser enviado para o chat",
        example={
            "message": "Olá! Assuma que você é o Dart Vader e responda como se fosse ele. Eu chego a você e digo: 'Olá Anakin, meu nome é Luke Skywalker, eu vou impedir você de dominar o universo."
        },
    ),
    log_tool: LogTool = Depends(Provide[Container.log_tool]),
    character_ai_tool: CharacterAiTool = Depends(Provide[Container.character_ai_tool]),
):
    """
    Conversar com um personagem.
    """
    try:
        log_tool.info("Conversando com personagem.")
        assert char_id is not None, "Character ID não pode ser nulo."
        assert body is not None, "Body não pode ser nulo."
        message: str = body.get("message")
        assert message is not None, "Texto não pode ser nulo."
        assert len(message) > 0, "Texto não pode ser vazio."
        response: CharacterAiResponse = await character_ai_tool.chat(
            token, char_id, message, chat_id
        )
        assert response is not None, "Resposta não pode ser nula."
        log_tool.info("Resposta obtida com sucesso.")
        return response
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
        log_tool.error(f"Erro ao conversar com personagem: {error_msg}")
        stack_trace: str = traceback.format_exc()
        log_tool.error(f"Traceback: {stack_trace}")
        return JSONResponse(
            content={
                "Message": error_msg,
                "StackTrace": stack_trace,
            },
            status_code=500,
        )
