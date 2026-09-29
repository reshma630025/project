import asyncio
import json
import os
import subprocess
import tempfile
import time
import urllib.request
import websockets

user_data = os.path.join(tempfile.gettempdir(), 'chrome_fresh_soc_profile')
chrome_cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--remote-debugging-port=9222",
    f"--user-data-dir={user_data}",
    "--disable-gpu",
    "--no-first-run",
    "about:blank"
]

proc = subprocess.Popen(chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2)

async def main():
    try:
        # Create a new tab navigating to http://127.0.0.1:8000/
        req = urllib.request.Request("http://127.0.0.1:9222/json/new?http://127.0.0.1:8000/", method="PUT")
        with urllib.request.urlopen(req, timeout=5) as resp:
            new_tab = json.loads(resp.read().decode())
        
        ws_url = new_tab['webSocketDebuggerUrl']
        print("Connected to TrustGuard tab:", new_tab.get('url'))

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

            await send("Page.enable")
            await send("Runtime.enable")
            await send("Page.navigate", {"url": "http://127.0.0.1:8000/"})
            await asyncio.sleep(4)

            # Check title and elements
            title_res = await send("Runtime.evaluate", {"expression": "document.title", "returnByValue": True})
            print("Document Title:", title_res.get("result", {}).get("value"))

            sidebar_pages = [
                'dashboard', 'deepfake', 'image', 'video', 'audio',
                'text', 'job', 'url', 'ocr', 'company', 'social',
                'camera', 'mic', 'protect', 'reports', 'history',
                'profile', 'settings'
            ]

            print(f"\n{'PAGE KEY':<12} | {'CLICK TARGET':<15} | {'SECTION ID':<15} | {'IS ACTIVE?':<10} | {'DISPLAY STYLE'}")
            print("-" * 75)

            for key in sidebar_pages:
                res = await send("Runtime.evaluate", {
                    "expression": f"""(() => {{
                        const el = document.querySelector('.navitem[data-page="{key}"]');
                        if (!el) return {{ found: false }};
                        el.click();
                        const sec = document.getElementById('page-{key}');
                        if (!sec) return {{ found: true, sectionExists: false }};
                        const isActive = sec.classList.contains('active');
                        const disp = window.getComputedStyle(sec).display;
                        return {{
                            found: true,
                            sectionExists: true,
                            isActive,
                            display: disp
                        }};
                    }})()""",
                    "returnByValue": True
                })
                inner_result = res.get("result", {})
                if "result" in inner_result:
                    val = inner_result["result"].get("value", {})
                else:
                    val = inner_result.get("value", {})
                if not val.get("found"):
                    status = "NAVITEM NOT FOUND"
                    sec_id = f"page-{key}"
                    active = "NO"
                    disp = "N/A"
                elif not val.get("sectionExists"):
                    status = "FOUND"
                    sec_id = f"page-{key} (MISSING)"
                    active = "NO"
                    disp = "MISSING"
                else:
                    status = "FOUND"
                    sec_id = f"page-{key}"
                    active = "YES" if val.get("isActive") else "NO"
                    disp = val.get("display")

                print(f"{key:<12} | {status:<15} | {sec_id:<15} | {active:<10} | {disp}")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(main())
