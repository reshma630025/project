"""
TrustGuard AI — Task Scheduler Registration Script
Registers the TrustGuardAI-AutoStart task in Windows Task Scheduler using clean subprocess argument arrays.
"""
import os
import subprocess
import sys

def register_task():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    vbs_path = os.path.join(project_root, "start_trustguard_background.vbs")
    
    cmd = [
        "schtasks", "/create",
        "/tn", "TrustGuardAI-AutoStart",
        "/tr", f'wscript.exe "{vbs_path}"',
        "/sc", "ONLOGON",
        "/f"
    ]
    
    print(f"Executing: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Exit Code: {res.returncode}")
    print(f"STDOUT: {res.stdout.strip()}")
    print(f"STDERR: {res.stderr.strip()}")
    
    return res.returncode == 0

if __name__ == "__main__":
    success = register_task()
    sys.exit(0 if success else 1)
