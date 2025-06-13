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

# 1.创建第一个工具retriever_tool
from langchain_huggingface import HuggingFaceEmbeddings

model_name = "./all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings=HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
import os
os.environ["USER_AGENT"]="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36"
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
loader=WebBaseLoader(
    "https://www.ibm.com/cn-zh/think/topics/langchain",
)
docs=loader.load()
documents=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
).split_documents(docs)

vector=FAISS.from_documents(documents,embeddings)
retriever=vector.as_retriever()

retriever_tool=create_retriever_tool(
    retriever,
    name="vectorstore_retriever",
    description="A tool that can search documents based on semantic similarity."
)

# 2.创建第二个工具search_tool(基于前面的Tavily)
import os
os.environ['TAVILY_API_KEY']="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"

from langchain_community.tools.tavily_search import TavilySearchResults
search_tool=TavilySearchResults(max_results=1)

tools=[search_tool,retriever_tool]
# 3.Agent

from langchain import hub #langchain提示词仓库,不用自己写提示词
#使用现成的提示词模板
prompt=hub.pull("hwchase17/openai-functions-agent")
print(prompt.messages)

from langchain.agents import create_tool_calling_agent
agent=create_tool_calling_agent(llm,tools,prompt)

from langchain.agents import AgentExecutor
agent_executor=AgentExecutor(agent=agent,tools=tools)

print(agent_executor.invoke({"input":"你好"}))
print(agent_executor.invoke({"input":"langchain是什么?"}))

