"""
TrustGuard AI — Social Media Fake Account Detector Training Pipeline (archive (15))
Trains SocialProfileNet on 5,000 user profiles with strict train/val/test isolation,
class imbalance weighting, zero leakage, and held-out test evaluation.
"""
import os
import sys
import json
import time
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, classification_report
)

sys.stdout.reconfigure(encoding='utf-8')

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = Path(r"C:\Users\paruc\Downloads\archive (15)\raw_user_profiles.csv")
ZIP_PATH = Path(r"C:\Users\paruc\Downloads\archive (15).zip")
MODELS_DIR = PROJECT_ROOT / "models" / "social"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

print("==========================================================")
print("  TRUSTGUARD AI: TRAINING SOCIAL MEDIA PROFILE MODEL      ")
print("==========================================================")

import zipfile
if not DATA_PATH.exists() and ZIP_PATH.exists():
    print(f"Loading data directly from zip: {ZIP_PATH}")
    with zipfile.ZipFile(ZIP_PATH, 'r') as z:
        df = pd.read_csv(z.open("raw_user_profiles.csv"))
else:
    print(f"Loading data from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

print(f"Raw dataset shape: {df.shape}")

# Feature Engineering & Selection
feature_cols = [
    'account_age_days',
    'profile_completeness',
    'followers_count',
    'following_count',
    'posts_count',
    'is_private',
    'is_verified',
    'profile_picture',
    'profile_banner',
    'has_bio',
    'has_website',
    'has_location'
]

# Convert booleans to floats
for col in feature_cols:
    if df[col].dtype == bool:
        df[col] = df[col].astype(float)
    else:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

# Add engineered features
df['follower_following_ratio'] = df['followers_count'] / (df['following_count'] + 1.0)
df['posts_per_day'] = df['posts_count'] / (df['account_age_days'] + 1.0)
feature_cols.extend(['follower_following_ratio', 'posts_per_day'])

# Target: is_fake (0 = Genuine, 1 = Fake)
y = df['is_fake'].astype(int).values
X = df[feature_cols].values

print(f"Selected {len(feature_cols)} features: {feature_cols}")
print(f"Class distribution: Genuine (0)={np.sum(y == 0)}, Fake (1)={np.sum(y == 1)}")

# Data Leakage Protection: Stratified 80/10/10 split
# 1. Split into train_val and test
X_train_val, X_test, y_train_val, y_test = train_test_split(
    X, y, test_size=0.10, random_state=42, stratify=y
)
# 2. Split train_val into train and val
X_train, X_val, y_train, y_val = train_test_split(
    X_train_val, y_train_val, test_size=0.1111, random_state=42, stratify=y_train_val  # ~10% of total
)

print(f"\nDataset Splits:")
print(f"  Training set:   {X_train.shape[0]} samples ({np.sum(y_train == 0)} genuine, {np.sum(y_train == 1)} fake)")
print(f"  Validation set: {X_val.shape[0]} samples ({np.sum(y_val == 0)} genuine, {np.sum(y_val == 1)} fake)")
print(f"  Test set:       {X_test.shape[0]} samples ({np.sum(y_test == 0)} genuine, {np.sum(y_test == 1)} fake)")

# STAGE 2: Zero Leakage Scaling — fit ONLY on X_train!
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# PyTorch Tensors
X_tr_t = torch.tensor(X_train_scaled, dtype=torch.float32)
y_tr_t = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)

X_va_t = torch.tensor(X_val_scaled, dtype=torch.float32)
y_va_t = torch.tensor(y_val, dtype=torch.float32).unsqueeze(1)

X_te_t = torch.tensor(X_test_scaled, dtype=torch.float32)
y_te_t = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)

train_loader = DataLoader(TensorDataset(X_tr_t, y_tr_t), batch_size=64, shuffle=True)
val_loader = DataLoader(TensorDataset(X_va_t, y_va_t), batch_size=64, shuffle=False)

# Model Architecture
class SocialProfileNet(nn.Module):
    def __init__(self, input_dim):
        super(SocialProfileNet, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.BatchNorm1d(64),
            nn.LeakyReLU(0.1),
            nn.Dropout(0.25),
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.LeakyReLU(0.1),
            nn.Dropout(0.2),
            nn.Linear(32, 16),
            nn.LeakyReLU(0.1),
            nn.Linear(16, 1)  # Single logit output for BCEWithLogitsLoss
        )

    def forward(self, x):
        return self.net(x)

input_dim = len(feature_cols)
model = SocialProfileNet(input_dim)

# Class Imbalance Weighting
neg_count = np.sum(y_train == 0)
pos_count = np.sum(y_train == 1)
pos_weight = torch.tensor([neg_count / pos_count], dtype=torch.float32)
criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
optimizer = optim.AdamW(model.parameters(), lr=0.003, weight_decay=1e-4)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3)

print("\nStarting Training...")
epochs = 35
best_val_loss = float('inf')
best_val_epoch = 0
best_model_state = None
history = []

start_time = time.time()
for epoch in range(1, epochs + 1):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for batch_x, batch_y in train_loader:
        optimizer.zero_grad()
        logits = model(batch_x)
        loss = criterion(logits, batch_y)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * batch_x.size(0)
        preds = (torch.sigmoid(logits) >= 0.5).float()
        correct += (preds == batch_y).sum().item()
        total += batch_y.size(0)
        
    train_loss = running_loss / total
    train_acc = correct / total
    
    # Validation
    model.eval()
    val_loss = 0.0
    val_correct = 0
    val_total = 0
    with torch.no_grad():
        for batch_x, batch_y in val_loader:
            logits = model(batch_x)
            loss = criterion(logits, batch_y)
            val_loss += loss.item() * batch_x.size(0)
            preds = (torch.sigmoid(logits) >= 0.5).float()
            val_correct += (preds == batch_y).sum().item()
            val_total += batch_y.size(0)
            
    val_loss = val_loss / val_total
    val_acc = val_correct / val_total
    scheduler.step(val_loss)
    
    history.append({
        "epoch": epoch,
        "train_loss": round(train_loss, 4),
        "train_acc": round(train_acc, 4),
        "val_loss": round(val_loss, 4),
        "val_acc": round(val_acc, 4)
    })
    
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        best_val_epoch = epoch
        best_model_state = model.state_dict().copy()
        
    if epoch % 5 == 0 or epoch == 1:
        print(f"Epoch {epoch:02d}/{epochs:02d} | Train Loss: {train_loss:.4f}, Train Acc: {train_acc*100:.1f}% | Val Loss: {val_loss:.4f}, Val Acc: {val_acc*100:.1f}%")

train_duration = time.time() - start_time
print(f"\nTraining completed in {train_duration:.2f}s. Best Epoch: {best_val_epoch} (Val Loss: {best_val_loss:.4f})")

# Load best checkpoint
model.load_state_dict(best_model_state)
model.eval()

# FINAL EVALUATION ON COMPLETELY HELD-OUT TEST SET
with torch.no_grad():
    test_logits = model(X_te_t)
    test_probs = torch.sigmoid(test_logits).squeeze().numpy()
    test_preds = (test_probs >= 0.5).astype(int)

test_acc = accuracy_score(y_test, test_preds)
test_prec = precision_score(y_test, test_preds, zero_division=0)
test_rec = recall_score(y_test, test_preds, zero_division=0)
test_f1 = f1_score(y_test, test_preds, zero_division=0)
test_auc = roc_auc_score(y_test, test_probs)
cm = confusion_matrix(y_test, test_preds).tolist()

print("\n==========================================================")
print("       HELD-OUT TEST SET PERFORMANCE METRICS              ")
print("==========================================================")
print(f"  Test Accuracy:     {test_acc*100:.2f}%")
print(f"  Precision:         {test_prec*100:.2f}%")
print(f"  Recall:            {test_rec*100:.2f}%")
print(f"  F1 Score:          {test_f1*100:.2f}%")
print(f"  ROC-AUC:           {test_auc:.4f}")
print(f"  Confusion Matrix:  {cm}")
print(f"    [TN={cm[0][0]}, FP={cm[0][1]}] (Genuine)")
print(f"    [FN={cm[1][0]}, TP={cm[1][1]}] (Fake)")
print("\nClassification Report:\n", classification_report(y_test, test_preds, target_names=["Genuine", "Fake"]))

# Save Model Checkpoint and Artifacts
checkpoint_path = MODELS_DIR / "best_model_profile.pt"
scaler_path = MODELS_DIR / "scaler_profile.pkl"
features_path = MODELS_DIR / "feature_names_profile.json"
metrics_path = MODELS_DIR / "training_metrics_profile.json"
meta_path = MODELS_DIR / "metadata_profile.json"

torch.save(best_model_state, checkpoint_path)
with open(scaler_path, "wb") as f:
    pickle.dump(scaler, f)
with open(features_path, "w", encoding="utf-8") as f:
    json.dump(feature_cols, f, indent=2)

metrics_data = {
    "model_name": "SocialProfileNet",
    "dataset": "archive (15) Comprehensive User Profiles",
    "dataset_source": r"C:\Users\paruc\Downloads\archive (15)\raw_user_profiles.csv",
    "total_samples": len(df),
    "train_samples": len(X_train),
    "val_samples": len(X_val),
    "test_samples": len(X_test),
    "features_count": len(feature_cols),
    "features": feature_cols,
    "best_epoch": best_val_epoch,
    "training_duration_seconds": round(train_duration, 2),
    "test_accuracy": round(test_acc, 4),
    "test_precision": round(test_prec, 4),
    "test_recall": round(test_rec, 4),
    "test_f1": round(test_f1, 4),
    "test_roc_auc": round(test_auc, 4),
    "confusion_matrix": cm,
    "classes": ["0: Genuine Account", "1: Fake / Malicious Account"],
    "class_distribution": {
        "train": {"genuine": int(np.sum(y_train == 0)), "fake": int(np.sum(y_train == 1))},
        "val": {"genuine": int(np.sum(y_val == 0)), "fake": int(np.sum(y_val == 1))},
        "test": {"genuine": int(np.sum(y_test == 0)), "fake": int(np.sum(y_test == 1))}
    }
}

with open(metrics_path, "w", encoding="utf-8") as f:
    json.dump(metrics_data, f, indent=2)

with open(meta_path, "w", encoding="utf-8") as f:
    json.dump({
        **metrics_data,
        "history": history
    }, f, indent=2)

print(f"\nAll artifacts saved successfully:")
print(f"  Model:     {checkpoint_path}")
print(f"  Scaler:    {scaler_path}")
print(f"  Features:  {features_path}")
print(f"  Metrics:   {metrics_path}")
print(f"  Metadata:  {meta_path}")
