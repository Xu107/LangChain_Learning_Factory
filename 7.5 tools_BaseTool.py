from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel, Field
from typing import Dict, Any, Type

class CalculatorInput(BaseModel):
    a: int = Field(..., description="第一个数字")
    b: int = Field(..., description="第二个数字")

class CalculatorTool(BaseTool):
    name: str = "calculator_tool"
    description: str = "接收两个数字并返回它们的乘积。"
    args_schema : Type[BaseModel] = CalculatorInput

    def _run(self, a: int, b: int) -> int:
        try:
            return a * b
        except Exception as e:
            raise ToolException(f"计算器工具出错：{str(e)}")

    async def _arun(self, a: int, b: int) -> int:
        try:
            return a * b
        except Exception as e:
            raise ToolException(f"计算器工具出错：{str(e)}")

# 使用
tool = CalculatorTool()
result = tool.invoke({"a": 3, "b": 4})
print(result)  # 输出 12

import asyncio
result_async = asyncio.run(tool.ainvoke({"a": 5, "b": 6}))
print(result_async)  # 输出 30