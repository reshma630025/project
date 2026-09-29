import urllib.request
import urllib.parse
import json
import io
import time
from PIL import Image
import wave
import struct
import sys

BASE = "http://127.0.0.1:8000"

def log(msg):
    print(msg, flush=True)

def api_request(endpoint, method="GET", data=None, token=None):
    url = f"{BASE}{endpoint}"
    headers = {}
    body = None

    if token:
        headers["Authorization"] = f"Bearer {token}"

    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode('utf-8'))

def api_multipart(endpoint, field_name, filename, file_bytes, content_type, token=None):
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = bytearray()
    body.extend(f"--{boundary}\r\n".encode('utf-8'))
    body.extend(f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'.encode('utf-8'))
    body.extend(f"Content-Type: {content_type}\r\n\r\n".encode('utf-8'))
    body.extend(file_bytes)
    body.extend(f"\r\n--{boundary}--\r\n".encode('utf-8'))

    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(f"{BASE}{endpoint}", data=bytes(body), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))

log("=== STEP 1: Health & Status ===")
h = api_request("/api/health")
s = api_request("/api/status")
log(f"Health: {h['status']} | ImageModel: {s.get('imageModel')}")

log("=== STEP 2: Auth Flow ===")
test_email = f"user_{int(time.time())}@trustguard.ai"
reg = api_request("/api/auth/register", method="POST", data={
    "email": test_email,
    "password": "Password2026!",
    "display_name": "Reshma A.",
    "organization": "TrustGuard Cyber Labs"
})
token = reg.get("token")
log(f"Registered user: {reg.get('user', {}).get('display_name')} with token: {token[:12]}...")

me = api_request("/api/auth/me", token=token)
log(f"GET /api/auth/me: {me.get('user', {}).get('display_name')}")

prof = api_request("/api/auth/profile", method="PUT", data={"display_name": "Reshma A., Lead Security Researcher"}, token=token)
log(f"PUT /api/auth/profile: {prof.get('user', {}).get('display_name')}")

log("=== STEP 3: Audio Segment Analysis ===")
wav_buf = io.BytesIO()
with wave.open(wav_buf, 'wb') as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(16000)
    samples = [int(4000 * (i % 60) / 60.0) for i in range(48000)]
    wav.writeframes(struct.pack(f'<{len(samples)}h', *samples))
aud = api_multipart("/api/analyze/audio", "audio", "voice.wav", wav_buf.getvalue(), "audio/wav", token=token)
log(f"Audio: {aud.get('classification')} | Segments: {aud.get('segments_analyzed')} | Risk: {aud.get('risk_score')}")

log("=== STEP 4: Image ViT ===")
img = Image.new('RGB', (100, 100), color=(120, 160, 200))
ibuf = io.BytesIO()
img.save(ibuf, format='JPEG')
img_res = api_multipart("/api/analyze/image", "image", "test.jpg", ibuf.getvalue(), "image/jpeg", token=token)
log(f"Image: {img_res.get('classification')} | Risk: {img_res.get('risk_score')}")

log("=== STEP 5: Text, Job, URL, OCR, Company, Social ===")
txt = api_request("/api/analyze/text", method="POST", data={"text": "URGENT: Click here to verify your account."}, token=token)
log(f"Text: {txt.get('classification')} | Risk: {txt.get('risk_score')}")

job = api_request("/api/analyze/job", method="POST", data={"description": "Work from home. Pay 100 registration fee."}, token=token)
log(f"Job: {job.get('classification')} | Risk: {job.get('risk_score')}")

url = api_request("/api/analyze/url", method="POST", data={"url": "http://secure-login-portal.tk/auth"}, token=token)
log(f"URL: {url.get('classification')} | Risk: {url.get('risk_score')}")

comp = api_request("/api/analyze/company", method="POST", data={"company_name": "Google", "domain": "google.com", "email": "hr@google.com"}, token=token)
log(f"Company: {comp.get('classification')} | Risk: {comp.get('risk_score')}")

soc = api_request("/api/analyze/social", method="POST", data={"content": "Crypto airdrop double promo!", "platform": "Twitter / X"}, token=token)
log(f"Social: {soc.get('classification')} | Risk: {soc.get('risk_score')}")

log("=== STEP 6: User-Scoped Stats & History ===")
st = api_request("/api/stats", token=token)
hist = api_request("/api/history", token=token)
log(f"User Scans: {st.get('scans')} | Threats: {st.get('threats')} | History entries: {len(hist)}")

log("ALL TESTS COMPLETED SUCCESSFULLY!")
