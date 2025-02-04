from langchain_core.tools import tool
from graphdatabase import *

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

def choose_agent(preferences):
    """
    根据用户偏好选择代理（目前示例逻辑，仅用于参考）
    """
    if preferences.get("style_check"):
        return "style_agent"
    if preferences.get("security_check"):
        return "security_agent"
    if preferences.get("performance_check"):
        return "performance_agent"
    return "default_agent"


def code_review(user_id, code, preferences):
    """
    主函数：处理代码审查请求
    1. 将原始代码片段存储到 Neo4j
    2. 根据用户偏好（示例逻辑）选择代理工具（此处仅作参考，LangGraph 内部会管理工具调用）
    3. 使用 LangGraph 的 React Agent 进行审查
    4. 将审查结果存储到 Neo4j 并返回结果
    """
    # 存储原始代码
    store_code_snippet(user_id, code)

    # 根据用户偏好选择代理工具（示例，实际工作流中 LangGraph 会根据配置自动调用工具）
    chosen_agent = choose_agent(preferences)
    agent_tool = AGENT_TOOLS.get(chosen_agent, AGENT_TOOLS["default_agent"])
    # （注意：此处 agent_tool 示例并未直接参与调用，LangGraph 内部会根据工具注册和提示管理调用流程）

    # 调用 LangGraph 的 React Agent 执行审查流程
    state = app.invoke(
        {"messages": [{"role": "user", "content": code}]},
        config={"configurable": {"thread_id": user_id}},
    )

    # 假设返回消息列表中最后一条为最终回复
    review_result = state["messages"][-1].content

    # 存储审查结果到 Neo4j
    store_review(user_id, code, review_result)

    return review_result

