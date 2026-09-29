import re
import subprocess
import os

with open(r'C:\Users\paruc\OneDrive\Desktop\project\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
for i, script in enumerate(scripts):
    with open(f'script_{i}.js', 'w', encoding='utf-8') as sf:
        sf.write(script)
    result = subprocess.run(['node', '--check', f'script_{i}.js'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error in script {i}:")
        print(result.stderr)
    else:
        print(f"Script {i} is OK")
