import os
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_google_genai import ChatGoogleGenerativeAI

class ModelLoader(BaseModel):
    model_provider: str = "gemini"
    config: Optional[dict] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = load_config()
    
    def load_llm(self):
        """Load and return the Gemini LLM model."""
        gemini_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        model_name = self.config["llm"]["gemini"]["model_name"]
        return ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=gemini_api_key,
            max_retries=5
        )