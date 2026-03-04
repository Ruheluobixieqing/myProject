"""认证路由：注册、登录（后续）。"""
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


@router.post("/register", response_model=RegisterResponse)
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
        raise HTTPException(status_code=400, detail=f"邮箱已存在: {e.email}")


@router.post("/login", response_model=LoginResponse)
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
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    except UserBannedError as e:
        raise HTTPException(status_code=403, detail=f"账号已封禁: {e.email}")
    except InvalidPasswordError:
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
