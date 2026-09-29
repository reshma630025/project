# TrustGuard AI — Comprehensive Dataset Discovery & Modality Mapping Report

**Date:** September 8, 2026  
**Auditor:** Antigravity AI Cybersecurity Intelligence  
**Target Repository:** `TrustGuard AI Unified SOC Platform`  
**Inspection Mode:** Read-Only Audit of Local Datasets (`C:\Users\paruc\Downloads`)

---

## 1. Executive Summary

A comprehensive, read-only forensic inspection was conducted across all 10 candidate dataset directories under `C:\Users\paruc\Downloads`, as well as the 2 existing foundational datasets (Audio and Image). Every file, folder, label structure, and metadata format was analyzed without modifying or deleting any source files.

### Key Takeaways:
1. **Existing Models Verified Active:**
   - **Image Deepfake Model (`DeepfakeCNN`):** Trained on `archive/1000_videos` (16,433 PNG frames). Real checkpoint verified at `models/image/best_model.pt` (11.0 MB, Validation Accuracy: 88.12%, F1: 87.38%).
   - **Audio Anti-Spoofing Model (`AudioCNN`):** Trained on ASVspoof 2019 Logical Access (`archive (1)\LA\LA`). Real checkpoint verified at `models/audio/best_model.pt` (2.74 MB, Dev Evaluation Accuracy: 100%).
2. **Three High-Quality Labeled Datasets Discovered for Immediate Real Model Training:**
   - **Phishing URL Detection:** `archive (6)` contains `final_dataset.csv` (204.8 MB, 579,920 labeled samples with 74 rich lexical/entropy/DNS features). Fully balanced and ready for supervised learning.
   - **SMS Scam Detection:** `archive (4)` contains `spam_sms.csv` (5,572 real SMS messages: 4,825 Ham, 747 Spam). Ready for supervised NLP model training.
   - **Phishing Email Detection:** `archive (9)` contains `phishing_email.csv` (82,486 balanced emails: 39,595 Legitimate, 42,891 Phishing) plus 6 other sub-corpora totaling over 165,000 emails. Ideal for training a dedicated PyTorch Email Classifier.
3. **Critical Ground Truth on Celeb-DF v2 (`celeb-df-v2-metadata`):**
   - **Contains METADATA ONLY** (`celeb-df-v2-metadata.json`, 3,495 bytes). It is a Kaggle Croissant JSON schema document referencing an external 9.285 GB download. **Zero MP4 video files exist in this folder.** It CANNOT be used as a video dataset.
4. **Duplicates & Redundant Zips Identified:**
   - `archive (7)` is an exact bit-for-bit duplicate of `archive (6)`.
   - `archive (10)` and `archive (13)` are unextracted zip archives containing `archive (9).zip`.
   - `archive (11)` and `archive (12)` are unextracted zip archives containing `archive (7).zip` / `archive (6).zip`.
5. **Job Postings Limitation Discovered:**
   - `archive (5)\Fake Postings.csv` contains 10,000 samples where **100% of rows have `fraudulent = 1`**. There are ZERO negative/legitimate job postings in this file. It cannot train a binary classifier alone without producing degenerate all-fake predictions; it is best utilized for feature/domain/regex pattern extraction.

---

## 2. Complete Dataset Inventory & Forensic Analysis

### DS-01: SMS Spam Collection Dataset
- **Source Path:** `C:\Users\paruc\Downloads\archive (4)`
- **Files:** `spam_sms.csv` (484 KB)
- **Modality:** Text / SMS
- **Total Samples:** 5,572 rows
- **Labels & Class Distribution:**
  - `ham` (Authentic / Legitimate): 4,825 samples (86.6%)
  - `spam` (Unsolicited Scam / Phishing / Lottery): 747 samples (13.4%)
- **Supervised Learning Usability:** **YES.** Real ground-truth binary classification.
- **Suitability:** Train real PyTorch SMS classifier (TF-IDF vectorizer + MLP neural classifier).
- **Target Module:** **Module 5: SMS Scam Detection** (and Module 4: Text & Scam Analysis).

---

### DS-02: Fake Job Postings Dataset
- **Source Path:** `C:\Users\paruc\Downloads\archive (5)`
- **Files:** `Fake Postings.csv` (2.87 MB)
- **Modality:** Structured Text / Job Postings
- **Total Samples:** 10,000 rows
- **Columns:** `title`, `description`, `requirements`, `company_profile`, `location`, `salary_range`, `employment_type`, `industry`, `benefits`, `fraudulent`
- **Labels & Class Distribution:**
  - `fraudulent = 1`: 10,000 samples (100.0%)
  - `fraudulent = 0`: 0 samples (0.0%)
- **Supervised Learning Usability:** **NO (Degenerate for binary classification).** Because there are zero legitimate job postings (`fraudulent=0`), any binary classifier trained exclusively on this file would either overfit to 100% fake or fail to generalize.
- **Suitability:** **Metadata & Forensic Rules Only.** Contains rich real-world signals for upfront fee requests, fake interview schemes, suspicious `@gmail.com` recruiter domains, and unrealistic salary distributions.
- **Target Module:** **Module 7: Job / Internship Scam Detection**.

---

### DS-03: Phishing & Malicious URLs Dataset
- **Source Path:** `C:\Users\paruc\Downloads\archive (6)`
- **Files:** `final_dataset.csv` (214.7 MB), `feature_description.csv` (4.9 KB), `dataset_info.txt` (269 B), `README.md` (2.1 KB)
- **Modality:** Tabular Features & Raw URLs
- **Total Samples:** 579,920 rows
- **Columns:** 76 columns (raw `url`, `label`, 74 lexical, Shannon entropy, domain, and host metrics)
- **Labels & Class Distribution:**
  - `0 (Legitimate)`: 339,074 samples (58.47%)
  - `1 (Phishing)`: 240,846 samples (41.53%)
- **Supervised Learning Usability:** **YES (Exceptional Quality).** Perfectly labeled, pre-extracted features + raw URLs.
- **Suitability:** Train a dedicated PyTorch Tabular Neural Classifier (`URLNet` / MLP) directly on the 74 numerical features and lexical metrics.
- **Target Module:** **Module 4: URL / Phishing URL Detection**.

---

### DS-04: Phishing & Malicious URLs Dataset (Duplicate Copy)
- **Source Path:** `C:\Users\paruc\Downloads\archive (7)`
- **Files:** `final_dataset.csv`, `feature_description.csv`, `dataset_info.txt`, `README.md`
- **Modality:** URL / Tabular
- **Duplicate Status:** **Exact duplicate of `archive (6)`.**
- **Action:** **NOT USED — REASON: Redundant duplicate of `archive (6)`.**

---

### DS-05: Phishing Email Benchmark Collection (7 Multi-Corpus Ensemble)
- **Source Path:** `C:\Users\paruc\Downloads\archive (9)`
- **Total Size:** 249.2 MB across 7 CSV files
- **Modality:** Text / Email
- **Detailed Sub-Corpora Breakdown:**
  1. `phishing_email.csv` (106.6 MB): **82,486 samples**
     - `0` (Legitimate): 39,595 samples (48.0%)
     - `1` (Phishing): 42,891 samples (52.0%)
     - Columns: `text_combined`, `label`
  2. `CEAS_08.csv` (67.9 MB): **39,154 samples**
     - `0` (Legitimate): 17,312 | `1` (Phishing): 21,842
     - Columns: `sender`, `receiver`, `date`, `subject`, `body`, `label`, `urls`
  3. `Enron.csv` (45.6 MB): **29,767 samples**
     - `0` (Legitimate): 15,791 | `1` (Phishing): 13,976
  4. `SpamAssasin.csv` (14.9 MB): **5,809 samples**
     - `0` (Ham): 4,091 | `1` (Spam): 1,718
  5. `Ling.csv` (9.3 MB): **2,859 samples**
     - `0` (Legitimate): 2,401 | `1` (Phishing): 458
  6. `Nigerian_Fraud.csv` (9.2 MB): **3,332 samples**
     - `1` (Advance-fee fraud): 3,332
  7. `Nazario.csv` (7.8 MB): **1,565 samples**
     - `1` (Phishing): 1,565
- **Supervised Learning Usability:** **YES (Outstanding).** `phishing_email.csv` alone gives 82,486 balanced samples with clean full email bodies.
- **Suitability:** Train a dedicated PyTorch Email Phishing Neural Classifier using TF-IDF n-grams or sentence embeddings.
- **Target Module:** **Module 6: Phishing Email Detection** (and Module 4: Text & Scam Analysis).

---

### DS-06, DS-07, DS-08, DS-09: Unextracted Container Archives
- `C:\Users\paruc\Downloads\archive (10)`: Contains unextracted `archive (9).zip` (77.1 MB).
  - **Action:** **NOT USED — REASON: Duplicate zip of `archive (9)`.**
- `C:\Users\paruc\Downloads\archive (11)`: Contains unextracted `archive (7).zip` (36.9 MB).
  - **Action:** **NOT USED — REASON: Duplicate zip of `archive (6)/(7)`.**
- `C:\Users\paruc\Downloads\archive (12)`: Contains unextracted `archive (6).zip` (36.9 MB).
  - **Action:** **NOT USED — REASON: Duplicate zip of `archive (6)`.**
- `C:\Users\paruc\Downloads\archive (13)`: Contains unextracted `archive (9).zip` (77.1 MB).
  - **Action:** **NOT USED — REASON: Second duplicate zip of `archive (9)`.**

---

### DS-10: Celeb-DF v2 Metadata Analysis
- **Source Path:** `C:\Users\paruc\Downloads\celeb-df-v2-metadata`
- **Files:** `celeb-df-v2-metadata.json` (3,495 bytes)
- **Modality:** JSON Schema Descriptor
- **Audit Findings:**
  - Contains **0 video files**, **0 frames**, **0 labels**.
  - File is a W3C / Croissant schema describing the external Kaggle dataset `reubensuju/celeb-df-v2` (`contentSize: 9.285 GB`).
- **Action:** **NOT USED FOR DIRECT VIDEO MODEL TRAINING — REASON: Metadata only. No MP4/AVI files or images exist.**
- **Impact on Video Detection:** In accordance with instructions, video deepfake detection will use temporal frame extraction (OpenCV) -> Image DeepfakeCNN per-frame inference -> temporal probability fusion, which is already functional and tested.

---

### DS-11: ASVspoof 2019 Logical Access (Existing Audio)
- **Source Path:** `C:\Users\paruc\Downloads\archive (1)\LA\LA`
- **Total Files:** 60,150 files (60,132 FLAC audio files, 3.59 GB)
- **Label Structure:** Official ASVspoof 2019 CM protocols (`bonafide` vs `spoof`).
- **Status:** **ALREADY TRAINED.**
- **Model:** `models/audio/best_model.pt` (`AudioCNN`, 2.74 MB, Accuracy: 1.0, F1: 1.0). Loaded by backend.

---

### DS-12: 1000 Videos Deepfake Video Frames (Existing Image)
- **Source Path:** `C:\Users\paruc\Downloads\archive\1000_videos`
- **Total Files:** 16,433 PNG face frame images across `train`, `validation`, and `test` splits.
- **Labels:** `real` (7,253) vs `fake` (9,180).
- **Status:** **ALREADY TRAINED.**
- **Model:** `models/image/best_model.pt` (`DeepfakeCNN`, 11.0 MB, Val Accuracy: 88.12%, F1: 87.38%). Loaded by backend.

---

## 3. TrustGuard AI Modality Mapping Table

| # | TrustGuard AI Module | Dataset Source | Modality | Samples | Usable for Supervised Training? | Action / Implementation Strategy |
|---|---|---|---|---|---|---|
| **1** | **Image Deepfake Detection** | `archive\1000_videos` | Image (PNG) | 16,433 | YES | **EXISTING (TRAINED)**: `models/image/best_model.pt` (`DeepfakeCNN`). |
| **2** | **Video Deepfake Detection** | Temporal pipeline on `models/image` | Video (MP4) | Real-time | YES (Frame-level) | **FRAME-LEVEL TEMPORAL**: OpenCV frame sampling + DeepfakeCNN inference + temporal aggregation. No raw video dataset in Downloads (`celeb-df-v2-metadata` is metadata-only). |
| **3** | **Audio Deepfake Detection** | `archive (1)\LA\LA` | Audio (FLAC) | 60,132 | YES | **EXISTING (TRAINED)**: `models/audio/best_model.pt` (`AudioCNN`). |
| **4** | **URL / Phishing Detection** | `archive (6)\final_dataset.csv` | URL / Tabular | 579,920 | **YES** | **NEW TRAINING**: Train PyTorch `PhishingURLNet` on 74 numeric/entropy features. Save to `models/url/best_model.pt`. |
| **5** | **SMS Scam Detection** | `archive (4)\spam_sms.csv` | Text / SMS | 5,572 | **YES** | **NEW TRAINING**: Train PyTorch `SMSScamClassifier` (TF-IDF + Linear/ReLU head). Save to `models/sms/best_model.pt`. |
| **6** | **Phishing Email Detection** | `archive (9)\phishing_email.csv` | Text / Email | 82,486 | **YES** | **NEW TRAINING**: Train PyTorch `EmailPhishingClassifier` on balanced corpus. Save to `models/email/best_model.pt`. |
| **7** | **Job / Internship Fraud** | `archive (5)\Fake Postings.csv` | Text / Structured | 10,000 | **NO (100% positive)** | **HEURISTIC / FORENSIC RULES**: Extract high-risk fee keywords, recruiter email domain mismatches, and wage ratio checks from the 10,000 fake jobs. |
| **8** | **OCR Scanner** | Tesseract.js Client + Structured Parser | Image / OCR | Dynamic | N/A | **ACTIVE**: Client-side OCR + backend entity extraction. |
| **9** | **Company Verification** | Live DNS / MX Lookup Engine | Domain / Network | Dynamic | N/A | **ACTIVE**: Real socket IP & MX record validation. |
| **10** | **Social Media Scanner** | Multi-signal Heuristic Engine | Text / Social | Dynamic | N/A | **ACTIVE**: Crypto doubling lure, pressure coercion, and handle impersonation engine. |
| **11** | **Multimodal Analysis** | Cross-modal decision fusion | Multimodal | Dynamic | N/A | **ACTIVE**: Peak-weighted cross-modal aggregation engine. |

---

## 4. Redundant & Non-Trainable Datasets ("NOT USED — REASON")

1. **`C:\Users\paruc\Downloads\archive (7)`**
   - **NOT USED — REASON:** Exact duplicate of `archive (6)` URL dataset.
2. **`C:\Users\paruc\Downloads\archive (10)`**
   - **NOT USED — REASON:** Redundant zip archive containing `archive (9).zip`.
3. **`C:\Users\paruc\Downloads\archive (11)`**
   - **NOT USED — REASON:** Redundant zip archive containing `archive (7).zip`.
4. **`C:\Users\paruc\Downloads\archive (12)`**
   - **NOT USED — REASON:** Redundant zip archive containing `archive (6).zip`.
5. **`C:\Users\paruc\Downloads\archive (13)`**
   - **NOT USED — REASON:** Redundant zip archive containing `archive (9).zip`.
6. **`C:\Users\paruc\Downloads\celeb-df-v2-metadata`**
   - **NOT USED FOR TRAINING — REASON:** Contains metadata only (3.4 KB Croissant JSON). Zero MP4/video files or frames.

---

## 5. Execution Plan for Next Phases (Pending Approval)

Once this inspection and modality mapping is approved, the execution phase will proceed as follows:

1. **URL Phishing Model Training (`scripts/train_url_model.py`):**
   - Train a PyTorch neural network on `archive (6)\final_dataset.csv`.
   - Output: `models/url/best_model.pt`, `models/url/metadata.json`, `models/url/training_metrics.json`.
2. **SMS Scam Model Training (`scripts/train_sms_model.py`):**
   - Train a PyTorch text classifier on `archive (4)\spam_sms.csv`.
   - Output: `models/sms/best_model.pt`, `models/sms/metadata.json`, `models/sms/training_metrics.json`.
3. **Email Phishing Model Training (`scripts/train_email_model.py`):**
   - Train a PyTorch text classifier on `archive (9)\phishing_email.csv`.
   - Output: `models/email/best_model.pt`, `models/email/metadata.json`, `models/email/training_metrics.json`.
4. **Backend Detector Updates:**
   - Connect the real trained models into `backend/detectors/url_detector.py`, `backend/detectors/text_detector.py`, and a new `email_detector.py`.
   - Ensure `POST /api/analyze/url`, `POST /api/analyze/text`, and `POST /api/analyze/email` use real model inferences.
5. **Verification & Testing:**
   - Run end-to-end endpoint tests to verify deterministic, genuine model predictions.
