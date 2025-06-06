# 1.聊天对话的ChatPromptTemplate，支持多种角色如：'human', 'user', 'ai', 'assistant', or 'system', HumanMessage, AIMessage
#导入langchain提示词模板库
from langchain_core.prompts import ChatPromptTemplate

#'human', 'user', 'ai', 'assistant', or 'system'
# SystemMessage, HumanMessage, AIMessage
# [SystemMessage(content='你是一个AI助手，你的名字是Bob', additional_kwargs={}, response_metadata={}), HumanMessage(content='你好', additional_kwargs={}, response_metadata={}), AIMessage(content='我很好，谢谢', additional_kwargs={}, response_metadata={}), HumanMessage(content='你的名字叫什么?', additional_kwargs={}, response_metadata={})]

chat_template=ChatPromptTemplate.from_messages(
    [
        ("system","你是一个AI助手，你的名字是{name}"),
        ("user","你好"),
        ("assistant","我很好，谢谢"),
        ("human","{user_input}"),
    ]
)

messages=chat_template.format_messages(name="Bob",user_input="你的名字叫什么?")
print(messages)

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

# result=llm.invoke(messages)
# print(result)

# 2.简单的template，不需要对话形式的，仅仅是一个str：
from langchain.prompts import PromptTemplate
prompt_template=PromptTemplate.from_template(
    "给我讲一个关于{content}的{adjective}笑话。"
)
prompt_messages=prompt_template.format(adjective="冷",content="猴子")
print(prompt_messages)
# print(llm.invoke(prompt_messages))

# 3.直接传入类
# [SystemMessage(content='你是一个中文到英文的AI翻译助手', additional_kwargs={}, response_metadata={}), HumanMessage(content='我不喜欢吃东西', additional_kwargs={}, response_metadata={})]
from langchain.prompts import HumanMessagePromptTemplate,ChatPromptTemplate
from langchain_core.messages import SystemMessage
chat_template=ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="你是一个中文到英文的AI翻译助手"
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)

messages=chat_template.format_messages(text="我不喜欢吃东西")
print(messages)

# 4.在特定位置插入消息列表（占位符/用户传入一个消息列表，将其插入到特定位置）
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import HumanMessage
prompt_template=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant."),
        MessagesPlaceholder("msgs") #存了一份聊天记录，类似于事先传给ai要咨询的商品信息等
    ]
)
prompt_template.invoke({"msgs":[HumanMessage(content="hi!"),HumanMessage(content="Hello!")]})
print(prompt_template)

# 5.Fewshot
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts import PromptTemplate

examples=[
    {
        "question":"你好",
        "answer":"Hello"
    },
    {
        "question":"谢谢",
        "answer":"Thanks"
    },
    {
        "question":"华盛顿的父亲是谁？",
        "answer":"乔治·华盛顿的父亲奥古斯丁·华盛顿和母亲玛丽·鲍尔·华盛顿都是英格兰人"
    },
]
example_prompt=PromptTemplate(input_variable=["question","answer"],template="输入：{question}\\n 输出：{answer}")
#input_variables=['answer', 'question'] input_types={} partial_variables={} template='问题:{question}\\n{answer}'
print(example_prompt)
prompt=FewShotPromptTemplate(
    examples=examples,#定义示例
    example_prompt=example_prompt,#定义格式，参数占位
    suffix="输入：{user_input}",
    input_variables=["user_input"]
)
print(prompt.format(user_input="你是谁？"))

"""

# 6.当Fewshot太多时，通过相似度挑选与问题相似的示例进行fewshot
# 收费

from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

examples_selector=SemanticSimilarityExampleSelector.from_examples(
    #可供选择的示例列表
    examples,
    #用于生成嵌入的嵌入类，该嵌入用于衡量语义相似性
    OpenAIEmbeddings(),
    #用于存储嵌入和执行相似性搜索的VectorStore类
    Chroma,
    #要生成的示例数目
    k=1
)

question="乔治·华盛顿的母亲是谁？"
selected_examples=examples_selector.select_examples({"question":question})
print(f"最相似的示例：{question}")

"""