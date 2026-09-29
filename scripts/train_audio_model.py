r"""
TrustGuard AI — Audio Deepfake Model Training (ASVspoof 2019 LA)
Uses Dataset 1: C:\Users\paruc\Downloads\archive (1)\LA\LA

Audio files: FLAC (dev split — audio available)
Labels: bonafide=0, spoof=1 (from cm_protocols)
Architecture: Lightweight CNN on Mel Spectrogram (CPU-compatible)

Run: python scripts/train_audio_model.py
"""
import os
import sys
import json
import time
import logging
import warnings
warnings.filterwarnings('ignore')

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from pathlib import Path
from datetime import datetime

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger("trustguard.train_audio")

# ── Paths ──────────────────────────────────────────────────────────────────────
DATASET_ROOT  = Path(r"C:\Users\paruc\Downloads\archive (1)\LA\LA")
DEV_AUDIO_DIR = DATASET_ROOT / "ASVspoof2019_LA_dev" / "flac"
DEV_PROTO     = DATASET_ROOT / "ASVspoof2019_LA_cm_protocols" / "ASVspoof2019.LA.cm.dev.trl.txt"
PROJECT_ROOT  = Path(__file__).resolve().parent.parent
MODELS_DIR    = PROJECT_ROOT / "models" / "audio"
DATA_DIR      = PROJECT_ROOT / "data"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ── Hyperparameters ────────────────────────────────────────────────────────────
SAMPLE_RATE  = 16000
MAX_DURATION = 3.0       # seconds per clip (trim/pad)
N_MELS       = 64
HOP_LENGTH   = 160       # 10ms hop at 16kHz
WIN_LENGTH   = 400       # 25ms window
MAX_FRAMES   = int((MAX_DURATION * SAMPLE_RATE) / HOP_LENGTH) + 1

BATCH_SIZE   = 32
EPOCHS       = 20
LR           = 1e-3
SEED         = 42
MAX_BONAFIDE = 2000      # limit to balance (bonafide is minority)
MAX_SPOOF    = 2000      # limit to balance

torch.manual_seed(SEED)
np.random.seed(SEED)


# ── Protocol Parser ────────────────────────────────────────────────────────────
def parse_protocol(proto_path: Path, audio_dir: Path):
    """Parses ASVspoof CM protocol: speaker | filename | - | - | bonafide/spoof"""
    samples = []
    with open(proto_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 5:
                continue
            fname  = parts[1]  # e.g. LA_D_1000265
            label  = parts[4]  # bonafide or spoof
            fpath  = audio_dir / f"{fname}.flac"
            if fpath.exists():
                label_int = 0 if label == "bonafide" else 1
                samples.append((fpath, label_int, label))
    return samples


# ── Precomputed Mel Filterbank Matrix ──────────────────────────────────────────
def _get_mel_filterbank(sr=SAMPLE_RATE, n_fft=512, n_mels=N_MELS):
    mel_min = 2595.0 * np.log10(1.0 + 20.0 / 700.0)
    mel_max = 2595.0 * np.log10(1.0 + (sr / 2.0) / 700.0)
    mel_pts = np.linspace(mel_min, mel_max, n_mels + 2)
    hz_pts  = 700.0 * (10.0 ** (mel_pts / 2595.0) - 1.0)
    bin_pts = np.floor((n_fft + 1) * hz_pts / sr).astype(int)

    fbank = np.zeros((n_mels, n_fft // 2 + 1), dtype=np.float32)
    for m in range(1, n_mels + 1):
        f_m_minus = bin_pts[m - 1]
        f_m       = bin_pts[m]
        f_m_plus  = bin_pts[m + 1]
        for k in range(f_m_minus, f_m):
            if f_m > f_m_minus:
                fbank[m - 1, k] = (k - f_m_minus) / (f_m - f_m_minus)
        for k in range(f_m, f_m_plus):
            if f_m_plus > f_m:
                fbank[m - 1, k] = (f_m_plus - k) / (f_m_plus - f_m)
    return torch.from_numpy(fbank)

MEL_FBANK   = _get_mel_filterbank()
HANN_WINDOW = torch.hann_window(WIN_LENGTH)


def compute_mel_spectrogram(audio: np.ndarray, sr: int,
                            n_mels: int = N_MELS,
                            hop_len: int = HOP_LENGTH,
                            win_len: int = WIN_LENGTH,
                            n_fft: int = 512) -> np.ndarray:
    """Compute log mel spectrogram using fast vectorized torch STFT."""
    target_len = int(MAX_DURATION * sr)
    if len(audio) < target_len:
        audio = np.pad(audio, (0, target_len - len(audio)))
    else:
        audio = audio[:target_len]

    t_audio  = torch.from_numpy(audio.astype(np.float32))
    stft     = torch.stft(
        t_audio,
        n_fft=n_fft,
        hop_length=hop_len,
        win_length=win_len,
        window=HANN_WINDOW,
        return_complex=True
    )
    stft_mag = torch.abs(stft)  # (n_fft // 2 + 1, n_frames)
    mel_spec = torch.matmul(MEL_FBANK, stft_mag)  # (n_mels, n_frames)
    log_mel  = torch.log(mel_spec + 1e-9)
    return log_mel.numpy().astype(np.float32)


# ── Audio Loading ──────────────────────────────────────────────────────────────
def load_flac(path: Path) -> tuple:
    try:
        import soundfile as sf
        data, sr = sf.read(str(path))
        if len(data.shape) > 1:
            data = data.mean(axis=1)
        data = data.astype(np.float32)
        # Resample to 16kHz if needed
        if sr != SAMPLE_RATE:
            target_len = int(len(data) * SAMPLE_RATE / sr)
            indices    = np.linspace(0, len(data) - 1, target_len)
            data       = np.interp(indices, np.arange(len(data)), data)
            sr         = SAMPLE_RATE
        return data, sr
    except Exception as e:
        logger.debug(f"Failed to load {path}: {e}")
        return None, None


# ── Dataset ────────────────────────────────────────────────────────────────────
class ASVspoofDataset(Dataset):
    def __init__(self, samples: list, augment: bool = False):
        self.samples = samples
        self.augment = augment

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label, _ = self.samples[idx]
        audio, sr = load_flac(path)

        if audio is None or sr is None:
            # Return zero spectrogram on failure
            mel = np.zeros((N_MELS, MAX_FRAMES), dtype=np.float32)
        else:
            # Basic augmentation for training
            if self.augment and label == 0:  # only augment bonafide (minority)
                if np.random.rand() > 0.5:
                    noise = np.random.normal(0, 0.002, len(audio)).astype(np.float32)
                    audio = audio + noise

            mel = compute_mel_spectrogram(audio, sr)
            # Normalize per-sample
            mel = (mel - mel.mean()) / (mel.std() + 1e-8)

        # Pad/trim to fixed width
        if mel.shape[1] < MAX_FRAMES:
            mel = np.pad(mel, ((0, 0), (0, MAX_FRAMES - mel.shape[1])))
        else:
            mel = mel[:, :MAX_FRAMES]

        # Add channel dim → (1, n_mels, n_frames)
        tensor = torch.from_numpy(mel).unsqueeze(0)
        return tensor, torch.tensor(label, dtype=torch.long)


# ── Model ──────────────────────────────────────────────────────────────────────
class AudioCNN(nn.Module):
    """
    Lightweight CNN for audio deepfake detection from mel spectrograms.
    Input: (batch, 1, n_mels=64, n_frames)
    """
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=(3,3), padding=1),
            nn.BatchNorm2d(32), nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=(3,3), padding=1),
            nn.BatchNorm2d(32), nn.ReLU(inplace=True),
            
            nn.MaxPool2d(2, 2), nn.Dropout2d(0.1),

            nn.Conv2d(32, 64, kernel_size=(3,3), padding=1),
            nn.BatchNorm2d(64), nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=(3,3), padding=1),
            nn.BatchNorm2d(64), nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2), nn.Dropout2d(0.15),

            nn.Conv2d(64, 128, kernel_size=(3,3), padding=1),
            nn.BatchNorm2d(128), nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((4, 4)),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.4),
            nn.Linear(256, 64),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        return self.classifier(self.features(x))


# ── Training / Eval ────────────────────────────────────────────────────────────
def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total_loss, correct, total = 0.0, 0, 0
    for mels, labels in loader:
        mels, labels = mels.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(mels)
        loss    = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * mels.size(0)
        preds   = outputs.argmax(dim=1)
        correct += (preds == labels).sum().item()
        total   += mels.size(0)
    return total_loss / total, correct / total


def eval_epoch(model, loader, criterion, device):
    model.eval()
    total_loss, correct, total = 0.0, 0, 0
    all_preds, all_labels, all_probs = [], [], []
    with torch.no_grad():
        for mels, labels in loader:
            mels, labels = mels.to(device), labels.to(device)
            outputs = model(mels)
            loss    = criterion(outputs, labels)
            total_loss += loss.item() * mels.size(0)
            probs   = torch.softmax(outputs, dim=1)[:, 1]
            preds   = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total   += mels.size(0)
            all_preds.extend(preds.cpu().numpy().tolist())
            all_labels.extend(labels.cpu().numpy().tolist())
            all_probs.extend(probs.cpu().numpy().tolist())
    return total_loss / total, correct / total, all_preds, all_labels, all_probs


def compute_metrics(preds, labels, probs):
    preds  = np.array(preds)
    labels = np.array(labels)
    probs  = np.array(probs)

    tp = int(np.sum((preds == 1) & (labels == 1)))
    tn = int(np.sum((preds == 0) & (labels == 0)))
    fp = int(np.sum((preds == 1) & (labels == 0)))
    fn = int(np.sum((preds == 0) & (labels == 1)))

    accuracy  = (tp + tn) / max(len(labels), 1)
    precision = tp / max(tp + fp, 1)
    recall    = tp / max(tp + fn, 1)
    f1        = 2 * precision * recall / max(precision + recall, 1e-9)

    # ROC-AUC
    thresholds = np.sort(np.unique(probs))[::-1]
    tprs, fprs = [], []
    for t in thresholds:
        p   = (probs >= t).astype(int)
        tpr = np.sum((p == 1) & (labels == 1)) / max(np.sum(labels == 1), 1)
        fpr = np.sum((p == 1) & (labels == 0)) / max(np.sum(labels == 0), 1)
    trapz_fn = getattr(np, 'trapezoid', getattr(np, 'trapz', None))
    roc_auc = abs(float(trapz_fn(np.array(tprs), np.array(fprs))))

    return {
        "accuracy":  round(accuracy, 4),
        "precision": round(precision, 4),
        "recall":    round(recall, 4),
        "f1":        round(f1, 4),
        "roc_auc":   round(roc_auc, 4),
        "confusion_matrix": [[tn, fp], [fn, tp]],
        "tp": tp, "tn": tn, "fp": fp, "fn": fn
    }


def main():
    print("\n" + "="*60)
    print("TrustGuard AI — Audio Deepfake Model Training")
    print("="*60)
    print(f"Dataset:   {DATASET_ROOT}")
    print(f"Protocol:  {DEV_PROTO}")
    print(f"Model dir: {MODELS_DIR}")
    print(f"Sample rate: {SAMPLE_RATE} Hz | Max duration: {MAX_DURATION}s")
    print(f"Mel bins: {N_MELS} | Max frames: {MAX_FRAMES}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    if not DEV_PROTO.exists():
        print("ERROR: Protocol file not found!")
        sys.exit(1)
    if not DEV_AUDIO_DIR.exists():
        print("ERROR: Audio directory not found!")
        sys.exit(1)

    # ── Parse protocol ─────────────────────────────────────────────────────────
    print("\n→ Parsing protocol file...")
    all_samples = parse_protocol(DEV_PROTO, DEV_AUDIO_DIR)

    bonafide_samples = [s for s in all_samples if s[1] == 0]
    spoof_samples    = [s for s in all_samples if s[1] == 1]

    print(f"  Available: {len(bonafide_samples)} bonafide + {len(spoof_samples)} spoof")
    print(f"  Label mapping: 0=bonafide (AUTHENTIC VOICE), 1=spoof (AI-GENERATED VOICE)")

    # Limit for CPU training
    rng = np.random.default_rng(SEED)
    b_idx = rng.permutation(len(bonafide_samples))[:MAX_BONAFIDE]
    s_idx = rng.permutation(len(spoof_samples))[:MAX_SPOOF]

    bonafide_used = [bonafide_samples[i] for i in b_idx]
    spoof_used    = [spoof_samples[i] for i in s_idx]
    all_used      = bonafide_used + spoof_used

    rng.shuffle(all_used)

    # 80/10/10 split
    n_total = len(all_used)
    n_train = int(0.80 * n_total)
    n_val   = int(0.10 * n_total)
    train_samples = all_used[:n_train]
    val_samples   = all_used[n_train:n_train + n_val]
    test_samples  = all_used[n_train + n_val:]

    print(f"\n→ Split (80/10/10 with seed={SEED}):")
    print(f"  Train: {len(train_samples)} "
          f"(bon={sum(1 for s in train_samples if s[1]==0)}, "
          f"spoof={sum(1 for s in train_samples if s[1]==1)})")
    print(f"  Val:   {len(val_samples)}")
    print(f"  Test:  {len(test_samples)}")

    # Save manifest
    manifest_rows = []
    for path, label_int, label_str in all_used:
        split = ("train" if (path, label_int, label_str) in train_samples
                 else "val" if (path, label_int, label_str) in val_samples
                 else "test")
        manifest_rows.append({
            "file_path": str(path),
            "dataset_source": "archive_(1)_ASVspoof2019_LA",
            "modality": "audio",
            "label": label_str,
            "label_int": label_int,
            "split": split,
            "format": ".flac"
        })

    import csv
    manifest_path = DATA_DIR / "audio_dataset_manifest.csv"
    with open(manifest_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=manifest_rows[0].keys())
        writer.writeheader()
        writer.writerows(manifest_rows)
    print(f"\n✓ Audio manifest saved: {manifest_path}")

    # ── Datasets / Loaders ─────────────────────────────────────────────────────
    print("\n→ Preparing mel spectrograms...")
    train_ds = ASVspoofDataset(train_samples, augment=True)
    val_ds   = ASVspoofDataset(val_samples,   augment=False)
    test_ds  = ASVspoofDataset(test_samples,  augment=False)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,  num_workers=0)
    val_loader   = DataLoader(val_ds,   batch_size=BATCH_SIZE, shuffle=False, num_workers=0)
    test_loader  = DataLoader(test_ds,  batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    # ── Model ─────────────────────────────────────────────────────────────────
    model = AudioCNN().to(device)
    param_count = sum(p.numel() for p in model.parameters())
    print(f"Model: AudioCNN | Parameters: {param_count:,}")

    # Equal weighting after balancing
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LR, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=3, factor=0.5)

    # ── Training ───────────────────────────────────────────────────────────────
    print("\n→ Training...")
    best_val_loss  = float('inf')
    best_val_acc   = 0.0
    patience_count = 0
    PATIENCE       = 5
    history        = []

    for epoch in range(1, EPOCHS + 1):
        t0 = time.time()
        tr_loss, tr_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        va_loss, va_acc, _, _, _ = eval_epoch(model, val_loader, criterion, device)
        scheduler.step(va_loss)

        elapsed = time.time() - t0
        lr = optimizer.param_groups[0]['lr']
        print(f"Epoch {epoch:02d}/{EPOCHS} | "
              f"Train loss={tr_loss:.4f} acc={tr_acc:.4f} | "
              f"Val loss={va_loss:.4f} acc={va_acc:.4f} | "
              f"LR={lr:.6f} | {elapsed:.1f}s", flush=True)

        history.append({
            "epoch": epoch, "train_loss": round(tr_loss, 4), "train_acc": round(tr_acc, 4),
            "val_loss": round(va_loss, 4), "val_acc": round(va_acc, 4)
        })

        if va_loss < best_val_loss:
            best_val_loss = va_loss
            best_val_acc  = va_acc
            torch.save(model.state_dict(), str(MODELS_DIR / "best_model.pt"))
            patience_count = 0
            print(f"  ✓ Best model saved (val_loss={va_loss:.4f})", flush=True)
        else:
            patience_count += 1
            if patience_count >= PATIENCE:
                print(f"  Early stopping at epoch {epoch}", flush=True)
                break

    # ── Test evaluation ────────────────────────────────────────────────────────
    print("\n→ Test evaluation...")
    model.load_state_dict(torch.load(str(MODELS_DIR / "best_model.pt"), map_location=device))
    _, test_acc, test_preds, test_labels, test_probs = eval_epoch(model, test_loader, criterion, device)
    metrics = compute_metrics(test_preds, test_labels, test_probs)

    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    print(f"  Accuracy:   {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    print(f"  Precision:  {metrics['precision']:.4f}")
    print(f"  Recall:     {metrics['recall']:.4f}")
    print(f"  F1 Score:   {metrics['f1']:.4f}")
    print(f"  ROC-AUC:    {metrics['roc_auc']:.4f}")
    print(f"  Confusion Matrix: TN={metrics['tn']} FP={metrics['fp']} FN={metrics['fn']} TP={metrics['tp']}")

    # ── Metadata ───────────────────────────────────────────────────────────────
    metadata = {
        "model_name":       "AudioCNN",
        "modality":         "audio",
        "dataset_sources":  ["archive_(1)_ASVspoof2019_LA_dev"],
        "dataset_type":     "ASVspoof 2019 Logical Access — voice anti-spoofing",
        "classes":          ["bonafide", "spoof"],
        "label_mapping":    {"0": "bonafide (AUTHENTIC VOICE)", "1": "spoof (AI-GENERATED VOICE)"},
        "sample_rate":      SAMPLE_RATE,
        "max_duration":     MAX_DURATION,
        "n_mels":           N_MELS,
        "max_frames":       MAX_FRAMES,
        "training_date":    datetime.now().isoformat(),
        "framework":        f"PyTorch {torch.__version__}",
        "device":           str(device),
        "train_samples":    len(train_samples),
        "val_samples":      len(val_samples),
        "test_samples":     len(test_samples),
        "epochs_completed": len(history),
        "best_val_loss":    round(best_val_loss, 4),
        "best_val_acc":     round(best_val_acc, 4),
        "accuracy":         metrics["accuracy"],
        "precision":        metrics["precision"],
        "recall":           metrics["recall"],
        "f1":               metrics["f1"],
        "roc_auc":          metrics["roc_auc"],
        "confusion_matrix": metrics["confusion_matrix"],
        "training_history": history,
        "version":          "1.0.0",
        "model_file":       "best_model.pt"
    }

    with open(MODELS_DIR / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    with open(MODELS_DIR / "training_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    with open(DATA_DIR / "reports" / "audio_training_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\n✓ Model saved:    {MODELS_DIR / 'best_model.pt'}")
    print(f"✓ Metadata saved: {MODELS_DIR / 'metadata.json'}")

    print("\n✓ Audio model training complete!")
    return metadata


if __name__ == "__main__":
    main()
