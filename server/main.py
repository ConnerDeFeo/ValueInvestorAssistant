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
    old = await fetch_10k_from_sec(request.url1)
    new = await fetch_10k_from_sec(request.url2)
    # 2. Parse them
    old_text = parse_html_to_text(old)
    new_text = parse_html_to_text(new)
    # 3. Diff them
    differences = compare_texts(old_text, new_text)
    
    response = bedrock.converse(
        modelId = "openai.gpt-oss-120b-1:0",
        messages=[
            {
                "role": "user", 
                "content": [{"text": 
                    f"""
                        You are analyzing 10-K filing changes for a value investor.  
                        Older filing: {request.url1}  
                        Newer filing: {request.url2}

                        Below are the extracted textual differences between them:  
                        {differences}

                        Your task: produce a concise, structured list showing **only what changed** in each section — 
                        not why it changed or what it means.

                        Format your output exactly like this:

                        ### Section Name
                        - [Change type]: [Short description of what changed]
                        ... (repeat for each change in the section)

                        Use these change types: **Added**, **Removed**, **Updated**, **Expanded**.  
                        If a section has no major changes, write `No major changes.`  
                        Do not include updates that are purely formatting, proxy reference, or date shifts.  
                        Do not include any commentary, title, or introduction — just the list of changes.  
                        Output must be in **Markdown** format and under **2000 tokens**.
                    """
                }]
            },
        ],
        inferenceConfig={"maxTokens": 2000, "temperature": 0}
    )

    content = response["output"]["message"]["content"]
    print(f"Bedrock response content: {content}")
    raw_text = "### No Text Generated\nNo summary was produced for this comparison:( Please try again."
    for item in content:
        if "text" in item:
            raw_text = item["text"]
            break
    return {
        "status": "success",
        "analysis": raw_text,
    }
    