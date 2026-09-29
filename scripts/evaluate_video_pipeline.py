"""
TrustGuard AI — Video Deepfake Pipeline Evaluation on Real Video Datasets (archive (16) Celeb-DF v2)
Evaluates production frame-level temporal aggregation pipeline on actual .mp4 test videos.
"""
import os
import sys
import time
import json
from pathlib import Path
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"c:\Users\paruc\OneDrive\Desktop\reshma1-main\reshma1-main")
sys.path.insert(0, str(PROJECT_ROOT))

from backend.detectors.video_detector import analyze_video_file

ARCHIVE_16 = Path(r"C:\Users\paruc\Downloads\archive (16)")
TEST_LIST = ARCHIVE_16 / "List_of_testing_videos.txt"
MODELS_VIDEO_DIR = PROJECT_ROOT / "models" / "video"
MODELS_VIDEO_DIR.mkdir(parents=True, exist_ok=True)

print("==========================================================")
print("  TRUSTGUARD AI: VIDEO PIPELINE BENCHMARK (CELEB-DF v2)   ")
print("==========================================================")

if not TEST_LIST.exists():
    print(f"Error: {TEST_LIST} not found!")
    sys.exit(1)

with open(TEST_LIST, "r") as f:
    lines = [line.strip().split(" ", 1) for line in f if line.strip()]

# Parse lines: label, rel_path
# In Celeb-DF v2 standard benchmark:
# 1 = Real (YouTube-real or Celeb-real)
# 0 = Fake (Celeb-synthesis)
real_videos = []
fake_videos = []

for label_str, rel_path in lines:
    label = int(label_str)
    full_path = ARCHIVE_16 / rel_path.replace("/", "\\")
    if full_path.exists():
        if label == 1:
            real_videos.append((full_path, 0)) # 0 = Authentic/Real
        else:
            fake_videos.append((full_path, 1)) # 1 = Deepfake/Manipulated

print(f"Found {len(real_videos)} real test videos and {len(fake_videos)} fake test videos in benchmark list.")

# Sample 30 real and 30 fake videos for balanced evaluation
np.random.seed(42)
sample_real_indices = np.random.choice(len(real_videos), size=min(30, len(real_videos)), replace=False)
sample_fake_indices = np.random.choice(len(fake_videos), size=min(30, len(fake_videos)), replace=False)

eval_set = [real_videos[i] for i in sample_real_indices] + [fake_videos[i] for i in sample_fake_indices]
np.random.shuffle(eval_set)

print(f"Selected {len(eval_set)} held-out .mp4 test videos ({len(sample_real_indices)} real, {len(sample_fake_indices)} fake).")

y_true = []
y_pred = []
y_scores = []
results_log = []

start_eval = time.time()
print("\nRunning frame-level temporal inference on videos...")

for idx, (vid_path, true_label) in enumerate(eval_set, 1):
    t0 = time.time()
    try:
        with open(vid_path, "rb") as vf:
            vid_bytes = vf.read()
        res = analyze_video_file(vid_bytes, sample_interval=1.0, max_frames=8)
        elapsed = time.time() - t0
        
        # Determine predicted binary label
        # 1 = Deepfake/Manipulated (if AI-GENERATED or SUSPICIOUS with risk >= 45)
        # 0 = Real
        risk = res.get("risk_score", 50.0)
        classification = res.get("classification", "UNCERTAIN")
        pred_label = 1 if (risk >= 45.0 or classification == "AI-GENERATED") else 0
        
        y_true.append(true_label)
        y_pred.append(pred_label)
        y_scores.append(risk)
        
        is_correct = (pred_label == true_label)
        status_sym = "✓" if is_correct else "✗"
        
        results_log.append({
            "video": vid_path.name,
            "folder": vid_path.parent.name,
            "true_class": "Real" if true_label == 0 else "Fake",
            "pred_class": "Real" if pred_label == 0 else "Fake",
            "risk_score": risk,
            "confidence": res.get("confidence", 0.0),
            "analyzed_frames": res.get("analyzed_frames", 0),
            "correct": is_correct,
            "duration_sec": res.get("duration", 0.0),
            "latency_sec": round(elapsed, 2)
        })
        
        if idx % 10 == 0 or idx == len(eval_set):
            print(f"[{idx:02d}/{len(eval_set):02d}] {vid_path.name[:25]:25s} | True: {'Real' if true_label==0 else 'Fake'} | Pred: {'Real' if pred_label==0 else 'Fake'} (Risk: {risk:.1f}/100) {status_sym} ({elapsed:.2f}s)")
            
    except Exception as e:
        print(f"Error processing {vid_path.name}: {e}")

total_time = time.time() - start_eval
y_true = np.array(y_true)
y_pred = np.array(y_pred)

acc = accuracy_score(y_true, y_pred)
prec = precision_score(y_true, y_pred, zero_division=0)
rec = recall_score(y_true, y_pred, zero_division=0)
f1 = f1_score(y_true, y_pred, zero_division=0)
cm = confusion_matrix(y_true, y_pred).tolist()

print("\n==========================================================")
print("     CELEB-DF v2 REAL VIDEO PIPELINE BENCHMARK RESULTS    ")
print("==========================================================")
print(f"  Pipeline Type:     Frame-Level Video Deepfake Detection (Temporal Aggregation)")
print(f"  Underlying Model:  DeepfakeCNN (PyTorch Image Checkpoint)")
print(f"  Test Videos:       {len(y_true)} (.mp4 format)")
print(f"  Video Accuracy:    {acc*100:.2f}%")
print(f"  Video Precision:   {prec*100:.2f}%")
print(f"  Video Recall:      {rec*100:.2f}%")
print(f"  Video F1 Score:    {f1*100:.2f}%")
print(f"  Confusion Matrix:  {cm}")
print(f"    [TN={cm[0][0]}, FP={cm[0][1]}] (Real Videos)")
print(f"    [FN={cm[1][0]}, TP={cm[1][1]}] (Fake Videos)")
print(f"  Total Eval Time:   {total_time:.2f}s (Avg {total_time/len(y_true):.2f}s/video)")

eval_payload = {
    "module": "Video Deepfake Detection",
    "pipeline_type": "Frame-Level Video Deepfake Detection",
    "model_type": "frame_level_aggregation",
    "dataset": "Celeb-DF v2 (archive (16))",
    "test_samples": len(y_true),
    "class_distribution": {"real": int(np.sum(y_true == 0)), "fake": int(np.sum(y_true == 1))},
    "metrics": {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1": round(f1, 4),
        "confusion_matrix": cm
    },
    "evaluation_time_seconds": round(total_time, 2),
    "sample_evaluations": results_log[:15]
}

eval_file = MODELS_VIDEO_DIR / "evaluation_metrics.json"
with open(eval_file, "w", encoding="utf-8") as f:
    json.dump(eval_payload, f, indent=2)

print(f"\nSaved video evaluation metrics to: {eval_file}")
