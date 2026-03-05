"""用户仓储接口：定义在领域层，由基础设施层实现。"""
from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

# 抽象方法是一种强制契约规则，它定义必须做什么，但不定义怎么做

# 抽象接口
class IUserRepository(ABC):
    @abstractmethod            # 抽象方法，子类必须实现
    def exists_by_email(self, email: str) -> bool:
        """按邮箱判断用户是否已存在。"""
        pass

    @abstractmethod
    def create(self, email: str, password_hash: str, username: str = "") -> "UserCreateResult":
        """创建用户，返回 id 与 email。"""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional["LoginUserResult"]:
        """按邮箱查找用户，用于登录；不存在返回 None。"""
        pass

    @abstractmethod
    def find_by_id(self, user_id: "UUID") -> Optional["CurrentUserResult"]:
        """按 id 查找用户，用于鉴权；不存在返回 None。"""
        pass


# 跨层数据传输
class UserCreateResult:
    """创建用户后的返回值，仅包含必要字段。"""
    def __init__(self, id: UUID, email: str):
        self.id = id
        self.email = email


class LoginUserResult:
    """登录时按邮箱查出的用户信息（不含明文密码）。"""
    def __init__(self, id: UUID, email: str, password_hash: str, role: str, status: str):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.status = status


class CurrentUserResult:
    """鉴权用：当前登录用户信息（不含密码）。"""
    def __init__(self, id: UUID, email: str, role: str, status: str):
        self.id = id
        self.email = email
        self.role = role
        self.status = status
