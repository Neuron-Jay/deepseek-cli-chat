import os
from openai import OpenAI

# --- 配置区域 ---
# 方法1：直接在代码中设置（适合快速测试，请注意不要上传到公开仓库）
# api_key = "你的_API_密钥"

# 方法2：通过环境变量设置（更安全，推荐）
# 你可以在运行前通过命令设置：export DEEPSEEK_API_KEY="你的_API_密钥"
api_key = os.environ.get("DEEPSEEK_API_KEY")

if not api_key:
    print("错误：未找到 API Key，请正确设置环境变量或在代码中填写。")
    exit()

# --- 初始化客户端 ---
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# --- 发送对话请求 ---
print("🤖 正在向 DeepSeek 提问...")
try:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个乐于助人的Python编程助手。"},
            {"role": "user", "content": "请用Python写一个判断闰年的函数，并解释其逻辑。"}
        ],
        temperature=0.3,
        max_tokens=300
    )

    print("\n✨ 回复内容：\n")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"\n❌ 请求发生错误: {e}")