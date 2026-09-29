import json
import csv
from pathlib import Path

inventory = [
    {
        "id": "DS-01",
        "dataset_name": "SMS Spam Collection Dataset",
        "source_folder": r"C:\Users\paruc\Downloads\archive (4)",
        "files": ["spam_sms.csv"],
        "modality": "text / SMS",
        "file_formats": [".csv"],
        "file_count": 1,
        "folder_count": 0,
        "total_size_mb": 0.46,
        "total_samples": 5572,
        "label_type": "Binary string ('ham', 'spam')",
        "classes": {
            "ham (authentic)": 4825,
            "spam (unsolicited / scam)": 747
        },
        "train_val_test_split": "No predefined split (requires stratified 80/10/10 split)",
        "usable_for_supervised_learning": True,
        "duplicate_status": "Unique",
        "target_module": "5. SMS Scam Detection (and Text & Scam Detection)",
        "action_recommendation": "SUITABLE FOR TRAINING — train real SMS text classification model (TF-IDF + PyTorch Classifier or Logistic Regression)",
        "legal_technical_status": "Legally & technically suitable (Standard open benchmark dataset)",
        "notes": "Real SMS messages with clean labels. 86.6% ham, 13.4% spam."
    },
    {
        "id": "DS-02",
        "dataset_name": "Fake Job Postings Dataset",
        "source_folder": r"C:\Users\paruc\Downloads\archive (5)",
        "files": ["Fake Postings.csv"],
        "modality": "text / Job Postings",
        "file_formats": [".csv"],
        "file_count": 1,
        "folder_count": 0,
        "total_size_mb": 2.87,
        "total_samples": 10000,
        "label_type": "Single-class positive ('fraudulent'=1)",
        "classes": {
            "fraudulent=1": 10000,
            "fraudulent=0": 0
        },
        "train_val_test_split": "No split",
        "usable_for_supervised_learning": False,
        "duplicate_status": "Unique folder, duplicated in archive (8).zip",
        "target_module": "7. Job / Internship Scam Detection",
        "action_recommendation": "METADATA & FORENSIC RULES ONLY — Not directly trainable as a binary classifier alone because class distribution is 100% positive (10,000 fake jobs, 0 legitimate). Can be used to extract high-risk corporate email domains, compensation anomalies, and scam text patterns for the rule/entity engine.",
        "legal_technical_status": "Legally suitable, but mathematically degenerate for supervised binary learning without legitimate job contrast",
        "notes": "Every row has fraudulent=1. Contains valuable signals: title, description, requirements, company_profile, salary_range, email domains."
    },
    {
        "id": "DS-03",
        "dataset_name": "Phishing & Malicious URLs Dataset (Lexical & Host Features)",
        "source_folder": r"C:\Users\paruc\Downloads\archive (6)",
        "files": ["final_dataset.csv", "feature_description.csv", "dataset_info.txt", "README.md"],
        "modality": "URL / Tabular Features",
        "file_formats": [".csv", ".txt", ".md"],
        "file_count": 4,
        "folder_count": 0,
        "total_size_mb": 204.80,
        "total_samples": 579920,
        "label_type": "Binary integer (0: Legitimate, 1: Phishing)",
        "classes": {
            "0 (Legitimate)": 339074,
            "1 (Phishing)": 240846
        },
        "train_val_test_split": "No predefined split (requires stratified train/val/test split)",
        "usable_for_supervised_learning": True,
        "duplicate_status": "Identical duplicate of archive (7); duplicated in archive (11) and archive (12)",
        "target_module": "4. URL / Phishing URL Detection",
        "action_recommendation": "SUITABLE FOR TRAINING — Excellent high-volume dataset with 74 lexical, host, and domain features plus raw URLs. Can train high-accuracy PyTorch tabular neural network / classifier.",
        "legal_technical_status": "Legally & technically suitable for production training",
        "notes": "58.47% legitimate, 41.53% phishing. 74 rich features including Shannon entropy, brand presence, IP hostnames, TLD length."
    },
    {
        "id": "DS-04",
        "dataset_name": "Phishing & Malicious URLs Dataset (Duplicate Copy 1)",
        "source_folder": r"C:\Users\paruc\Downloads\archive (7)",
        "files": ["final_dataset.csv", "feature_description.csv", "dataset_info.txt", "README.md"],
        "modality": "URL / Tabular Features",
        "file_formats": [".csv", ".txt", ".md"],
        "file_count": 4,
        "folder_count": 0,
        "total_size_mb": 204.80,
        "total_samples": 579920,
        "label_type": "Binary integer (0: Legitimate, 1: Phishing)",
        "classes": {
            "0 (Legitimate)": 339074,
            "1 (Phishing)": 240846
        },
        "train_val_test_split": "No predefined split",
        "usable_for_supervised_learning": True,
        "duplicate_status": "DUPLICATE of archive (6)",
        "target_module": "4. URL / Phishing URL Detection",
        "action_recommendation": "NOT USED — REASON: Exact bit-for-bit duplicate of archive (6). archive (6) will be used as the primary source.",
        "legal_technical_status": "Redundant copy",
        "notes": "Identical hash, row count, and schema as archive (6)."
    },
    {
        "id": "DS-05",
        "dataset_name": "Phishing Email Benchmark Collection (7 Corpus Ensemble)",
        "source_folder": r"C:\Users\paruc\Downloads\archive (9)",
        "files": ["phishing_email.csv", "CEAS_08.csv", "Enron.csv", "SpamAssasin.csv", "Ling.csv", "Nigerian_Fraud.csv", "Nazario.csv"],
        "modality": "text / Email",
        "file_formats": [".csv"],
        "file_count": 7,
        "folder_count": 0,
        "total_size_mb": 249.19,
        "total_samples": 165004,
        "label_type": "Binary integer (0: Legitimate/Ham, 1: Phishing/Spam)",
        "classes": {
            "phishing_email.csv (Primary)": {"0 (Legitimate)": 39595, "1 (Phishing)": 42891, "total": 82486},
            "CEAS_08.csv": {"0": 17312, "1": 21842, "total": 39154},
            "Enron.csv": {"0": 15791, "1": 13976, "total": 29767},
            "SpamAssasin.csv": {"0": 4091, "1": 1718, "total": 5809},
            "Ling.csv": {"0": 2401, "1": 458, "total": 2859},
            "Nigerian_Fraud.csv": {"1": 3332, "total": 3332},
            "Nazario.csv": {"1": 1565, "total": 1565}
        },
        "train_val_test_split": "No predefined split across individual CSVs (requires stratified train/val/test split)",
        "usable_for_supervised_learning": True,
        "duplicate_status": "Unique folder, duplicated in archive (10) and archive (13)",
        "target_module": "6. Phishing Email Detection (and Text & Scam Detection)",
        "action_recommendation": "SUITABLE FOR TRAINING — Comprehensive email phishing dataset. 'phishing_email.csv' provides 82,486 balanced samples with 'text_combined' and 'label'. Ideal for training a dedicated PyTorch Email Phishing Classifier.",
        "legal_technical_status": "Legally & technically suitable for academic and production detection models",
        "notes": "Excellent multi-source collection covering corporate, Nigerian 419 scams, Spear phishing, and CEAS benchmarks."
    },
    {
        "id": "DS-06",
        "dataset_name": "archive (10) — Zip container of Email Dataset",
        "source_folder": r"C:\Users\paruc\Downloads\archive (10)",
        "files": ["archive (9).zip"],
        "modality": "metadata / zip archive",
        "file_formats": [".zip"],
        "file_count": 1,
        "folder_count": 0,
        "total_size_mb": 77.12,
        "total_samples": 0,
        "label_type": "N/A (archive file)",
        "classes": {},
        "train_val_test_split": "N/A",
        "usable_for_supervised_learning": False,
        "duplicate_status": "DUPLICATE of archive (9)",
        "target_module": "6. Phishing Email Detection",
        "action_recommendation": "NOT USED — REASON: Unextracted zip duplicate of archive (9). archive (9) already contains the extracted CSVs.",
        "legal_technical_status": "Redundant container",
        "notes": "Contains archive (9).zip."
    },
    {
        "id": "DS-07",
        "dataset_name": "archive (11) — Zip container of URL Dataset",
        "source_folder": r"C:\Users\paruc\Downloads\archive (11)",
        "files": ["archive (7).zip"],
        "modality": "metadata / zip archive",
        "file_formats": [".zip"],
        "file_count": 1,
        "folder_count": 0,
        "total_size_mb": 36.86,
        "total_samples": 0,
        "label_type": "N/A (archive file)",
        "classes": {},
        "train_val_test_split": "N/A",
        "usable_for_supervised_learning": False,
        "duplicate_status": "DUPLICATE of archive (6) and archive (7)",
        "target_module": "4. URL / Phishing URL Detection",
        "action_recommendation": "NOT USED — REASON: Unextracted zip duplicate of archive (6)/(7).",
        "legal_technical_status": "Redundant container",
        "notes": "Contains archive (7).zip."
    },
    {
        "id": "DS-08",
        "dataset_name": "archive (12) — Zip container of URL Dataset",
        "source_folder": r"C:\Users\paruc\Downloads\archive (12)",
        "files": ["archive (6).zip"],
        "modality": "metadata / zip archive",
        "file_formats": [".zip"],
        "file_count": 1,
        "folder_count": 0,
        "total_size_mb": 36.86,
        "total_samples": 0,
        "label_type": "N/A (archive file)",
        "classes": {},
        "train_val_test_split": "N/A",
        "usable_for_supervised_learning": False,
        "duplicate_status": "DUPLICATE of archive (6) and archive (7)",
        "target_module": "4. URL / Phishing URL Detection",
        "action_recommendation": "NOT USED — REASON: Unextracted zip duplicate of archive (6)/(7).",
        "legal_technical_status": "Redundant container",
        "notes": "Contains archive (6).zip."
    },
    {
        "id": "DS-09",
        "dataset_name": "archive (13) — Zip container of Email Dataset",
        "source_folder": r"C:\Users\paruc\Downloads\archive (13)",
        "files": ["archive (9).zip"],
        "modality": "metadata / zip archive",
        "file_formats": [".zip"],
        "file_count": 1,
        "folder_count": 0,
        "total_size_mb": 77.12,
        "total_samples": 0,
        "label_type": "N/A (archive file)",
        "classes": {},
        "train_val_test_split": "N/A",
        "usable_for_supervised_learning": False,
        "duplicate_status": "DUPLICATE of archive (9)",
        "target_module": "6. Phishing Email Detection",
        "action_recommendation": "NOT USED — REASON: Second unextracted zip duplicate of archive (9).",
        "legal_technical_status": "Redundant container",
        "notes": "Contains archive (9).zip."
    },
    {
        "id": "DS-10",
        "dataset_name": "Celeb-DF v2 Metadata",
        "source_folder": r"C:\Users\paruc\Downloads\celeb-df-v2-metadata",
        "files": ["celeb-df-v2-metadata.json"],
        "modality": "metadata only (JSON Schema / Croissant format)",
        "file_formats": [".json"],
        "file_count": 1,
        "folder_count": 0,
        "total_size_mb": 0.003,
        "total_samples": 0,
        "label_type": "N/A (Schema metadata)",
        "classes": {},
        "train_val_test_split": "N/A",
        "usable_for_supervised_learning": False,
        "duplicate_status": "Unique metadata descriptor",
        "target_module": "2. Video Deepfake Detection",
        "action_recommendation": "NOT USED FOR DIRECT MODEL TRAINING — REASON: Contains ZERO video files (.mp4) and zero frame images. It is a 3.4 KB Kaggle Croissant metadata descriptor indicating the full dataset is 9.285 GB hosted externally on Kaggle.",
        "legal_technical_status": "Informational metadata reference only. Cannot train video models from schema JSON.",
        "notes": "Confirmed: No videos, no bounding boxes, no raw data. References external Kaggle URL: https://www.kaggle.com/datasets/reubensuju/celeb-df-v2/versions/1"
    },
    {
        "id": "DS-11",
        "dataset_name": "ASVspoof 2019 Logical Access (LA) — Speech Anti-Spoofing",
        "source_folder": r"C:\Users\paruc\Downloads\archive (1)\LA\LA",
        "files": ["ASVspoof2019_LA_dev/*.flac", "ASVspoof2019_LA_eval/*.flac", "ASVspoof2019_LA_cm_protocols/*.txt"],
        "modality": "audio / FLAC",
        "file_formats": [".flac", ".txt"],
        "file_count": 60150,
        "folder_count": 7,
        "total_size_mb": 3590.00,
        "total_samples": 60132,
        "label_type": "Protocol file text mapping (bonafide vs spoof)",
        "classes": {
            "bonafide (authentic human speech)": 2548,
            "spoof (AI synthesized / voice converted)": 22296
        },
        "train_val_test_split": "Official challenge splits: dev (24,844 files) and eval (71,237 protocol entries)",
        "usable_for_supervised_learning": True,
        "duplicate_status": "Unique original dataset",
        "target_module": "3. Audio / Voice Deepfake Detection",
        "action_recommendation": "ALREADY TRAINED & INTEGRATED — Real trained model exists at models/audio/best_model.pt (AudioCNN, 100% test accuracy).",
        "legal_technical_status": "Official ASVspoof 2019 challenge dataset",
        "notes": "Fully verified. Existing AudioCNN model checkpoint is valid and loaded on startup."
    },
    {
        "id": "DS-12",
        "dataset_name": "1000 Videos Deepfake Video Frames",
        "source_folder": r"C:\Users\paruc\Downloads\archive\1000_videos",
        "files": ["train/real/*.png", "train/fake/*.png", "validation/real/*.png", "validation/fake/*.png", "test/real/*.png", "test/fake/*.png"],
        "modality": "image / face frames",
        "file_formats": [".png"],
        "file_count": 16433,
        "folder_count": 9,
        "total_size_mb": 402.96,
        "total_samples": 16433,
        "label_type": "Folder-based binary labels ('real', 'fake')",
        "classes": {
            "real": 7253,
            "fake": 9180
        },
        "train_val_test_split": "Predefined official directory splits (train: 11,500, val: 2,464, test: 2,469)",
        "usable_for_supervised_learning": True,
        "duplicate_status": "Unique original dataset",
        "target_module": "1. Image Deepfake Detection & 2. Video Deepfake Temporal Analysis",
        "action_recommendation": "ALREADY TRAINED & INTEGRATED — Real trained model exists at models/image/best_model.pt (DeepfakeCNN, 88.12% accuracy, 87.38% F1). Also powers video detection via OpenCV temporal frame sampling.",
        "legal_technical_status": "Academic research benchmark",
        "notes": "Fully verified. Existing DeepfakeCNN model checkpoint is valid and loaded on startup."
    }
]

# Write JSON
out_json = Path(r"C:\Users\paruc\OneDrive\Desktop\Reshma\data\dataset_inventory.json")
out_json.parent.mkdir(parents=True, exist_ok=True)
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(inventory, f, indent=2)
print("Saved:", out_json)

# Write CSV
out_csv = Path(r"C:\Users\paruc\OneDrive\Desktop\Reshma\data\dataset_inventory.csv")
with open(out_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Dataset ID", "Dataset Name", "Source Folder", "Modality",
        "File Formats", "File Count", "Total Size (MB)", "Total Samples",
        "Classes", "Supervised Learning Usable?", "Duplicate Status",
        "Target TrustGuard Module", "Recommendation"
    ])
    for item in inventory:
        classes_str = "; ".join([f"{k}: {v}" for k, v in item["classes"].items()]) if isinstance(item["classes"], dict) else str(item["classes"])
        writer.writerow([
            item["id"],
            item["dataset_name"],
            item["source_folder"],
            item["modality"],
            " ".join(item["file_formats"]),
            item["file_count"],
            item["total_size_mb"],
            item["total_samples"],
            classes_str,
            "YES" if item["usable_for_supervised_learning"] else "NO",
            item["duplicate_status"],
            item["target_module"],
            item["action_recommendation"]
        ])
print("Saved:", out_csv)
