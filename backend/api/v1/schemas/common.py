"""通用响应模型。"""
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """认证等接口的统一错误体，便于前端根据 code 做分支。"""
    code: str = Field(..., description="错误码，如 EMAIL_ALREADY_EXISTS")
    message: str = Field(..., description="给人看的提示")
    details: dict | None = Field(None, description="额外信息，如 email、field 等")
