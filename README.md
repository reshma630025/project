# TrustGuard AI — Real Model Content Detection & Deepfake Security

TrustGuard AI is an enterprise-grade content authenticity platform designed to detect deepfakes, synthetic media, phishing, job scams, and social media fraud using real pretrained AI vision models, audio forensics, natural language algorithms, and domain security checks.

---

## 🚀 How to Run in Localhost

The FastAPI backend runs the server and directly hosts the frontend application at `http://127.0.0.1:8000`.

### Option 1: Quick Start (Windows)
Double-click [`run.bat`](file:///c:/Users/paruc/OneDrive/Desktop/git5/run.bat) or run in PowerShell:
```powershell
.\run.ps1
```

### Option 2: Run via Command Line
```powershell
& "C:\Users\paruc\AppData\Local\Programs\Python\Python313\python.exe" -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```
Or with standard python:
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### Option 3: Access the Web App in Your Browser
Open your web browser and navigate to:
```text
http://127.0.0.1:8000
```

---

## 🎯 Detection Modules (100% Real Model Predictions)

| # | Module | Endpoint | Detection Technology |
|---|---|---|---|
| 1 | **Image Deepfake** | `POST /api/analyze/image` | Pretrained Vision Transformer (`dima806/deepfake_vs_real_image_detection`), Error Level Analysis (ELA), multi-scale letterbox padding. |
| 2 | **Video Deepfake** | `POST /api/analyze/video` | OpenCV temporal frame extraction (8 representative frames), per-frame model inference, visual timeline. |
| 3 | **Audio / Voice Deepfake** | `POST /api/analyze/audio` | Soundfile / Librosa decoding, STFT Spectral Centroid, Flux, Rolloff, and Vocoder artifact detection. |
| 4 | **Text & Scam Detection** | `POST /api/analyze/text` | Multilingual regex pattern matcher targeting OTP harvesting, wire transfer / cryptocurrency demands, urgency coercion, and prize scams. |
| 5 | **Job & Internship Fraud** | `POST /api/analyze/job` & `POST /api/analyze/internship` | Upfront fee solicitation detection, personal vs corporate recruiter email verification (`@gmail` vs corporate domain), and salary ratio analysis. |
| 6 | **URL Scanner** | `POST /api/analyze/url` | Shannon entropy analysis, raw IP hostnames, suspicious TLDs (`.tk`, `.xyz`), brand typo-squatting, and credential harvesting paths. |
| 7 | **OCR Scanner** | `POST /api/analyze/ocr` | Real Tesseract.js client OCR combined with backend structured entity parsing (Company, Email, Phone, Salary, Registration Fee). |
| 8 | **Company Verification** | `POST /api/analyze/company` | Live system DNS address resolution, MX record lookup, and corporate email domain alignment. |
| 9 | **Social Media Protection** | `POST /api/analyze/social` | Crypto doubling airdrop lures, high-pressure engagement bait, celebrity impersonation, and off-platform redirect detection. |
| 10 | **Live Stats & History** | `GET /api/stats` & `GET /api/history` | SQLite database (`trustguard.db`) recording every scan with timestamps, content labels, risk levels, and confidence scores. |

---

## 📊 Unified 5-Tier Risk Scale
- **0–20**: `LOW RISK` (Green / `#33d19a`) — Standard authentic markers verified.
- **21–40**: `MODERATE RISK` (Amber / `#f5b942`) — Minor anomalies; cross-referencing advised.
- **41–60**: `HIGH RISK` (Coral / `#f2495c`) — Significant synthetic / scam signals detected.
- **61–80**: `VERY HIGH RISK` (Deep Red / `#e63946`) — Highly likely manipulated, deceptive, or phishing.
- **81–100**: `CRITICAL RISK` (Crimson / `#ff1e42`) — Severe threat / deepfake / fraudulent solicitation.

---

## 🧪 Testing All Endpoints

Run the automated test suite against the running server:
```powershell
python test_all_endpoints.py
```
