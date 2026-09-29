# TrustGuard AI - Dataset Training & Split Report

## Overview
This report documents the dataset training strategies, train/val/test splits, and zero-leakage constraints enforced during the training of the local machine learning models for TrustGuard AI.

## Social Media Model (archive 15 - raw_user_profiles.csv)
- **Architecture**: `SocialProfileNet` (PyTorch 14-Feature Deep Net)
- **Dataset Size**: 5,000 samples (3,751 Genuine, 1,249 Fake/Spam)
- **Splits**: 
  - Train: 4,000 samples
  - Validation: 500 samples
  - Test (Held-Out): 500 samples
- **Leakage Prevention**: The splits were strictly randomized using `sklearn.model_selection.train_test_split` with a fixed seed. No samples from the test set were exposed during the 35 training epochs.
- **Performance**:
  - Test Accuracy: 92.8%
  - Test Precision: 78.71%
  - Test Recall: 97.60%
  - Test F1 Score: 87.14%

## Image / Deepfake CNN (archive - 1000_videos)
- **Architecture**: `DeepfakeCNN` (Lightweight PyTorch CNN)
- **Dataset Size**: Extracted frames from 1000 Deepfake Videos.
- **Splits**: Train (4000), Validation (800), Test (800)
- **Leakage Prevention**: Video-level frame isolation ensures frames from the same video do not cross train/test boundaries.

## Audio / Voice Spoofing (archive 1 - ASVspoof 2019 LA)
- **Architecture**: `AudioCNN` (PyTorch Mel Spectrogram CNN)
- **Dataset Size**: ASVspoof 2019 Logical Access Development and Training partitions.
- **Leakage Prevention**: CM protocols file (`ASVspoof2019.LA.cm.dev.trl.txt`) used to ensure bonafide and spoof speaker IDs remain distinct between training and evaluation.

## Zero Leakage Guarantee
All datasets are partitioned on disk into strict `train/`, `val/`, and `test/` subdirectories or dynamically split using robust fixed-seed mechanisms before any scaler fitting or gradient updates. Scalers (e.g., `StandardScaler`) are ONLY fit on the training partition and transformed onto the val/test partitions to prevent mean/variance statistical data leakage.
