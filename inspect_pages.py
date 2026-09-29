import re

with open('index.html', encoding='utf-8') as f:
    content = f.read()

# Look for top-level pages
top_pages = re.findall(r'<section[^>]*id=["\'](page-[^"\']+)["\'][^>]*>', content)
print(f"Top-level section pages found ({len(top_pages)}):")
for p in top_pages:
    print("  id =", p)

# Check all sidebar items in index.html
sidebar_match = re.search(r'<aside[^>]*id=["\']sidebar["\'][^>]*>([\s\S]*?)</aside>', content)
if sidebar_match:
    sidebar_html = sidebar_match.group(1)
    items = re.findall(r'data-page=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</li>', sidebar_html)
    print(f"\nSidebar items ({len(items)}):")
    for page_key, label_html in items:
        # strip svg
        label = re.sub(r'<[^>]+>', '', label_html).strip()
        has_section = f"page-{page_key}" in top_pages
        print(f"  data-page='{page_key}' [{label}] -> id='page-{page_key}': {'EXISTS' if has_section else 'MISSING SECTION!'}")

# Check any errors or unclosed elements or duplicate IDs
print("\nChecking all IDs in index.html for duplicates:")
all_ids = re.findall(r'\bid=["\']([^"\']+)["\']', content)
from collections import Counter
counts = Counter(all_ids)
duplicates = {k: v for k, v in counts.items() if v > 1}
if duplicates:
    print("Duplicate IDs found:", duplicates)
else:
    print("No duplicate IDs found.")
