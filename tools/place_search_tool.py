from langchain.tools import tool
from utils.place_info_search import TavilyPlaceSearchTool

class PlaceSearchTool:
    def __init__(self):
        self.tavily_search = TavilyPlaceSearchTool()
        
        @tool
        def search_attractions(place: str) -> str:
            """Search attractions of a place"""
            tavily_result = self.tavily_search.tavily_search_attractions(place)
            return f"Following are the attractions of {place}: {tavily_result}"
        
        @tool
        def search_restaurants(place: str) -> str:
            """Search restaurants of a place"""
            tavily_result = self.tavily_search.tavily_search_restaurants(place)
            return f"Following are the restaurants of {place}: {tavily_result}"
        
        @tool
        def search_activities(place: str) -> str:
            """Search activities of a place"""
            tavily_result = self.tavily_search.tavily_search_activity(place)
            return f"Following are the activities of {place}: {tavily_result}"
        
        @tool
        def search_transportation(place: str) -> str:
            """Search transportation of a place"""
            tavily_result = self.tavily_search.tavily_search_transportation(place)
            return f"Following are the modes of transportation available in {place}: {tavily_result}"
        
        self.place_search_tool_list = [
            search_attractions,
            search_restaurants,
            search_activities,
            search_transportation
        ]