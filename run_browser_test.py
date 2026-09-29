import asyncio
import json
import os
import subprocess
import tempfile
import time
import urllib.request
import websockets

user_data = os.path.join(tempfile.gettempdir(), 'chrome_cdp_profile')
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
        with urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=5) as resp:
            tabs = json.loads(resp.read().decode())
        ws_url = None
        for t in tabs:
            if t.get('type') == 'page' and t.get('webSocketDebuggerUrl'):
                ws_url = t['webSocketDebuggerUrl']
                break
        
        if not ws_url:
            print("No page tab found in Chrome!")
            return

        async with websockets.connect(ws_url) as ws:
            req_id = 0
            
            async def send(method, params=None):
                nonlocal req_id
                req_id += 1
                msg = {"id": req_id, "method": method, "params": params or {}}
                await ws.send(json.dumps(msg))
                return req_id

            # Enable Console, Runtime, Page, Network
            await send("Console.enable")
            await send("Runtime.enable")
            await send("Page.enable")
            await send("Network.enable")
            await send("Network.setCacheDisabled", {"cacheDisabled": True})
            
            console_logs = []
            exceptions = []

            # Background listener
            async def listen():
                try:
                    while True:
                        raw = await ws.recv()
                        msg = json.loads(raw)
                        method = msg.get("method")
                        if method == "Console.messageAdded":
                            console_logs.append(msg["params"]["message"])
                        elif method == "Runtime.consoleAPICalled":
                            console_logs.append(msg["params"])
                        elif method == "Runtime.exceptionThrown":
                            exceptions.append(msg["params"])
                except asyncio.CancelledError:
                    pass
                except Exception as e:
                    pass

            listen_task = asyncio.create_task(listen())

            print("Navigating to http://127.0.0.1:8000/ ...")
            await send("Page.navigate", {"url": "http://127.0.0.1:8000/"})
            await asyncio.sleep(4)

            # Evaluate checking page state
            eval_res_id = await send("Runtime.evaluate", {
                "expression": """(() => {
                    const pages = Array.from(document.querySelectorAll('.page')).map(p => ({
                        id: p.id,
                        active: p.classList.contains('active'),
                        display: window.getComputedStyle(p).display
                    }));
                    const activePage = pages.find(p => p.active);
                    return {
                        title: document.title,
                        activePage: activePage ? activePage.id : 'NONE',
                        allPagesCount: pages.length,
                        hasGotoPage: typeof window.gotoPage === 'function' || typeof gotoPage === 'function',
                        hasAPI: typeof window.tgAPI !== 'undefined'
                    };
                })()""",
                "returnByValue": True
            })

            await asyncio.sleep(1)

            listen_task.cancel()

            print("\n=== CONSOLE LOGS & ERRORS ===")
            if not console_logs and not exceptions:
                print("No console logs or errors captured.")
            for cl in console_logs:
                print("CONSOLE:", cl)
            for ex in exceptions:
                print("EXCEPTION:", json.dumps(ex, indent=2))

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(main())
