from langchain_tavily import TavilySearch

class TavilyPlaceSearchTool:
    def __init__(self):
        self.tavily_tool = TavilySearch(topic="general", include_answer="advanced")

    def _search(self, query: str) -> str:
        result = self.tavily_tool.invoke({"query": query})
        return result.get("answer") if isinstance(result, dict) and result.get("answer") else result

    def tavily_search_attractions(self, place: str) -> dict:
        """Search attractions using Tavily."""
        return self._search(f"top attractive places in and around {place}")
    
    def tavily_search_restaurants(self, place: str) -> dict:
        """Search restaurants using Tavily."""
        return self._search(f"what are the top 10 restaurants and eateries in and around {place}.")
    
    def tavily_search_activity(self, place: str) -> dict:
        """Search activities using Tavily."""
        return self._search(f"activities in and around {place}")

    def tavily_search_transportation(self, place: str) -> dict:
        """Search transportation modes using Tavily."""
        return self._search(f"What are the different modes of transportations available in {place}")