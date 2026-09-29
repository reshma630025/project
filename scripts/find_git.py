import os
import shutil

git_path = shutil.which("git")
print("shutil.which('git'):", git_path)

common_paths = [
    r"C:\Program Files\Git\cmd\git.exe",
    r"C:\Program Files\Git\bin\git.exe",
    r"C:\Program Files (x86)\Git\cmd\git.exe",
    r"C:\Users\paruc\AppData\Local\Programs\Git\cmd\git.exe"
]
for p in common_paths:
    print(p, "exists:", os.path.exists(p))
