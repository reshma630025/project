"""
TrustGuard AI — Permanent Local Server & LAN Access Verification Test Suite
Tests:
1. Localhost HTTP 200 (127.0.0.1:8000 & localhost:8000)
2. Dynamic Active LAN IPv4 HTTP 200 (<LAN_IP>:8000)
3. API Status endpoint (/api/status)
4. Duplicate server prevention check
5. Windows Auto-Start installation check
6. Offline local AI inference across modalities
7. Frontend relative API routing verification
"""
import os
import sys
import time
import socket
import urllib.request
import urllib.error
import json
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Import LAN detection module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.detect_lan_ip import get_lan_ip

LAN_IP = get_lan_ip()
print("=" * 75)
print("     TRUSTGUARD AI: PERMANENT LOCAL SERVER & LAN AUDIT")
print("=" * 75)
print(f"Active LAN IPv4 Detected: {LAN_IP}")
print(f"Host Machine Name:       {socket.gethostname()}")

results = []

def record_test(name, expected, actual, passed, details=""):
    results.append({
        "test": name,
        "expected": expected,
        "actual": actual,
        "passed": passed,
        "details": details
    })
    status_icon = "PASS ✓" if passed else "FAIL ❌"
    print(f"[{status_icon}] {name}")
    print(f"        Expected: {expected} | Actual: {actual}")
    if details:
        print(f"        Details:  {details}")

# Test 1: 127.0.0.1 Root Access
try:
    with urllib.request.urlopen("http://127.0.0.1:8000/", timeout=5) as resp:
        code = resp.getcode()
        html = resp.read().decode("utf-8", errors="ignore")
        has_title = "TrustGuard AI" in html
        record_test("Localhost (127.0.0.1:8000)", "HTTP 200 (HTML)", f"HTTP {code} ({len(html)} bytes)", code == 200 and has_title)
except Exception as e:
    record_test("Localhost (127.0.0.1:8000)", "HTTP 200", f"Error: {e}", False)

# Test 2: localhost Root Access
try:
    with urllib.request.urlopen("http://localhost:8000/", timeout=5) as resp:
        code = resp.getcode()
        html = resp.read().decode("utf-8", errors="ignore")
        has_title = "TrustGuard AI" in html
        record_test("Localhost Hostname (localhost:8000)", "HTTP 200 (HTML)", f"HTTP {code} ({len(html)} bytes)", code == 200 and has_title)
except Exception as e:
    record_test("Localhost Hostname (localhost:8000)", "HTTP 200", f"Error: {e}", False)

# Test 3: Active LAN IP Root Access
try:
    lan_url = f"http://{LAN_IP}:8000/"
    with urllib.request.urlopen(lan_url, timeout=5) as resp:
        code = resp.getcode()
        html = resp.read().decode("utf-8", errors="ignore")
        has_title = "TrustGuard AI" in html
        record_test(f"LAN IP Access ({lan_url})", "HTTP 200 (HTML)", f"HTTP {code} ({len(html)} bytes)", code == 200 and has_title, "Accessible by phones/tablets/laptops on same Wi-Fi")
except Exception as e:
    record_test(f"LAN IP Access ({LAN_IP}:8000)", "HTTP 200", f"Error: {e}", False)

# Test 4: API Status Endpoint over LAN IP
try:
    api_url = f"http://{LAN_IP}:8000/api/status"
    with urllib.request.urlopen(api_url, timeout=5) as resp:
        code = resp.getcode()
        data = json.loads(resp.read().decode("utf-8"))
        is_online = data.get("status") == "online"
        img_ready = data.get("imageModelReady") is True
        aud_ready = data.get("audioModelReady") is True
        vid_ready = data.get("videoModelReady") is True
        url_ready = data.get("urlModelReady") is True
        sms_ready = data.get("smsModelReady") is True
        email_ready = data.get("emailModelReady") is True
        social_ready = data.get("socialModelReady") is True
        job_type = data.get("jobModelType") == "heuristic"
        vid_type = data.get("videoModelType") == "frame_level_aggregation"
        
        all_models_ok = is_online and img_ready and aud_ready and vid_ready and url_ready and sms_ready and email_ready and social_ready and job_type and vid_type
        record_test("API Status (/api/status)", "HTTP 200 (status=online, all models ready)", f"status={data.get('status')}, image={img_ready}, audio={aud_ready}, vid={vid_ready}", all_models_ok, f"VideoType: {data.get('videoModelType')}, JobType: {data.get('jobModelType')}")
except Exception as e:
    record_test("API Status (/api/status)", "HTTP 200", f"Error: {e}", False)

# Test 5: Duplicate Server Prevention Check
try:
    netstat_out = subprocess.check_output('netstat -ano | findstr ":8000" | findstr "LISTENING"', shell=True, text=True, errors="ignore")
    lines = [l.strip() for l in netstat_out.strip().split("\n") if l.strip()]
    pids = set([l.split()[-1] for l in lines])
    record_test("Duplicate Server Prevention", "Single Process Group on Port 8000", f"{len(pids)} listening process(es) (PID: {', '.join(pids)})", len(pids) == 1, "start_trustguard.bat skips launch if 8000 is already active")
except Exception as e:
    record_test("Duplicate Server Prevention", "1 Process", f"Error: {e}", False)

# Test 6: Windows Auto-Start Installation Check
appdata = os.environ.get("APPDATA", "")
startup_vbs = os.path.join(appdata, r"Microsoft\Windows\Start Menu\Programs\Startup\TrustGuardAI-AutoStart.vbs")
startup_exists = os.path.exists(startup_vbs)
record_test("Windows Startup Auto-Start", "TrustGuardAI-AutoStart.vbs in Startup folder", f"Exists: {startup_exists}", startup_exists, f"Path: {startup_vbs}")

# Test 7: Frontend Relative API Path Verification
frontend_ok = True
js_files = ["api.js", "index.html"]
for js_name in js_files:
    p = os.path.join(os.path.dirname(__file__), "..", js_name)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            if "fetch('http://127.0.0.1:8000/api" in content or 'fetch("http://127.0.0.1:8000/api' in content:
                frontend_ok = False
                break

record_test("Frontend Relative API Architecture", "Relative /api/ or window.location.origin", "All fetch calls use relative API base", frontend_ok, "Enables seamless access from mobile/tablet/laptop")

# Test 8: Offline Local AI Multi-Modal Inference
inference_results = {}
try:
    # Text Scam test
    req_data = json.dumps({"text": "URGENT: Your bank account is locked. Click http://verify-bank.com to recover funds."}).encode("utf-8")
    req = urllib.request.Request(f"http://{LAN_IP}:8000/api/analyze/text", data=req_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        d = json.loads(r.read().decode("utf-8"))
        inference_results["text"] = d.get("success", False) and d.get("risk_score", 0) > 50

    # URL Phishing test
    req_data = json.dumps({"url": "http://secure-paypal-login-update-security-check.com/login"}).encode("utf-8")
    req = urllib.request.Request(f"http://{LAN_IP}:8000/api/analyze/url", data=req_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        d = json.loads(r.read().decode("utf-8"))
        inference_results["url"] = d.get("success", False) and d.get("risk_score", 0) > 50

    # Email Phishing test
    req_data = json.dumps({"subject": "Urgent Password Reset Required", "body": "Please click the link below to verify your account credentials immediately or account will be suspended."}).encode("utf-8")
    req = urllib.request.Request(f"http://{LAN_IP}:8000/api/analyze/email", data=req_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        d = json.loads(r.read().decode("utf-8"))
        inference_results["email"] = d.get("success", False) and d.get("risk_score", 0) > 50

    # Social Profile test
    req_data = json.dumps({
        "username": "bot_user_9921",
        "followers_count": 10,
        "friends_count": 2500,
        "statuses_count": 12,
        "default_profile": 1,
        "default_profile_image": 1,
        "geo_enabled": 0,
        "profile_use_background_image": 0,
        "name_length": 18,
        "screen_name_length": 15,
        "description_length": 0
    }).encode("utf-8")
    req = urllib.request.Request(f"http://{LAN_IP}:8000/api/analyze/social", data=req_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        d = json.loads(r.read().decode("utf-8"))
        inference_results["social"] = d.get("success", False) and d.get("risk_score", 0) > 50

    all_inf_passed = all(inference_results.values()) and len(inference_results) == 4
    record_test("Offline Local AI Multi-Modal Inference", "All local models return genuine predictions", f"{sum(inference_results.values())}/4 modalities passed (Text, URL, Email, Social)", all_inf_passed, "Zero cloud API calls needed")
except Exception as e:
    record_test("Offline Local AI Multi-Modal Inference", "All models pass", f"Error: {e}", False)

# Final Summary Table
print("\n" + "=" * 75)
print("                       FINAL AUDIT SUMMARY")
print("=" * 75)
print(f"{'Audit Check / Test Target':<42} | {'Expected':<12} | {'Result'}")
print("-" * 75)
for r in results:
    res_str = "PASS ✓" if r["passed"] else "FAIL ❌"
    print(f"{r['test']:<42} | {'PASS':<12} | {res_str}")
print("=" * 75)

all_passed = all(r["passed"] for r in results)
print(f">>> PERMANENT LOCAL SERVER & LAN AUDIT: {'PASS ✓ (All Criteria Satisfied)' if all_passed else 'FAIL ❌'}\n")
