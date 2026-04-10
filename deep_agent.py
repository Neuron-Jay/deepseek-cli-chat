"""
DeepSeek V3.2 文本分析机器人
- 支持对.txt, .docx,.pdf文件类型的分析功能
- 目前支持的skill: summary
"""

from openai import OpenAI
import json
import os
from docx import Document
import fitz
from dotenv import load_dotenv

# ====== API KEY ======
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise ValueError("❌ 未找到 DEEPSEEK_API_KEY，请在 .env 文件中设置")

# ====== 初始化客户端 ======
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# ====== 1. 文件读取能力（核心能力）======

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def read_pdf(file_path):
    pdf = fitz.open(file_path)
    full_text = []
    for page in pdf:
        text_page = page.get_text()
        full_text.append(text_page)
    pdf.close()
    return "\n".join(full_text)

def read_file(file_path):
    if not os.path.exists(file_path):
        return "文件不存在"

    if file_path.endswith(".txt"):
        return read_txt(file_path)

    elif file_path.endswith(".docx"):
        return read_docx(file_path)

    elif file_path.endswith(".pdf"):
        return read_pdf(file_path)

    else:
        return "暂不支持该文件类型"


# ====== 2. Skill ======

# ====== summary功能 ======
def summary(text):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个专业的学术助手，请用简洁清晰的语言总结文本的核心内容"},
            {"role": "user", "content": f"请将以下文本总结为：1. 背景;2. 问题;3. 方法;4. 结果;5. 意义。\n{text}"}
        ],
        temperature = 0.7
    )
    return response.choices[0].message.content


# ====== 3. 工具注册 ======

tools = {
    "read_file": read_file,
    "summary": summary
}


# ====== 4. Agent核心 ======

def deep_agent(file_path):
    print(f"\n📂 目标文件: {file_path}")

    # Step 1: 读取文件
    content = read_file(file_path)

    if content.startswith("文件不存在") or content.startswith("暂不支持"):
        print(content)
        return

    print("\n📖 文件读取成功，长度:", len(content))

    # Step 2: 调用总结
    print("\n🧠 正在总结...\n")

    result = summary(content[:5000])  # 防止超长（先截断）

    print("📝 总结结果：\n")
    print(result)


# ====== 5. 运行 ======

if __name__ == "__main__":
    file_path = input("请输入文件路径(text_file_repository\文件名): ")
    deep_agent(file_path)
