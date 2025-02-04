from langchain_core.tools import tool

# 定义代理工具（示例工具，你可以替换成实际逻辑）
@tool
def style_check(code: str):
    """检查代码风格"""
    # 这里可以集成 flake8 等工具检查代码风格
    return "代码风格评分：85/100"

@tool
def security_check(code: str):
    """检查代码安全性"""
    # 这里可以集成 Bandit 等工具检查代码安全性
    return "安全性评分：90/100"

@tool
def performance_check(code: str):
    """检查代码性能"""
    # 这里可以集成 Pyinstrument 等工具检查代码性能
    return "性能评分：80/100"

# 定义工具映射（此处仅作示例，目前 LangGraph 内部会管理工具调用）
AGENT_TOOLS = {
    "style_agent": style_check,
    "security_agent": security_check,
    "performance_agent": performance_check,
    "default_agent": lambda code: "默认审查：无问题",
}