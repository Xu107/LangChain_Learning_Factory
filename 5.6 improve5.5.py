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

# 初始化聊天历史
temp_chat_history = ChatMessageHistory()
temp_chat_history.add_ai_message("你好")
temp_chat_history.add_user_message("我叫Jack，你好")
temp_chat_history.add_ai_message("你今天心情怎么样")
temp_chat_history.add_user_message("我今天挺开心的")
temp_chat_history.add_ai_message("你今天下午在做什么")
temp_chat_history.add_user_message("我今天下午在打篮球")
print("原始聊天历史：")
print(temp_chat_history.messages)

# 方案1：修改总结函数，不在执行过程中修改历史记录
def summarize_messages_fixed(chain_input):
    stored_messages = temp_chat_history.messages
    if len(stored_messages) == 0:
        return chain_input

    # 创建总结提示
    summarization_prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ('user', "将上述聊天消息浓缩成一条摘要消息，尽可能包含多个具体细节")
    ])

    # 生成总结
    summarization_chain = summarization_prompt | llm
    summary_message = summarization_chain.invoke({"chat_history": stored_messages})

    # 将总结添加到输入中，而不是直接修改历史记录
    chain_input["chat_history"] = [summary_message]
    return chain_input


# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ('system', '你是一个AI助手'),
    MessagesPlaceholder(variable_name="chat_history"),
    ('human', '{input1}')
])

# 创建可运行链
runnable = prompt | llm

# 方案1的实现
print("\n=== 方案1：在链中手动处理总结 ===")
try:
    # 先进行总结
    input_data = {"input1": "名字，下午在干嘛，心情"}
    summarized_input = summarize_messages_fixed(input_data)

    # 然后调用模型
    response = runnable.invoke(summarized_input)
    print("回复：", response.content)
except Exception as e:
    print("方案1出错：", e)

print("\n=== 方案2：分离总结和对话流程 ===")

# 方案2：完全分离总结和对话流程
def create_summary_and_respond():
    stored_messages = temp_chat_history.messages

    # 1. 先创建总结
    if len(stored_messages) > 0:
        summarization_prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="chat_history"),
            ('user', "将上述聊天消息浓缩成一条摘要消息，尽可能包含多个具体细节")
        ])

        summarization_chain = summarization_prompt | llm
        summary_message = summarization_chain.invoke({"chat_history": stored_messages})
        print("生成的总结：", summary_message.content)

        # 2. 用总结替换历史记录
        temp_chat_history.clear()
        temp_chat_history.add_message(summary_message)

    # 3. 现在使用带有总结的历史记录进行对话
    chain_with_history = RunnableWithMessageHistory(
        runnable,
        lambda session_id: temp_chat_history,
        input_messages_key="input1",
        history_messages_key="chat_history"
    )

    # 4. 进行对话
    response = chain_with_history.invoke(
        {"input1": "名字，下午在干嘛，心情"},
        config={"configurable": {"session_id": "unused"}}
    )

    return response


try:
    response = create_summary_and_respond()
    print("回复：", response.content)
    print("当前历史记录：", temp_chat_history.messages)
except Exception as e:
    print("方案2出错：", e)

print("\n=== 方案3：使用条件总结（推荐） ===")


# 方案3：更智能的条件总结方案
def smart_summarize_if_needed(session_id: str, max_messages: int = 6):
    """智能总结：只有当消息数量超过阈值时才进行总结"""
    if len(temp_chat_history.messages) <= max_messages:
        return temp_chat_history

    # 需要总结时
    stored_messages = temp_chat_history.messages
    summarization_prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ('user', "将上述聊天消息浓缩成一条摘要消息，尽可能包含多个具体细节")
    ])

    summarization_chain = summarization_prompt | llm
    summary_message = summarization_chain.invoke({"chat_history": stored_messages})

    # 创建新的历史记录实例
    new_history = ChatMessageHistory()
    new_history.add_message(summary_message)

    # 可以选择保留最近的几条消息
    recent_messages = stored_messages[-2:]  # 保留最近2条消息
    for msg in recent_messages:
        new_history.add_message(msg)

    # 更新全局历史记录
    temp_chat_history.clear()
    for msg in new_history.messages:
        temp_chat_history.add_message(msg)

    return temp_chat_history


# 重新设置历史记录用于测试
temp_chat_history.clear()
temp_chat_history.add_ai_message("你好")
temp_chat_history.add_user_message("我叫Jack，你好")
temp_chat_history.add_ai_message("你今天心情怎么样")
temp_chat_history.add_user_message("我今天挺开心的")
temp_chat_history.add_ai_message("你今天下午在做什么")
temp_chat_history.add_user_message("我今天下午在打篮球")

# 创建智能总结链
smart_chain = RunnableWithMessageHistory(
    runnable,
    smart_summarize_if_needed,
    input_messages_key="input1",
    history_messages_key="chat_history"
)

try:
    response = smart_chain.invoke(
        {"input1": "名字，下午在干嘛，心情"},
        config={"configurable": {"session_id": "test"}}
    )
    print("回复：", response.content)
    print("处理后的历史记录数量：", len(temp_chat_history.messages))
    for i, msg in enumerate(temp_chat_history.messages):
        print(f"{i + 1}. {type(msg).__name__}: {msg.content[:50]}...")
except Exception as e:
    print("方案3出错：", e)