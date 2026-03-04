"""认证相关请求/响应模型。"""
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="邮箱，必填且需要校验唯一性")
    password: str = Field(..., min_length=5, description="密码，至少 5 位")
    username: str | None = Field(None, max_length=255, description="用户名，可选，可重复")


class RegisterResponse(BaseModel):
    id: str = Field(..., description="用户 id")
    email: str = Field(..., description="邮箱")

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="邮箱")
    password: str = Field(..., description="密码")


class LoginResponse(BaseModel):
    access_token: str = Field(..., description="JWT")
    token_type: str = Field(default="bearer", description="类型")
    expires_in: int = Field(..., description="有效秒数")
