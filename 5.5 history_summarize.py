# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_core.runnables import RunnablePassthrough
#
# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# load_dotenv(override=True)
# llm=ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
#     api_key=os.getenv("OPENAI_API_KEY"),  # if you prefer to pass api key in directly instaed of using env vars
#     base_url=os.getenv("BASE_URL"),
#     # organization="...",
#     # other params...
# )
#
# temp_chat_history=ChatMessageHistory()
# temp_chat_history.add_ai_message("你好")
# temp_chat_history.add_user_message("我叫Jack，你好")
# temp_chat_history.add_ai_message("你今天心情怎么样")
# temp_chat_history.add_user_message("我今天挺开心的")
# temp_chat_history.add_ai_message("你今天下午在做什么")
# temp_chat_history.add_user_message("我今天下午在打篮球")
# print(temp_chat_history.messages)
#
# prompt=ChatPromptTemplate.from_messages(
#     [
#         (
#             'system',
#             '你是一个AI助手'
#         ),
#         MessagesPlaceholder(variable_name="chat_history"),
#         (
#             'human',
#             '{input1}'
#         )
#     ]
# )
#
# runnable=prompt | llm
# chain_with_message_history=RunnableWithMessageHistory(
#     runnable,
#     lambda session_id:temp_chat_history, #get_session_history: GetSessionHistoryCallable,
#     input_messages_key="input1",
#     history_message_key="chat_history"
# )
#
# def summarize_messages(chain_input):
#     stored_messages=temp_chat_history.messages
#     if len(stored_messages)==0:
#         return False
#     summarization_prompt=ChatPromptTemplate.from_messages(
#         [
#             MessagesPlaceholder(variable_name="chat_history"),
#             (
#                 'user',
#                 "将上述聊天消息浓缩成一条摘要消息，尽可能包含多个具体细节"
#             )
#         ]
#     )
#     summarization_chain=summarization_prompt | llm
#     summarry_message=summarization_chain.invoke({"chat_history":stored_messages})
#     temp_chat_history.clear()
#     temp_chat_history.add_message(summarry_message)
#     return True
#
# chain_with_summarization=(
#     RunnablePassthrough.assign(messages_summarized=summarize_messages)
#     | chain_with_message_history
# )
# response=chain_with_summarization.invoke(
#     input={"input1":"名字，下午在干嘛，心情"},
#     config={"configurable":{"session_id":"unused"}}
# )
# print(response.content)
# print(temp_chat_history.messages)
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(override=True)
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL"),
)

temp_chat_history = ChatMessageHistory()
temp_chat_history.add_ai_message("你好")
temp_chat_history.add_user_message("我叫Jack，你好")
temp_chat_history.add_ai_message("你今天心情怎么样")
temp_chat_history.add_user_message("我今天挺开心的")
temp_chat_history.add_ai_message("你今天下午在做什么")
temp_chat_history.add_user_message("我今天下午在打篮球")
print(temp_chat_history.messages)

# ChatPromptTemplate setup
prompt = ChatPromptTemplate.from_messages(
    [
        ('system', '你是一个AI助手'),
        MessagesPlaceholder(variable_name="chat_history"),
        ('human', '{input1}')
    ]
)

runnable = prompt | llm
chain_with_message_history = RunnableWithMessageHistory(
    runnable,
    lambda session_id: temp_chat_history,  # get_session_history: GetSessionHistoryCallable
    input_messages_key="input1",
    history_messages_key="chat_history"
)


# Function to summarize the messages
def summarize_messages(chain_input):
    stored_messages = temp_chat_history.messages
    if len(stored_messages) == 0:
        return False

    # Create a prompt to summarize the chat history
    summarization_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            ('user', "将上述聊天消息浓缩成一条摘要消息，尽可能包含多个具体细节")
        ]
    )

    # Create the summarization chain
    summarization_chain = summarization_prompt | llm

    # Invoke the summarization chain
    summary_message = summarization_chain.invoke({"chat_history": stored_messages})

    # Clear the stored messages and add the summary
    temp_chat_history.clear()
    temp_chat_history.add_message(summary_message)
    return True


# Assign the summarization to the chain
chain_with_summarization = (
        RunnablePassthrough.assign(messages_summarized=summarize_messages)
        | chain_with_message_history
)

# Ensure that `chat_history` is passed to the template
response = chain_with_summarization.invoke(
    input={"input1": "名字，下午在干嘛，心情"},
    config={"configurable": {"session_id": "unused"}}
)

# Print the response and updated chat history
print(response.content)
print(temp_chat_history.messages)
