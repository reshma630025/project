import re
import subprocess
import tempfile
import os

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find the main inline script block
m = re.search(r'<script(?:\s+[^>]*)?>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
# We know block 3 was the main script
script_tags = list(re.finditer(r'<script(?:\s+[^>]*)?>(.*?)</script>', content, re.DOTALL | re.IGNORECASE))
main_script = None
for s in script_tags:
    code = s.group(1).strip()
    if len(code) > 1000:
        main_script = code
        break

if not main_script:
    print("Could not find main script")
    exit(1)

with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as tf:
    tf.write(main_script)
    temp_path = tf.name

try:
    proc = subprocess.run(["node", "-c", temp_path], capture_output=True, text=True)
    print("Return code:", proc.returncode)
    print("STDOUT:", proc.stdout)
    print("STDERR:", proc.stderr)
finally:
    if os.path.exists(temp_path):
        os.remove(temp_path)
