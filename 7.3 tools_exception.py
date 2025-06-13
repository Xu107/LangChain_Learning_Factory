from langchain_core.tools import StructuredTool
from langchain_core.tools import ToolException

def get_weather(city:str)->int:
    """获取给定城市的天气"""
    raise ToolException(f"错误，没有名为{city}的城市")

def _handle_error(error:ToolException)->str:
    #设置全局异常处理函数，不在工具调用时处理异常信息，而是编辑全局的异常处理解耦工具功能逻辑与异常处理逻辑解耦合
    return f"工具执行期间发生以下错误：'{error.args[0]}"


get_weather_tool=StructuredTool.from_function(
    func=get_weather,
    #默认情况下，如果函数抛出ToolException，则将ToolException的message作为相应
    #如果设置为True，则将返回ToolException异常文本，False将会抛出ToolException
    handle_tool_error=True,
    # handle_tool_error="没有找到这个城市",  #也可以直接返回，不用设置True或False
    # handle_tool_error=_handle_error,
)
response=get_weather_tool.invoke({"city":"foobar"})
print(response)
'''
    总结：
        handle_tool_error可以有三种赋值方式：
        1.默认为True，将直接返回ToolException raise时抛出的文本信息
        2.直接赋值str，输出异常信息
        3.赋值全局异常处理函数，将Tool功能逻辑与异常处理逻辑解耦合,注意:此时的args参数即为func的输入参数
'''