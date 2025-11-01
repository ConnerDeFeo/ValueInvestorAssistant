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
    
    total_differences = 0
    for _, changes in differences.items():
        total_differences += len(changes["added"]) + len(changes["removed"]) + len(changes["unchanged"])
    print(f"Total differences found: {total_differences}")
    response = bedrock.converse(
        modelId = "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        messages=[
            {
                "role": "user", 
                "content": [{"text": 
                    f"""
                        You are analyzing 10-K filing changes for a value investor for the following two filings:
                        Older filing: {request.url1} and newer filing: {request.url2}

                        
                        The following are the differences between them, with removed being the contents that are 
                        in the first financial statement and not the second, and added being the contents
                        that are in the second statement and not the first:
                        {differences}

                        Your goal is to produce a concise, structured list showing only what changed in each section — not why it changed or what it means.

                        Format your output as follows:

                        Section Name
                        - [Change type]: [Short description of what changed]
                        ... repeat for each change in the section

                        Use these change types: Added, Removed, Updated, Expanded, or Minor edits.
                        Be concise — each bullet should be under 20 words.
                        If a section has no major changes, write “No major changes.”
                        Do not provide a title or introduction — just the list of changes. 
                        Provide your response in markdown format. Use headings for section names.
                    """
                }]
            }
        ],
        inferenceConfig={"maxTokens": 500, "temperature": 0.5}
    )

    raw_text = response["output"]["message"]["content"][0]["text"]
    return {
        "status": "success",
        "analysis": raw_text,
    }
    