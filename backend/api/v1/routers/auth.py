"""认证路由：注册、登录（后续）。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from application.services.auth_service import AuthService, EmailAlreadyExistsError
from infrastructure.persistence.database import get_db
from infrastructure.persistence.postgres.user_repository import UserRepository
from infrastructure.security import PasswordHasher
from api.v1.schemas.auth import RegisterRequest, RegisterResponse

router = APIRouter()

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(
        user_repository=UserRepository(db),
        password_hasher=PasswordHasher(),
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
