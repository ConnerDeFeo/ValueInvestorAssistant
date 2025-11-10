import httpx
import re
from bs4 import BeautifulSoup
import difflib
from dynamo import update_item
import boto3

# Fetch 10-K filing from SEC EDGAR
def fetch_10k_from_sec(url: str):
    headers = {
        "User-Agent": "Conner DeFeo ninjanerozz@gmail.com"
    }

    with httpx.Client() as client:
        response = client.get(url, headers=headers, follow_redirects=True)

        if response.status_code == 200:
            return response.text
        else:
            return None
        
def extract_cik_from_url(url):
    """
    Extracts the CIK from the SEC URL.
    """
    match = re.search(r'/data/(\d+)/', url)
    if match:
        return match.group(1).lstrip('0')  # remove leading zeros
    return None

def parse_html_to_text(html_content, requested_sections):
    """
    Extract key sections from a 10-K filing
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style tags
    for script in soup(["script", "style"]):
        script.decompose()
    # Get all text
    full_text = soup.get_text(separator='\n', strip=True)
    
    # Define the section patterns to look for
    section_patterns = {
        # Part I
        "risk_factors": r"Item\s+1A\s*[\.:-]\s*Risk Factors",
        "unresolved_staff_comments": r"Item\s+1B\s*[\.:-]\s*Unresolved Staff Comments",
        "cybersecurity": r"Item\s+1C\s*[\.:-]\s*Cybersecurity",
        "properties": r"Item\s+2\s*[\.:-]\s*Properties",
        "legal_proceedings": r"Item\s+3\s*[\.:-]\s*Legal Proceedings",
        "mine_safety": r"Item\s+4\s*[\.:-]\s*Mine Safety Disclosures",

        # Part II
        "market_for_registrants_common_equity": r"Part\s+(2|II)\s+Item\s+5\s*[\.:-]\s*Market\s+for\s+Registrant.s\s+Common\s+Equity",
        "selected_financial_data": r"Item\s+6\s*[\.:-]\s*Selected Financial Data",
        "managements_discussion_and_analysis": r"Item\s+7\s*[\.:-]\s*Management.s Discussion and Analysis of Financial Condition and Results of Operations",
        "quantitative_and_qualitative_disclosures": r"Item\s+7A\s*[\.:-]\s*Quantitative and Qualitative Disclosures about Market Risk",
        "financial_statements_and_supplementary_data": r"Item\s+8\s*[\.:-]\s*Financial Statements and Supplementary Data",
        "changes_in_and_disagreements_with_accountants": r"Item\s+9\s*[\.:-]\s*Changes in and Disagreements with Accountants on Accounting and Financial Disclosure",
        "controls_and_procedures": r"Item\s+9A\s*[\.:-]\s*Controls and Procedures",
        "other_information": r"Item\s+9B\s*[\.:-]\s*Other Information",
        
        "disclosures_regarding_foreign_jurisdictions_that_prevent_inspection": r"Item\s+9C\s*[\.:-]\s*Disclosure\sRegarding\sForeign\sJurisdictions\sThat\sPrevent\sInspections",

        # Part III
        "directors_and_executive_officers": r"Part\s+(3|III)\s+Item\s+10\s*[\.:-]\s*Directors, Executive Officers and Corporate Governance",
        "executive_compensation": r"Item\s+11\s*[\.:-]\s*Executive Compensation",
        "security_ownership_of_certain_beneficial_owners_and_management": r"Item\s+12\s*[\.:-]\s*Security Ownership of Certain Beneficial Owners and Management",
        "certain_relationships_and_related_transactions": r"Item\s+13\s*[\.:-]\s*Certain Relationships and Related Transactions",
        "principal_accountant_fees_and_services": r"Item\s+14\s*[\.:-]\s*Principal Accountant Fees and Services",

        # Part IV
        "exhibits_and_financial_statement_schedules": r"Part\s+(4|IV)\s+Item\s+15\s*[\.:-]\s*Exhibits and Financial Statement Schedules",
    }
    prev  = list(re.finditer(r"(Item)\s+1\s*[\.:-]\s*(Business)", full_text, re.IGNORECASE))
    if not prev:
        raise ValueError("Could not find the Business section in the filing.")
    currentMatch = prev[0] if len(prev) == 1 else prev[1] # ignore heading
    currentTitle = "business"
    sections = {}
    tokens = 0
    for key, pattern in section_patterns.items():
        section_matches = list(re.finditer(pattern, full_text, re.IGNORECASE))
        # Older fililngs do not have certain sections
        if not section_matches:
            print(f"Section {key} not found in filing.")
            continue
        section_match = section_matches[0] if len(section_matches) == 1 else section_matches[1]  # ignore heading
        if currentTitle in requested_sections:
            start_pos = currentMatch.end()
            end_pos = section_match.start()
            section_text = full_text[start_pos:end_pos].strip()
            sections[currentTitle] = section_text
            tokens += len(section_text) / 4  # rough estimate

        currentMatch = section_match
        currentTitle = key

    if not sections:
        raise ValueError("Could not find any sections in the filing.")
    return sections, tokens

MAX_TOKENS = 100000
OUTPUT_TOKENS = 4000
def compare_10k_filings_worker(event, context):
    # Helper to update job status
    def update_job_status(result, status):
        update_item(
            'comparison_jobs',
            key={'job_id': job_id},
            update_expression='SET #status = :status, #result = :result',
            expression_attribute_names={'#status': 'status', "#result": "result"},
            expression_attribute_values={
                ':status': status,
                ':result': result
            }
        )
    try:
        url1 = event['url1']
        url2 = event['url2']
        job_id = event['jobId']
        sections = event['sections']

        # 1. Fetch both 10-Ks
        old = fetch_10k_from_sec(url1.replace('/ix?doc=', ''))
        new = fetch_10k_from_sec(url2.replace('/ix?doc=', ''))
        if not old or not new:
            # Update status
            update_job_status("Failed to fetch one or both filings.", "FAILED")
            return
        old_cik = extract_cik_from_url(url1)
        new_cik = extract_cik_from_url(url2)
        if old_cik != new_cik:
            update_job_status("The two filings belong to different companies (CIKs do not match).", "FAILED")
            return
        old_text, old_tokens = parse_html_to_text(old, set(sections))
        new_text, new_tokens = parse_html_to_text(new, set(sections))
        tokens = old_tokens + new_tokens
        print(f"Estimated tokens for Bedrock call: {tokens}")

        if tokens > MAX_TOKENS:  # leave some buffer
            update_job_status(f"The differences between the selected sections exceed the token limit for analysis (MAX:{MAX_TOKENS}, ACTUAL:{tokens}). Please choose fewer sections.", "FAILED")
            return
        
        try:
            bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
            response = bedrock.converse(
                modelId = "openai.gpt-oss-120b-1:0",
                messages=[
                    {
                        "role": "user", 
                        "content": [{"text": 
                            f"""
                                You are a value investor analyzing 10-K changes for certain sections.
                                Your goal is to return a marked-down formatted summary of key insights from the changes between the two filings.

                                RULES:
                                - Separate insights by section, with a heading for each section
                                - If a section has no significant changes, state "No significant changes"
                                - Skip administrative updates (dates, formatting, minor legal updates)
                                - Give bullet points for each insight

                                You are given the differences between two 10-K filings for the same company:
                                Old Filing Section:
                                {old_text}
                                New Filing Section:
                                {new_text}

                            """
                        }]
                    },
                ],
                inferenceConfig={"maxTokens": OUTPUT_TOKENS, "temperature": 0}
            )
            content = response["output"]["message"]["content"]
            print("response", response['usage'])
            raw_text = "### No Text Generated\nNo summary was produced for this comparison:( Please try again."
            for item in content:
                if "text" in item:
                    raw_text = item["text"]
                    break
            update_job_status(raw_text, "COMPLETED")
        except Exception as e:
            print(f"Error calling Bedrock: {str(e)}")
            update_job_status(f"Too many changes were detected for analysis. Please narrow your selection.", "FAILED")
    except Exception as e:
        print(f"Error fetching filings: {str(e)}")
        update_job_status(f"Internal Server Error: {str(e)}", "FAILED")