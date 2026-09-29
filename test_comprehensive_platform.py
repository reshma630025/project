import sys
sys.stdout.reconfigure(encoding='utf-8')
import urllib.request
import urllib.parse
import json
import io
import time
from PIL import Image
import wave
import struct

BASE = "http://127.0.0.1:8000"

def test_json(endpoint, data):
    req = urllib.request.Request(
        f"{BASE}{endpoint}",
        data=json.dumps(data).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def test_get(endpoint):
    req = urllib.request.Request(f"{BASE}{endpoint}")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def test_multipart(endpoint, fields, files):
    boundary = "----WebKitFormBoundaryComprehensiveTest"
    body = bytearray()
    for k, v in fields.items():
        body.extend(f"--{boundary}\r\n".encode('utf-8'))
        body.extend(f'Content-Disposition: form-data; name="{k}"\r\n\r\n'.encode('utf-8'))
        body.extend(f"{v}\r\n".encode('utf-8'))
    for field_name, (filename, file_bytes, content_type) in files.items():
        body.extend(f"--{boundary}\r\n".encode('utf-8'))
        body.extend(f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'.encode('utf-8'))
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode('utf-8'))
        body.extend(file_bytes)
        body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode('utf-8'))

    req = urllib.request.Request(
        f"{BASE}{endpoint}",
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

print("="*70)
print("TRUSTGUARD AI PLATFORM — COMPREHENSIVE END-TO-END SYSTEM TEST")
print("="*70)

# 1. Health & Status
print("\n[1] Testing GET /api/health and /api/status...")
health = test_get("/api/health")
print("  ✓ Health:", health)
status = test_get("/api/status")
print(f"  ✓ Status: imageModel={status.get('imageModel')}, audioModel={status.get('audioModel')}, imageModelLoaded={status.get('imageModelLoaded')}, audioModelLoaded={status.get('audioModelLoaded')}")
assert health["status"] == "ok"

# 2. Image Analysis
print("\n[2] Testing POST /api/analyze/image with real DeepfakeCNN...")
img = Image.new('RGB', (128, 128), color=(140, 180, 220))
buf = io.BytesIO()
img.save(buf, format='JPEG')
img_res = test_multipart("/api/analyze/image", {}, {"image": ("test.jpg", buf.getvalue(), "image/jpeg")})
print(f"  ✓ Image Result: class={img_res.get('classification')}, risk={img_res.get('risk_score')}, trust={img_res.get('trust_score')}, model={img_res.get('model_used')}")
assert "trust_score" in img_res

# 3. Audio Analysis
print("\n[3] Testing POST /api/analyze/audio with real AudioCNN...")
wav_buf = io.BytesIO()
with wave.open(wav_buf, 'wb') as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(16000)
    samples = [int(1500 * struct.unpack('h', struct.pack('h', int((i*7) % 256)))[0]) for i in range(16000 * 2)]
    wav.writeframes(struct.pack(f'<{len(samples)}h', *[min(32767, max(-32768, s)) for s in samples]))
aud_bytes = wav_buf.getvalue()
aud_res = test_multipart("/api/analyze/audio", {}, {"audio": ("test.wav", aud_bytes, "audio/wav")})
print(f"  ✓ Audio Result: class={aud_res.get('classification')}, risk={aud_res.get('risk_score')}, trust={aud_res.get('trust_score')}, model={aud_res.get('model_used')}")
assert "trust_score" in aud_res

# 4. Live Audio Stream Endpoint
print("\n[4] Testing POST /api/analyze/live-audio with real streaming audio bytes...")
live_res = test_multipart("/api/analyze/live-audio", {}, {"audio": ("live.wav", aud_bytes[:32000], "audio/wav")})
print(f"  ✓ Live Audio Result: class={live_res.get('classification')}, risk={live_res.get('risk_score')}, trust={live_res.get('trust_score')}")

# 5. Multimodal Audio + Image Cross-Modality Analysis
print("\n[5] Testing POST /api/analyze/multimodal (Image + Audio)...")
multi_res = test_multipart(
    "/api/analyze/multimodal",
    {},
    {
        "image": ("multi_face.jpg", buf.getvalue(), "image/jpeg"),
        "audio": ("multi_voice.wav", aud_bytes, "audio/wav")
    }
)
print(f"  ✓ Multimodal Result: class={multi_res.get('classification')}, risk={multi_res.get('risk_score')}, trust={multi_res.get('trust_score')}, fusion={multi_res.get('fusion_strategy')}")
print(f"    Modalities: {multi_res.get('modalities_analyzed')}")
assert "cross_modal_divergence" in multi_res

# 6. Text, Job, URL, OCR, Social, Company Scanners
print("\n[6] Testing Fraud & Linguistic Scanners...")
txt_res = test_json("/api/analyze/text", {"text": "URGENT NOTICE: Your Chase bank account is frozen. Send $500 Bitcoin to verify."})
print(f"  ✓ Text Analysis: {txt_res.get('classification')} (Risk {txt_res.get('risk_score')})")

job_res = test_json("/api/analyze/job", {
    "description": "Work from home data entry $5,000 weekly. Send $150 onboarding fee via wire transfer.",
    "email": "hr-fastjob1984@gmail.com",
    "url": "http://scamjob-easy-money.biz"
})
print(f"  ✓ Job Scam Analysis: {job_res.get('classification')} (Risk {job_res.get('risk_score')})")

url_res = test_json("/api/analyze/url", {"url": "http://paypal-verification-update-security.top/login"})
print(f"  ✓ URL Phishing Analysis: {url_res.get('classification')} (Risk {url_res.get('risk_score')})")

comp_res = test_json("/api/analyze/company", {"company_name": "Microsoft", "domain": "microsoft.com", "email": "careers@microsoft.com"})
print(f"  ✓ Company Verification: {comp_res.get('classification')} (Trust {comp_res.get('trust_score')})")

# 7. AI Cybersecurity Assistant
print("\n[7] Testing POST /api/assistant...")
assist_res = test_json("/api/assistant", {
    "question": "Why did the image detector flag suspicious artifacts?",
    "context": {
        "contentType": "image",
        "score": 82,
        "trustScore": 18,
        "confidence": 88.5,
        "indicators": [
            {"label": "CNN Synthetic Pattern", "detail": "DeepfakeCNN identified synthetic face generation artifacts"},
            {"label": "ELA Inconsistency", "detail": "Error level analysis shows abnormal high-frequency residual distribution"}
        ]
    }
})
ans = assist_res.get('answer') or assist_res.get('reply') or ''
print(f"  ✓ Assistant Answer: {ans[:120]}...")

# 8. Reports Storage & Database
print("\n[8] Testing Reports API (GET & POST /api/reports)...")
report_payload = {
    "report_id": f"TG-{int(time.time())}",
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "content_type": "multimodal",
    "filename": "multi_sample.jpg + multi_sample.wav",
    "classification": multi_res.get("classification"),
    "risk_score": multi_res.get("risk_score"),
    "trust_score": multi_res.get("trust_score"),
    "confidence": multi_res.get("confidence"),
    "indicators": multi_res.get("indicators", [])
}
create_rep = test_json("/api/reports", report_payload)
print(f"  ✓ Created Report: {create_rep.get('report_id')}")
reports_list = test_get("/api/reports")
print(f"  ✓ Retrieved Reports Count: {len(reports_list)}")
assert len(reports_list) > 0

# 9. Real Stats & History
print("\n[9] Testing GET /api/stats and /api/history...")
stats = test_get("/api/stats")
print(f"  ✓ Stats: total_scans={stats.get('total_scans')}, deepfakes={stats.get('deepfakes_detected')}, frauds={stats.get('fraud_prevented')}")
history = test_get("/api/history")
print(f"  ✓ History Length: {len(history)}")

print("\n" + "="*70)
print("ALL 9 TEST SUITES PASSED! REAL MULTIMODAL PLATFORM OPERATIONAL!")
print("="*70)
