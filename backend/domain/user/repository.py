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


# 跨层数据传输
class UserCreateResult:
    """创建用户后的返回值，仅包含必要字段。"""
    def __init__(self, id: UUID, email: str):
        self.id = id
        self.email = email
