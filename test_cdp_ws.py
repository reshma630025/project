import subprocess
import time
import json
import urllib.request
import tempfile
import os
import asyncio
import websockets

user_data = os.path.join(tempfile.gettempdir(), 'chrome_test_profile')
chrome_cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--remote-debugging-port=9222",
    f"--user-data-dir={user_data}",
    "--disable-gpu",
    "--disable-extensions",
    "--no-first-run",
    "http://127.0.0.1:8000"
]

proc = subprocess.Popen(chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(3)

async def main():
    try:
        with urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=5) as resp:
            tabs = json.loads(resp.read().decode())
        target_tab = next((t for t in tabs if '8000' in t.get('url', '')), tabs[0])
        ws_url = target_tab['webSocketDebuggerUrl']
        print(f"Connecting to: {ws_url}", flush=True)
        async with websockets.connect(ws_url) as ws:
            print("Connected!", flush=True)
            msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": "document.title", "returnByValue": True}}
            await ws.send(json.dumps(msg))
            resp = await ws.recv()
            print("Received:", resp, flush=True)
    except Exception as e:
        print("Error:", e, flush=True)
    finally:
        proc.terminate()

asyncio.run(main())
