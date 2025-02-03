from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
# 直接从 langgraph 内部引入 OpenAI 模型（避免直接引用 langchain）
from langchain_openai import ChatOpenAI
# 使用 langgraph 内部的工具装饰器（不依赖 langchain_core）
from langchain_core.tools import tool

from config import *
from database import *

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

# 初始化 OpenAI 模型（这里使用 LangGraph 内置的 ChatOpenAI，内部已支持 bind_tools 接口）
model = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=OPENAI_KEY)

# 初始化内存检查点，用于保存 agent 的状态
checkpointer = MemorySaver()

# 注册工具并创建 LangGraph 应用（React Agent）
tools = [style_check, security_check, performance_check]
app = create_react_agent(model, tools=tools, checkpointer=checkpointer)





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



def classify_task(query: str) -> str:
    """
    使用 LLM 判断任务类型。
    这里简单地生成一个提示语，然后利用模型的预测结果作为任务类型标签。
    示例提示：
    “请判断下面任务描述的类型。任务描述：‘{query}’，请输出一个简短的标签，比如 code_review、doc_review 或 other。”
    """
    prompt = f"请判断下面任务描述的类型。任务描述：'{query}'。请输出一个简短的标签，比如 code_review, doc_review, or other。"
    task_type = model.predict(prompt)  # ChatOpenAI 通常提供 predict 方法
    return task_type.strip().lower()

def multi_agent_dispatcher(user_id: str, query: str, preferences: dict) -> str:
    """
    多代理调度器：
    1. 先根据用户请求内容利用 LLM 判断任务类型
    2. 根据判断结果路由到相应的代理处理流程
       目前示例中，如果任务类型中包含 "code" 或等于 "code_review"，则调用 code_review，
       否则调用默认代理（此处仅返回默认审查结果）
    """
    task_type = classify_task(query)
    print("判断任务类型：", task_type)
    if "code" in task_type or task_type == "code_review":
        # 调用代码审查代理
        return code_review(user_id, query, preferences)
    else:
        # 其他任务暂未实现，示例中直接调用默认代理工具
        default_result = AGENT_TOOLS["default_agent"](query)
        return default_result

# 示例调用
if __name__ == "__main__":
    user_id = "123"
    query = "def add(a, b): return a + b"  # 或者直接使用变量 code，保持一致
    preferences = {
        "style_check": True,
        "security_check": False,
        "performance_check": True,
    }
    result = multi_agent_dispatcher(user_id, query, preferences)
    print("审查结果：", result)