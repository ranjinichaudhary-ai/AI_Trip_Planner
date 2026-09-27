# entire app streamlit UI
# Create endpoint
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_travel_agent(query:QueryRequest):
    return {"message": "Hello, this is a query endpoint!"}