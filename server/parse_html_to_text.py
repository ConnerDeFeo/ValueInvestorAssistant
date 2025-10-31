from bs4 import BeautifulSoup
import re

def parse_html_to_text(html_content: str) -> str:
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
        "business": r"(Item|item|ITEM)\s+1\s*[\.:−-]\s*(Business|business|BUSINESS)",
        "risk_factors": r"(Item|item|ITEM)\s+1A\s*[\.:−-]\s*(Risk Factors|risk factors|RISK FACTORS)",
    }

    business_matches = list(re.finditer(section_patterns["business"], full_text, re.IGNORECASE))
    if len(business_matches) < 2:
        # If only one match, it might be the actual section (no TOC)
        business_match = business_matches[0] if business_matches else None
    else:
        # Use the SECOND match (skip TOC)
        business_match = business_matches[1]

    risk_factors_matches = list(re.finditer(section_patterns["risk_factors"], full_text, re.IGNORECASE))
    if len(risk_factors_matches) < 2:
        # If only one match, it might be the actual section (no TOC)
        risk_factors_match = risk_factors_matches[0] if risk_factors_matches else None
    else:
        # Use the SECOND match (skip TOC)
        risk_factors_match = risk_factors_matches[1]
    if not business_match or not risk_factors_match:
        raise ValueError("Could not find both 'Item 1. Business' and 'Item 1A. Risk Factors' sections.")
    business_start = business_match.end()
    risk_factors_start = risk_factors_match.start()
    extracted_text = full_text[business_start:risk_factors_start].strip()
    return extracted_text