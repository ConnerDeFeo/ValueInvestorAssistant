from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3

from fetch_10k_from_sec import fetch_10k_from_sec
from parse_html_to_text import parse_html_to_text
from compare_texts import compare_texts

app = FastAPI()
session = boto3.Session(profile_name="admin")
bedrock = session.client(service_name="bedrock-runtime", region_name="us-east-2")

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
        
    response = bedrock.converse(
        modelId = "us.amazon.nova-lite-v1:0",
        messages=[
            {
                "role": "user", 
                "content": [{"text": 
                    f"""
                        You are a financial analysts, and comparing two financial statements:
                        {request.url1} and {request.url2}
                        These are the differences between them, with filling_one_diff being the contents that are 
                        in the first financial statement and not the second, and filling_two diff being the contents
                        that are in the second statement and not the first:
                        {differences}

                        Explain any changes that have occured. Do this in 100 tokens or less.
                    """
                }]
            }
        ],
        inferenceConfig={"maxTokens": 100, "temperature": 0.3, "topP": 0.3}
    )

    raw_text = response["output"]["message"]["content"][0]["text"]
    return {
        "status": "success",
        "analysis": raw_text,
    }
    