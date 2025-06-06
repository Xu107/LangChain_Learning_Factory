# LCEL (LangChain Expression Language) Runnable: stream；invoke；batch
#调式强烈建议使用''' '''隔绝其他方法，观测不同块输出
import asyncio
import os
from dotenv import load_dotenv
load_dotenv(override=True)

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


# 1.流式调用 llm.stream()
chunks=[]
for chunk in llm.stream("天空是什么颜色？"):
    chunks.append(chunk)
    print(chunk.content,end="|",flush=True)
print(chunks)


#2.链式调用--异步调用示例1-StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
prompt=ChatPromptTemplate.from_template("请讲一个关于{topic}的笑话")
parser=StrOutputParser()
chain=prompt | llm | parser
#异步调用需要定义函数
async def async_stream(topic):
    async for chunk in chain.astream({"topic":topic}):
        print(f"[{topic}]",chunk,end="|",flush=True)#替代了chunk.content

async def main_async():
    #同时执行两个不同任务,使用asyncio.gather
    await asyncio.gather(
        async_stream('鹦鹉'),
        async_stream('小狗')
    )
asyncio.run(main_async())
    #[鹦鹉]和[小狗]的输出混杂在一起


#2.链式调用--异步调用示例2-JsonOutputParser
import asyncio
from langchain_core.output_parsers import JsonOutputParser
chain2=(
    llm | JsonOutputParser()
)

async def async_stream2():
    async for text in chain2.astream(
        "以JSON链式输出法国、西班牙和日本的国家及其人口列表"
        "使用一个带有'countries’外部键的字典，其中包含国家"
        "列表。每个国家应给有键'name'和'population'"
    ):
        print(text,flush=True)
asyncio.run(async_stream2())

#3.events事件监控过程中各个环节的输入输出等
async def async_stream3():
    events=[]
    async for event in llm.astream_events("Hello",version='v2'):
        events.append(event)
    print(events)
asyncio.run(async_stream3())
