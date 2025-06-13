from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. 构造文本
docs = [
    "LangChain 是一个开源大模型应用框架。",
    "FAISS 可以高效做向量相似性检索。",
    "BGE 模型在中文检索上效果很强。"
]

splitter = RecursiveCharacterTextSplitter(chunk_size=20, chunk_overlap=5)
docs = splitter.create_documents(docs)

# 2. 向量化
model_name = "./all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
vectorstore = FAISS.from_documents(docs, embeddings)

# 3. 保存到本地
vectorstore.save_local("my_faiss_index")

# 4. 读取本地
loaded_vectorstore = FAISS.load_local(
    "my_faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# 5. 相似性搜索
query = "LangChain 是什么？"
results = loaded_vectorstore.similarity_search(query, k=2)
for i, r in enumerate(results):
    print(f"Top {i+1}: {r.page_content}")
