import re

with open('scratch_main_script.js', encoding='utf-8') as f:
    script = f.read()

with open('index.html', encoding='utf-8') as f:
    html = f.read()

calls = re.findall(r'document\.getElementById\([\'"]([^\'"]+)[\'"]\)(\s*\??\.)', script)
print(f"Total getElementById calls: {len(calls)}")

missing_without_opt = []
missing_with_opt = []
for gid, dot in calls:
    pattern1 = f'id="{gid}"'
    pattern2 = f"id='{gid}'"
    if pattern1 not in html and pattern2 not in html:
        if '?.' in dot:
            missing_with_opt.append(gid)
        else:
            missing_without_opt.append(gid)

print(f"\nCRITICAL: Missing IDs accessed WITHOUT optional chaining: {len(set(missing_without_opt))}")
for gid in sorted(set(missing_without_opt)):
    print("  ❌", gid)

print(f"\nMissing IDs accessed WITH optional chaining: {len(set(missing_with_opt))}")
for gid in sorted(set(missing_with_opt)):
    print("  ⚠️", gid)

# Listeners attached without optional chaining
listeners = re.findall(r'document\.getElementById\([\'"]([^\'"]+)[\'"]\)\.addEventListener', script)
print(f"\nListeners attached without optional chaining: {len(listeners)}")
for lid in sorted(set(listeners)):
    if f'id="{lid}"' not in html and f"id='{lid}'" not in html:
        print(f"  ❌ CRASH: document.getElementById('{lid}').addEventListener(...) - '{lid}' is missing in HTML!")
