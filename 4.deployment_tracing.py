'''
    LangChain服务部署与链路监控
        1.LangServe服务部署 （REST API）
        2.LangSmith Tracing（跟踪）
        3.Verbose（详细日志打印）
        4.Debug（调试日志打印）
'''

#1.LangServe（未成功，可跳过）
#pip install --upgrade "langserve[all]"
#使用LangChain CLI快速启动LangServe  pip install -U langchain-cli
#cmd输入 langchain app new "项目名(此处my-app)"
#使用poetry管理依赖(类似于java maven)
# (1)pip install pipx
# (2)pipx ensurepath
# (3)pipx install poetry
# (4)poetry add langchain
# (5)poetry add langchain-openai
# 配置api key环境变量
# poetry run langchain serve --port=8000

#有问题 跳过

# 2.LangSmith→只需要配置环境即可，使用langchain做应用开发时自动调用
# https://smith.langchain.com/
'''
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
os.environ["TAVILY_API_KEY"] = "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"
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
tools=[TavilySearchResults(max_results=1,tavily_api_key=os.getenv("TAVILY_API_KEY"))]
prompt=ChatPromptTemplate.from_messages(
    [
        ('system','你是一位AI助手'),
        ('placeholder',"{chat_history}"),
        ('human','{input}'),
        ('placeholder','{agent_scratchpad}')
    ]
)

agent=create_tool_calling_agent(llm,tools,prompt)
agent_executor=AgentExecutor(agent=agent,tools=tools)
response=agent_executor.invoke(
    {"input":"谁指导了2023年的电影《奥本海默》，他多少岁了？"}
)
print(response)
'''
# 3.详细中间重要结果日志verbos→通过langchain.globals控制
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor,create_tool_calling_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain.globals import set_verbose,set_debug

import os
from dotenv import load_dotenv
os.environ["TAVILY_API_KEY"] = "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"
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
tools=[TavilySearchResults(max_results=1,tavily_api_key=os.getenv("TAVILY_API_KEY"))]
prompt=ChatPromptTemplate.from_messages(
    [
        ('system','你是一位AI助手'),
        ('placeholder','{chat_history}'),
        ('human','{input}'),
        ('placeholder','{agent_scratchpad}')
    ]
)
agent=create_tool_calling_agent(llm,tools,prompt)
set_verbose(True)
# set_debug(True)
agent_executor=AgentExecutor(agent=agent,tools=tools)
response=agent_executor.invoke({"input":"谁指导了2023年的电影《奥本海默》，他多少岁了？"})
print(response)

# 4.详细中间结果日志verbos→通过langchain.globals控制
from langchain.globals import set_verbose,set_debug
#set_verbose(True)→set_debug(True)