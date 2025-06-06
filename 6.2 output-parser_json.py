from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel,Field

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

#自定义数据结构
class Joke(BaseModel):
    setup : str=Field(description="设置笑话的问题")
    punchline : str=Field(description="解决笑话的答案")

#提示LLM填充数据结构的查询意图
joke_query="告诉我一个笑话"
#设置解析器+将指令注入模板
parser=JsonOutputParser(pydantic_object=Joke)#JsonOutputParser()
prompt=PromptTemplate(
    template="回答问题的查询。\n{format_instructions}\n{query}\n",
    input_variables=["query"],#动态参数
    partial_variables={"format_instructions":parser.get_format_instructions()}#静态参数
)
print(parser.get_format_instructions())
chain=prompt | llm | parser

response=chain.invoke({"query":joke_query})
print(response)
# 流式调用
# for s in chain.stream({"query":joke_query}):
#     print(s)

