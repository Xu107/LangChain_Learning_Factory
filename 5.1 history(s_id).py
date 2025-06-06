'''
    LangChain消息管理与聊天历史存储
        1.消息存储在内存
        2.消息持久化到redis
        3.修改聊天历史
        4.裁剪消息
        5.总结记忆
'''

# 1.消息存储在内存
# chat_history_memory.py
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import BaseChatMessageHistory

import os
from dotenv import load_dotenv
os.environ["TAVILY_API_KEY"] = "your TAVILY_API_KEY"
load_dotenv(override=True)
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
        ('system','You\'re an assistant who\'s good at {ability}. Respond in 20 words or fewer'),
        MessagesPlaceholder(variable_name="history"),#历史消息占位符
        ('human','{input1}')
    ]
)
runnable=prompt | llm

#用来存储会话历史记录
store={}

#获取会话历史函数，输入：session_id；输出：会话历史记录
def get_session_history(session_id:str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id]=ChatMessageHistory()
    return store[session_id]

# 创建一个带绘画历史记的Runnable
with_message_history=RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input1",
    history_messages_key="history"
)

response=with_message_history.invoke(
    input={"ability":"math","input1":"余弦是什么意思?"},
    config={"configurable":{"session_id":"abc123"}}
)
print(response)

response=with_message_history.invoke(
    input={"ability":"math","input1":"什么？"},
    config={"configurable":{"session_id":"abc123"}}
)
print(response)

response=with_message_history.invoke(
    input={"ability":"math","input1":"什么？"},
    config={"configurable":{"session_id":"def234"}}
)
print(response)

