# 2.配置用户+会话id唯一键
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
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

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory #存入内存中的
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
#引入langchain针对会话配置：
from langchain_core.runnables import ConfigurableFieldSpec

prompt=ChatPromptTemplate.from_messages(
    [
        ('system','You\'re an assistant who\'s good at {ability}. Respond in 20 words or fewer'),
        MessagesPlaceholder(variable_name="history"),
        ('human','{input1}')
    ]
)
runnable=prompt | llm
store={}

def get_session_history(user_id:str,conversation_id:str)->BaseChatMessageHistory:
    if (user_id,conversation_id) not in store:
        store[(user_id,conversation_id)]=ChatMessageHistory()
    return store[(user_id,conversation_id)]

with_message_history=RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input1",
    history_messages_key="history",
    history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="User ID",
            description="用户唯一标识",
            default="",
            is_shared=True
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="对话的唯一标识符",
            default="",
            is_shared=True
        )
        #扩展几个参数此处加几个ConfigurableFieldSpec
    ]
)

response=with_message_history.invoke(
    input={"ability":"math","input1":"余弦是什么意思？"},
    config={"configurable":{"user_id":"123","conversation_id":"1"}}
)
print(response)

response=with_message_history.invoke(
    input={"ability":"math","input1":"什么？"},
    config={"configurable":{"user_id":"123","conversation_id":"1"}}
)
print(response)

response=with_message_history.invoke(
    input={"ability":"math","input1":"什么？"},
    config={"configurable":{"user_id":"456","conversation_id":"1"}}
)
print(response)