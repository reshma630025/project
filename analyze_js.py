import re
from collections import Counter

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find the main inline script
parts = text.split('<script>')
if len(parts) > 1:
    script_part = parts[1].split('</script>')[0]
    start_line = text[:text.find('<script>')].count('\n') + 1
    print(f"Main script starts at line {start_line}, length: {len(script_part.splitlines())} lines")
    
    # Check functions
    funcs = re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(', script_part)
    print(f"Total named functions: {len(funcs)}")
    dup_funcs = {k: v for k, v in Counter(funcs).items() if v > 1}
    print(f"Duplicate functions ({len(dup_funcs)}):", dup_funcs)
    
    # Check duplicate const/let
    lines = script_part.splitlines()
    decls = []
    for i, line in enumerate(lines):
        m = re.match(r'^\s*(?:let|const|var)\s+([a-zA-Z0-9_$]+)', line)
        if m:
            decls.append((m.group(1), start_line + i, line.strip()))
    
    dup_decls = {k: v for k, v in Counter([d[0] for d in decls]).items() if v > 1}
    print(f"Duplicate top-level declarations ({len(dup_decls)}):", dup_decls)
    for k in dup_decls:
        for name, lno, raw in decls:
            if name == k:
                print(f"   Line {lno}: {raw}")
else:
    print("Could not find <script> tag")
