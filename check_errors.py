import re
from collections import Counter
import sys

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()
    lines = content.splitlines()

print(f"Total lines on disk: {len(lines)}")

# 1. Check for Duplicate IDs in HTML
ids = re.findall(r'\bid=["\']([^"\']+)["\']', content)
id_counts = Counter(ids)
dup_ids = {k: v for k, v in id_counts.items() if v > 1}
print(f"\n1. Duplicate IDs ({len(dup_ids)}):")
for k, v in dup_ids.items():
    print(f"   id='{k}' appears {v} times")

# 2. Check for syntax issues inside <script>
script_match = re.search(r'<script\b[^>]*>([\s\S]*?)</script>', content, re.I)
if script_match:
    script_content = script_match.group(1)
    script_start_line = content[:script_match.start()].count('\n') + 1
    print(f"\n2. Main <script> tag starts at line {script_start_line}")
    
    # Check brace/bracket/parenthesis balance
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    in_string = False
    str_char = None
    in_comment = False
    in_line_comment = False
    
    for lno, line in enumerate(script_content.splitlines()):
        actual_line = script_start_line + lno
        i = 0
        while i < len(line):
            c = line[i]
            if not in_string and not in_comment and not in_line_comment:
                if c in ['"', "'", '`']:
                    in_string = True
                    str_char = c
                elif c == '/' and i + 1 < len(line) and line[i+1] == '/':
                    break # rest of line is comment
                elif c == '/' and i + 1 < len(line) and line[i+1] == '*':
                    in_comment = True
                    i += 1
                elif c in '({[':
                    stack.append((c, actual_line, i+1))
                elif c in ')}]':
                    if not stack:
                        print(f"   EXTRA closing '{c}' at line {actual_line}:{i+1}")
                    else:
                        top, top_line, top_col = stack.pop()
                        if pairs[c] != top:
                            print(f"   MISMATCHED '{c}' at line {actual_line}:{i+1}, expected closer for '{top}' from line {top_line}:{top_col}")
            elif in_string:
                if c == '\\':
                    i += 1 # skip escaped char
                elif c == str_char:
                    in_string = False
            elif in_comment:
                if c == '*' and i + 1 < len(line) and line[i+1] == '/':
                    in_comment = False
                    i += 1
            i += 1
            
    if stack:
        print(f"   UNCLOSED brackets/parentheses at end of script ({len(stack)}):")
        for top, top_line, top_col in stack[-5:]:
            print(f"     '{top}' opened at line {top_line}:{top_col}")
    else:
        print("   Braces/brackets/parentheses balance: PERFECT!")

# 3. Check for any unresolved variables, duplicate lets, or illegal statements
decl_pattern = re.compile(r'^\s*(?:let|const)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)', re.M)
top_decls = []
for lno, line in enumerate(script_content.splitlines()):
    m = re.match(r'^\s*(?:let|const)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)', line)
    if m:
        top_decls.append((m.group(1), script_start_line + lno, line.strip()))

dup_decls = Counter([d[0] for d in top_decls])
found_dups = {k: v for k, v in dup_decls.items() if v > 1}
print(f"\n3. Duplicate top-level let/const declarations ({len(found_dups)}):")
for k, v in found_dups.items():
    print(f"   Variable '{k}' declared {v} times:")
    for name, line_num, raw in top_decls:
        if name == k:
            print(f"     Line {line_num}: {raw}")
