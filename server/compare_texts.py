import difflib

def compare_texts(text1: str, text2: str) -> dict:
    # Split into lines for comparison
    lines1 = text1.splitlines(keepends=True)
    lines2 = text2.splitlines(keepends=True)
    print("Text1 lines:", len(lines1))
    print("Text2 lines:", len(lines2))
    
    # Create a diff
    differ = difflib.Differ()
    diff = list(differ.compare(lines1, lines2))
    
    # Parse the diff output
    changes = {
        "added": [],
        "removed": [],
        "unchanged": []
    }
    print("Diff length:", len(diff))
    for line in diff:
        if line.startswith('+ '):
            changes["added"].append(line[2:])
        elif line.startswith('- '):
            changes["removed"].append(line[2:])
        elif line.startswith('  '):
            changes["unchanged"].append(line[2:])
    
    return changes