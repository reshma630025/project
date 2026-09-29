with open('index.html', encoding='utf-8') as f:
    content = f.read()

import re

sections = re.findall(r'<section\s+class="page[^"]*"\s+id="([^"]+)"', content)
print("Sections found:", sections)

buttons = re.findall(r'<button[^>]*id="([^"]+)"', content)
print("\nButtons with IDs found:", sorted(buttons))

inputs = re.findall(r'<(?:input|textarea|select)[^>]*id="([^"]+)"', content)
print("\nInputs with IDs found:", sorted(inputs))
