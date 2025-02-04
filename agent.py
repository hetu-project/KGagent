from graphdatabase import *
from config import *
from model import *

def classify_task(query: str) -> IntendCheck:
    """
    使用 LLM 判断任务类型。
    示例提示：
    “请判断下面任务描述的类型。任务描述：‘{query}’，请输出一个 JSON 对象，包含字段：
       - intent：任务类型，必须是 'code_review', 'chitchat', 'question' 或 'other' 之一，
       - confidence：置信度（0-1），
       - details：可选的说明。”
    输出结果直接解析为 IntendCheck 对象。
    """
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract the user intent from the following description. "
                    "Output must be valid JSON strictly following the format with keys: "
                    "'intent' (one of: 'code_review', 'chitchat', 'question', 'other'), "
                    "'confidence' (a float between 0 and 1), and optionally 'details'."
                )
            },
            {
                "role": "user",
                "content": query
            },
        ],
        response_format=IntendCheck,
    )
    intend_result = completion.choices[0].message.parsed
    print("Extracted Intent Check:")
    print(intend_result)
    return intend_result


def additioncal_extract(intend:str, query: str) -> str:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract the code review preferences from the following description. "
                        "Output must be valid JSON strictly following the format with keys: "
                        "'style_check', 'security_check', and 'performance_check'."
                    )
                },
                {
                    "role": "user",
                    "content": query
                },
            ],
            response_format=CodePreferences,
        )
    preferences = completion.choices[0].message.parsed

    print("Extracted Code Preferences:")
    print(preferences)
