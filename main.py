from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from agent.agentic_workflow import build_graph

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str


@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        graph = build_graph(provider="groq")
        output = graph.invoke({"messages": [query.question]})

        if isinstance(output, dict) and "messages" in output:
            answer = output["messages"][-1].content
        else:
            answer = str(output)

        return {"answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
