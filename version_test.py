from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# response_1 = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "system", "content": "你是一个准确的信息提供者。"},
#         {"role": "user", "content": "你是谁？你的具体模型名称、版本号是什么？你的知识库截止到什么时候？"}
#     ],
#     temperature=0,
#     stream=False
# )
#
# print("模型身份信息:", response_1.choices[0].message.content)
# print("响应头中的模型名称:", response_1.model)


response_2 = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who is the current president of the United States? Just give the name."}
    ],
    # 关键！尝试指定一个具体的时间点版本
    extra_body={
        "date": "2025-12-01"
    },
    temperature=0,
    stream=False
)

print(response_2.choices[0].message.content)