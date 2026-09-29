import os
from pathlib import Path

dl_path = Path(r"C:\Users\paruc\Downloads")
print(f"Scanning {dl_path} for social media or instagram datasets...\n", flush=True)

for item in sorted(dl_path.iterdir()):
    name_lower = item.name.lower()
    if any(k in name_lower for k in ["social", "insta", "profile", "spammer", "fake", "account", "archive"]):
        is_dir = item.is_dir()
        size = ""
        if not is_dir:
            size = f" ({round(item.stat().st_size / (1024*1024), 2)} MB)"
        print(f"[{'DIR' if is_dir else 'FILE'}] {item.name}{size}", flush=True)
