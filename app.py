from fastapi import FastAPI
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
from fastapi.responses import JSONResponse
import os   

app= FastAPI()

class QueryRequest(BaseModel):
    query:str
    
@app.get("/query") # This is our End Point from where all the magic starts.
async  def query_travel_agent(query:QueryRequest):
    try:
        print(query)
        graph = GraphBuilder(model_provider="groq") # Graph Builder Object is Created
        react_app = graph() # Graph is built
        png_graph = react_app.get_graph().draw_mermaid_png() # We're saving the graph 
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)
            
        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
        # Assuming request is pydantic object like: {"question":"your text"}
        messages={"messages": [query.query]}
        output = react_app.invoke(messages) # Here we invoke the message
        
        # If result is dict with messages:
        if isinstance(output,dict) and "messages" in output:
            final_output = output["messages"][-1].content # Last AI Response
        else:
            final_output = str(output)
        return {"answer":final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
