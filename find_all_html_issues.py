import re
from html.parser import HTMLParser

with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

lines = html_content.splitlines()

# Void elements that do not require closing tags in HTML5
VOID_ELEMENTS = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
    'link', 'meta', 'param', 'source', 'track', 'wbr'
}

class DetailedHTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tag_stack = []
        self.errors = []
        self.warnings = []
        
    def handle_starttag(self, tag, attrs):
        pos = self.getpos()
        # Check duplicate attributes
        attr_names = [a[0].lower() for a in attrs]
        if len(attr_names) != len(set(attr_names)):
            dups = [x for x in attr_names if attr_names.count(x) > 1]
            self.errors.append(f"Line {pos[0]}: Duplicate attribute '{dups[0]}' in <{tag}>")
        
        if tag.lower() not in VOID_ELEMENTS:
            self.tag_stack.append((tag.lower(), pos[0]))
            
    def handle_endtag(self, tag):
        pos = self.getpos()
        t = tag.lower()
        if t in VOID_ELEMENTS:
            self.warnings.append(f"Line {pos[0]}: Closing tag </{t}> for void element")
            return
            
        if not self.tag_stack:
            self.errors.append(f"Line {pos[0]}: Unexpected closing tag </{t}> with empty stack")
            return
            
        expected, start_line = self.tag_stack[-1]
        if expected == t:
            self.tag_stack.pop()
        else:
            # Look up stack to see if it's an unclosed ancestor
            found_idx = None
            for idx in range(len(self.tag_stack) - 1, -1, -1):
                if self.tag_stack[idx][0] == t:
                    found_idx = idx
                    break
            if found_idx is not None:
                # Tags between found_idx and top were unclosed
                unclosed = self.tag_stack[found_idx + 1:]
                for ut, ul in unclosed:
                    self.errors.append(f"Line {pos[0]}: Tag <{ut}> opened at line {ul} was never closed before </{t}>")
                self.tag_stack = self.tag_stack[:found_idx]
            else:
                self.errors.append(f"Line {pos[0]}: Unexpected closing tag </{t}> (expected </{expected}> opened at line {start_line})")

validator = DetailedHTMLValidator()
validator.feed(html_content)

print(f"Total HTML errors found: {len(validator.errors)}")
for e in validator.errors[:30]:
    print("  ERROR:", e)

if validator.tag_stack:
    print(f"\nUnclosed tags remaining at EOF ({len(validator.tag_stack)}):")
    for ut, ul in validator.tag_stack:
        print(f"  Unclosed <{ut}> opened at line {ul}")
else:
    print("\nZero unclosed tags at EOF!")

print(f"\nTotal warnings: {len(validator.warnings)}")
for w in validator.warnings[:10]:
    print("  WARN:", w)
