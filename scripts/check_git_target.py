import os
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

p_git5 = Path(r"C:\Users\paruc\OneDrive\Desktop\git5")
p_reshma = Path(r"C:\Users\paruc\OneDrive\Desktop\Reshma")

print(f"git5 exists: {p_git5.exists()}", flush=True)
if p_git5.exists():
    files = list(p_git5.glob("*"))
    print(f"git5 item count: {len(files)}", flush=True)
    for f in files[:10]:
        print(f"  git5: {f.name}", flush=True)

print(f"Reshma exists: {p_reshma.exists()}", flush=True)
if p_reshma.exists():
    files = list(p_reshma.glob("*"))
    print(f"Reshma item count: {len(files)}", flush=True)
