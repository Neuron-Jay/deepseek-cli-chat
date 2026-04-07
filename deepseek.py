"""
DeepSeek API 流式输出示例（stream=True）
逐字打印 AI 回复，像打字机效果。
"""

import os
from dotenv import load_dotenv
from openai import OpenAI


# --- 配置区域 ---
# 方法1：直接在代码中设置（适合快速测试，请注意不要上传到公开仓库）
# api_key = "你的_API_密钥"

# 方法2：通过环境变量设置（更安全，推荐）
# 你可以在运行前通过命令设置：export DEEPSEEK_API_KEY="你的_API_密钥"

# 1.加载.env文件中的变量
load_dotenv()
# 2.从环境变量中提取key
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    print("错误：未找到 API Key，请正确设置环境变量或在代码中填写。")
    exit()

# --- 初始化客户端 ---
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# ---------- 用户输入 ----------
print("🤖 正在向 DeepSeek 提问...（请关闭网络代理服务使用）")
system_prompt = input("请设定AI的人设：")
user_question = input("请输入你的问题：")

# ---------- 流式请求 ----------
print("\n🤖 AI 回复（实时逐字输出）：\n")

try:
    # 开启流式输出
    stream = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ],
        temperature=0.7,
        max_tokens=3000,      # 可根据需要调整，例如 2000
        stream=True          # 关键参数
    )

    # 逐块接收并打印
    for chunk in stream:
        # 每个 chunk 中可能包含多个 choices，通常取第一个
        delta = chunk.choices[0].delta
        if delta.content:               # 有内容才打印
            print(delta.content, end="", flush=True)

    # 打印结束后换行
    print("\n")

except Exception as e:
    print(f"\n❌ 错误：{e}")