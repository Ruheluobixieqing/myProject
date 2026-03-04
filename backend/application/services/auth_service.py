"""认证相关应用服务：注册、登录（后续步骤）等。"""
from __future__ import annotations
from typing import Protocol
from uuid import UUID

from domain.user import IUserRepository
from domain.user.repository import LoginUserResult


class PasswordHasher(Protocol):
    def hash(self, plain: str) -> str: ...
    def verify(self, plain: str, hashed: str) -> bool: ...


class TokenCreator(Protocol):
    def create(self, user_id: UUID, role: str) -> tuple[str, int]:
        """签发 token，返回 (token 字符串, 有效秒数)。"""
        ...


class AuthService:
    """用户注册、登录等用例。"""

    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: PasswordHasher,
        token_creator: TokenCreator,
    ):
        self._repo = user_repository
        self._hasher = password_hasher
        self._token_creator = token_creator

    def register(self, email: str, password: str, username: str = "") -> RegisterResult:
        """注册：校验邮箱唯一性，哈希密码后落库。"""
        if self._repo.exists_by_email(email):
            raise EmailAlreadyExistsError(email)
        password_hash = self._hasher.hash(password)
        result = self._repo.create(email=email, password_hash=password_hash, username=username or "")
        return RegisterResult(id=result.id, email=result.email)

    def login(self, email: str, password: str) -> LoginResult:
        """登录：校验邮箱存在、未封禁、密码正确后签发 token。"""
        user = self._repo.find_by_email(email)
        if user is None:
            raise UserNotFoundError(email)
        if user.status == "banned":
            raise UserBannedError(email)
        if not self._hasher.verify(password, user.password_hash):
            raise InvalidPasswordError()
        token, expires_in = self._token_creator.create(user.id, user.role)
        return LoginResult(access_token=token, token_type="bearer", expires_in=expires_in)


class RegisterResult:
    def __init__(self, id: UUID, email: str):
        self.id = id
        self.email = email


class LoginResult:
    def __init__(self, access_token: str, token_type: str, expires_in: int):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in


class EmailAlreadyExistsError(ValueError):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"邮箱已存在: {email}")


class UserNotFoundError(ValueError):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"用户不存在: {email}")


class UserBannedError(ValueError):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"账号已封禁: {email}")


class InvalidPasswordError(ValueError):
    def __init__(self):
        super().__init__("密码错误")
