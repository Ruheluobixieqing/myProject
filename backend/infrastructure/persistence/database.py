"""数据库引擎与会话。"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from infrastructure.config import settings

engine = create_engine(
    settings.DATABASE_URL,         # 数据库连接字符串，从配置读取
    pool_pre_ping=True,            # 连接池“预检”机制
    echo=True,                     # 开发环境可改为 True 打印 SQL；生产环境建议关闭以提高性能
)

SessionLocal = sessionmaker(
    autocommit=False,              # 自动 / 手动控制事务提交
    autoflush=False,               # 自动 / 手动控制 flush 时机，FastAPI 官方推荐在需要查询最新数据时手动 db.flush()
    bind=engine                    # 绑定引擎
)

# ORM 基类，所有 ORM 模型都继承它
Base = declarative_base()


def get_db():
    """依赖注入用：每次请求一个会话，用完关闭。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        
        db.close()
