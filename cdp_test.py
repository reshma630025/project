import subprocess
import time
import json
import urllib.request
import tempfile
import os

user_data = os.path.join(tempfile.gettempdir(), 'chrome_test_profile')
chrome_cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--remote-debugging-port=9222",
    f"--user-data-dir={user_data}",
    "--disable-gpu",
    "--no-first-run",
    "http://127.0.0.1:8000"
]

proc = subprocess.Popen(chrome_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(3)

try:
    with urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=5) as resp:
        tabs = json.loads(resp.read().decode())
        print(f"Tabs count: {len(tabs)}")
        for t in tabs:
            print(f"Tab: {t.get('title')} ({t.get('url')}) - WS: {t.get('webSocketDebuggerUrl')}")
except Exception as e:
    print("Failed to reach CDP /json:", e)

proc.terminate()
