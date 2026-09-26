from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from agent.agentic_workflow import GraphBuilder

load_dotenv()

app = FastAPI(title="AI Travel Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def health_check():
    """Health check endpoint for container monitoring and cloud load balancers."""
    return {"status": "healthy", "service": "AI Travel Planner API"}

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    """Process travel queries through the LangGraph AI agent."""
    try:
        agent = GraphBuilder(model_provider="gemini")()
        output = agent.invoke({"messages": [query.question]})
        raw = output["messages"][-1].content
        
        # Format text parts cleanly (handles Gemini multi-part responses)
        answer = "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in raw) if isinstance(raw, list) else str(raw)
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})