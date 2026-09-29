import subprocess
import os
import ctypes
from ctypes import wintypes

GIT_EXE = r"C:\Users\paruc\AppData\Local\GitHubDesktop\app-3.6.5\resources\app\git\cmd\git.exe"

# 1. Clean up scratch scripts
scratch = [
    "check_cred_helper.py",
    "check_creds.py",
    "check_processes.py",
    "find_gh_helpers.py",
    "query_creds.py",
    "read_gh_token.py",
    "test_push_auth.py",
    "do_push.py",
    "prepare_and_push.py",
    "debug_git.py"
]
for f in scratch:
    if os.path.exists(f):
        try:
            os.remove(f)
            print("Removed scratch:", f)
        except Exception:
            pass

# 2. Get GitHub token from Windows Credential Manager
advapi32 = ctypes.windll.advapi32

class CREDENTIAL_ATTRIBUTE(ctypes.Structure):
    _fields_ = [
        ('Keyword', wintypes.LPWSTR),
        ('Flags', wintypes.DWORD),
        ('ValueSize', wintypes.DWORD),
        ('Value', ctypes.c_char_p)
    ]

class CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ('Flags', wintypes.DWORD),
        ('Type', wintypes.DWORD),
        ('TargetName', wintypes.LPWSTR),
        ('Comment', wintypes.LPWSTR),
        ('LastWritten', wintypes.FILETIME),
        ('CredentialBlobSize', wintypes.DWORD),
        ('CredentialBlob', ctypes.POINTER(ctypes.c_char)),
        ('Persist', wintypes.DWORD),
        ('AttributeCount', wintypes.DWORD),
        ('Attributes', ctypes.POINTER(CREDENTIAL_ATTRIBUTE)),
        ('TargetAlias', wintypes.LPWSTR),
        ('UserName', wintypes.LPWSTR)
    ]

PCREDENTIAL = ctypes.POINTER(CREDENTIAL)
CredRead = advapi32.CredReadW
CredRead.argtypes = [wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(PCREDENTIAL)]
CredRead.restype = wintypes.BOOL
CredFree = advapi32.CredFree
CredFree.argtypes = [ctypes.c_void_p]

target = "GitHub - https://api.github.com/reshma630025"
cred_ptr = PCREDENTIAL()

if not CredRead(target, 1, 0, ctypes.byref(cred_ptr)):
    print("Error: Could not read credentials from Windows Credential Manager")
    exit(1)

cred = cred_ptr.contents
raw_blob = ctypes.string_at(cred.CredentialBlob, cred.CredentialBlobSize)
token = raw_blob.decode('utf-8', errors='ignore')
username = cred.UserName
CredFree(cred_ptr)

print(f"Loaded credentials for: {username}")

def run_git(args, mask=None):
    display_cmd = list(args)
    if mask:
        display_cmd = [x.replace(mask, "***") for x in display_cmd]
    print(f"\n>>> Running: git {' '.join(display_cmd)}")
    res = subprocess.run([GIT_EXE] + args, capture_output=True, text=True)
    if res.stdout:
        out = res.stdout.strip()
        if mask:
            out = out.replace(mask, "***")
        print(out)
    if res.stderr:
        err = res.stderr.strip()
        if mask:
            err = err.replace(mask, "***")
        print(err)
    print(f"EXIT CODE: {res.returncode}")
    return res

# 3. Stage any remaining changes and commit
run_git(["add", "-A"])
status_res = run_git(["status", "--porcelain"])
if status_res.stdout.strip():
    run_git(["commit", "-m", "TrustGuard AI full functional platform"])

# 4. Set clean remote URLs
TARGET_URL = "https://github.com/reshma630025/reshma.git"
run_git(["remote", "set-url", "origin", TARGET_URL])

# 5. Push using authenticated URL
auth_url = f"https://{username}:{token}@github.com/reshma630025/reshma.git"
print("\n>>> Pushing code to GitHub...")
push_res = run_git(["push", "--force", auth_url, "main:main"], mask=token)

if push_res.returncode == 0:
    print("\n=======================================================")
    print("SUCCESS: Code successfully force-pushed to:")
    print(TARGET_URL)
    print("=======================================================")
else:
    print(f"\nPush failed with code: {push_res.returncode}")

# Ensure clean remote URL in local git config
run_git(["remote", "set-url", "origin", TARGET_URL])
run_git(["remote", "-v"])
