import difflib

def compare_texts(oldText, newText):
    differences = {}
    for key in oldText.keys():
        if key not in newText:
            raise ValueError(f"Section {key} not found in second text for comparison.")
        # Split into lines for comparison
        lines1 = oldText[key].splitlines(keepends=True)
        lines2 = newText[key].splitlines(keepends=True)
        lines1 = [line for line in lines1 if len(line)>10]  # remove empty lines
        lines2 = [line for line in lines2 if len(line)>10]  # remove empty lines
        # Create a diff
        differ = difflib.Differ()
        diff = list(differ.compare(lines1, lines2))
        
        # Parse the diff output
        changes = {
            "removed": [], # removed from old filing
            "added": [], # added in new filing
            "unchanged": []
        }
        for line in diff:
            if line.startswith('+ '):
                changes["added"].append(line[2:])
            elif line.startswith('- '):
                changes["removed"].append(line[2:])
            elif line.startswith('  '):
                changes["unchanged"].append(line[2:])
        differences[key] = changes

    return differences