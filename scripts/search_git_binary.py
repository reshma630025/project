import os
import sys
from pathlib import Path

search_roots = [
    Path(r"C:\Users\paruc"),
    Path(r"C:\Program Files"),
    Path(r"C:\Program Files (x86)"),
    Path(r"C:\ProgramData"),
    Path(r"C:\tools")
]

found = []
for root in search_roots:
    if not root.exists():
        continue
    print(f"Searching {root} for git.exe...", flush=True)
    try:
        for p in root.rglob("git.exe"):
            # Skip temp or cache
            if "AppData\\Local\\Temp" not in str(p):
                found.append(str(p))
                print("FOUND:", p, flush=True)
                if len(found) >= 5:
                    break
    except Exception as e:
        print(f"Error scanning {root}: {e}", flush=True)
    if found:
        break

print("All found git binaries:", found, flush=True)
