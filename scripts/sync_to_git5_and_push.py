import os
import sys
import shutil
import subprocess
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC_DIR = Path(r"C:\Users\paruc\OneDrive\Desktop\Reshma")
DST_DIR = Path(r"C:\Users\paruc\OneDrive\Desktop\git5")
REPO_URL = "https://github.com/reshma630025/reshma1.git"
COMMIT_MSG = "Complete TrustGuard AI project"

print("==================================================", flush=True)
print("TRUSTGUARD AI — GITHUB PROJECT SYNC & PUSH", flush=True)
print(f"Source:      {SRC_DIR}", flush=True)
print(f"Destination: {DST_DIR}", flush=True)
print(f"Target Repo: {REPO_URL}", flush=True)
print("==================================================", flush=True)

# 1. Update .gitignore in Source & Destination
GITIGNORE_CONTENT = """# Python & Environment
__pycache__/
*.py[cod]
*$py.class
*.so
.env
.venv
env/
venv/
ENV/

# Node & Package Managers
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Datasets & Downloads
archive*/
*.zip
*.tar.gz
*.csv.gz

# Cache & Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDEs & System
.vscode/
.idea/
*.swp
*.swo
Thumbs.db
Desktop.ini
.DS_Store

# Temporary & Logs
*.log
*.tmp
*.temp
chrome_*_profile/
.system_generated/
scratch/
"""

(SRC_DIR / ".gitignore").write_text(GITIGNORE_CONTENT, encoding="utf-8")
(DST_DIR / ".gitignore").write_text(GITIGNORE_CONTENT, encoding="utf-8")
print("Updated .gitignore with comprehensive exclusion rules.", flush=True)

# 2. Sync files from SRC_DIR to DST_DIR
EXCLUDE_DIRS = {".git", "__pycache__", ".pytest_cache", ".idea", ".vscode"}
EXCLUDE_EXTS = {".log", ".tmp", ".pyc"}

copied_count = 0
for root, dirs, files in os.walk(SRC_DIR):
    rel_root = Path(root).relative_to(SRC_DIR)
    
    # Filter out excluded directories
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith("chrome_")]
    
    dest_dir = DST_DIR / rel_root
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    for f in files:
        if any(f.endswith(ext) for ext in EXCLUDE_EXTS):
            continue
        if f.startswith(".git"):
            continue
            
        src_file = Path(root) / f
        dst_file = dest_dir / f
        
        # Copy if destination doesn't exist or mtime/size differs
        if not dst_file.exists() or src_file.stat().st_mtime > dst_file.stat().st_mtime or src_file.stat().st_size != dst_file.stat().st_size:
            shutil.copy2(src_file, dst_file)
            copied_count += 1

print(f"Synced {copied_count} updated/new files to {DST_DIR}", flush=True)

GIT_BIN = r"C:\Users\paruc\AppData\Local\GitHubDesktop\app-3.6.5\resources\app\git\cmd\git.exe"
if not os.path.exists(GIT_BIN):
    GIT_BIN = r"C:\Users\paruc\AppData\Local\github-copilot-git-2.53.0-4\cmd\git.exe"

print(f"Using Git binary: {GIT_BIN}", flush=True)

# 3. Configure Git in DST_DIR
def run_git(args, check=True):
    cmd = [GIT_BIN] + args
    print(f">> Running: {' '.join(cmd)}", flush=True)
    res = subprocess.run(cmd, cwd=str(DST_DIR), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.stdout:
        print(res.stdout.strip(), flush=True)
    if res.stderr:
        print(f"[stderr] {res.stderr.strip()}", flush=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"Git command failed: {' '.join(cmd)} with code {res.returncode}")
    return res

# Check git init
if not (DST_DIR / ".git").exists():
    run_git(["init"])

# 4. Stage files
run_git(["add", "-A"])

# Verify what is staged and check sizes
status = run_git(["status", "--porcelain"], check=False).stdout
staged_files = [line[3:].strip() for line in status.splitlines() if line.startswith(("A ", "M ", "D "))]
print(f"Total staged files for commit: {len(staged_files)}", flush=True)

large_files = []
for rel_path in staged_files:
    fp = DST_DIR / rel_path
    if fp.is_file():
        size_mb = fp.stat().st_size / (1024 * 1024)
        if size_mb > 25.0:
            large_files.append((rel_path, size_mb))

if large_files:
    print("Files > 25MB:", large_files, flush=True)
else:
    print("No files exceed 25MB. Safe for GitHub push.", flush=True)

# 5. Commit
run_git(["commit", "-m", COMMIT_MSG], check=False)

# 6. Set branch to main
run_git(["branch", "-M", "main"])

# 7. Set remote origin
remotes = run_git(["remote", "-v"], check=False).stdout
if "origin" in remotes:
    run_git(["remote", "set-url", "origin", REPO_URL])
else:
    run_git(["remote", "add", "origin", REPO_URL])

print(f"Remote origin set to {REPO_URL}", flush=True)

# 8. Force Push to origin main
print("\nInitiating force push to GitHub...", flush=True)
push_res = run_git(["push", "-u", "origin", "main", "--force"], check=False)

if push_res.returncode == 0:
    print("\nSUCCESS: Complete project successfully pushed to https://github.com/reshma630025/reshma1.git", flush=True)
else:
    print(f"\nPush returned exit code: {push_res.returncode}", flush=True)

# 9. Final status verification
run_git(["status"])
