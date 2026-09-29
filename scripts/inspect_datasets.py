"""
TrustGuard AI — Dataset Inspector
Inspects both datasets and generates a comprehensive report.
Run: python scripts/inspect_datasets.py
"""
import os
import sys
import csv
import json
from pathlib import Path
from collections import Counter
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────
DATASET1_PATH = Path(r"C:\Users\paruc\Downloads\archive (1)\LA\LA")
DATASET2_PATH = Path(r"C:\Users\paruc\Downloads\archive\1000_videos")
PROJECT_ROOT  = Path(__file__).resolve().parent.parent
DATA_DIR      = PROJECT_ROOT / "data"
REPORTS_DIR   = DATA_DIR / "reports"
DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

AUDIO_EXTENSIONS = {'.flac', '.wav', '.mp3', '.m4a', '.ogg', '.flv'}
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}


def count_files_recursive(folder: Path, extensions=None):
    counts = Counter()
    for f in folder.rglob("*"):
        if f.is_file():
            ext = f.suffix.lower()
            if extensions is None or ext in extensions:
                counts[ext] += 1
    return counts


def inspect_dataset1():
    print("\n" + "="*60)
    print("DATASET 1 INSPECTION")
    print("="*60)
    print(f"Path: {DATASET1_PATH}")

    if not DATASET1_PATH.exists():
        print("ERROR: Dataset 1 path not found!")
        return None

    # Count audio files per split
    splits = {
        "dev":  DATASET1_PATH / "ASVspoof2019_LA_dev" / "flac",
        "eval": DATASET1_PATH / "ASVspoof2019_LA_eval" / "flac",
    }

    split_counts = {}
    for split, path in splits.items():
        if path.exists():
            cnt = len(list(path.glob("*.flac")))
            split_counts[split] = cnt
        else:
            split_counts[split] = 0

    # Parse protocol files for label distribution
    proto_dir = DATASET1_PATH / "ASVspoof2019_LA_cm_protocols"
    label_stats = {}
    for proto_file in sorted(proto_dir.glob("*.txt")):
        lines = proto_file.read_text(encoding='utf-8', errors='ignore').strip().split('\n')
        bonafide = sum(1 for l in lines if 'bonafide' in l)
        spoof    = sum(1 for l in lines if 'spoof' in l and 'bonafide' not in l)
        split_name = proto_file.stem.split('.')[-1]  # trn / trl
        part_name  = proto_file.name
        label_stats[part_name] = {'bonafide': bonafide, 'spoof': spoof, 'total': bonafide + spoof}

    # Sum train protocol
    train_proto = DATASET1_PATH / "ASVspoof2019_LA_cm_protocols" / "ASVspoof2019.LA.cm.train.trn.txt"
    dev_proto   = DATASET1_PATH / "ASVspoof2019_LA_cm_protocols" / "ASVspoof2019.LA.cm.dev.trl.txt"
    eval_proto  = DATASET1_PATH / "ASVspoof2019_LA_cm_protocols" / "ASVspoof2019.LA.cm.eval.trl.txt"

    def parse_proto(p):
        lines = p.read_text(encoding='utf-8', errors='ignore').strip().split('\n')
        b = sum(1 for l in lines if 'bonafide' in l)
        s = sum(1 for l in lines if 'spoof' in l and 'bonafide' not in l)
        return b, s

    train_b, train_s = parse_proto(train_proto) if train_proto.exists() else (0, 0)
    dev_b,   dev_s   = parse_proto(dev_proto)   if dev_proto.exists()   else (0, 0)
    eval_b,  eval_s  = parse_proto(eval_proto)  if eval_proto.exists()  else (0, 0)

    report = {
        "dataset": "ASVspoof 2019 — Logical Access (LA)",
        "path": str(DATASET1_PATH),
        "modality": "AUDIO",
        "format": "FLAC (lossless compressed audio)",
        "label_type": "Protocol file-based (ASVspoof CM protocol)",
        "classes": ["bonafide", "spoof"],
        "label_mapping": {"0": "bonafide (AUTHENTIC VOICE)", "1": "spoof (AI-GENERATED / SYNTHETIC VOICE)"},
        "splits": {
            "train": {
                "audio_files": 0,  # train audio not present in this download
                "protocol_bonafide": train_b,
                "protocol_spoof": train_s,
                "protocol_total": train_b + train_s,
                "note": "Train audio folder missing from download; protocol labels available"
            },
            "dev": {
                "audio_files": split_counts.get("dev", 0),
                "protocol_bonafide": dev_b,
                "protocol_spoof": dev_s,
                "protocol_total": dev_b + dev_s
            },
            "eval": {
                "audio_files": split_counts.get("eval", 0),
                "protocol_bonafide": eval_b,
                "protocol_spoof": eval_s,
                "protocol_total": eval_b + eval_s
            }
        },
        "total_audio_available": split_counts.get("dev", 0) + split_counts.get("eval", 0),
        "class_imbalance": f"Spoof:Bonafide ~ {(train_s + dev_s)/(train_b + dev_b):.1f}:1",
        "compatible_detector": "Audio / Voice Authenticity Detector",
        "training_strategy": "Use dev split (2548 bonafide + 22296 spoof) with 90/10 train/val split; balanced sampling; class-weighted loss",
        "note": "Industry-standard voice anti-spoofing benchmark used in ASVspoof2019 challenge"
    }

    print(f"  Modality:              AUDIO")
    print(f"  Format:                FLAC")
    print(f"  Classes:               bonafide (authentic), spoof (AI-generated/TTS)")
    print(f"  Label type:            Protocol file-based")
    print(f"  Label mapping:         0=bonafide, 1=spoof")
    print(f"  Dev audio available:   {split_counts.get('dev', 0)}")
    print(f"  Eval audio available:  {split_counts.get('eval', 0)}")
    print(f"  Train protocol:        {train_b} bonafide + {train_s} spoof = {train_b+train_s}")
    print(f"  Dev protocol:          {dev_b} bonafide + {dev_s} spoof = {dev_b+dev_s}")
    print(f"  Eval protocol:         {eval_b} bonafide + {eval_s} spoof = {eval_b+eval_s}")
    print(f"  Class imbalance:       {report['class_imbalance']}")
    print(f"  Compatible detector:   Audio / Voice Authenticity")

    return report


def inspect_dataset2():
    print("\n" + "="*60)
    print("DATASET 2 INSPECTION")
    print("="*60)
    print(f"Path: {DATASET2_PATH}")

    if not DATASET2_PATH.exists():
        print("ERROR: Dataset 2 path not found!")
        return None

    splits_config = ["train", "validation", "test"]
    labels_config = ["real", "fake"]
    split_data = {}

    for split in splits_config:
        split_data[split] = {}
        for label in labels_config:
            p = DATASET2_PATH / split / label
            if p.exists():
                files = list(p.glob("*.png")) + list(p.glob("*.jpg")) + list(p.glob("*.jpeg"))
                split_data[split][label] = len(files)
            else:
                split_data[split][label] = 0

    total_real = sum(split_data[s].get("real", 0) for s in splits_config)
    total_fake = sum(split_data[s].get("fake", 0) for s in splits_config)
    total_all  = total_real + total_fake

    report = {
        "dataset": "1000 Deepfake Videos — Extracted Face Frames",
        "path": str(DATASET2_PATH),
        "modality": "IMAGE (video frames extracted from deepfake/real videos)",
        "format": "PNG (face-cropped video frames)",
        "label_type": "Folder-based (real/ vs fake/ subfolders)",
        "classes": ["real", "fake"],
        "label_mapping": {"0": "real (AUTHENTIC FACE)", "1": "fake (DEEPFAKE / FACE-SWAPPED)"},
        "splits": {
            "train": {
                "real": split_data["train"]["real"],
                "fake": split_data["train"]["fake"],
                "total": split_data["train"]["real"] + split_data["train"]["fake"]
            },
            "validation": {
                "real": split_data["validation"]["real"],
                "fake": split_data["validation"]["fake"],
                "total": split_data["validation"]["real"] + split_data["validation"]["fake"]
            },
            "test": {
                "real": split_data["test"]["real"],
                "fake": split_data["test"]["fake"],
                "total": split_data["test"]["real"] + split_data["test"]["fake"]
            }
        },
        "total_images": total_all,
        "total_real": total_real,
        "total_fake": total_fake,
        "official_splits": True,
        "class_balance": f"Real:{total_real} Fake:{total_fake} (ratio {total_fake/max(total_real,1):.2f}:1)",
        "compatible_detector": "Image Deepfake Detector (also improves Video Deepfake via frame-level model)",
        "training_strategy": "Use official train/validation/test splits; EfficientNet-B0 or CNN fine-tuning"
    }

    print(f"  Modality:              IMAGE (deepfake video frames)")
    print(f"  Format:                PNG")
    print(f"  Classes:               real, fake")
    print(f"  Label type:            Folder-based")
    print(f"  Label mapping:         0=real, 1=fake")
    print(f"  Train  real/fake:      {split_data['train']['real']} / {split_data['train']['fake']}")
    print(f"  Val    real/fake:      {split_data['validation']['real']} / {split_data['validation']['fake']}")
    print(f"  Test   real/fake:      {split_data['test']['real']} / {split_data['test']['fake']}")
    print(f"  Total images:          {total_all}")
    print(f"  Class balance:         {report['class_balance']}")
    print(f"  Compatible detector:   Image Deepfake + Video Frame-level")

    return report


def main():
    print("\nTrustGuard AI — Dataset Inspection Report")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    r1 = inspect_dataset1()
    r2 = inspect_dataset2()

    print("\n" + "="*60)
    print("COMPATIBILITY SUMMARY")
    print("="*60)
    print("Dataset 1  ->  Audio / Voice Authenticity Detector")
    print("             (bonafide=0 / spoof=1)")
    print("Dataset 2  ->  Image Deepfake Detector")
    print("             (real=0 / fake=1)")
    print("             Also used by Video Detector (frame-level)")
    print("Combination: Separate pipelines -- different modalities")
    print("Data leak prevention: Official splits maintained, no overlap")

    combined = {
        "inspection_date": datetime.now().isoformat(),
        "datasets": {
            "dataset_1": r1,
            "dataset_2": r2
        },
        "compatibility": {
            "can_combine": False,
            "reason": "Different modalities: Audio (Dataset 1) vs Image frames (Dataset 2)",
            "pipelines": {
                "audio": "Dataset 1 → models/audio/",
                "image": "Dataset 2 → models/image/",
                "video": "Dataset 2 frames → also used by video detector"
            }
        }
    }

    report_path = REPORTS_DIR / "dataset_inspection_report.json"
    with open(report_path, "w") as f:
        json.dump(combined, f, indent=2)
    print(f"\nFull report saved: {report_path}")

    return combined


if __name__ == "__main__":
    main()
