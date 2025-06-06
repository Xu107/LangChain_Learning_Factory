from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai.chat_models import ChatOpenAI
REDIS_URL="redis://localhost:6379/0"

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
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
        (
            'system',
            "You're an assistant who's good at {ability}. Respond in 20 words or fewer"
        ),
        MessagesPlaceholder(variable_name="history"),
        ('human','{input1}')
    ]
)
runnable=prompt | llm

store={}
def get_message_history(session_id:str)->RedisChatMessageHistory:#与之前相比，只有获取消息的方式进行改变
    return RedisChatMessageHistory(session_id,url=REDIS_URL)

with_message_history=RunnableWithMessageHistory(
    runnable,
    get_message_history,
    input_messages_key="input1",
    history_messages_key="history"
)
response=with_message_history.invoke(
    input={"ability":"math","input1":"余弦是什么？"},
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
    config={"configurable":{"session_id":"abc456"}}
)
print(response)