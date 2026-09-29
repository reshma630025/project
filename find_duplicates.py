import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('index.html', encoding='utf-8') as f:
    content = f.read()

script_m = re.findall(r'<script\b[^>]*>([\s\S]*?)</script>', content)
script = script_m[2]

lines = script.split('\n')
declarations = {}
for i, line in enumerate(lines):
    m = re.match(r'^(let|const|var)\s+([^;]+);', line.strip())
    if m:
        kind = m.group(1)
        rest = m.group(2)
        tokens = re.split(r'[,=]', rest)
        for tok in tokens:
            name = tok.strip().split()[0] if tok.strip() else ''
            name = re.sub(r'[^a-zA-Z0-9_$]', '', name)
            if name and not name[0].isdigit() and name not in ['true', 'false', 'null', 'undefined', 'new', 'function']:
                declarations.setdefault(name, []).append((i + 1, kind, line.strip()[:70]))

print("Top-level declarations appearing more than once:")
for name, entries in sorted(declarations.items()):
    if len(entries) > 1:
        print(f"\n[DUPLICATE] '{name}' ({len(entries)} times):")
        for line_num, kind, text in entries:
            print(f"   Line {line_num} [{kind}]: {text}")
