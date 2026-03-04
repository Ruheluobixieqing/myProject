# FastAPI 项目标准启动文件 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # CORS，Cross-Origin Resource Sharing 跨域资源共享

from infrastructure.persistence.database import get_db

app = FastAPI(title="MyProject API", version="0.1.0")

# CORS，浏览器安全机制，禁止页面向不同源的服务器发送请求，除非服务器显式允许
# CORS 中间件配置
app.add_middleware(
    CORSMiddleware,                   # 添加 CORS 中间件
    allow_origins=["*"],              # 允许所有来源
    allow_credentials=True,           # 允许携带 Cookie/Authorization 头
    allow_methods=["*"],              # 允许所有 HTTP 方法
    allow_headers=["*"],              # 允许所有请求头
)

@app.get("/health")
def health():
    """健康检查，便于部署与排查。"""
    # 生产级健康检查应该包括：数据库连接、Redis、外部服务连通性等
    return {"status": "ok"}

from api.v1 import api_router

app.include_router(api_router)
