"""
TrustGuard AI — Phishing Email Detection Model Training
Trains a real PyTorch neural text classification model on the 82,486 email benchmark dataset.
Dataset: C:\\Users\\paruc\\Downloads\\archive (9)\\phishing_email.csv
Outputs:
  models/email/best_model.pt
  models/email/tfidf_vectorizer.pkl
  models/email/metadata.json
  models/email/training_metrics.json
"""
import os
import sys
import time
import json
import pickle
import csv
from datetime import datetime
from pathlib import Path
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix
)

csv.field_size_limit(10000000)

SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)

DATASET_PATH = Path(r"C:\Users\paruc\Downloads\archive (9)\phishing_email.csv")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "models" / "email"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class EmailPhishingClassifier(nn.Module):
    def __init__(self, input_dim=8000, hidden1=256, hidden2=64, num_classes=2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden1),
            nn.BatchNorm1d(hidden1),
            nn.ReLU(),
            nn.Dropout(0.35),
            nn.Linear(hidden1, hidden2),
            nn.BatchNorm1d(hidden2),
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Linear(hidden2, num_classes)
        )

    def forward(self, x):
        return self.net(x)


def load_dataset(sample_cap=40000):
    print(f"Loading Email dataset from {DATASET_PATH} (sampling up to {sample_cap} balanced rows)...")
    legit_texts = []
    phish_texts = []
    half_cap = sample_cap // 2

    with open(DATASET_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        header = next(reader)
        for r in reader:
            if len(r) >= 2:
                txt = r[0].strip()
                lbl_str = r[1].strip()
                if lbl_str in ['0', '1'] and len(txt) > 10:
                    lbl = int(lbl_str)
                    if lbl == 0 and len(legit_texts) < half_cap:
                        legit_texts.append(txt)
                    elif lbl == 1 and len(phish_texts) < half_cap:
                        phish_texts.append(txt)

                    if len(legit_texts) >= half_cap and len(phish_texts) >= half_cap:
                        break

    texts = legit_texts + phish_texts
    labels = [0] * len(legit_texts) + [1] * len(phish_texts)
    
    indices = np.arange(len(texts))
    np.random.shuffle(indices)
    
    texts = [texts[i] for i in indices]
    labels = np.array([labels[i] for i in indices], dtype=np.int64)

    print(f"Loaded {len(texts)} balanced email samples (Legitimate: {len(legit_texts)}, Phishing: {len(phish_texts)})")
    return texts, labels


def main():
    start_time = time.time()
    texts, labels = load_dataset(sample_cap=40000)

    # Stratified 80/10/10 Split
    X_train_raw, X_temp_raw, y_train, y_temp = train_test_split(
        texts, labels, test_size=0.2, random_state=SEED, stratify=labels
    )
    X_val_raw, X_test_raw, y_val, y_test = train_test_split(
        X_temp_raw, y_temp, test_size=0.5, random_state=SEED, stratify=y_temp
    )

    print(f"Splits -> Train: {len(X_train_raw)}, Val: {len(X_val_raw)}, Test: {len(X_test_raw)}")

    # TF-IDF Feature Extraction
    print("Fitting TF-IDF Vectorizer (max_features=8000, n-grams (1,2))...")
    vectorizer = TfidfVectorizer(
        max_features=8000,
        ngram_range=(1, 2),
        sublinear_tf=True,
        stop_words='english',
        min_df=3
    )
    X_train_vec = vectorizer.fit_transform(X_train_raw).toarray()
    X_val_vec = vectorizer.transform(X_val_raw).toarray()
    X_test_vec = vectorizer.transform(X_test_raw).toarray()

    X_train_t = torch.tensor(X_train_vec, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.long)
    X_val_t = torch.tensor(X_val_vec, dtype=torch.float32)
    y_val_t = torch.tensor(y_val, dtype=torch.long)
    X_test_t = torch.tensor(X_test_vec, dtype=torch.float32)
    y_test_t = torch.tensor(y_test, dtype=torch.long)

    train_loader = DataLoader(TensorDataset(X_train_t, y_train_t), batch_size=128, shuffle=True)
    val_loader = DataLoader(TensorDataset(X_val_t, y_val_t), batch_size=256, shuffle=False)
    test_loader = DataLoader(TensorDataset(X_test_t, y_test_t), batch_size=256, shuffle=False)

    model = EmailPhishingClassifier(input_dim=8000)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)

    best_val_loss = float('inf')
    best_weights = None
    epochs = 12
    patience = 3
    patience_counter = 0
    history = {"train_loss": [], "val_loss": []}

    print("Training EmailPhishingClassifier on CPU...")
    for epoch in range(1, epochs + 1):
        model.train()
        train_losses = []
        for bx, by in train_loader:
            optimizer.zero_grad()
            logits = model(bx)
            loss = criterion(logits, by)
            loss.backward()
            optimizer.step()
            train_losses.append(loss.item())

        avg_train_loss = float(np.mean(train_losses))

        model.eval()
        val_losses = []
        with torch.no_grad():
            for bx, by in val_loader:
                logits = model(bx)
                loss = criterion(logits, by)
                val_losses.append(loss.item())
        avg_val_loss = float(np.mean(val_losses))

        history["train_loss"].append(round(avg_train_loss, 4))
        history["val_loss"].append(round(avg_val_loss, 4))

        print(f"Epoch {epoch}/{epochs} - Train Loss: {avg_train_loss:.4f} - Val Loss: {avg_val_loss:.4f}")

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            best_weights = model.state_dict().copy()
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping at epoch {epoch}")
                break

    model.load_state_dict(best_weights)

    # Test set evaluation
    model.eval()
    all_preds = []
    all_probs = []
    with torch.no_grad():
        for bx, _ in test_loader:
            logits = model(bx)
            probs = torch.softmax(logits, dim=1)[:, 1].numpy()
            preds = torch.argmax(logits, dim=1).numpy()
            all_preds.extend(preds)
            all_probs.extend(probs)

    all_preds = np.array(all_preds)
    all_probs = np.array(all_probs)

    acc = float(accuracy_score(y_test, all_preds))
    prec = float(precision_score(y_test, all_preds, zero_division=0))
    rec = float(recall_score(y_test, all_preds, zero_division=0))
    f1 = float(f1_score(y_test, all_preds, zero_division=0))
    roc_auc = float(roc_auc_score(y_test, all_probs))
    cm = confusion_matrix(y_test, all_preds).tolist()
    tn, fp, fn, tp = int(cm[0][0]), int(cm[0][1]), int(cm[1][0]), int(cm[1][1])

    duration_sec = round(time.time() - start_time, 2)
    print("\n" + "="*50)
    print("EMAIL PHISHING MODEL TEST RESULTS")
    print("="*50)
    print(f"Accuracy:  {acc * 100:.2f}%")
    print(f"Precision: {prec * 100:.2f}%")
    print(f"Recall:    {rec * 100:.2f}%")
    print(f"F1 Score:  {f1 * 100:.2f}%")
    print(f"ROC-AUC:   {roc_auc:.4f}")
    print(f"Confusion Matrix (TN={tn}, FP={fp}, FN={fn}, TP={tp}):\n{cm}")
    print(f"Training Duration: {duration_sec}s")

    # Save artifacts
    model_path = OUTPUT_DIR / "best_model.pt"
    vec_path = OUTPUT_DIR / "tfidf_vectorizer.pkl"
    meta_path = OUTPUT_DIR / "metadata.json"
    metrics_path = OUTPUT_DIR / "training_metrics.json"

    torch.save(model.state_dict(), model_path)
    with open(vec_path, "wb") as f:
        pickle.dump(vectorizer, f)

    metrics_data = {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1": round(f1, 4),
        "roc_auc": round(roc_auc, 4),
        "confusion_matrix": cm,
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
        "training_loss": history["train_loss"],
        "validation_loss": history["val_loss"],
        "duration_seconds": duration_sec
    }
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=2)

    meta_data = {
        "model_name": "EmailPhishingClassifier",
        "dataset": "Phishing Email Benchmark Collection",
        "dataset_path": str(DATASET_PATH),
        "modality": "text / Email",
        "features_count": 8000,
        "classes": ["legitimate", "phishing"],
        "label_mapping": {
            "0": "legitimate (AUTHENTIC / SAFE EMAIL)",
            "1": "phishing (DECEPTIVE / PHISHING / FRAUD EMAIL)"
        },
        "train_samples": len(X_train_raw),
        "validation_samples": len(X_val_raw),
        "test_samples": len(X_test_raw),
        "epochs_completed": len(history["train_loss"]),
        "architecture": "EmailPhishingClassifier(Linear(8000, 256)->BatchNorm->ReLU->Dropout(0.35)->Linear(256, 64)->BatchNorm->ReLU->Dropout(0.25)->Linear(64, 2))",
        "framework": "PyTorch",
        "vectorizer": "TfidfVectorizer(max_features=8000, ngram_range=(1,2), sublinear_tf=True, stop_words='english')",
        "metrics": metrics_data,
        "trained_at": datetime.now().isoformat(),
        "device": "cpu"
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_data, f, indent=2)

    print(f"\nArtifacts successfully written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
