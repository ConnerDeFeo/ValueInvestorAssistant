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

    # Begin with the business section
    prev  = list(re.finditer(r"(Item)\s+1\s*[\.:-]\s*(Business)", full_text, re.IGNORECASE))
    if not prev:
        raise ValueError("Could not find the Business section in the filing.")
    currentMatch = prev[0] if len(prev) == 1 else prev[1] # ignore heading
    currentTitle = "business"
    sections = {}
    for key, pattern in section_patterns.items():
        section_matches = list(re.finditer(pattern, full_text, re.IGNORECASE))
        # Older fililngs do not have certain sections
        if not section_matches:
            print(f"Section {key} not found in filing.")
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