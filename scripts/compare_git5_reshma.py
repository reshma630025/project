import os
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

git5 = Path(r"C:\Users\paruc\OneDrive\Desktop\git5")
reshma = Path(r"C:\Users\paruc\OneDrive\Desktop\Reshma")

print(f"git5 mtime: {git5.stat().st_mtime}", flush=True)
print(f"Reshma mtime: {reshma.stat().st_mtime}", flush=True)

# Check index.html mtime in both
idx_git5 = git5 / "index.html"
idx_reshma = reshma / "index.html"
print(f"index.html git5 exists: {idx_git5.exists()} (size: {idx_git5.stat().st_size if idx_git5.exists() else 0}, mtime: {idx_git5.stat().st_mtime if idx_git5.exists() else 0})", flush=True)
print(f"index.html Reshma exists: {idx_reshma.exists()} (size: {idx_reshma.stat().st_size if idx_reshma.exists() else 0}, mtime: {idx_reshma.stat().st_mtime if idx_reshma.exists() else 0})", flush=True)

# Check git remotes in both
for name, p in [("git5", git5), ("Reshma", reshma)]:
    git_dir = p / ".git"
    print(f"{name} has .git: {git_dir.exists()}", flush=True)
    if git_dir.exists():
        cfg = git_dir / "config"
        if cfg.exists():
            print(f"--- {name} git config ---", flush=True)
            print(cfg.read_text(encoding="utf-8", errors="replace"), flush=True)
