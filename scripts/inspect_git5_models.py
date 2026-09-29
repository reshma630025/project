import os
import sys
from pathlib import Path
import shutil

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

git5 = Path(r"C:\Users\paruc\OneDrive\Desktop\git5")
reshma = Path(r"C:\Users\paruc\OneDrive\Desktop\Reshma")

print(f"git5 exists: {git5.exists()}", flush=True)

# Check models in git5 vs Reshma
print(f"git5 models exists: {(git5 / 'models').exists()}", flush=True)
if (git5 / 'models').exists():
    for p in (git5 / 'models').rglob("*"):
        if p.is_file():
            print(f"  git5 model: {p.relative_to(git5)} ({p.stat().st_size} bytes)", flush=True)

print(f"Reshma models exists: {(reshma / 'models').exists()}", flush=True)
if (reshma / 'models').exists():
    for p in (reshma / 'models').rglob("*"):
        if p.is_file():
            print(f"  Reshma model: {p.relative_to(reshma)} ({p.stat().st_size} bytes)", flush=True)
