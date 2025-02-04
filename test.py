from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
# 直接从 langgraph 内部引入 OpenAI 模型（避免直接引用 langchain）
from langchain_openai import ChatOpenAI
# 使用 langgraph 内部的工具装饰器（不依赖 langchain_core）


from config import *
from model import *
from database import *
from agent import *
from codereview import *


# 初始化 OpenAI 模型（这里使用 LangGraph 内置的 ChatOpenAI，内部已支持 bind_tools 接口）
model = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=OPENAI_KEY)

# 初始化内存检查点，用于保存 agent 的状态
checkpointer = MemorySaver()

# 注册工具并创建 LangGraph 应用（React Agent）
tools = [style_check, security_check, performance_check]
app = create_react_agent(model, tools=tools, checkpointer=checkpointer)


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