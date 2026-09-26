from langgraph.prebuilt import create_react_agent
from prompt_library.prompt import SYSTEM_PROMPT
from utils.model_loader import ModelLoader
from tools import get_tools

class GraphBuilder:
    def __init__(self, model_provider: str = "gemini"):
        self.llm = ModelLoader(model_provider=model_provider).load_llm()
        self.tools = get_tools()

    def __call__(self):
        """Build and return the compiled ReAct agent."""
        return create_react_agent(self.llm, self.tools, prompt=SYSTEM_PROMPT)