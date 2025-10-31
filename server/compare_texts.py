import difflib

def compare_texts(text1: str, text2: str) -> dict:
    # Split into lines for comparison
    lines1 = text1['business'].splitlines(keepends=True)
    lines2 = text2['business'].splitlines(keepends=True)

    # Create a diff
    differ = difflib.Differ()
    diff = list(differ.compare(lines1, lines2))
    
    # Parse the diff output
    changes = {
        "filling_one_diff": [],
        "filling_two_diff": [],
        "unchanged_count": []
    }
    for line in diff:
        if line.startswith('+ '):
            changes["filling_one_diff"].append(line[2:])
        elif line.startswith('- '):
            changes["filling_two_diff"].append(line[2:])
        elif line.startswith('  '):
            changes["unchanged_count"].append(line[2:])
    
    return changes