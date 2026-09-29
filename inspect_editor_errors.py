import html.parser
import re

with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

lines = html_content.splitlines(keepends=True)
print(f"Total lines: {len(lines)}")

# 1. HTML check
class HTMLValidator(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.tags = []
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
    def handle_endtag(self, tag):
        pass

validator = HTMLValidator()
try:
    validator.feed(html_content)
    print("HTML Parser: clean, no structural parsing exceptions")
except Exception as e:
    print("HTML Parser error:", e)

# 2. Extract script tags
script_tags = list(re.finditer(r'<script(?:\s+[^>]*)?>(.*?)</script>', html_content, re.DOTALL | re.IGNORECASE))
print(f"Total inline <script> blocks found: {len(script_tags)}")

for i, match in enumerate(script_tags):
    js_text = match.group(1)
    start_pos = match.start()
    line_no = html_content[:start_pos].count('\n') + 1
    end_line_no = line_no + js_text.count('\n')
    print(f"\nScript Block {i+1}: lines {line_no} to {end_line_no} ({len(js_text)} chars)")
    
    # Check brace/bracket/paren balances in this script block
    # Note: Strings and regexes can contain braces, so let's strip strings and comments first
    # Simple tokenizer to strip comments and strings
    in_single_quote = False
    in_double_quote = False
    in_backtick = False
    in_line_comment = False
    in_block_comment = False
    
    clean_chars = []
    idx = 0
    paren_stack = []
    brace_stack = []
    bracket_stack = []
    
    errors = []
    
    while idx < len(js_text):
        c = js_text[idx]
        nxt = js_text[idx+1] if idx+1 < len(js_text) else ''
        
        if in_line_comment:
            if c == '\n':
                in_line_comment = False
            idx += 1
            continue
        if in_block_comment:
            if c == '*' and nxt == '/':
                in_block_comment = False
                idx += 2
                continue
            idx += 1
            continue
        if in_single_quote:
            if c == '\\':
                idx += 2
                continue
            if c == "'":
                in_single_quote = False
            idx += 1
            continue
        if in_double_quote:
            if c == '\\':
                idx += 2
                continue
            if c == '"':
                in_double_quote = False
            idx += 1
            continue
        if in_backtick:
            if c == '\\':
                idx += 2
                continue
            if c == '`':
                in_backtick = False
            idx += 1
            continue
            
        # Not in string or comment
        if c == '/' and nxt == '/':
            in_line_comment = True
            idx += 2
            continue
        if c == '/' and nxt == '*':
            in_block_comment = True
            idx += 2
            continue
        if c == "'":
            in_single_quote = True
            idx += 1
            continue
        if c == '"':
            in_double_quote = True
            idx += 1
            continue
        if c == '`':
            in_backtick = True
            idx += 1
            continue
            
        # Track line number of current char
        char_line = line_no + js_text[:idx].count('\n')
        
        if c == '(':
            paren_stack.append((char_line, c))
        elif c == ')':
            if not paren_stack:
                errors.append(f"Unmatched closing ')' at line {char_line}")
            else:
                paren_stack.pop()
        elif c == '{':
            brace_stack.append((char_line, c))
        elif c == '}':
            if not brace_stack:
                errors.append(f"Unmatched closing '}}' at line {char_line}")
            else:
                brace_stack.pop()
        elif c == '[':
            bracket_stack.append((char_line, c))
        elif c == ']':
            if not bracket_stack:
                errors.append(f"Unmatched closing ']' at line {char_line}")
            else:
                bracket_stack.pop()
                
        idx += 1

    if in_single_quote:
        errors.append("Unclosed single quote at end of script")
    if in_double_quote:
        errors.append("Unclosed double quote at end of script")
    if in_backtick:
        errors.append("Unclosed backtick template literal at end of script")
    if in_block_comment:
        errors.append("Unclosed block comment at end of script")
    for l, ch in paren_stack:
        errors.append(f"Unclosed '(' opened at line {l}")
    for l, ch in brace_stack:
        errors.append(f"Unclosed '{{' opened at line {l}")
    for l, ch in bracket_stack:
        errors.append(f"Unclosed '[' opened at line {l}")
        
    print(f"Brace/Bracket/String parser found {len(errors)} issues:")
    for err in errors[:20]:
        print("  -", err)
