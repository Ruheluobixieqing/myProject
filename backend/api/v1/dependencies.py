"""API 层依赖：鉴权等。"""
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from infrastructure.persistence.database import get_db
from infrastructure.persistence.postgres.user_repository import UserRepository
from infrastructure.security import decode_access_token
from domain.user.repository import CurrentUserResult

# 声明 Bearer 认证，Swagger 会据此显示「Authorize」并在请求中自动带上 Authorization 头
http_bearer = HTTPBearer(auto_error=False)

# 与 auth 错误格式一致
def _err(status_code: int, code: str, message: str, details: dict | None = None):
    raise HTTPException(
        status_code=status_code,
        detail={"code": code, "message": message, "details": details or {}},
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(http_bearer),
    db: Session = Depends(get_db),
) -> CurrentUserResult:
    """从 Authorization: Bearer <token> 解析 JWT，校验后返回当前用户；无效或封禁则 401/403。"""
    if not credentials:
        _err(401, "UNAUTHORIZED", "缺少或无效的 Authorization 头")
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        _err(401, "INVALID_TOKEN", "token 无效或已过期")
    sub = payload.get("sub")
    if not sub:
        _err(401, "INVALID_TOKEN", "token 无效")
    try:
        user_id = UUID(sub)
    except ValueError:
        _err(401, "INVALID_TOKEN", "token 无效")
    repo = UserRepository(db)
    user = repo.find_by_id(user_id)
    if user is None:
        _err(401, "USER_NOT_FOUND", "用户不存在或已删除")
    if user.status == "banned":
        _err(403, "USER_BANNED", "账号已封禁", {"email": user.email})
    return user


def require_admin(current_user: CurrentUserResult = Depends(get_current_user)) -> CurrentUserResult:
    """要求当前用户为管理员，否则 403。"""
    if current_user.role != "admin":
        _err(403, "FORBIDDEN", "需要管理员权限")
    return current_user
