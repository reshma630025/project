"""
Verify AudioCNN on truly unseen ASVspoof 2019 LA samples.
Tests 200 unseen bonafide and 200 unseen spoof files that were never in the training/validation/test manifest.
"""
import os
import sys
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix
)

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"c:\Users\paruc\OneDrive\Desktop\reshma1-main\reshma1-main")
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.train_audio_model import AudioCNN, parse_protocol, load_flac, compute_mel_spectrogram, SAMPLE_RATE, N_MELS, MAX_FRAMES

DATASET_ROOT = Path(r"C:\Users\paruc\Downloads\archive (1)\LA\LA")
DEV_AUDIO_DIR = DATASET_ROOT / "ASVspoof2019_LA_dev" / "flac"
DEV_PROTO = DATASET_ROOT / "ASVspoof2019_LA_cm_protocols" / "ASVspoof2019.LA.cm.dev.trl.txt"
MANIFEST_PATH = PROJECT_ROOT / "data" / "audio_dataset_manifest.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "audio" / "best_model.pt"

print("==========================================================")
print("   INDEPENDENT AUDIT: AUDIOCNN ON TRULY UNSEEN SAMPLES   ")
print("==========================================================")

# Load previously used manifest to ensure 100% disjoint exclusion
used_df = pd.read_csv(MANIFEST_PATH)
used_files = set(Path(p).name for p in used_df['file_path'])
print(f"Loaded {len(used_files)} previously sampled audio files.")

# Parse protocol for all available samples
all_samples = parse_protocol(DEV_PROTO, DEV_AUDIO_DIR)
unseen_bonafide = [s for s in all_samples if s[1] == 0 and s[0].name not in used_files]
unseen_spoof = [s for s in all_samples if s[1] == 1 and s[0].name not in used_files]

print(f"Available truly unseen pool: {len(unseen_bonafide)} bonafide, {len(unseen_spoof)} spoof.")

# Sample 100 truly unseen bonafide and 100 truly unseen spoof
np.random.seed(12345)
sample_bon = [unseen_bonafide[i] for i in np.random.choice(len(unseen_bonafide), size=min(100, len(unseen_bonafide)), replace=False)]
sample_spf = [unseen_spoof[i] for i in np.random.choice(len(unseen_spoof), size=min(100, len(unseen_spoof)), replace=False)]
test_pool = sample_bon + sample_spf
np.random.shuffle(test_pool)

print(f"Testing on {len(test_pool)} truly unseen audio samples ({len(sample_bon)} bonafide, {len(sample_spf)} spoof)...")

# Load model
model = AudioCNN()
state = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
model.load_state_dict(state)
model.eval()

y_true = []
y_pred = []
y_probs = []

start_t = time.time()
for fpath, label_int, label_str in test_pool:
    data, sr = load_flac(fpath)
    if data is None:
        continue
    mel = compute_mel_spectrogram(data, sr=sr)
    mel = (mel - mel.mean()) / (mel.std() + 1e-8)
    if mel.shape[1] < MAX_FRAMES:
        mel = np.pad(mel, ((0, 0), (0, MAX_FRAMES - mel.shape[1])))
    else:
        mel = mel[:, :MAX_FRAMES]
    t_in = torch.from_numpy(mel).unsqueeze(0).unsqueeze(0).float()
    
    with torch.no_grad():
        out = model(t_in)
        prob = torch.softmax(out, dim=1)[0, 1].item()
        pred = 1 if prob >= 0.5 else 0
        
    y_true.append(label_int)
    y_pred.append(pred)
    y_probs.append(prob)

total_time = time.time() - start_t
y_true = np.array(y_true)
y_pred = np.array(y_pred)
y_probs = np.array(y_probs)

acc = accuracy_score(y_true, y_pred)
prec = precision_score(y_true, y_pred, zero_division=0)
rec = recall_score(y_true, y_pred, zero_division=0)
f1 = f1_score(y_true, y_pred, zero_division=0)
roc_auc = roc_auc_score(y_true, y_probs)
cm = confusion_matrix(y_true, y_pred).tolist()

print("\n--- INDEPENDENT UNSEEN TEST EVALUATION ---")
print(f"  Samples Tested:    {len(y_true)} (100 Bonafide, 100 Spoof)")
print(f"  Unseen Accuracy:   {acc*100:.2f}%")
print(f"  Unseen Precision:  {prec*100:.2f}%")
print(f"  Unseen Recall:     {rec*100:.2f}%")
print(f"  Unseen F1 Score:   {f1*100:.2f}%")
print(f"  Unseen ROC-AUC:    {roc_auc:.4f}")
print(f"  Confusion Matrix:  {cm}")
print(f"    [TN={cm[0][0]}, FP={cm[0][1]}] (Bonafide)")
print(f"    [FN={cm[1][0]}, TP={cm[1][1]}] (Spoof)")
print(f"  Evaluation Time:   {total_time:.2f}s")

# Save audit results
out_file = PROJECT_ROOT / "models" / "audio" / "independent_test_audit.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump({
        "model_name": "AudioCNN",
        "dataset": "ASVspoof 2019 LA (archive (1))",
        "unseen_samples_tested": len(y_true),
        "unseen_accuracy": round(acc, 4),
        "unseen_precision": round(prec, 4),
        "unseen_recall": round(rec, 4),
        "unseen_f1": round(f1, 4),
        "unseen_roc_auc": round(roc_auc, 4),
        "confusion_matrix": cm,
        "evaluation_duration_seconds": round(total_time, 2)
    }, f, indent=2)

print(f"\nSaved independent audit to: {out_file}")
