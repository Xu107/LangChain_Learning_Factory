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

from langchain.output_parsers import YamlOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field

#定义数据结构
class Joke(BaseModel):
    setup:str=Field(description="设置笑话的问题")
    punchline:str=Field(description="解答笑话的答案")
joke_query="告诉我一个笑话"
parser=YamlOutputParser(pydantic_object=Joke)
prompt=PromptTemplate(
    template="回答问题的查询。\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions":parser.get_format_instructions()}
)
chain=prompt | llm
print(parser.get_format_instructions())
response=chain.invoke({"query":joke_query})
print(response.content)
