"""ORM (Object-Relational Mapping，对象关系映射)模型：仅用于持久化，放在基础设施层。"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid

# 继承 SQLAlchemy 的基类，提供 ORM 功能
from infrastructure.persistence.database import Base

class UserRole:
    USER = "user"
    ADMIN = "admin"
    VISITOR = "visitor"


class UserStatus:
    ACTIVE = "active"
    BANNED = "banned"


# 表定义
# 类名 UserModel，表名 users
class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(255), unique=False, nullable=False) 
    password_hash = Column(String(255), nullable=False)
    role = Column(String(32), nullable=False, default=UserRole.USER)
    status = Column(String(32), nullable=False, default=UserStatus.ACTIVE)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
