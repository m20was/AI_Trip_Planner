import os
from langchain.tools import tool
from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool

class PlaceSearchTool:
    def __init__(self):
        self.google_api_key = os.environ.get("GPLACES_API_KEY")
        self.google_places_search = GooglePlaceSearchTool(self.google_api_key)
        self.tavily_search = TavilyPlaceSearchTool()
        
        @tool
        def search_attractions(place: str) -> str:
            """Search attractions of a place"""
            try:
                attractions_result = self.google_places_search.google_search_attractions(place)
                if attractions_result:
                    return f"Following are the attractions of {place} as suggested by google: {attractions_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_attractions(place)
                return f"Google cannot find the details due to {e}. \nFollowing are the attractions of {place}: {tavily_result}"
        
        @tool
        def search_restaurants(place: str) -> str:
            """Search restaurants of a place"""
            try:
                restaurants_result = self.google_places_search.google_search_restaurants(place)
                if restaurants_result:
                    return f"Following are the restaurants of {place} as suggested by google: {restaurants_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_restaurants(place)
                return f"Google cannot find the details due to {e}. \nFollowing are the restaurants of {place}: {tavily_result}"
        
        @tool
        def search_activities(place: str) -> str:
            """Search activities of a place"""
            try:
                restaurants_result = self.google_places_search.google_search_activity(place)
                if restaurants_result:
                    return f"Following are the activities in and around {place} as suggested by google: {restaurants_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_activity(place)
                return f"Google cannot find the details due to {e}. \nFollowing are the activities of {place}: {tavily_result}"
        
        @tool
        def search_transportation(place: str) -> str:
            """Search transportation of a place"""
            try:
                restaurants_result = self.google_places_search.google_search_transportation(place)
                if restaurants_result:
                    return f"Following are the modes of transportation available in {place} as suggested by google: {restaurants_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_transportation(place)
                return f"Google cannot find the details due to {e}. \nFollowing are the modes of transportation available in {place}: {tavily_result}"
        
        self.place_search_tool_list = [
            search_attractions,
            search_restaurants,
            search_activities,
            search_transportation
        ]