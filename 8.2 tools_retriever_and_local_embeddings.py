# pip install huggingface_hub
# pip install sentence-transformers
# pip install -U langchain-huggingface
# pip install faiss-gpu  注意:windows不支持;使用以下cpu版本
# pip install faiss-cpu
# huggingface-cli download sentence-transformers/all-mpnet-base-v2 --local-dir ./all-mpnet-base-v2
# 使用开源的Embeddings代替OpenAIEmbeddings实现向量数据库检索与RAG,langchain有与huggingface深度合作的包,不需要自己进行重写
from langchain_huggingface import HuggingFaceEmbeddings

# https://huggingface.co/sentence-transformers/all-mpnet-base-v2
# https://api.python.langchain.com/en/latest/embeddings/langchain_huggingface.embeddings.huggingface.HuggingFaceEmbeddings.html
model_name = "./all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
mpnet_embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

import os
os.environ["USER_AGENT"]="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36"
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings  付费,遗弃;使用开源免费版本地安装的'sentence-transformers/all-mpnet-base-v2'
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader=WebBaseLoader(
    "https://www.ibm.com/cn-zh/think/topics/langchain",
)
docs=loader.load()
# for i, doc in enumerate(docs):
#     print(f"Document {i+1}:")
#     print(doc.page_content[:200])  # 只打印前200个字符
#     print(f"Metadata: {doc.metadata}")
documents=RecursiveCharacterTextSplitter(
    chunk_size=1000,#每个文档块最大字符数
    chunk_overlap=200
    #第一块包含字符1到1000,第二块包含字符801-1800,第三块包含字符1601-2600
).split_documents(docs)

#将网页文本转化为向量并存储(内存中)
vector=FAISS.from_documents(documents,mpnet_embeddings)
retriever=vector.as_retriever()

print(retriever.invoke("langchain")[0])

#封装成agent可以调用的tool
from langchain.tools.retriever import create_retriever_tool
retriever_tool=create_retriever_tool(
    retriever,
    name="vectorstore_retriever",
    description="A tool that can search documents based on semantic similarity."
)

