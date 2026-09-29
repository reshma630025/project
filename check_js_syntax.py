import re
import sys

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()
    lines = content.splitlines(keepends=True)

print(f"Total lines in index.html: {len(lines)}")
print(f"Total characters: {len(content)}")

# Find all script blocks with line numbers
script_blocks = []
in_script = False
start_line = 0
buf = []

for i, line in enumerate(lines, 1):
    if "<script>" in line or ("<script " in line and "src=" not in line):
        in_script = True
        start_line = i
        buf = []
        continue
    if "</script>" in line and in_script:
        in_script = False
        script_blocks.append((start_line, i, "".join(buf)))
        buf = []
        continue
    if in_script:
        buf.append(line)

print(f"Found {len(script_blocks)} inline script tag(s):")
for idx, (s, e, code) in enumerate(script_blocks, 1):
    print(f"  Block {idx}: lines {s} to {e} ({len(code.splitlines())} lines of code)")
