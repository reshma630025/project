"""
TrustGuard AI — Unified Dataset Manifest Generator
Indexes both real datasets on disk without modifying anything:
1. Dataset 1 (Audio): C:\\Users\\paruc\\Downloads\\archive (1)\\LA\\LA
2. Dataset 2 (Image): C:\\Users\\paruc\\Downloads\\archive\\1000_videos

Generates:
- data/dataset_manifest.csv
- data/reports/dataset_manifest_summary.json
"""

import os
import sys
import csv
import json
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

AUDIO_ROOT = Path(r"C:\Users\paruc\Downloads\archive (1)\LA\LA")
IMAGE_ROOT = Path(r"C:\Users\paruc\Downloads\archive\1000_videos")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = DATA_DIR / "reports"
DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def generate_manifest():
    print("=" * 65)
    print("TrustGuard AI — Generating Unified Dataset Manifest")
    print("=" * 65)

    manifest_rows = []
    summary = {
        "generated_at": datetime.now().isoformat(),
        "datasets": {}
    }

    # 1. Dataset 2: Images (1000_videos deepfake face frames)
    print("\n→ Indexing Dataset 2 (Images)...")
    img_counts = {"train": {"real": 0, "fake": 0}, "validation": {"real": 0, "fake": 0}, "test": {"real": 0, "fake": 0}}
    total_images = 0

    if IMAGE_ROOT.exists():
        for split in ["train", "validation", "test"]:
            for label_str, label_int in [("real", 0), ("fake", 1)]:
                folder = IMAGE_ROOT / split / label_str
                if folder.exists():
                    for f in folder.glob("*.png"):
                        sz = f.stat().st_size
                        manifest_rows.append({
                            "file_path": str(f),
                            "filename": f.name,
                            "dataset_source": "archive_1000_videos",
                            "modality": "image",
                            "split": split,
                            "label": label_str,
                            "label_int": label_int,
                            "format": ".png",
                            "specs": "128x128_rgb",
                            "size_bytes": sz
                        })
                        img_counts[split][label_str] += 1
                        total_images += 1
        print(f"  Indexed {total_images:,} image files.")
        summary["datasets"]["image_deepfake"] = {
            "root": str(IMAGE_ROOT),
            "modality": "image",
            "total_samples": total_images,
            "splits": img_counts
        }
    else:
        print(f"  WARNING: Image dataset not found at {IMAGE_ROOT}")

    # 2. Dataset 1: Audio (ASVspoof 2019 LA)
    print("\n→ Indexing Dataset 1 (Audio)...")
    audio_counts = {"dev": {"bonafide": 0, "spoof": 0}, "eval": {"bonafide": 0, "spoof": 0}}
    total_audio = 0

    dev_audio_dir = AUDIO_ROOT / "ASVspoof2019_LA_dev" / "flac"
    dev_proto = AUDIO_ROOT / "ASVspoof2019_LA_cm_protocols" / "ASVspoof2019.LA.cm.dev.trl.txt"

    eval_audio_dir = AUDIO_ROOT / "ASVspoof2019_LA_eval" / "flac"
    eval_proto = AUDIO_ROOT / "ASVspoof2019_LA_cm_protocols" / "ASVspoof2019.LA.cm.eval.trl.txt"

    # Index Dev
    if dev_proto.exists() and dev_audio_dir.exists():
        with open(dev_proto, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 5:
                    fname = parts[1]
                    lbl = parts[4].lower()
                    fpath = dev_audio_dir / f"{fname}.flac"
                    if fpath.exists():
                        lbl_int = 0 if lbl == "bonafide" else 1
                        sz = fpath.stat().st_size
                        manifest_rows.append({
                            "file_path": str(fpath),
                            "filename": fpath.name,
                            "dataset_source": "archive_(1)_ASVspoof2019_LA",
                            "modality": "audio",
                            "split": "dev",
                            "label": lbl,
                            "label_int": lbl_int,
                            "format": ".flac",
                            "specs": "16kHz_flac",
                            "size_bytes": sz
                        })
                        audio_counts["dev"][lbl] = audio_counts["dev"].get(lbl, 0) + 1
                        total_audio += 1
        print(f"  Indexed Dev audio: {audio_counts['dev']}")

    # Index Eval if exists
    if eval_proto.exists() and eval_audio_dir.exists():
        with open(eval_proto, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 5:
                    fname = parts[1]
                    lbl = parts[4].lower()
                    fpath = eval_audio_dir / f"{fname}.flac"
                    if fpath.exists():
                        lbl_int = 0 if lbl == "bonafide" else 1
                        sz = fpath.stat().st_size
                        manifest_rows.append({
                            "file_path": str(fpath),
                            "filename": fpath.name,
                            "dataset_source": "archive_(1)_ASVspoof2019_LA",
                            "modality": "audio",
                            "split": "eval",
                            "label": lbl,
                            "label_int": lbl_int,
                            "format": ".flac",
                            "specs": "16kHz_flac",
                            "size_bytes": sz
                        })
                        audio_counts["eval"][lbl] = audio_counts["eval"].get(lbl, 0) + 1
                        total_audio += 1
        print(f"  Indexed Eval audio: {audio_counts['eval']}")

    print(f"  Indexed {total_audio:,} audio files.")
    summary["datasets"]["audio_antispoof"] = {
        "root": str(AUDIO_ROOT),
        "modality": "audio",
        "total_samples": total_audio,
        "splits": audio_counts
    }

    summary["total_manifest_records"] = len(manifest_rows)

    manifest_csv = DATA_DIR / "dataset_manifest.csv"
    print(f"\n→ Writing {manifest_csv} ({len(manifest_rows):,} rows)...")
    if manifest_rows:
        with open(manifest_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(manifest_rows[0].keys()))
            writer.writeheader()
            writer.writerows(manifest_rows)
        print(f"✓ Saved manifest CSV: {manifest_csv}")

    summary_json = REPORTS_DIR / "dataset_manifest_summary.json"
    with open(summary_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"✓ Saved manifest summary: {summary_json}")
    print("\nDataset preparation complete!\n")

if __name__ == "__main__":
    generate_manifest()
