import json
import os
import re
import subprocess
import tempfile
import time
import urllib.request
import websockets
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()
    full_html = "".join(lines)

print("Disk index.html line count:", len(lines))

# Find script tags
script_blocks = []
in_script = False
start_line = 0
current_block = []

for idx, line in enumerate(lines):
    if "<script>" in line or "<script " in line:
        if "src=" not in line:
            in_script = True
            start_line = idx + 1
            current_block = []
            continue
    if "</script>" in line and in_script:
        in_script = False
        end_line = idx + 1
        script_blocks.append((start_line, end_line, "".join(current_block)))
        current_block = []
        continue
    if in_script:
        current_block.append(line)

print(f"Found {len(script_blocks)} inline script blocks.")
for s, e, content in script_blocks:
    print(f"Block from line {s} to line {e} ({len(content.splitlines())} lines)")

# Launch Chrome to compileScript each block
user_data = os.path.join(tempfile.gettempdir(), 'chrome_compile_script_profile')
chrome_cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--remote-debugging-port=9226",
    f"--user-data-dir={user_data}",
    "--disable-gpu",
    "--no-first-run",
    "http://127.0.0.1:8000/"
]

proc = subprocess.Popen(chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2)

import asyncio

async def validate():
    try:
        req = urllib.request.Request("http://127.0.0.1:9226/json/new?http://127.0.0.1:8000/", method="PUT")
        with urllib.request.urlopen(req, timeout=5) as resp:
            tab = json.loads(resp.read().decode())

        ws_url = tab['webSocketDebuggerUrl']
        async with websockets.connect(ws_url) as ws:
            req_id = 0
            async def send(method, params=None):
                nonlocal req_id
                req_id += 1
                await ws.send(json.dumps({"id": req_id, "method": method, "params": params or {}}))
                while True:
                    raw = await ws.recv()
                    data = json.loads(raw)
                    if data.get("id") == req_id:
                        return data

            await send("Page.enable")
            await send("Runtime.enable")

            # Check for compilation errors
            for s, e, content in script_blocks:
                print(f"\nValidating script block (lines {s}-{e})...")
                res = await send("Runtime.compileScript", {
                    "expression": content,
                    "sourceURL": "index.html",
                    "persistScript": False
                })
                print("compileScript response:", json.dumps(res, indent=2))
                if "exceptionDetails" in res.get("result", {}):
                    ex = res["result"]["exceptionDetails"]
                    err_line = s + ex.get("lineNumber", 0)
                    print(f"--> SYNTAX ERROR at line {err_line}: {ex.get('text')} - {ex.get('exception', {}).get('description')}")
                else:
                    print(f"--> Script block (lines {s}-{e}) compiled successfully! No syntax errors.")
    finally:
        proc.terminate()

asyncio.run(validate())
