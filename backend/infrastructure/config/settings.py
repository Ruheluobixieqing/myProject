from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """读取应用配置"""

    # 从根目录的 .env 中读取环境变量
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    # 数据库配置
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/myproject"

    # 鉴权相关，暂时保留
    # SECRET_KEY: str = ""
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()
