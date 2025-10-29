from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompareRequest(BaseModel):
    url1: str
    url2: str

@app.post("/compare")
async def compare_filings(request: CompareRequest):
    # 1. Fetch both 10-Ks
    # 2. Parse them
    # 3. Diff them
    # 4. Return results
    return {
        "changes": ["Example change 1", "Example change 2"],
        "url1": request.url1,
        "url2": request.url2
    }