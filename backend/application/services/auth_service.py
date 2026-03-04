"""认证相关应用服务：注册、登录（后续步骤）等。"""
from __future__ import annotations
from typing import Protocol
from uuid import UUID

from domain.user import IUserRepository


class PasswordHasher(Protocol):
    def hash(self, plain: str) -> str: ...
    def verify(self, plain: str, hashed: str) -> bool: ...


class AuthService:
    """用户注册、登录等用例。"""

    def __init__(self, user_repository: IUserRepository, password_hasher: PasswordHasher):
        self._repo = user_repository
        self._hasher = password_hasher

    def register(self, email: str, password: str, username: str = "") -> RegisterResult:
        """注册：校验邮箱唯一性，哈希密码后落库。"""
        if self._repo.exists_by_email(email):
            raise EmailAlreadyExistsError(email)
        password_hash = self._hasher.hash(password)
        result = self._repo.create(email=email, password_hash=password_hash, username=username or "")
        return RegisterResult(id=result.id, email=result.email)


class RegisterResult:
    def __init__(self, id: UUID, email: str):
        self.id = id
        self.email = email


class EmailAlreadyExistsError(ValueError):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"邮箱已存在: {email}")
