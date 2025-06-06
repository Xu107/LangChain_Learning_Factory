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

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import XMLOutputParser
actor_query="生成周星驰的电影作品列表，按照最新的时间降序"
parser=XMLOutputParser()
prompt=PromptTemplate(
    template="回答用户的查询.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions":parser.get_format_instructions()}
)
print("parser.get_format_instructions():",parser.get_format_instructions())
chain=prompt | llm
response=chain.invoke({"query":actor_query})
xml_output=parser.parse(response.content)
print("response.content:",response.content)
print("xml_output:",xml_output)

#添加一些标签以根据特定需求定制输出，添加自定义风格
parser=XMLOutputParser(tags=["movies","actor","film","name","genre"])
print("specific parser.get_format_instructions():", parser.get_format_instructions())
prompt=PromptTemplate(
    template="回答用户的查询。\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions":parser.get_format_instructions()}
)
chain = prompt | llm
response=chain.invoke({"query":actor_query})
xml_output=parser.parse(response.content)
print("response.content:",response.content)
print("xml_output:",xml_output)

#流式调用
chain=prompt | llm | parser
for s in chain.stream({"query":actor_query}):
    print(s)



