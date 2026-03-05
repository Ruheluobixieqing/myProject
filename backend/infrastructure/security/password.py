"""密码哈希：使用 bcrypt，不经过 passlib，避免 passlib 自检触发的 72 字节限制报错。"""
import bcrypt

# bcrypt 算法限制：只使用密码的前 72 字节（UTF-8）
_MAX_PASSWORD_BYTES = 72


def _to_bytes(plain: str) -> bytes:
    return plain.encode("utf-8")[:_MAX_PASSWORD_BYTES]


class PasswordHasher:
    def hash(self, plain: str) -> str:
        data = _to_bytes(plain)
        return bcrypt.hashpw(data, bcrypt.gensalt(rounds=12)).decode("utf-8")

    def verify(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(_to_bytes(plain), hashed.encode("utf-8"))
