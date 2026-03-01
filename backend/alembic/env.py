"""Alembic 运行环境：从 settings 读 DATABASE_URL，用 Base.metadata 做迁移。"""
import sys
from pathlib import Path

# 保证从 backend 目录运行时能导入 infrastructure
backend_dir = Path(__file__).resolve().parent.parent        # 获取 backend 目录
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy.pool import NullPool
from alembic import context
from infrastructure.config import settings              # 数据库 URL 来源
from infrastructure.persistence.database import Base    # 声明基类
from infrastructure.persistence.postgres import models  # noqa: F401  # 让 Base.metadata 包含 UserModel

config = context.config
if config.config_file_name is not None:           # 如果配置文件存在，则读取配置文件
    fileConfig(config.config_file_name)           # 加载 alembic.ini 的日志配置

# 使用项目配置的数据库 URL，不写死在 alembic.ini
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)    # 动态设置数据库 URL

# 目标元数据
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """离线模式：只生成 SQL，不连库，不执行。"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,                          # 将参数渲染为字面量
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()                     # 执行迁移


def run_migrations_online() -> None:
    """在线模式：连接数据库执行迁移。"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),  
        prefix="sqlalchemy.",
        poolclass=NullPool,                                     # 禁用连接池，迁移脚本执行完立即释放连接
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
