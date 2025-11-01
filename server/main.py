from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3
import os

from fetch_10k_from_sec import fetch_10k_from_sec
from parse_html_to_text import parse_html_to_text
from compare_texts import compare_texts
from extract_cik_from_url import extract_cik_from_url

app = FastAPI()
if os.getenv("env") == "production":
    bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-2")
else:
    session = boto3.Session(profile_name="admin")
    bedrock = session.client(service_name="bedrock-runtime", region_name="us-east-2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOW_ORIGINS")],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompareRequest(BaseModel):
    url1: str
    url2: str

@app.get("/")
def read_root():
    return {"status": "ok", "message": "FastAPI is running"}

@app.post("/compare")
async def compare_filings(request: CompareRequest):
    if request.url1 == request.url2:
        return {
            "status": "error",
            "analysis": "The provided URLs are identical. Please provide two different 10-K filing URLs to compare.",
        }
    # 1. Fetch both 10-Ks
    old = await fetch_10k_from_sec(request.url1.replace('/ix?doc=', ''))
    new = await fetch_10k_from_sec(request.url2.replace('/ix?doc=', ''))
    if not old or not new:
        return {
            "status": "error",
            "analysis": "Failed to fetch one or both of the provided URLs. Please ensure they are valid 10-K filing URLs.",
        }
    old_cik = extract_cik_from_url(request.url1)
    new_cik = extract_cik_from_url(request.url2)
    if old_cik != new_cik:
        return {
            "status": "error",
            "analysis": "The provided URLs do not belong to the same company (CIK mismatch). Please provide URLs for the same company's filings.",
        }
    # 2. Parse them
    old_text = parse_html_to_text(old)
    new_text = parse_html_to_text(new)
    # 3. Diff them
    differences = compare_texts(old_text, new_text)
    
    try:
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

                            Your task: produce a concise **Markdown list of changes per section**, using only these change types: **Added, Removed, Updated, Expanded**.  

                            Rules:
                            - Include **only substantive changes**; ignore minor wording changes, formatting, proxy references, date shifts, footers, or table-of-contents updates.
                            - Do not include explanations, analysis, or commentary — only the change type and a short description.
                            - Format exactly like this:
                                ### Section Name
                                - [Change type]: [Short description of what changed]
                                ... (repeat for each change in the section)

                            If a section has no major changes, write: `No major changes.`
                        """
                    }]
                },
            ],
            inferenceConfig={"maxTokens": 3000, "temperature": 0}
        )
    except Exception as e:
        return {
            "status": "error",
            "analysis": f"An error occurred during analysis: {str(e)}",
        }

    content = response["output"]["message"]["content"]
    print("response", response['usage'])
    raw_text = "### No Text Generated\nNo summary was produced for this comparison:( Please try again."
    for item in content:
        if "text" in item:
            raw_text = item["text"]
            break
    return {
        "status": "success",
        "analysis": raw_text,
    }
    