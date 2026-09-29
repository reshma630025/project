import asyncio
import json
import os
import subprocess
import tempfile
import time
import urllib.request
import websockets

user_data = os.path.join(tempfile.gettempdir(), 'chrome_debug_profile_88')
chrome_cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--remote-debugging-port=9223",
    f"--user-data-dir={user_data}",
    "--disable-gpu",
    "--no-first-run",
    "http://127.0.0.1:8000/"
]

proc = subprocess.Popen(chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2)

async def main():
    try:
        # Get list of targets
        req = urllib.request.Request("http://127.0.0.1:9223/json", method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            tabs = json.loads(resp.read().decode())
        
        target_tab = None
        for t in tabs:
            if t.get('type') == 'page':
                target_tab = t
                break
        
        if not target_tab:
            print("No page tab found!")
            return

        ws_url = target_tab['webSocketDebuggerUrl']
        print("Connected to tab:", target_tab.get('url'))

        async with websockets.connect(ws_url) as ws:
            req_id = 0
            async def send(method, params=None):
                nonlocal req_id
                req_id += 1
                msg = {"id": req_id, "method": method, "params": params or {}}
                await ws.send(json.dumps(msg))
                while True:
                    raw = await ws.recv()
                    data = json.loads(raw)
                    if data.get("id") == req_id:
                        return data

            await send("Console.enable")
            await send("Runtime.enable")
            await send("Page.enable")
            
            # Wait for page to fully load
            await asyncio.sleep(2)

            res = await send("Runtime.evaluate", {
                "expression": "JSON.stringify({href: window.location.href, title: document.title, htmlLen: document.documentElement.outerHTML.length, navitems: document.querySelectorAll('.navitem').length})",
                "returnByValue": True
            })
            print("Full res:", json.dumps(res, indent=2))

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(main())
