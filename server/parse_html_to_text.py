from bs4 import BeautifulSoup

def parse_html_to_text(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    
    for script in soup(["script", "style"]):
        script.decompose()
    
    text = soup.get_text()
    print(f"Raw text length: {len(text)}")  # Add this
    print(f"First 500 chars: {text[:500]}")  # Add this
    
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    print(f"Number of lines after cleaning: {len(lines)}")  # Add this
    
    return '\n'.join(lines)