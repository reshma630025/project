"""
TrustGuard AI — Video Dataset Metric Evaluation (Celeb-DF v2 & FaceForensics++ C23)
Evaluates video-level predictions with the frame-level aggregation pipeline
and saves separate metrics, confusion matrix plots, and metadata for both benchmarks.
"""
import os
import sys
import glob
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.detectors.video_detector import analyze_video_file

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
MODELS_VIDEO_DIR = os.path.join(PROJECT_ROOT, "models", "video")
os.makedirs(MODELS_VIDEO_DIR, exist_ok=True)

print("=" * 70)
print("     TRUSTGUARD AI: VIDEO BENCHMARK METRIC EVALUATION")
print("=" * 70)

def evaluate_dataset(name, real_paths, fake_paths):
    print(f"\nEvaluating Benchmark: {name}")
    print(f"  Real Videos: {len(real_paths)}, Fake Videos: {len(fake_paths)}")
    
    y_true = []
    y_pred = []
    y_scores = []
    video_records = []

    # Real videos (label = 0)
    for p in real_paths:
        with open(p, "rb") as f:
            vbytes = f.read()
        res = analyze_video_file(vbytes)
        pred_label = res.get("classification") or res.get("status", "UNKNOWN")
        risk = res.get("risk_score", 0.0)
        is_pred_fake = 1 if (risk > 40.0 or pred_label in ["AI-GENERATED", "LIKELY AI-GENERATED", "SUSPICIOUS"]) else 0
        y_true.append(0)
        y_pred.append(is_pred_fake)
        y_scores.append(risk)
        video_records.append({
            "file": os.path.basename(p),
            "ground_truth": "REAL",
            "prediction": pred_label,
            "risk_score": risk,
            "confidence": res.get("confidence", 0.0),
            "analyzed_frames": res.get("analyzed_frames", 0)
        })

    # Fake videos (label = 1)
    for p in fake_paths:
        with open(p, "rb") as f:
            vbytes = f.read()
        res = analyze_video_file(vbytes)
        pred_label = res.get("classification") or res.get("status", "UNKNOWN")
        risk = res.get("risk_score", 0.0)
        is_pred_fake = 1 if (risk > 40.0 or pred_label in ["AI-GENERATED", "LIKELY AI-GENERATED", "SUSPICIOUS"]) else 0
        y_true.append(1)
        y_pred.append(is_pred_fake)
        y_scores.append(risk)
        video_records.append({
            "file": os.path.basename(p),
            "ground_truth": "FAKE",
            "prediction": pred_label,
            "risk_score": risk,
            "confidence": res.get("confidence", 0.0),
            "analyzed_frames": res.get("analyzed_frames", 0)
        })

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))

    total = len(y_true)
    acc = (tp + tn) / total if total > 0 else 0.0
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0

    print(f"  Results for {name}:")
    print(f"    Total Videos: {total} (TP: {tp}, FP: {fp}, TN: {tn}, FN: {fn})")
    print(f"    Accuracy:  {acc * 100:.2f}%")
    print(f"    Precision: {prec * 100:.2f}%")
    print(f"    Recall:    {rec * 100:.2f}%")
    print(f"    F1 Score:  {f1 * 100:.2f}%")

    metrics = {
        "dataset_name": name,
        "evaluation_level": "video_level",
        "total_test_videos": total,
        "real_videos": len(real_paths),
        "fake_videos": len(fake_paths),
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "accuracy": f"{acc * 100:.2f}%",
        "accuracy_raw": round(acc, 4),
        "precision": f"{prec * 100:.2f}%",
        "precision_raw": round(prec, 4),
        "recall": f"{rec * 100:.2f}%",
        "recall_raw": round(rec, 4),
        "f1": f"{f1 * 100:.2f}%",
        "f1_raw": round(f1, 4),
        "videoModelType": "frame_level_aggregation",
        "tested_samples": video_records
    }
    return metrics, (tp, fp, tn, fn)

# 1. Celeb-DF v2
c16_real = glob.glob(r"C:\Users\paruc\Downloads\archive (16)\Celeb-real\*.mp4") + glob.glob(r"C:\Users\paruc\Downloads\archive (16)\YouTube-real\*.mp4")
c16_fake = glob.glob(r"C:\Users\paruc\Downloads\archive (16)\Celeb-synthesis\*.mp4")
celebdf_metrics, cm_celeb = evaluate_dataset("Celeb-DF v2 (archive (16))", c16_real[:10], c16_fake[:10])

with open(os.path.join(MODELS_VIDEO_DIR, "celebdf_metrics.json"), "w") as f:
    json.dump(celebdf_metrics, f, indent=2)
print(f"  ✓ Saved models/video/celebdf_metrics.json")

# 2. FaceForensics++ C23
c17_real = glob.glob(r"C:\Users\paruc\Downloads\archive (17)\**\original\*.mp4", recursive=True) + glob.glob(r"C:\Users\paruc\Downloads\archive (17)\**\original_sequences\*.mp4", recursive=True)
c17_fake = [f for f in glob.glob(r"C:\Users\paruc\Downloads\archive (17)\**\*.mp4", recursive=True) if "original" not in f]
ffpp_metrics, cm_ffpp = evaluate_dataset("FaceForensics++ C23 (archive (17))", c17_real[:10], c17_fake[:10])

with open(os.path.join(MODELS_VIDEO_DIR, "ffpp_metrics.json"), "w") as f:
    json.dump(ffpp_metrics, f, indent=2)
print(f"  ✓ Saved models/video/ffpp_metrics.json")

# 3. Plot Confusion Matrices
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for ax, (tp, fp, tn, fn), title in zip(axes, [cm_celeb, cm_ffpp], ["Celeb-DF v2 (Video-Level)", "FaceForensics++ C23 (Video-Level)"]):
    cm = np.array([[tn, fp], [fn, tp]])
    im = ax.imshow(cm, cmap="Blues", interpolation="nearest")
    ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Pred Authentic", "Pred Manipulated"], fontsize=10)
    ax.set_yticklabels(["True Authentic", "True Manipulated"], fontsize=10)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center", color="white" if cm[i, j] > cm.max()/2 else "black", fontsize=14, fontweight="bold")
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

plt.tight_layout()
cm_path = os.path.join(MODELS_VIDEO_DIR, "confusion_matrix.png")
plt.savefig(cm_path, dpi=200)
plt.close()
print(f"  ✓ Saved models/video/confusion_matrix.png")

# Also copy to reports/confusion_matrices/
rep_cm_dir = os.path.join(PROJECT_ROOT, "reports", "confusion_matrices")
os.makedirs(rep_cm_dir, exist_ok=True)
import shutil
shutil.copy(cm_path, os.path.join(rep_cm_dir, "video_confusion_matrix.png"))

# 4. Save metadata.json
video_meta = {
    "model_name": "DeepfakeCNN (Frame-Level Aggregation)",
    "videoModelType": "frame_level_aggregation",
    "evaluation_standard": "Video-Level Held-Out Testing",
    "base_image_model": "models/image/best_model.pt",
    "temporal_sampling": "16 evenly spaced deterministic keyframes",
    "datasets": {
        "celeb_df_v2": {
            "source": "archive (16)",
            "accuracy": celebdf_metrics["accuracy"],
            "f1": celebdf_metrics["f1"],
            "precision": celebdf_metrics["precision"],
            "recall": celebdf_metrics["recall"]
        },
        "faceforensics_pp": {
            "source": "archive (17)",
            "accuracy": ffpp_metrics["accuracy"],
            "f1": ffpp_metrics["f1"],
            "precision": ffpp_metrics["precision"],
            "recall": ffpp_metrics["recall"]
        }
    }
}

with open(os.path.join(MODELS_VIDEO_DIR, "metadata.json"), "w") as f:
    json.dump(video_meta, f, indent=2)
print(f"  ✓ Saved models/video/metadata.json")
print("\n>>> ALL VIDEO BENCHMARK EVALUATION ARTIFACTS GENERATED SUCCESSFULLY! ✓")
