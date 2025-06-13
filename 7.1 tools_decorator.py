"""
    LangChain自定义工具:
        1.@tool装饰器:args_schema定义pydantic参数
        2.StructuredTool.from_function:允许更多配置和同步异步实现规范,需要动态生成工具时
        3.子类化BaseTool

"""
#1.tool装饰器
from langchain_core.tools import tool
@tool
def multiply(a:int,b:int)->int:
    """Multiply two numbers."""
    return a*b
print(multiply.name)#默认函数名
print(multiply.description)
print(multiply.args)
#异步实现
@tool
async def amultiply(a:int,b:int)->int:
    """Multiply two numbers"""
    return a*b

#自定义工具名称和json参数
from pydantic import BaseModel,Field
class CalculatorInput(BaseModel):
     a:int = Field(description="first number")
     b:int=Field(description="second number")

@tool("multiplication-tool",args_schema=CalculatorInput,return_direct=True)
def multiply(a:int,b:int)->int:
    """Multiply two numbers."""
    return a*b

print(multiply.name)
print(multiply.description)
print(multiply.args)
print(multiply.return_direct)