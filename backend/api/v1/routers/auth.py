"""认证路由：注册、登录（后续）。错误响应统一为 detail: { code, message, details }。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from application.services.auth_service import (
    AuthService,
    EmailAlreadyExistsError,
    UserNotFoundError,
    UserBannedError,
    InvalidPasswordError,
)
from infrastructure.persistence.database import get_db
from infrastructure.persistence.postgres.user_repository import UserRepository
from infrastructure.security import PasswordHasher, create_access_token
from api.v1.schemas.auth import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse

router = APIRouter()


class _JwtTokenCreator:
    def create(self, user_id, role):
        return create_access_token(user_id, role)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(
        user_repository=UserRepository(db),
        password_hasher=PasswordHasher(),
        token_creator=_JwtTokenCreator(),
    )


def _err(status_code: int, code: str, message: str, details: dict | None = None):
    raise HTTPException(
        status_code=status_code,
        detail={"code": code, "message": message, "details": details or {}},
    )


@router.post(
    "/register",
    response_model=RegisterResponse,
    responses={
        400: {"description": "邮箱已存在", "content": {"application/json": {"example": {"detail": {"code": "EMAIL_ALREADY_EXISTS", "message": "该邮箱已被注册", "details": {"email": "user@example.com"}}}}}},
    },
)
def register(body: RegisterRequest, service: AuthService = Depends(get_auth_service)):
    """用户注册：邮箱必填且唯一，用户名可选可重复。"""
    try:
        result = service.register(
            email=body.email,
            password=body.password,
            username=body.username or "",
        )
        return RegisterResponse(id=str(result.id), email=result.email)
    except EmailAlreadyExistsError as e:
        _err(400, "400", "该邮箱已被注册", {"email": e.email})

    
@router.post(
    "/login",
    response_model=LoginResponse,
    responses={
        401: {"description": "邮箱或密码错误", "content": {"application/json": {"example": {"detail": {"code": "401", "message": "邮箱或密码错误", "details": {}}}}}},
        403: {"description": "账号已封禁", "content": {"application/json": {"example": {"detail": {"code": "403", "message": "账号已封禁，无法登录", "details": {"email": "user@example.com"}}}}}},
    },
)
def login(body: LoginRequest, service: AuthService = Depends(get_auth_service)):
    """登录：邮箱+密码，返回 access_token。"""
    try:
        result = service.login(email=body.email, password=body.password)
        return LoginResponse(
            access_token=result.access_token,
            token_type=result.token_type,
            expires_in=result.expires_in,
        )
    except UserNotFoundError:
        _err(401, "401", "邮箱或密码错误")
    except UserBannedError as e:
        _err(403, "403", "账号已封禁，无法登录", {"email": e.email})
    except InvalidPasswordError:
        _err(401, "401", "邮箱或密码错误")
