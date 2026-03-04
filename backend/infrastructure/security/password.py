"""密码哈希：放在基础设施层，使用 passlib。"""
from passlib.context import CryptContext

_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


class PasswordHasher:
    def hash(self, plain: str) -> str:
        return _context.hash(plain)

    def verify(self, plain: str, hashed: str) -> bool:
        return _context.verify(plain, hashed)
