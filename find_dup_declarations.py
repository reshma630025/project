import re

with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Check lines 1845 to 3890 (inside the script tag)
# Exclude lines 3681 to 3880
decl_counts = {}
for idx, line in enumerate(lines):
    line_num = idx + 1
    if line_num < 1845 or line_num > 3890:
        continue
    # If we skip 3681-3880:
    if 3681 <= line_num <= 3880:
        continue
    
    # Check top-level const or let (starts with 'const ' or 'let ' or 'var ')
    m = re.match(r'^\s*(?:const|let|var)\s+([a-zA-Z0-9_$]+)', line)
    if m:
        name = m.group(1)
        # only if not inside a function or block (indent == 0)
        indent = len(line) - len(line.lstrip())
        if indent == 0:
            if name in decl_counts:
                decl_counts[name].append(line_num)
            else:
                decl_counts[name] = [line_num]

print("Top-level declarations with multiple occurrences (excluding lines 3681-3880):")
duplicates = {k: v for k, v in decl_counts.items() if len(v) > 1}
if duplicates:
    for k, v in duplicates.items():
        print(f"  {k}: lines {v}")
else:
    print("  None! Zero duplicates found when lines 3681-3880 are removed.")
