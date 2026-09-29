import html.parser
import re

with open("index.html", "r", encoding="utf-8") as f:
    html_text = f.read()

# 1. HTML validity
class MyHTMLParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.tags = []
        self.open_tags = []
        self.errors = []
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        for k, v in attrs:
            if k == 'id' and v:
                self.ids.add(v)
    def handle_endtag(self, tag):
        pass

parser = MyHTMLParser()
parser.feed(html_text)
print("=== HTML VALIDATION ===")
print(f"Total HTML tags parsed: {len(parser.tags)}")
print(f"Total unique IDs found in DOM: {len(parser.ids)}")

# 2. Extract script
script_match = re.search(r'<script(?:\s+[^>]*)?>(.*?)</script>', html_text, re.DOTALL | re.IGNORECASE)
scripts = list(re.finditer(r'<script(?:\s+[^>]*)?>(.*?)</script>', html_text, re.DOTALL | re.IGNORECASE))
main_script = ""
for s in scripts:
    c = s.group(1).strip()
    if len(c) > 1000:
        main_script = c
        break

print("\n=== JS DOM ID REFERENCE VALIDATION ===")
# Find all document.getElementById('...')
referenced_ids = set(re.findall(r"document\.getElementById\(['\"]([a-zA-Z0-9_-]+)['\"]\)", main_script))
print(f"Total unique element IDs queried by getElementById: {len(referenced_ids)}")

missing_ids = []
for el_id in sorted(referenced_ids):
    if el_id not in parser.ids:
        # Check if it might be dynamically created or optional
        missing_ids.append(el_id)

print(f"Element IDs queried in JS but not in initial DOM ({len(missing_ids)}):")
for m in missing_ids:
    print(f"  - {m}")

# 3. Check for any duplicate top-level functions or variables in JS
print("\n=== JS SYNTAX SANITY ===")
# Check quotes & brackets
stack = []
tokens = {')': '(', '}': '{', ']': '['}
in_str = None
escape = False
line_no = 1
col = 1
errors = []

idx = 0
while idx < len(main_script):
    ch = main_script[idx]
    if ch == '\n':
        line_no += 1
        col = 1
        idx += 1
        continue
    
    # Simple comment skip
    if not in_str and ch == '/' and idx + 1 < len(main_script):
        if main_script[idx+1] == '/':
            # line comment
            end_nl = main_script.find('\n', idx)
            if end_nl == -1:
                break
            idx = end_nl
            continue
        elif main_script[idx+1] == '*':
            # block comment
            end_c = main_script.find('*/', idx + 2)
            if end_c == -1:
                errors.append(f"Unterminated block comment starting at line {line_no}")
                break
            line_no += main_script[idx:end_c+2].count('\n')
            idx = end_c + 2
            continue

    if in_str:
        if escape:
            escape = False
        elif ch == '\\':
            escape = True
        elif ch == in_str:
            in_str = None
    else:
        if ch in ('"', "'", '`'):
            in_str = ch
        elif ch in ('(', '{', '['):
            stack.append((ch, line_no))
        elif ch in (')', '}', ']'):
            if not stack or stack[-1][0] != tokens[ch]:
                errors.append(f"Mismatched closing '{ch}' at line {line_no} (expected matching for {stack[-1] if stack else 'none'})")
            else:
                stack.pop()
    idx += 1
    col += 1

if stack:
    for unclosed in stack:
        errors.append(f"Unclosed '{unclosed[0]}' from line {unclosed[1]}")

if errors:
    print(f"Found {len(errors)} syntax balance errors:")
    for e in errors:
        print("  *", e)
else:
    print("Zero syntax balance errors! All parentheses, brackets, braces, strings, and comments match cleanly.")
