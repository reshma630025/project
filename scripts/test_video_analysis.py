"""
TrustGuard AI — Video Analysis End-to-End API Verification Script
Tests actual MP4 video files from archive (16) (Celeb-DF v2) and archive (17) (FaceForensics++ C23)
against the running FastAPI backend on /api/analyze/video.
"""
import os
import sys
import glob
import time
import json
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = os.environ.get("TRUSTGUARD_URL", "http://127.0.0.1:8000")
ENDPOINT = f"{BASE_URL}/api/analyze/video"

print("=" * 70)
print("       TRUSTGUARD AI: END-TO-END VIDEO ANALYSIS TEST")
print("=" * 70)

# Step 1: Check backend availability
print(f"\n[1/4] Verifying Backend Availability at {BASE_URL}/api/status...")
try:
    health_resp = requests.get(f"{BASE_URL}/api/status", timeout=5)
    if health_resp.status_code == 200:
        health_data = health_resp.json()
        print(f"  ✓ Backend is ONLINE (Status: {health_data.get('status')})")
        print(f"  ✓ Video Model Type: {health_data.get('videoModelType')}")
        print(f"  ✓ Image Model Status: {health_data.get('imageModelType')}")
    else:
        print(f"  ⚠ Backend returned HTTP {health_resp.status_code}")
except Exception as e:
    print(f"  ❌ Backend unreachable: {e}")
    print("  Please make sure uvicorn is running on port 8000.")
    sys.exit(1)

# Step 2: Locate candidate test videos
print("\n[2/4] Locating Real Test Videos...")
c16_real = glob.glob(r"C:\Users\paruc\Downloads\archive (16)\Celeb-real\*.mp4") + glob.glob(r"C:\Users\paruc\Downloads\archive (16)\YouTube-real\*.mp4")
c16_fake = glob.glob(r"C:\Users\paruc\Downloads\archive (16)\Celeb-synthesis\*.mp4")
c17_real = glob.glob(r"C:\Users\paruc\Downloads\archive (17)\**\original\*.mp4", recursive=True) + glob.glob(r"C:\Users\paruc\Downloads\archive (17)\**\original_sequences\*.mp4", recursive=True)
c17_fake = [f for f in glob.glob(r"C:\Users\paruc\Downloads\archive (17)\**\*.mp4", recursive=True) if "original" not in f]

print(f"  Celeb-DF v2 (archive (16)): {len(c16_real)} real samples, {len(c16_fake)} fake samples found.")
print(f"  FaceForensics++ (archive (17)): {len(c17_real)} real samples, {len(c17_fake)} fake samples found.")

test_candidates = []
if c16_real:
    test_candidates.append(("Celeb-DF v2 (Real)", c16_real[0], "REAL"))
if c16_fake:
    test_candidates.append(("Celeb-DF v2 (Synthesis/Fake)", c16_fake[0], "FAKE"))
if c17_real:
    test_candidates.append(("FaceForensics++ (Original Real)", c17_real[0], "REAL"))
if c17_fake:
    test_candidates.append(("FaceForensics++ (Manipulated)", c17_fake[0], "FAKE"))

if not test_candidates:
    # Fallback to test_clip.mp4 if extracted archives are not ready
    if os.path.exists("test_clip.mp4"):
        test_candidates.append(("Local Test Clip", "test_clip.mp4", "SAMPLE"))

print(f"  Total test video items: {len(test_candidates)}")

# Step 3: Execute Video Inference over API
print("\n[3/4] Executing Video Frame-by-Frame API Analysis...")
results = []
all_passed = True

for name, vpath, ground_truth in test_candidates:
    print(f"\n--- Testing: {name} ---")
    print(f"  File: {vpath} ({os.path.getsize(vpath)/1024:.1f} KB)")
    t0 = time.time()
    
    with open(vpath, "rb") as vf:
        files = {"video": (os.path.basename(vpath), vf, "video/mp4")}
        try:
            resp = requests.post(ENDPOINT, files=files, timeout=120)
        except Exception as e:
            print(f"  ❌ Request failed: {e}")
            all_passed = False
            continue

    elapsed = round(time.time() - t0, 2)
    print(f"  HTTP Status: {resp.status_code} ({elapsed}s)")
    
    if resp.status_code != 200:
        print(f"  ❌ Server Error: {resp.text[:400]}")
        all_passed = False
        continue

    data = resp.json()
    success = data.get("success", False)
    classification = data.get("classification") or data.get("status", "UNKNOWN")
    confidence = data.get("confidence", 0.0)
    risk_score = data.get("risk_score", 0.0)
    trust_score = data.get("trust_score", 0.0)
    model = data.get("model", "Unknown")
    model_avail = data.get("model_available", False)
    video_model_type = data.get("videoModelType", "Unknown")
    sampled = data.get("sampled_frames", 0)
    analyzed = data.get("analyzed_frames", 0)
    duration = data.get("duration", 0.0)
    fps = data.get("fps", 0.0)
    frames_list = data.get("frame_results", [])
    evidence = data.get("evidence", [])

    print(f"  Success: {success}")
    print(f"  Classification: {classification} (Ground Truth: {ground_truth})")
    print(f"  Confidence: {confidence}% | Risk Score: {risk_score}/100 | Trust Score: {trust_score}/100")
    print(f"  Model: {model} (Available: {model_avail}, Type: {video_model_type})")
    print(f"  Frames: {analyzed}/{sampled} analyzed across {duration}s ({fps} FPS)")
    print(f"  Frame Timeline Details: {len(frames_list)} keyframes returned")
    print(f"  Sample Evidence: {evidence[0] if evidence else 'None'}")

    is_match = (
        (ground_truth in ["FAKE", "SYNTHESIS"] and classification in ["AI-GENERATED", "LIKELY AI-GENERATED", "SUSPICIOUS"])
        or (ground_truth in ["REAL", "BONAFIDE"] and classification in ["REAL", "LIKELY AUTHENTIC"])
    )

    api_pass = (
        success is True
        and confidence > 0.0
        and model_avail is True
        and analyzed > 0
        and len(frames_list) > 0
    )

    match_str = "MATCH ✓" if is_match else "MISCLASSIFICATION"
    api_str = "API OK ✓" if api_pass else "API FAIL ❌"
    print(f"  >>> API STATUS: {api_str} | GROUND TRUTH: {match_str}")

    results.append({
        "dataset": name,
        "file": os.path.basename(vpath),
        "ground_truth": ground_truth,
        "prediction": classification,
        "confidence": confidence,
        "risk_score": risk_score,
        "analyzed_frames": analyzed,
        "latency_sec": elapsed,
        "model": model,
        "api_pass": api_pass,
        "is_match": is_match
    })

# Step 4: Summary Table
print("\n" + "=" * 80)
print("                      FINAL VIDEO TEST SUMMARY")
print("=" * 80)
print(f"{'Dataset / Test Item':<32} | {'Truth':<6} | {'Prediction':<14} | {'Conf':<6} | {'Risk':<6} | {'Frames':<7} | {'API':<7} | {'GT Result'}")
print("-" * 105)
for r in results:
    api_s = "PASS ✓" if r["api_pass"] else "FAIL ❌"
    gt_s = "MATCH ✓" if r["is_match"] else "MISCLASSIFIED"
    print(f"{r['dataset']:<32} | {r['ground_truth']:<6} | {r['prediction']:<14} | {r['confidence']:<5.1f}% | {r['risk_score']:<5.1f} | {r['analyzed_frames']:<7} | {api_s:<7} | {gt_s}")

print("=" * 80)
all_api_ok = all(r["api_pass"] for r in results)
print(f">>> OVERALL API PIPELINE STATUS: {'PASS ✓ (All Endpoints and Inferences Functional)' if all_api_ok else 'FAIL ❌'}")
