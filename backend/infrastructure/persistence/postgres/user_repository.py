"""用户仓储实现：依赖 ORM 与 Session，实现领域层 IUserRepository。"""
from uuid import UUID
from sqlalchemy.orm import Session

from domain.user.repository import IUserRepository, UserCreateResult, LoginUserResult
from infrastructure.persistence.postgres.models import UserModel, UserRole, UserStatus


# 具体实现
class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self._db = db

    def exists_by_email(self, email: str) -> bool:
        return self._db.query(UserModel).filter(UserModel.email == email).first() is not None

    def find_by_email(self, email: str) -> LoginUserResult | None:
        user = self._db.query(UserModel).filter(UserModel.email == email).first()
        if user is None:
            return None
        return LoginUserResult(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role,
            status=user.status,
        )

    def create(self, email: str, password_hash: str, username: str = "") -> UserCreateResult:
        user = UserModel(
            email=email,
            username=username,
            password_hash=password_hash,
            role=UserRole.USER,
            status=UserStatus.ACTIVE,
        )
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return UserCreateResult(id=user.id, email=user.email)
