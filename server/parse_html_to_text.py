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
        "risk_factors": r"(Item|item|ITEM)\s+1A\s*[\.:-]\s*(Risk Factors|risk factors|RISK FACTORS)",
        "unresolved_staff_comments": r"(Item|item|ITEM)\s+1B\s*[\.:-]\s*(Unresolved Staff Comments|unresolved staff comments|UNRESOLVED STAFF COMMENTS)",
        "cybersecurity": r"(Item|item|ITEM)\s+1C\s*[\.:-]\s*(Cybersecurity|cybersecurity|CYBERSECURITY)",
        "properties": r"(Item|item|ITEM)\s+2\s*[\.:-]\s*(Properties|properties|PROPERTIES)",
        "legal_proceedings": r"(Item|item|ITEM)\s+3\s*[\.:-]\s*(Legal Proceedings|legal proceedings|LEGAL PROCEEDINGS)",
        "mine_safety": r"(Item|item|ITEM)\s+4\s*[\.:-]\s*(Mine Safety Disclosures|mine safety disclosures|MINE SAFETY DISCLOSURES)",
        "market_for_registrants_common_equity": r"(Item|item|ITEM)\s+5\s*[\.:-]\s*(Market for Registrant's Common Equity|market for registrant's common equity|MARKET FOR REGISTRANT'S COMMON EQUITY)",
    }

    # Begin with the business section
    prev  = list(re.finditer(r"(Item|item|ITEM)\s+1\s*[\.:-]\s*(Business|business|BUSINESS)", full_text, re.IGNORECASE))
    if not prev:
        raise ValueError("Could not find the Business section in the filing.")
    currentMatch = prev[0] if len(prev) == 1 else prev[1] # ignore heading
    currentTitle = "business"
    sections = {}
    for key, pattern in section_patterns.items():
        section_matches = list(re.finditer(pattern, full_text, re.IGNORECASE))
        # Older fililngs do not have certain sections
        if not section_matches:
            continue
        section_match = section_matches[0] if len(section_matches) == 1 else section_matches[1]  # ignore heading
        start_pos = currentMatch.end()
        end_pos = section_match.start()
        section_text = full_text[start_pos:end_pos].strip()

        # Add results
        sections[currentTitle] = section_text
        currentMatch = section_match
        currentTitle = key
    print(len(sections))
    if not sections:
        raise ValueError("Could not find any sections in the filing.")
    return sections