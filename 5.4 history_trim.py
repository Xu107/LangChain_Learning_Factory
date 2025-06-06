from langchain_core.runnables.history import RunnableWithMessageHistory,RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

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

temp_chat_history=ChatMessageHistory()
temp_chat_history.add_ai_message("你好")
temp_chat_history.add_user_message("我叫Jack，你好")
temp_chat_history.add_ai_message("你今天心情怎么样")
temp_chat_history.add_user_message("我今天挺开心的")
temp_chat_history.add_ai_message("你今天下午在做什么")
temp_chat_history.add_user_message("我今天下午在打篮球")
print(temp_chat_history.messages)

prompt=ChatPromptTemplate.from_messages(
    [
        (
            'system',
            '你是一个AI助手'
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        (
            'human',
            '{input1}'
        )
    ]
)

runnable= prompt | llm

def trim_messages(chain_input):
    stored_messages=temp_chat_history.messages
    if len(stored_messages)<=2:
        return False
    temp_chat_history.clear()
    for message in stored_messages[-2:]:#只保留两条历史记录
        temp_chat_history.add_message(message)
    return True


chain_with_message_history=RunnableWithMessageHistory(
    runnable,
    lambda session_id:temp_chat_history,
    input_messages_key="input1",
    history_messages_key="chat_history"
)

chain_with_triming=(
    RunnablePassthrough.assign(messages_trimmed=trim_messages)
    | chain_with_message_history
)

response=chain_with_triming.invoke(
    input={"input1":"我下午在打篮球"},   #我今天下午在干吗？    #我叫什么名字
    config={"configurable":{"session_id":"unused"}},
)
print(response.content)
#打篮球听起来很有趣！你是和朋友一起打，还是参加了什么比赛呢？
#你今天下午在打篮球。你觉得打得怎么样？
#抱歉，我无法知道你的名字。你可以告诉我你的名字吗？
print(temp_chat_history.messages)
