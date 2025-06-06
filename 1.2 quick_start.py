# 1.快速开始
import os
from dotenv import load_dotenv
load_dotenv(override=True)

#引入langchain聊天场景的提示词模板
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm=ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("OPENAI_API_KEY"),  # if you prefer to pass api key in directly instaed of using env vars
    base_url=os.getenv("BASE_URL"),
    # organization="...",
    # other params...
)

prompt=ChatPromptTemplate.from_messages(
[
    {"role": "system", "content": "You are a helpful assistant that translates English to Chinese."},
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "你好，你好吗？"},
    {"role": "user", "content": "{input}"},
]
)
# 与如下形式等价：
# prompt=ChatPromptTemplate.from_messages(
#     [
#         ("system","你是世界级翻译专家"),
#         ("user","{input}")
#     ]
# )

chain=prompt | llm
result=chain.invoke({"input":"请翻译如下例句：I love China."})
# 等价于；可以json传入也可以键值对传入
# result=chain.invoke(input="请翻译如下例句：I love China.")
print(result)

# 2.string后处理格式输出
from langchain_core.output_parsers import StrOutputParser
str_output_parser=StrOutputParser()
str_chain=prompt | llm | str_output_parser
result=str_chain.invoke({"input":"请翻译如下例句：I love China."})
print(result)

# 3.json后处理格式输出
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser

prompt=PromptTemplate.from_template(
    "请将以下内容翻译成中文并以Json形式返回：{text}"
)
json_parser=JsonOutputParser()
llm=ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("OPENAI_API_KEY"),  # if you prefer to pass api key in directly instaed of using env vars
    base_url=os.getenv("BASE_URL"),
    # organization="...",
    # other params...
)
no_json_chain=prompt | llm
no_json_result=no_json_chain.invoke({"text": "Hello, how are you?"})
print(no_json_result)
json_chain=no_json_chain | json_parser
json_result=json_chain.invoke({"text": "Hello, how are you?"})
print(json_result)

