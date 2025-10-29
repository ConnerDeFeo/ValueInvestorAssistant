from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from fetch_10k_from_sec import fetch_10k_from_sec
from parse_html_to_text import parse_html_to_text
from compare_texts import compare_texts

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
    filing1 = await fetch_10k_from_sec(request.url1)
    filing2 = await fetch_10k_from_sec(request.url2)
    # 2. Parse them
    filling1_text = parse_html_to_text(filing1)
    filling2_text = parse_html_to_text(filing2)
    # 3. Diff them
    differences = compare_texts(filling1_text, filling2_text)
        
    return {
        "status": "success",
        "added_count": len(differences["added"]),
        "removed_count": len(differences["removed"]),
        "unchanged_count": len(differences["unchanged"]),
        "sample_added": differences["added"][:10],  # First 10 new lines
        "sample_removed": differences["removed"][:10],  # First 10 removed lines
    }
    