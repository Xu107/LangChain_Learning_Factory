
import os
os.environ['TAVILY_API_KEY']="your_tavily_api_key"

from langchain_community.tools.tavily_search import TavilySearchResults
search=TavilySearchResults(max_results=2)
print(search.invoke("今天上海天气怎么样?"))

