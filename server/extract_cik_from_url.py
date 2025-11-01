import re
def extract_cik_from_url(url):
    """
    Extracts the CIK from the SEC URL.
    """
    match = re.search(r'/data/(\d+)/', url)
    if match:
        return match.group(1).lstrip('0')  # remove leading zeros
    return None