"""
DeepSeek API 多轮对话 + 流式输出 + JSON持久化
- 自动加载/保存对话历史到 conversation.json
- 支持连续对话，AI 会记住之前的内容
- 输入 'save' 手动保存并退出
- 输入 'exit' 直接退出（自动保存）
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# ==================== 第一步：加载 API Key ====================
# 1. 加载项目根目录下的 .env 文件（里面写了 DEEPSEEK_API_KEY=sk-xxx）
load_dotenv()

# 2. 从环境变量中读取 API Key
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    print("❌ 错误：未找到 API Key，请在 .env 文件中设置 DEEPSEEK_API_KEY")
    exit(1)

# ==================== 第二步：初始化 OpenAI 客户端 ====================
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# ==================== 第三步：定义历史文件路径 ====================
HISTORY_FILE = "conversation.json"

# ==================== 第四步：加载或初始化对话历史 ====================
def load_conversation():
    """从 JSON 文件读取之前的对话历史，如果文件不存在则返回一个初始化的 system 消息"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("⚠️ 历史文件损坏，将开始新对话。")
                return [{"role": "system", "content": "你是一个乐于助人的AI助手。"}]
    else:
        # 第一次运行，设定 system 人设（你可以自由修改）
        return [{"role": "system", "content": "你是一个乐于助人的AI助手。"}]

def save_conversation(conversation):
    """将当前的对话历史保存到 JSON 文件"""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(conversation, f, ensure_ascii=False, indent=2)

# 加载历史
conversation = load_conversation()
print(f"📂 已加载 {len(conversation)-1} 条历史消息（不含 system）")

# ==================== 第五步：多轮对话主循环 ====================
print("\n🤖 聊天开始！输入 'exit' 退出，输入 'save' 保存并退出，直接回车继续对话。\n")

while True:
    # 获取用户输入
    user_input = input("你：")

    # 处理退出命令
    if user_input.lower() == "exit":
        save_conversation(conversation)
        print("✅ 对话已保存到 conversation.json，再见！")
        break

    if user_input.lower() == "save":
        save_conversation(conversation)
        print("✅ 已保存当前对话历史，可以继续聊天。")
        continue

    # 将用户消息加入历史
    conversation.append({"role": "user", "content": user_input})

    # ==================== 第六步：调用 API 并流式输出 ====================
    print("AI：", end="", flush=True)

    try:
        # 发送整个对话历史给 DeepSeek，开启流式输出
        stream = client.chat.completions.create(
            model="deepseek-chat",
            messages=conversation,
            temperature=0.7,
            max_tokens=3000,      # 可根据需要调整
            stream=True
        )

        # 收集 AI 的完整回复（用于保存到历史）
        full_reply = ""

        # 逐块接收并打印
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                print(delta.content, end="", flush=True)
                full_reply += delta.content

        # 换行，并将 AI 的回复加入历史
        print()
        conversation.append({"role": "assistant", "content": full_reply})

        # 可选：自动保存每轮对话（防止中途崩溃丢失）
        # 如果你希望每轮都自动保存，可以取消下面一行的注释
        # save_conversation(conversation)

    except Exception as e:
        print(f"\n❌ 发生错误：{e}")
        # 如果出错，移除刚才加入的用户消息，避免污染历史
        conversation.pop()
        # 继续循环

# 程序结束时，历史已经通过 exit 或 save 保存