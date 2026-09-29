import asyncio
import json
import os
import subprocess
import tempfile
import time
import urllib.request
import websockets
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

user_data = os.path.join(tempfile.gettempdir(), 'chrome_live_val_profile_2')
port = 9229
chrome_cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    f"--remote-debugging-port={port}",
    f"--user-data-dir={user_data}",
    "--disable-gpu",
    "--no-first-run",
    "http://127.0.0.1:8000/"
]

proc = subprocess.Popen(chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2.5)

console_messages = []
exceptions = []

async def main():
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{port}/json", method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            tabs = json.loads(resp.read().decode())
        
        target_tab = None
        for t in tabs:
            if t.get('type') == 'page':
                target_tab = t
                break
        
        if not target_tab:
            print("ERROR: No Chrome page tab found!")
            return
        
        ws_url = target_tab['webSocketDebuggerUrl']
        print(f"Connected to Chrome tab: {ws_url}")
        
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
                    if "method" in data:
                        if data["method"] == "Runtime.consoleAPICalled":
                            args = [str(a.get('value', a.get('description', ''))) for a in data["params"]["args"]]
                            msg_text = " ".join(args)
                            console_messages.append((data["params"]["type"], msg_text))
                        elif data["method"] == "Runtime.exceptionThrown":
                            ex = data["params"]["exceptionDetails"]
                            exceptions.append(ex)
                    if data.get("id") == req_id:
                        return data

            async def eval_js(expression):
                res = await send("Runtime.evaluate", {
                    "expression": expression,
                    "returnByValue": True,
                    "awaitPromise": True
                })
                # In CDP, res["result"]["result"]["value"]
                inner = res.get("result", {}).get("result", {})
                return inner.get("value")

            await send("Console.enable")
            await send("Runtime.enable")
            await send("Page.enable")
            
            # Navigate cleanly to http://127.0.0.1:8000/
            await send("Page.navigate", {"url": "http://127.0.0.1:8000/"})
            await asyncio.sleep(2.5)
            
            # 1. Check title and basic state
            doc_title = await eval_js("document.title")
            print(f"Page Title: {doc_title}")
            
            # 2. Check API initialization
            api_init = await eval_js("typeof window.tgAPI !== 'undefined'")
            print(f"window.tgAPI initialized: {api_init}")
            
            # 3. Check for any JS parser/compile exceptions
            print(f"\nExceptions on initial load: {len(exceptions)}")
            for ex in exceptions:
                print(f"  [EXCEPTION]: {ex.get('text')} - {ex.get('exception', {}).get('description')}")
            
            # 4. Test Sidebar Navigation Buttons
            pages = [
                'dashboard', 'deepfake', 'image', 'video', 'audio',
                'text', 'job', 'url', 'ocr', 'company',
                'social', 'camera', 'mic', 'protect', 'reports',
                'history', 'profile', 'settings'
            ]
            
            print(f"\nTesting navigation for all {len(pages)} sidebar modules:")
            nav_success = 0
            for p in pages:
                res = await eval_js(f"""
                    (() => {{
                        const btn = document.querySelector(`.navitem[data-page='{p}']`);
                        if (!btn) return 'BUTTON_NOT_FOUND';
                        btn.click();
                        const targetSection = document.getElementById('page-{p}');
                        if (!targetSection) return 'SECTION_NOT_FOUND';
                        const isActive = targetSection.classList.contains('active');
                        return isActive ? 'OK' : 'NOT_ACTIVE';
                    }})()
                """)
                if res == 'OK':
                    nav_success += 1
                    print(f"  ✓ Module '{p}' -> section #page-{p} ACTIVE")
                else:
                    print(f"  ✗ Module '{p}' FAILED: {res}")
            
            print(f"\nNavigation Result: {nav_success}/{len(pages)} modules switched successfully.")
            
            # 5. Test Text Analysis submission
            print("\nTesting Text & Scam Detection analysis flow...")
            text_res = await eval_js("""
                (async () => {
                    const input = document.getElementById('scamTextInput');
                    const btn = document.getElementById('analyzeTextBtn');
                    if (!input || !btn) return 'INPUT_OR_BTN_MISSING';
                    input.value = 'URGENT: Your bank account is suspended. Click http://secure-update-verify.com to verify password immediately.';
                    btn.click();
                    for (let i = 0; i < 25; i++) {
                        await new Promise(r => setTimeout(r, 200));
                        const resCard = document.getElementById('textResult');
                        if (resCard && resCard.classList.contains('show')) {
                            return resCard.innerText.slice(0, 180).replace(/\\n+/g, ' ');
                        }
                    }
                    return 'TIMEOUT';
                })()
            """)
            print(f"Text Analysis Output: {text_res}")
            
            # 6. Test URL Analysis submission
            print("\nTesting URL Scanner analysis flow...")
            url_res = await eval_js("""
                (async () => {
                    const input = document.getElementById('urlInput');
                    const btn = document.getElementById('urlScanBtn');
                    if (!input || !btn) return 'INPUT_OR_BTN_MISSING';
                    input.value = 'http://127.0.0.1:8000';
                    btn.click();
                    for (let i = 0; i < 25; i++) {
                        await new Promise(r => setTimeout(r, 200));
                        const resCard = document.getElementById('urlResult');
                        if (resCard && resCard.classList.contains('show')) {
                            return resCard.innerText.slice(0, 180).replace(/\\n+/g, ' ');
                        }
                    }
                    return 'TIMEOUT';
                })()
            """)
            print(f"URL Scanner Output: {url_res}")

            # 7. Test Job / Internship Analysis flow
            print("\nTesting Job / Internship analysis flow...")
            job_res = await eval_js("""
                (async () => {
                    const title = document.getElementById('jobTitle');
                    const comp = document.getElementById('jobCompany');
                    const desc = document.getElementById('jobDescription');
                    const fee = document.getElementById('jobFee');
                    const btn = document.getElementById('analyzeJobBtn');
                    if (!title || !btn) return 'JOB_INPUT_MISSING';
                    title.value = 'Data Entry Specialist';
                    if (comp) comp.value = 'QuickPay LLC';
                    if (desc) desc.value = 'Work 2 hours daily, earn $5000/week! Telegram interview only.';
                    if (fee) fee.value = '50';
                    btn.click();
                    for (let i = 0; i < 25; i++) {
                        await new Promise(r => setTimeout(r, 200));
                        const resCard = document.getElementById('jobResult');
                        if (resCard && resCard.classList.contains('show')) {
                            return resCard.innerText.slice(0, 180).replace(/\\n+/g, ' ');
                        }
                    }
                    return 'TIMEOUT';
                })()
            """)
            print(f"Job Scanner Output: {job_res}")

            # 8. Test Company Verification flow
            print("\nTesting Company Verification flow...")
            comp_res = await eval_js("""
                (async () => {
                    const name = document.getElementById('companyName');
                    const dom = document.getElementById('companyDomain');
                    const btn = document.getElementById('verifyCompanyBtn');
                    if (!name || !btn) return 'COMP_INPUT_MISSING';
                    name.value = 'Google';
                    if (dom) dom.value = 'google.com';
                    btn.click();
                    for (let i = 0; i < 25; i++) {
                        await new Promise(r => setTimeout(r, 200));
                        const resCard = document.getElementById('companyResult');
                        if (resCard && resCard.classList.contains('show')) {
                            return resCard.innerText.slice(0, 180).replace(/\\n+/g, ' ');
                        }
                    }
                    return 'TIMEOUT';
                })()
            """)
            print(f"Company Verification Output: {comp_res}")

            print(f"\n==========================================")
            print(f"Total Runtime Exceptions: {len(exceptions)}")
            print(f"Total Console Logs Captured: {len(console_messages)}")
            if len(exceptions) == 0:
                print("✓ ZERO JAVASCRIPT SYNTAX OR RUNTIME PARSER EXCEPTIONS!")
            else:
                for ex in exceptions:
                    print("EXCEPTION:", ex)
            print(f"==========================================")

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(main())
