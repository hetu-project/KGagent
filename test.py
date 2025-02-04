from config import *
from model import *
from graphdatabase import *
from agent import *
from codereview import *




def multi_agent_dispatcher(user_id: str, query: str, preferences: dict) -> str:
    """
    多代理调度器：
    1. 先根据用户请求内容利用 LLM 判断任务类型
    2. 根据判断结果路由到相应的代理处理流程
       目前示例中，如果任务类型中包含 "code" 或等于 "code_review"，则调用 code_review，
       否则调用默认代理（此处仅返回默认审查结果）
    """
    task_info = classify_task(query)  # 这里返回的是一个对象，而不是字符串
    task_type = task_info.intent  # 提取具体的意图字段
    print(f"判断任务类型： {task_info}")  # 打印整个 task_info 以便调试

    if task_type == IntentType.CODE_REVIEW:  # 这里改为直接对比 IntentType 枚举值
        return code_review(user_id, query, preferences)
    else:
        default_result = AGENT_TOOLS["default_agent"](query)
        return default_result

if __name__ == "__main__":
    user_id = "123"
    query = "def add(a, b): return a + b"  
    preferences = {
        "style_check": True,
        "security_check": False,
        "performance_check": True,
    }
    result = multi_agent_dispatcher(user_id, query, preferences)
    print("审查结果：", result)