#1.StructuredTool
#StructuredTool.from_function类方法提供比@tool装饰器更多的可配置性而无需太多额外的代码
from langchain_core.tools import StructuredTool
import asyncio

def multiply(a:int,b:int)->int:
    """Multiply two numbers"""
    return a*b
async def amultiply(a:int,b:int)->int:
    """Multiply two numbers"""
    return a*b

async def main():
    #func参数：指定一个同步函数，当在同步上下文中调用工具时，会使用同步函数来进行操作
    #coroutine参数：指定一个异步函数，当在异步上下文中调用工具时，会使用异步函数来进行操作
    calculator=StructuredTool.from_function(func=multiply,coroutine=amultiply)
    print(calculator.invoke({"a":2,"b":3}))
    #ainvoke异步调用,async+await；asyncio.gather
    print(await calculator.ainvoke({"a":4,"b":5}))

asyncio.run(main())

#2.自定义参数
from pydantic import BaseModel,Field
class CalculatorInput(BaseModel):
    a:int=Field(description="First number")
    b:int=Field(description="Second number")

async def async_addition(a:int,b:int)->int:
    """Add two numbers"""
    return a+b

async def main():
    calculator=StructuredTool.from_function(
        func=multiply,
        name="Calculator",
        description="multiply numbers",
        args_schema=CalculatorInput,
        return_direct=True,
        coroutine=async_addition
    )
    print(calculator.invoke({"a":6,"b":7}))
    print(await calculator.ainvoke({"a":10,"b":11}))
    print(calculator.name)
    print(calculator.description)
    print(calculator.args)

#运行异步主函数
asyncio.run(main())