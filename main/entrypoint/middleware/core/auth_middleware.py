from fastapi import Depends
from fastapi.security import HTTPBearer

from main.entrypoint.utils.exceptions.unauthorized_exception import (
    UnauthorizedException,
)

security = HTTPBearer()


async def get_token(security: HTTPBearer = Depends(security)) -> str:
    token: str = security.credentials
    if token is None:
        raise UnauthorizedException("Token not found")
    return token
