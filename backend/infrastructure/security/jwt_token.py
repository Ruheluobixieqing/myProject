"""JWT 签发与校验：放在基础设施层，供登录与鉴权使用。"""
from uuid import UUID
import jwt
from datetime import datetime, timedelta

from infrastructure.config import settings


def create_access_token(user_id: UUID, role: str) -> tuple[str, int]:
    """签发 access_token。返回 (token 字符串, 有效秒数)。"""
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return token, int(expires_delta.total_seconds())


def decode_access_token(token: str) -> dict | None:
    """解码并校验 token，失败返回 None。"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )
        return payload
    except jwt.PyJWTError:
        return None
