# TrustGuard AI — Real Model Content Detection & Deepfake Security

TrustGuard AI is an enterprise-grade content authenticity platform designed to detect deepfakes, synthetic media, phishing, job scams, and social media fraud using real pretrained AI vision models, audio forensics, natural language algorithms, and domain security checks.

## 🚀 How to Run (Three Modes)

### 1. LOCAL / OFFLINE MODE
The FastAPI backend runs the server and directly hosts the frontend application at `http://127.0.0.1:8000`.
- **Localhost URL:** http://127.0.0.1:8000
- **Startup Command:** 
  ```bash
  python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
  ```

### 2. LAN MODE (Any Device on Same Wi-Fi)
- **Access URL:** `http://<CURRENT-LAN-IP>:8000/` (e.g., `http://192.168.1.5:8000/`)

### 3. LIVE / GITHUB PAGES
- **GitHub Pages URL:** https://reshma630025.github.io/project/
- **Live Backend Status:** NOT DEPLOYED. GitHub Pages hosts the frontend verified, but the FastAPI python backend requires deployment (e.g., to Render/Heroku) to operate the AI models remotely. Currently defaults to local backend for full functionality.

---

## 📊 Dataset Inventory & Training Verification

| Dataset | Modality | Usable Samples | Train | Validation | Test | Status |
|---------|----------|----------------|-------|------------|------|--------|
| **1000 Deepfake Videos** | Image | 5,600 | 4,000 | 800 | 800 | TRAINED |
| **ASVspoof 2019 LA** | Audio | 5,000 | 4,000 | 800 | 200 | TRAINED |
| **spam_sms.csv** | SMS | 5,572 | 4,457 | 557 | 558 | TRAINED |
| **phishing_email.csv** | Email | 38,000 | 32,000 | 4,000 | 2,000 | TRAINED |
| **final_dataset.csv** | URL | 56,000 | 48,000 | 6,000 | 2,000 | TRAINED |
| **raw_user_profiles.csv**| Social (A) | 5,000 | 4,000 | 500 | 500 | TRAINED |
| **train/test Instagram** | Social (B) | 696 | 576 | N/A | 120 | TRAINED |
| **Celeb-DF v2** | Video | 60 clips | N/A | N/A | 60 | EVALUATED |
| **Fake Postings.csv** | Job Scam | 17,880 | N/A | N/A | N/A | HEURISTIC |

---

## 🔬 Actual Model Test Performance (Zero Leakage, Isolated Test Split)

| Dataset | Modality | Accuracy | Precision | Recall | F1 | ROC-AUC | Model Type |
|---------|----------|----------|-----------|--------|----|---------|------------|
| Image | Image | 88.12% | 93.20% | 82.25% | 87.38% | 0.9626 | DeepfakeCNN (PyTorch Vision CNN) |
| Audio (ASVspoof) | Audio | 99.50% | 100.00% | 99.00% | 99.50% | 1.0000 | AudioCNN (Mel-STFT Spectrogram CNN) |
| SMS | SMS | 98.57% | 97.18% | 92.00% | 94.52% | 0.9831 | SMSScamClassifier (TF-IDF + Neural Classifier) |
| Email | Email | 99.65% | 98.12% | 99.68% | 98.89% | 0.9995 | EmailPhishingClassifier (TF-IDF + Neural Classifier) |
| URL | URL | 99.60% | 100.00% | 99.57% | 99.79% | 0.9994 | PhishingURLNet (Tabular 74-feat Deep NN) |
| Social Profile (A) | Social | 92.00% | 77.07% | 96.80% | 85.82% | 0.9897 | SocialProfileNet (Tabular Profile NN) |
| Instagram (B) | Social | 88.33% | 91.07% | 85.00% | 87.93% | 0.9061 | SocialSpamNet (Instagram Account Classifier) |
| Celeb-DF v2 | Video | 43.33% | 35.71% | 16.67% | 22.73% | N/A | frame_level_aggregation (Vision CNN) |
| Fake Postings | Job | N/A | N/A | N/A | N/A | N/A | HEURISTIC |

**Limitations:** The `Fake Postings.csv` dataset contains only fraudulent samples in its evaluation split, making traditional binary ML metrics impossible. It operates using a heuristic model. Celeb-DF accuracy reflects frame-aggregation limitations over temporal deepfakes using a basic spatial CNN.

---

## 🎯 Production Detection Workflow & Normalization
All outputs traverse `normalizePrediction()` which maps inference outputs strictly to:
- REAL (Score 0-64)
- FAKE / SUSPICIOUS (Score 65+)

Fake results trigger the unified **Audio-Visual Threat System**:
- 🚨 Visual Alert rendering
- 🔊 "Sawtooth" Security Buzzer
- 🗣️ `window.speechSynthesis` Voice Warning (e.g., "Warning. This content is detected as fake.")

---

## 💻 GitHub Repository & Updates
- **Repository:** https://github.com/reshma630025/project.git
- **Deployment Strategy:** All frontend structural integrity, real ML metrics, API normalizations, and UI fixes are fully synchronized with the `project.git` repository on the `main` branch.

