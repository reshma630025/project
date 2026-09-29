# TrustGuard AI — Social Media Model Training & Evaluation Report

**Model Name:** `SocialSpamNet` (Deep Tabular Neural Classifier)  
**Task:** Fake Account, Bot & Spammer Profile Detection  
**Evaluation Date:** September 8, 2026  
**Primary Dataset:** Kaggle Instagram Fake Spammer Genuine Accounts (`C:\Users\paruc\Downloads\archive (14)`)  
**Secondary Dataset Reference:** Fake Profile and Post Detection on Social Media (`C:\Users\paruc\Downloads\archive (15)`)  
**Framework:** PyTorch 2.6.0+cpu / scikit-learn  
**Artifact Directory:** `models/social/`

---

## 1. Dataset Inspection & Characteristics

### Dataset Path: `C:\Users\paruc\Downloads\archive (14)`
- **Files:** `train.csv` (18,733 bytes), `test.csv` (3,932 bytes)
- **Train Set Size:** 576 samples
- **Test Set Size:** 120 samples (Official unseen benchmark split)
- **Target Feature:** `fake`
  - `0`: Genuine / Authentic Profile (50.0% in train: 288 samples; 50.0% in test: 60 samples)
  - `1`: Fake / Spammer / Bot Profile (50.0% in train: 288 samples; 50.0% in test: 60 samples)
  - Class balance: Exactly 1.0 (Zero class imbalance)
- **Null / Missing Values:** 0 across all columns
- **Input Features (11):**
  1. `profile pic` (binary int: 0 or 1): Whether account possesses a customized profile image.
  2. `nums/length username` (float [0, 1]): Ratio of numeric digits to total username character length.
  3. `fullname words` (integer): Total token count in the profile full name.
  4. `nums/length fullname` (float [0, 1]): Ratio of numeric digits to full name character length.
  5. `name==username` (binary int: 0 or 1): Whether username matches full name identically.
  6. `description length` (integer): Character count of the biography/bio field.
  7. `external URL` (binary int: 0 or 1): Presence of an outbound web link in bio.
  8. `private` (binary int: 0 or 1): Account privacy flag.
  9. `#posts` (integer): Total lifetime published posts.
  10. `#followers` (integer): Total follower count.
  11. `#follows` (integer): Total following count.

---

## 2. Model Architecture: `SocialSpamNet`

A deep tabular multi-layer perceptron designed specifically for social network profile telemetry:

```text
Input (11 normalized profile features)
  │
  ▼
Linear(11, 64) -> BatchNorm1d(64) -> LeakyReLU(negative_slope=0.1) -> Dropout(0.25)
  │
  ▼
Linear(64, 32) -> BatchNorm1d(32) -> LeakyReLU(negative_slope=0.1) -> Dropout(0.15)
  │
  ▼
Linear(32, 16) -> LeakyReLU(negative_slope=0.1)
  │
  ▼
Linear(16, 2)
  │
  ▼
Softmax (Genuine: Class 0 vs Fake/Spammer: Class 1)
```

- **Total Trainable Parameters:** 3,602 parameters
- **Optimizer:** AdamW (`lr=0.003, weight_decay=1e-4`)
- **Loss Function:** CrossEntropyLoss
- **Scheduler:** ReduceLROnPlateau (`factor=0.5, patience=5`)
- **Batch Size:** 32 | **Epochs:** 40 | **Training Time:** 3.16 seconds

---

## 3. Test Set Evaluation Performance

Evaluated strictly on the 120 official unseen test profiles (`test.csv`):

| Metric | Score | Performance Assessment |
|---|---|---|
| **Accuracy** | **90.83%** | 109 / 120 test accounts correctly classified |
| **Precision** | **92.98%** | Very low false positive rate (identifies real accounts reliably) |
| **Recall** | **88.33%** | 53 out of 60 actual fake/bot accounts detected |
| **F1 Score** | **90.60%** | Exceptional harmonic mean of precision and recall |

### Confusion Matrix (Test Set N=120)

```text
                  Predicted Genuine (0)    Predicted Fake (1)
Actual Genuine (0)        56 (TN)                  4 (FP)
Actual Fake (1)            7 (FN)                 53 (TP)
```

- **True Negatives (TN):** 56 authentic profiles verified as Genuine
- **True Positives (TP):** 53 spam/bot profiles caught and flagged as Fake
- **False Positives (FP):** 4 profiles falsely flagged (3.3% false alarm rate)
- **False Negatives (FN):** 7 evasive bots missed (5.8% evasion rate)

---

## 4. Exported Production Artifacts

All model artifacts are persisted in the version-controlled model repository:

- `models/social/best_model.pt`: Serialized PyTorch state dictionary (best validation checkpoint).
- `models/social/scaler.pkl`: Serialized `StandardScaler` fitted on the 11 feature distributions.
- `models/social/feature_names.json`: Canonical feature order descriptor for inference alignment.
- `models/social/metadata.json`: Machine-readable training metadata, split sizes, and timestamp.

---

## 5. Integration Summary

- **Backend Integration:** Wrapped in `SocialMediaDetector` in `backend/detectors/social_detector.py`.
- **API Endpoint:** `POST /api/analyze/social` (supports raw manual profile fields, dataset row dicts, or CSV upload).
- **Frontend UI:** Integrated into the Universal "Verify Any Content" Dashboard and the dedicated Social Media Verification page (`#page-social`).
- **Database Tracking:** Every social scan logs classification, confidence, risk score, and profile telemetry into SQLite `scan_history`.
