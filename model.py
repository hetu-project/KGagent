from pydantic import BaseModel



class IntentType(str, Enum):
    """意图类型枚举"""
    CODE_REVIEW = "code_review"    # 代码审核
    CHITCHAT = "chitchat"          # 闲聊
    QUESTION = "question"          # 技术问题
    OTHER = "other"                # 其他意图

class IntendCheck(BaseModel):
    intent: IntentType  # 使用枚举类型字段
    confidence: float   # 可添加置信度评分
    details: str | None = None  # 可选的细节说明


class CodePreferences(BaseModel):
    style_check: bool = Field(..., description="是否进行代码风格检查")
    security_check: bool = Field(..., description="是否进行安全性检查")
    performance_check: bool = Field(..., description="是否进行性能检查")


intend_model_dict = {"code_review": CodePreferences}