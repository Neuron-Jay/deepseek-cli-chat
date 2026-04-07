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

# --- 发送对话请求 ---
print("🤖 正在向 DeepSeek 提问...")
try:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": input("请为DeepSeek设定你想要的人设：")},
            {"role": "user", "content": input("请输入你想要DeepSeek回答的问题：")}
        ],
        temperature=0.3,
        max_tokens=300
    )

    print("\n✨ 回复内容：\n")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"\n❌ 请求发生错误: {e}")