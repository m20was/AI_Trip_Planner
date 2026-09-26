from langchain.tools import tool
from langchain_tavily import TavilySearch

tavily = TavilySearch(topic="general", include_answer="advanced")

@tool
def search_places(query: str) -> str:
    """Search for attractions, restaurants, activities, and transport in any city."""
    res = tavily.invoke({"query": query})
    return res.get("answer", str(res))

class PlaceSearchTool:
    place_search_tool_list = [search_places]