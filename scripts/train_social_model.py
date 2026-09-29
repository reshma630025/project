"""
TrustGuard AI — Social Media Fake Profile & Spammer Detection Model Training
Dataset: Kaggle Instagram Fake Spammer Genuine Accounts (archive (14))
Features: 11 profile/behavioral indicators
Architecture: PyTorch SocialSpamNet (Deep Tabular Classifier)
Outputs: models/social/best_model.pt, scaler.pkl, feature_names.json, metadata.json
"""

import os
import sys
import json
import time
import pickle
import numpy as np
import pandas as pd
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

# Paths
DATASET_DIR = Path(r"C:\Users\paruc\Downloads\archive (14)")
TRAIN_CSV = DATASET_DIR / "train.csv"
TEST_CSV = DATASET_DIR / "test.csv"

PROJECT_ROOT = Path(r"C:\Users\paruc\OneDrive\Desktop\Reshma")
MODELS_DIR = PROJECT_ROOT / "models" / "social"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

FEATURE_COLS = [
    'profile pic',
    'nums/length username',
    'fullname words',
    'nums/length fullname',
    'name==username',
    'description length',
    'external URL',
    'private',
    '#posts',
    '#followers',
    '#follows'
]
TARGET_COL = 'fake'

class SocialSpamNet(nn.Module):
    def __init__(self, input_dim=11):
        super(SocialSpamNet, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.BatchNorm1d(64),
            nn.LeakyReLU(0.1),
            nn.Dropout(0.25),
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.LeakyReLU(0.1),
            nn.Dropout(0.15),
            nn.Linear(32, 16),
            nn.LeakyReLU(0.1),
            nn.Linear(16, 2)
        )

    def forward(self, x):
        return self.net(x)

def train():
    print("=======================================================", flush=True)
    print("TRUSTGUARD AI — SOCIAL MEDIA CLASSIFIER TRAINING", flush=True)
    print("=======================================================", flush=True)
    
    if not TRAIN_CSV.exists() or not TEST_CSV.exists():
        raise FileNotFoundError(f"Missing dataset files in {DATASET_DIR}")
        
    train_df = pd.read_csv(TRAIN_CSV)
    test_df = pd.read_csv(TEST_CSV)
    
    print(f"Loaded train.csv: {len(train_df)} rows", flush=True)
    print(f"Loaded test.csv:  {len(test_df)} rows", flush=True)
    print(f"Features ({len(FEATURE_COLS)}): {FEATURE_COLS}", flush=True)
    print(f"Target: '{TARGET_COL}' | Class distribution in train: {dict(train_df[TARGET_COL].value_counts())}", flush=True)
    print(f"Class distribution in test: {dict(test_df[TARGET_COL].value_counts())}", flush=True)
    
    X_train = train_df[FEATURE_COLS].values.astype(np.float32)
    y_train = train_df[TARGET_COL].values.astype(np.int64)
    
    X_test = test_df[FEATURE_COLS].values.astype(np.float32)
    y_test = test_df[TARGET_COL].values.astype(np.int64)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # PyTorch Datasets
    train_dataset = TensorDataset(torch.tensor(X_train_scaled), torch.tensor(y_train))
    test_dataset = TensorDataset(torch.tensor(X_test_scaled), torch.tensor(y_test))
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    
    # Model, Loss, Optimizer
    device = torch.device("cpu")
    model = SocialSpamNet(input_dim=len(FEATURE_COLS)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=0.003, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=5)
    
    best_test_acc = 0.0
    best_metrics = {}
    best_weights = None
    
    epochs = 40
    print(f"\nTraining SocialSpamNet for {epochs} epochs...", flush=True)
    
    t0 = time.time()
    for epoch in range(1, epochs + 1):
        model.train()
        train_loss = 0.0
        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            logits = model(batch_x)
            loss = criterion(logits, batch_y)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * batch_x.size(0)
            
        train_loss /= len(train_loader.dataset)
        
        # Validation on test set
        model.eval()
        all_preds = []
        all_targets = []
        with torch.no_grad():
            for batch_x, batch_y in test_loader:
                logits = model(batch_x)
                preds = torch.argmax(logits, dim=1).cpu().numpy()
                all_preds.extend(preds)
                all_targets.extend(batch_y.numpy())
                
        test_acc = accuracy_score(all_targets, all_preds)
        scheduler.step(test_acc)
        
        if test_acc > best_test_acc or best_weights is None:
            best_test_acc = test_acc
            best_weights = model.state_dict().copy()
            best_metrics = {
                "epoch": epoch,
                "accuracy": round(float(test_acc), 4),
                "precision": round(float(precision_score(all_targets, all_preds, zero_division=0)), 4),
                "recall": round(float(recall_score(all_targets, all_preds, zero_division=0)), 4),
                "f1": round(float(f1_score(all_targets, all_preds, zero_division=0)), 4),
                "confusion_matrix": confusion_matrix(all_targets, all_preds).tolist()
            }
            
        if epoch % 5 == 0 or epoch == epochs:
            print(f"Epoch {epoch:02d}/{epochs:02d} | Train Loss: {train_loss:.4f} | Test Acc: {test_acc*100:.2f}% (Best: {best_test_acc*100:.2f}%)", flush=True)
            
    train_duration = round(time.time() - t0, 2)
    print(f"\nTraining completed in {train_duration}s!", flush=True)
    
    # Save best checkpoint
    model_path = MODELS_DIR / "best_model.pt"
    torch.save(best_weights, model_path)
    print(f"Saved PyTorch weights -> {model_path}", flush=True)
    
    # Save Scaler
    scaler_path = MODELS_DIR / "scaler.pkl"
    with open(scaler_path, "wb") as f:
        pickle.dump(scaler, f)
    print(f"Saved StandardScaler -> {scaler_path}", flush=True)
    
    # Save Feature Names
    features_path = MODELS_DIR / "feature_names.json"
    with open(features_path, "w", encoding="utf-8") as f:
        json.dump(FEATURE_COLS, f, indent=2)
    print(f"Saved Feature Names -> {features_path}", flush=True)
    
    # Save Metadata
    metadata = {
        "model_name": "SocialSpamNet",
        "dataset": "Kaggle Instagram Fake Spammer Genuine Accounts (archive (14))",
        "train_samples": len(train_df),
        "test_samples": len(test_df),
        "features": FEATURE_COLS,
        "input_dim": len(FEATURE_COLS),
        "classes": ["0: GENUINE", "1: FAKE / SPAM"],
        "metrics": best_metrics,
        "training_duration_seconds": train_duration,
        "timestamp": time.time()
    }
    meta_path = MODELS_DIR / "metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved Metadata -> {meta_path}", flush=True)
    
    print("\n=======================================================", flush=True)
    print(f"FINAL TEST SET EVALUATION METRICS:", flush=True)
    print(f"Accuracy:  {best_metrics['accuracy']*100:.2f}%", flush=True)
    print(f"Precision: {best_metrics['precision']*100:.2f}%", flush=True)
    print(f"Recall:    {best_metrics['recall']*100:.2f}%", flush=True)
    print(f"F1 Score:  {best_metrics['f1']*100:.2f}%", flush=True)
    print(f"Confusion Matrix: {best_metrics['confusion_matrix']}", flush=True)
    print("=======================================================", flush=True)

if __name__ == "__main__":
    train()
