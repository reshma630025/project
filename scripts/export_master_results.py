"""
TrustGuard AI — Export Master Final Test Results & Video Confusion Matrix
Compiles all held-out test evaluations into FINAL_TEST_RESULTS.json and FINAL_TEST_RESULTS.csv
and generates video_confusion_matrix.png.
"""
import os
import sys
import json
import csv
from pathlib import Path
from datetime import datetime

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(r"c:\Users\paruc\OneDrive\Desktop\reshma1-main\reshma1-main")
CM_DIR = PROJECT_ROOT / "reports" / "confusion_matrices"
CM_DIR.mkdir(parents=True, exist_ok=True)

# Generate Video Confusion Matrix PNG
cm_vid = np.array([[21, 9], [25, 5]])
plt.figure(figsize=(6, 5))
plt.imshow(cm_vid, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Video Deepfake Benchmark (Celeb-DF v2)', fontsize=12, fontweight='bold', pad=12)
plt.colorbar()
tick_marks = np.arange(2)
plt.xticks(tick_marks, ['Real', 'Deepfake'], fontsize=10)
plt.yticks(tick_marks, ['Real', 'Deepfake'], fontsize=10)
thresh = cm_vid.max() / 2.0
for i in range(2):
    for j in range(2):
        plt.text(j, i, f'{cm_vid[i, j]}', ha='center', va='center',
                 color='white' if cm_vid[i, j] > thresh else 'black',
                 fontsize=11, fontweight='bold')
plt.ylabel('True Label', fontsize=11, fontweight='bold')
plt.xlabel('Predicted Label', fontsize=11, fontweight='bold')
plt.tight_layout()
vid_cm_path = CM_DIR / "video_confusion_matrix.png"
plt.savefig(vid_cm_path, dpi=200)
plt.close()
print(f"Generated {vid_cm_path.name} successfully.")

master_results = [
    {
        "module": "Image Deepfake",
        "dataset": "archive (1000 Videos)",
        "train_samples": 4000,
        "val_samples": 800,
        "test_samples": 800,
        "accuracy": "88.12%",
        "precision": "93.20%",
        "recall": "82.25%",
        "f1": "87.38%",
        "roc_auc": "0.9626",
        "model_type": "DeepfakeCNN (PyTorch Vision CNN)"
    },
    {
        "module": "Audio Deepfake",
        "dataset": "archive (1) ASVspoof 2019 LA",
        "train_samples": 4000,
        "val_samples": 800,
        "test_samples": 200,
        "accuracy": "99.50%",
        "precision": "100.00%",
        "recall": "99.00%",
        "f1": "99.50%",
        "roc_auc": "1.0000",
        "model_type": "AudioCNN (Mel-STFT Spectrogram CNN)"
    },
    {
        "module": "SMS Scam",
        "dataset": "archive (4) spam_sms.csv",
        "train_samples": 4457,
        "val_samples": 557,
        "test_samples": 558,
        "accuracy": "98.57%",
        "precision": "97.18%",
        "recall": "92.00%",
        "f1": "94.52%",
        "roc_auc": "0.9831",
        "model_type": "SMSScamClassifier (TF-IDF + Neural Classifier)"
    },
    {
        "module": "URL Phishing",
        "dataset": "archive (6) final_dataset.csv",
        "train_samples": 48000,
        "val_samples": 6000,
        "test_samples": 2000,
        "accuracy": "99.60%",
        "precision": "100.00%",
        "recall": "99.57%",
        "f1": "99.79%",
        "roc_auc": "0.9994",
        "model_type": "PhishingURLNet (Tabular 74-feat Deep NN)"
    },
    {
        "module": "Email Phishing",
        "dataset": "archive (9) phishing_email.csv",
        "train_samples": 32000,
        "val_samples": 4000,
        "test_samples": 2000,
        "accuracy": "99.65%",
        "precision": "98.12%",
        "recall": "99.68%",
        "f1": "98.89%",
        "roc_auc": "0.9995",
        "model_type": "EmailPhishingClassifier (TF-IDF + Neural Classifier)"
    },
    {
        "module": "Social Media (Profiles)",
        "dataset": "archive (15) raw_user_profiles.csv",
        "train_samples": 4000,
        "val_samples": 500,
        "test_samples": 500,
        "accuracy": "92.00%",
        "precision": "77.07%",
        "recall": "96.80%",
        "f1": "85.82%",
        "roc_auc": "0.9897",
        "model_type": "SocialProfileNet (Tabular Profile NN)"
    },
    {
        "module": "Social Media (Instagram)",
        "dataset": "archive (14) test.csv / train.csv",
        "train_samples": 576,
        "val_samples": "N/A",
        "test_samples": 120,
        "accuracy": "88.33%",
        "precision": "91.07%",
        "recall": "85.00%",
        "f1": "87.93%",
        "roc_auc": "0.9061",
        "model_type": "SocialSpamNet (Instagram Account Classifier)"
    },
    {
        "module": "Video Deepfake",
        "dataset": "archive (16) Celeb-DF v2 Benchmark",
        "train_samples": "N/A",
        "val_samples": "N/A",
        "test_samples": 60,
        "accuracy": "43.33%",
        "precision": "35.71%",
        "recall": "16.67%",
        "f1": "22.73%",
        "roc_auc": "N/A",
        "model_type": "frame_level_aggregation (Vision CNN)"
    },
    {
        "module": "Job / Internship Scam",
        "dataset": "archive (5) Fake Postings.csv",
        "train_samples": "N/A (100% fraudulent)",
        "val_samples": "N/A",
        "test_samples": "N/A",
        "accuracy": "N/A",
        "precision": "N/A",
        "recall": "N/A",
        "f1": "N/A",
        "roc_auc": "N/A",
        "model_type": "Heuristic Forensics (jobModelType=heuristic)"
    }
]

final_json = PROJECT_ROOT / "FINAL_TEST_RESULTS.json"
final_csv = PROJECT_ROOT / "FINAL_TEST_RESULTS.csv"

with open(final_json, "w", encoding="utf-8") as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "evaluation_standard": "Held-Out TEST Split Unbiased Evaluation (Zero Leakage)",
        "results": master_results
    }, f, indent=2)

with open(final_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "module", "dataset", "train_samples", "val_samples", "test_samples",
        "accuracy", "precision", "recall", "f1", "roc_auc", "model_type"
    ])
    writer.writeheader()
    for r in master_results:
        writer.writerow(r)

print("Exported FINAL_TEST_RESULTS.json and FINAL_TEST_RESULTS.csv successfully.")
