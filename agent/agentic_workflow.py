from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool

class GraphBuilder:
    def __init__(self, model_provider: str = "groq"):
        self.llm = ModelLoader(model_provider=model_provider).load_llm()
        
        self.tools = [
            *WeatherInfoTool().weather_tool_list,
            *PlaceSearchTool().place_search_tool_list,
            *CalculatorTool().calculator_tool_list,
            *CurrencyConverterTool().currency_converter_tool_list
        ]
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        
    def agent_function(self, state: MessagesState):
        """Main agent function"""
        user_question = state["messages"]
        input_question = [SYSTEM_PROMPT] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"messages": [response]}

    def build_graph(self):
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agent", END)
        return graph_builder.compile()
        
    def __call__(self):
        return self.build_graph()