# 🧠 LangChain_Factory 学习记录仓库

本项目旨在系统性地学习并实践 [LangChain](https://github.com/langchain-ai/langchain) 框架中的核心模块，结合 OpenAI gpt-4o-mini 模型能力，构建一个可供日后开发参考的 LLM 代码库。通过分阶段脚本命名与模块划分，逐步掌握 LangChain 在 Prompt 构造、流式输出 (Stream) 、部署跟踪、历史记录及持久化、多模态交互、输出解析、Agent 调用等方面的核心技术。

## 📁 项目结构概览


## 📌 学习目标与进度


| 模块编号 | 学习主题               | 技术关键词                                                                                                                                                                      | 学习状态  |
|------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------| --------- |
| 1    | 快速入门               | ChatOpenAI, ChatPromptTemplate, invoke                                                                                                                                     | ✅ 已完成 |
| 2    | Prompt Engineering | PromptTemplate, SystemMessage, HumanMessage, AIMessage, FewShotPromptTemplate                                                                                              | ✅ 已完成 |
| 3    | 流式输出               | Stream, Asyncio                                                                                                                                                            | ✅ 已完成 |
| 4    | 调试与追踪              | LangServe, LangSmith, Verbose, Debug                                                                                                                                       | ✅ 已完成 |
| 5    | 会话历史管理             | ChatMessageHistory, MessagesPlaceholder, RunnableWithMessageHistory, BaseChatMessageHistory, ConfigurableFieldSpec, Redis, RedisChatMessageHistory, Messages Trim&Summarize | ✅ 已完成 |
| 6    | 多模态与解析             | 图文输入, JSON/YAML/XML 结构化输出: Base64, JsonOutputParser, XMLOutputParser, YamlOutputParser, Pydantic (BaseModel, Field)                                                        | ✅ 已完成 |
| 7    | 自定义工具调用            |                                                     | 🔄 进行中 |
| 8    | Agent智能体           |                                                     | 🔄 进行中 |
| 9    | RAG 检索增强生成         |                                                     | 🔄 进行中 |
| 10   | 基于 RAG 实现文档问答      |                                                     | 🔄 进行中 |
| 11   | LangGraph...       |                                                     | 🔄 进行中 |


## 🌟 实验说明

> ✅ 所有代码均经过实验验证可正常运行，学习过程中建议使用python多段注释''' '''分割观察研究每部分执行结果

## 🧩 技术栈

- LangChain
- OpenAI gpt-4o-mini
- Pydantic / JSON Schema
- Redis / Gradio / Streamlit（可拓展）
- Python >= 3.9

  使用时请将env文件修改为 ".env" 文件以供load_dotenv()函数加载项目环境变量

## 📝 后续计划

- [ ]  整合多模态 Agent 多轮对话（图文问答）
- [ ]  使用 LangGraph 构建复杂对话流程图
- [ ]  调研 Web UI demo 页面
- [ ]  补充添加Jupyter Notebook执行代码以供可视化

## 🔒 API Key 提示

请在 `.env` 文件中设置以下环境变量：

### LangSmith 平台配置
LANGSMITH_API_KEY="你的 LangSmith API 密钥"

LANGSMITH_PROJECT="你的 LangSmith 项目名称"

### OpenAI 接口配置
OPENAI_API_KEY="你的 OpenAI API 密钥"

BASE_URL="你的 OpenAI API 接口地址（如为代理服务，请填写代理地址）"

## 📚 参考资料

- [LangChain 官方文档](https://docs.langchain.com/)
- [LangSmith](https://docs.smith.langchain.com/)
- [2025吃透LangChain大模型全套教程（LLM+RAG+OpenAI+Agent）](https://www.bilibili.com/video/BV1BgfBYoEpQ?spm_id_from=333.788.videopod.sections&vd_source=0f72224dce55d1f258be21ec3ad13c7a)
---

> 本项目由个人持续更新维护，旨在全面掌握 LangChain 的设计哲学与模块工程化实践。如果你也在学习 LangChain，欢迎交流探讨 🤝

> 项目持续更新中...
