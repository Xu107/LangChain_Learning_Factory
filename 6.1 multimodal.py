import base64
import httpx
from langchain_core.messages import HumanMessage

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

#1.单张图片传送

image_url="https://q9.itc.cn/images01/20241017/b2a500d482f94d199c379477096daf7d.jpeg"
image_data=base64.b64encode(httpx.get(image_url).content).decode("utf-8")
image_url2="https://q7.itc.cn/images01/20241019/26cc6409f17747f5a6a2aa266e7bbdd9.jpeg"
image_data2=base64.b64encode(httpx.get(image_url2).content).decode("utf-8")

message=HumanMessage(
    content=[
        {"type":"text","text":"用中文描述这幅画"},
        {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{image_data}"}},
        # {"type":"image_url","image_url":{"url":image_url}}#不推荐，可能存在网络问题，LLM下载时可能出错，建议使用本地base64编码,e.g.内网图片
    ]
)
response=llm.invoke([message])
print(response.content)
# 这幅画描绘了一个宁静的自然景观。画面左侧是一棵光秃秃的树，树干粗壮，枝条向四周伸展，显得有些孤独。树的旁边是一片广阔的绿色田野，田野上生长着丰盈的作物，给人一种生机勃勃的感觉。远处的山丘在夕阳的映照下，轮廓柔和，显得温暖而宁静。太阳正缓缓落下，散发出金黄色的光芒，照亮了整个画面，营造出一种温馨而宁静的氛围。天空的颜色从蓝色渐变为橙色，形成了美丽的渐变效果，给人一种宁静而祥和的感觉。整体上，这幅画展现了自然的美丽与宁静，令人心旷神怡。

#2.多张图片传送
#多图片传送
message=HumanMessage(
    content=[
        {"type":"text","text":"这两张图片是一样的吗？"},
        {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{image_data}"}},
        {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{image_data2}"}}
    ]
)
response=llm.invoke([message])
print(response.content)

#3.工具调用
#一些多模态模型也支持工具调用功能。要使用此类模型调用工具，只需以通常的方式将工具绑定到他们，然后使用所需类型的内容块（例如，包含图像数据）调用模型。

from langchain_core.tools import tool
from typing import Literal
@tool
def weather_tool(weather:Literal["晴朗的","多云的","多雨的","下雪的"]) -> None:
    """Describe the weather"""
    pass

model_with_tools=llm.bind_tools([weather_tool])
message=HumanMessage(
    content=[
        {"type":"text","text":"用中文描述两张图片中的天气"},
        {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{image_data}"}},
        {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{image_data2}"}}
    ]
)
response=model_with_tools.invoke([message])
print(response.tool_calls)





