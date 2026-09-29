import asyncio
import json
import urllib.request
import websockets
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

async def main():
    # Connect to existing Chrome or new tab
    req = urllib.request.Request("http://127.0.0.1:9224/json/list")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            tabs = json.loads(resp.read().decode())
    except Exception as e:
        print("Could not connect to port 9224:", e)
        return

    tab = [t for t in tabs if t.get('type') == 'page'][0]
    ws_url = tab['webSocketDebuggerUrl']
    print("Connecting to tab:", tab['url'])

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

        async def eval_js(expr):
            r = await send("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
            inner = r.get("result", {})
            return inner.get("value")

        # Test company verification in browser
        res = await eval_js("""(async () => {
            gotoPage('company');
            const name = document.getElementById('compName');
            const dom = document.getElementById('compDomain');
            const em = document.getElementById('compEmail');
            const btn = document.getElementById('compVerifyBtn');
            name.value = "Google";
            dom.value = "google.com";
            em.value = "recruiter@google.com";
            
            console.log("Calling btn.click()");
            btn.click();
            
            for (let i = 0; i < 20; i++) {
                await new Promise(r => setTimeout(r, 200));
                const resWrap = document.getElementById('compResult');
                if (resWrap && resWrap.classList.contains('show')) {
                    return {
                        success: true,
                        rendered: true,
                        html: resWrap.innerHTML.slice(0, 200),
                        title: resWrap.querySelector('.pred-title')?.textContent
                    };
                }
            }
            const resWrap = document.getElementById('compResult');
            return {
                success: false,
                rendered: false,
                classes: resWrap ? resWrap.className : 'no element',
                html: resWrap ? resWrap.innerHTML : 'no element'
            };
        })()""")
        print("Company debug result:", res)

        # Test assistant in browser with polling
        assist = await eval_js("""(async () => {
            openAssistant();
            const inp = document.getElementById('assistInput');
            const btn = document.getElementById('assistSendBtn');
            inp.value = "What does the Trust Score mean?";
            btn.click();
            
            for (let i = 0; i < 25; i++) {
                await new Promise(r => setTimeout(r, 200));
                const botMsgs = Array.from(document.querySelectorAll('#assistBody .msg.bot')).map(m => m.textContent);
                if (botMsgs.length >= 2) {
                    return {
                        success: true,
                        count: botMsgs.length,
                        reply: botMsgs[botMsgs.length - 1]
                    };
                }
            }
            const botMsgs = Array.from(document.querySelectorAll('#assistBody .msg.bot')).map(m => m.textContent);
            return {
                success: false,
                count: botMsgs.length,
                msgs: botMsgs
            };
        })()""")
        print("Assistant debug result:", assist)

if __name__ == '__main__':
    asyncio.run(main())
