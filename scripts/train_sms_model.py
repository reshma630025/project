"""
TrustGuard AI — SMS Scam Detection Model Training
Trains a real PyTorch neural text classification model on the SMS Spam Collection dataset.
Dataset: C:\\Users\\paruc\\Downloads\\archive (4)\\spam_sms.csv
Outputs:
  models/sms/best_model.pt
  models/sms/tfidf_vectorizer.pkl
  models/sms/metadata.json
  models/sms/training_metrics.json
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

# Set deterministic seed
SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)

DATASET_PATH = Path(r"C:\Users\paruc\Downloads\archive (4)\spam_sms.csv")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "models" / "sms"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class SMSScamClassifier(nn.Module):
    def __init__(self, input_dim=5000, hidden1=128, hidden2=32, num_classes=2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden1),
            nn.BatchNorm1d(hidden1),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden1, hidden2),
            nn.BatchNorm1d(hidden2),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden2, num_classes)
        )

    def forward(self, x):
        return self.net(x)


def load_dataset():
    print(f"Loading SMS dataset from {DATASET_PATH}...")
    texts = []
    labels = []
    with open(DATASET_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        header = next(reader)
        for r in reader:
            if len(r) >= 2:
                lbl = r[0].strip().lower()
                txt = r[1].strip()
                if lbl in ['ham', 'spam'] and txt:
                    texts.append(txt)
                    labels.append(1 if lbl == 'spam' else 0)

    print(f"Loaded {len(texts)} samples (Ham: {labels.count(0)}, Spam: {labels.count(1)})")
    return texts, np.array(labels)


def main():
    start_time = time.time()
    texts, labels = load_dataset()

    # Stratified Train (80%), Val (10%), Test (10%)
    X_train_raw, X_temp_raw, y_train, y_temp = train_test_split(
        texts, labels, test_size=0.2, random_state=SEED, stratify=labels
    )
    X_val_raw, X_test_raw, y_val, y_test = train_test_split(
        X_temp_raw, y_temp, test_size=0.5, random_state=SEED, stratify=y_temp
    )

    print(f"Splits -> Train: {len(X_train_raw)}, Val: {len(X_val_raw)}, Test: {len(X_test_raw)}")

    # TF-IDF Feature Extraction
    print("Fitting TF-IDF Vectorizer (max_features=5000, n-grams (1,2))...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        sublinear_tf=True,
        stop_words='english'
    )
    X_train_vec = vectorizer.fit_transform(X_train_raw).toarray()
    X_val_vec = vectorizer.transform(X_val_raw).toarray()
    X_test_vec = vectorizer.transform(X_test_raw).toarray()

    # Convert to PyTorch Tensors
    X_train_t = torch.tensor(X_train_vec, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.long)
    X_val_t = torch.tensor(X_val_vec, dtype=torch.float32)
    y_val_t = torch.tensor(y_val, dtype=torch.long)
    X_test_t = torch.tensor(X_test_vec, dtype=torch.float32)
    y_test_t = torch.tensor(y_test, dtype=torch.long)

    train_loader = DataLoader(TensorDataset(X_train_t, y_train_t), batch_size=64, shuffle=True)
    val_loader = DataLoader(TensorDataset(X_val_t, y_val_t), batch_size=128, shuffle=False)
    test_loader = DataLoader(TensorDataset(X_test_t, y_test_t), batch_size=128, shuffle=False)

    # Calculate class weights to handle ~6.5:1 imbalance
    class_counts = np.bincount(y_train)
    total_samples = len(y_train)
    weights = torch.tensor([total_samples / (2.0 * class_counts[0]), total_samples / (2.0 * class_counts[1])], dtype=torch.float32)
    print(f"Class weights (Ham, Spam): {weights.tolist()}")

    model = SMSScamClassifier(input_dim=5000)
    criterion = nn.CrossEntropyLoss(weight=weights)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)

    best_val_loss = float('inf')
    best_weights = None
    epochs = 15
    patience = 4
    patience_counter = 0
    history = {"train_loss": [], "val_loss": []}

    print("Training SMSScamClassifier on CPU...")
    for epoch in range(1, epochs + 1):
        model.train()
        train_losses = []
        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            logits = model(batch_x)
            loss = criterion(logits, batch_y)
            loss.backward()
            optimizer.step()
            train_losses.append(loss.item())

        avg_train_loss = float(np.mean(train_losses))

        # Validation
        model.eval()
        val_losses = []
        with torch.no_grad():
            for batch_x, batch_y in val_loader:
                logits = model(batch_x)
                loss = criterion(logits, batch_y)
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

    # Load best weights
    model.load_state_dict(best_weights)

    # Test set evaluation
    model.eval()
    all_preds = []
    all_probs = []
    with torch.no_grad():
        for batch_x, _ in test_loader:
            logits = model(batch_x)
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
    print("SMS MODEL TEST RESULTS")
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
        "model_name": "SMSScamClassifier",
        "dataset": "SMS Spam Collection",
        "dataset_path": str(DATASET_PATH),
        "modality": "text / SMS",
        "classes": ["ham", "spam"],
        "label_mapping": {
            "0": "ham (LEGITIMATE SMS)",
            "1": "spam (SCAM / PHISHING / FRAUDULENT SMS)"
        },
        "train_samples": len(X_train_raw),
        "validation_samples": len(X_val_raw),
        "test_samples": len(X_test_raw),
        "epochs_completed": len(history["train_loss"]),
        "architecture": "SMSScamClassifier(Linear(5000, 128)->BatchNorm->ReLU->Dropout(0.3)->Linear(128, 32)->BatchNorm->ReLU->Dropout(0.2)->Linear(32, 2))",
        "framework": "PyTorch",
        "vectorizer": "TfidfVectorizer(max_features=5000, ngram_range=(1,2), sublinear_tf=True)",
        "metrics": metrics_data,
        "trained_at": datetime.now().isoformat(),
        "device": "cpu"
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_data, f, indent=2)

    print(f"\nArtifacts successfully written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
