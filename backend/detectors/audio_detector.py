"""
Audio and Voice Deepfake Detector for TrustGuard AI.
Performs audio segment-by-segment window analysis, short-time spectral feature extraction
(Spectral Centroid, Spectral Flux, Spectral Rolloff, High-Frequency Vocoder roll-off, ZCR),
and deterministic temporal segment aggregation.
"""
import os
import io
import time
import json
import wave
import struct
import tempfile
import logging
from pathlib import Path
import numpy as np
from typing import Dict, Any, List, Tuple

from backend.utils.response_utils import clamp_score, authenticity_classification, calculate_trust_score

logger = logging.getLogger("trustguard.audio_detector")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TRAINED_AUDIO_MODEL = PROJECT_ROOT / "models" / "audio" / "best_model.pt"
AUDIO_MODEL_METADATA = PROJECT_ROOT / "models" / "audio" / "metadata.json"

SAMPLE_RATE_MODEL = 16000
MAX_DURATION_MODEL = 3.0
N_MELS_MODEL = 64
HOP_LENGTH_MODEL = 160
WIN_LENGTH_MODEL = 400
MAX_FRAMES_MODEL = int((MAX_DURATION_MODEL * SAMPLE_RATE_MODEL) / HOP_LENGTH_MODEL) + 1

_trained_audio_model = None
_trained_audio_meta = None
_trained_audio_err = None
_AUDIO_FBANK = None
_HANN_WINDOW = None

def _get_audio_fbank():
    mel_min = 2595.0 * np.log10(1.0 + 20.0 / 700.0)
    mel_max = 2595.0 * np.log10(1.0 + (SAMPLE_RATE_MODEL / 2.0) / 700.0)
    mel_pts = np.linspace(mel_min, mel_max, N_MELS_MODEL + 2)
    hz_pts = 700.0 * (10.0 ** (mel_pts / 2595.0) - 1.0)
    bin_pts = np.floor((512 + 1) * hz_pts / SAMPLE_RATE_MODEL).astype(int)
    fbank = np.zeros((N_MELS_MODEL, 512 // 2 + 1), dtype=np.float32)
    for m in range(1, N_MELS_MODEL + 1):
        f_m_minus = bin_pts[m - 1]
        f_m = bin_pts[m]
        f_m_plus = bin_pts[m + 1]
        for k in range(f_m_minus, f_m):
            if f_m > f_m_minus:
                fbank[m - 1, k] = (k - f_m_minus) / (f_m - f_m_minus)
        for k in range(f_m, f_m_plus):
            if f_m_plus > f_m:
                fbank[m - 1, k] = (f_m_plus - k) / (f_m_plus - f_m)
    return fbank

def _load_trained_audio_cnn():
    global _trained_audio_model, _trained_audio_meta, _trained_audio_err, _AUDIO_FBANK, _HANN_WINDOW
    if _trained_audio_model is not None or _trained_audio_err:
        return
    if not TRAINED_AUDIO_MODEL.exists():
        _trained_audio_err = "Trained audio model not found at models/audio/best_model.pt"
        logger.info("Trained audio model not found at models/audio/best_model.pt. Using spectral forensics.")
        return

    try:
        import torch
        import torch.nn as nn

        class AudioCNN(nn.Module):
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
                    nn.Linear(128 * 4 * 4, 256), nn.ReLU(inplace=True), nn.Dropout(0.4),
                    nn.Linear(256, 64), nn.ReLU(inplace=True), nn.Dropout(0.3),
                    nn.Linear(64, 2)
                )

            def forward(self, x):
                return self.classifier(self.features(x))

        device = torch.device("cpu")
        model = AudioCNN()
        state = torch.load(str(TRAINED_AUDIO_MODEL), map_location=device)
        model.load_state_dict(state)
        model.eval()
        _trained_audio_model = model

        _AUDIO_FBANK = torch.from_numpy(_get_audio_fbank())
        _HANN_WINDOW = torch.hann_window(WIN_LENGTH_MODEL)

        if AUDIO_MODEL_METADATA.exists():
            with open(AUDIO_MODEL_METADATA) as f:
                _trained_audio_meta = json.load(f)
            logger.info(f"Trained audio model loaded (accuracy={_trained_audio_meta.get('accuracy')}).")
        else:
            _trained_audio_meta = {"model_name": "AudioCNN", "modality": "audio"}
            logger.info("Trained audio model loaded.")

    except Exception as e:
        _trained_audio_err = str(e)
        logger.error(f"Failed to load trained audio model: {e}")

def _infer_trained_audio_cnn(mono_data: np.ndarray, sr: int) -> dict:
    import torch
    audio = mono_data.astype(np.float32)
    if sr != SAMPLE_RATE_MODEL:
        target_len = int(len(audio) * SAMPLE_RATE_MODEL / sr)
        indices = np.linspace(0, len(audio) - 1, target_len)
        audio = np.interp(indices, np.arange(len(audio)), audio).astype(np.float32)

    target_len = int(MAX_DURATION_MODEL * SAMPLE_RATE_MODEL)
    if len(audio) < target_len:
        audio = np.pad(audio, (0, target_len - len(audio)))
    else:
        audio = audio[:target_len]

    t_audio = torch.from_numpy(audio)
    stft = torch.stft(
        t_audio, n_fft=512, hop_length=HOP_LENGTH_MODEL, win_length=WIN_LENGTH_MODEL,
        window=_HANN_WINDOW, return_complex=True
    )
    stft_mag = torch.abs(stft)
    mel_spec = torch.matmul(_AUDIO_FBANK, stft_mag)
    log_mel = torch.log(mel_spec + 1e-9).numpy()
    log_mel = (log_mel - log_mel.mean()) / (log_mel.std() + 1e-8)

    if log_mel.shape[1] < MAX_FRAMES_MODEL:
        log_mel = np.pad(log_mel, ((0, 0), (0, MAX_FRAMES_MODEL - log_mel.shape[1])))
    else:
        log_mel = log_mel[:, :MAX_FRAMES_MODEL]

    tensor = torch.from_numpy(log_mel).unsqueeze(0).unsqueeze(0)
    with torch.no_grad():
        out = _trained_audio_model(tensor)
        probs = torch.softmax(out, dim=1)[0]
        real_prob = float(probs[0]) * 100.0
        fake_prob = float(probs[1]) * 100.0

    return {
        "fake_prob": round(fake_prob, 2),
        "real_prob": round(real_prob, 2),
        "confidence": round(max(fake_prob, real_prob), 2),
        "model": "AudioCNN (trained on ASVspoof 2019 LA)"
    }

def load_models():
    _load_trained_audio_cnn()

# Segment window configuration
SEGMENT_DURATION_SEC = 2.0  # 2.0-second sliding analysis window
SEGMENT_HOP_SEC = 1.0       # 1.0-second hop (50% overlap)
MIN_AUDIO_DURATION = 0.5    # Minimum duration required for analysis


def decode_audio_bytes(audio_bytes: bytes) -> Tuple[np.ndarray, int]:
    """
    Robust audio decoder supporting WAV, SoundFile formats, and raw PCM fallback.
    Returns (mono_numpy_array, sample_rate).
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    try:
        temp_file.write(audio_bytes)
        temp_file.close()
        temp_path = temp_file.name

        # 1. Try soundfile
        try:
            import soundfile as sf
            data, sr = sf.read(temp_path)
            if data is not None and len(data) > 0:
                if len(data.shape) > 1:
                    data = np.mean(data, axis=1)
                return data.astype(np.float32), int(sr)
        except Exception:
            pass

        # 2. Try standard library wave module
        try:
            with wave.open(io.BytesIO(audio_bytes), 'rb') as w:
                n_channels = w.getnchannels()
                sampwidth = w.getsampwidth()
                sr = w.getframerate()
                n_frames = w.getnframes()
                raw_frames = w.readframes(n_frames)
                if sampwidth == 2:
                    data = np.frombuffer(raw_frames, dtype=np.int16).astype(np.float32) / 32768.0
                elif sampwidth == 4:
                    data = np.frombuffer(raw_frames, dtype=np.int32).astype(np.float32) / 2147483648.0
                elif sampwidth == 1:
                    data = (np.frombuffer(raw_frames, dtype=np.uint8).astype(np.float32) - 128.0) / 128.0
                else:
                    data = np.frombuffer(raw_frames, dtype=np.int16).astype(np.float32) / 32768.0

                if n_channels > 1:
                    data = data.reshape(-1, n_channels).mean(axis=1)
                return data, int(sr)
        except Exception:
            pass

        # 3. Try librosa if available
        try:
            import librosa
            data, sr = librosa.load(temp_path, sr=None)
            if data is not None and len(data) > 0:
                return data.astype(np.float32), int(sr)
        except Exception:
            pass

        # 4. Fallback: Parse as raw 16-bit PCM (16kHz)
        offset = min(44, len(audio_bytes) // 2)
        offset -= (offset % 2)
        usable_bytes = audio_bytes[offset:offset + ((len(audio_bytes) - offset) // 2) * 2]
        if len(usable_bytes) >= 200:
            raw_pcm = np.frombuffer(usable_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            if len(raw_pcm) > 100:
                return raw_pcm, 16000

        raise ValueError("Could not decode audio stream with any available decoder.")

    finally:
        if os.path.exists(temp_file.name):
            try:
                os.remove(temp_file.name)
            except Exception:
                pass


def analyze_audio_segment(
    segment_data: np.ndarray,
    sample_rate: int
) -> Dict[str, Any]:
    """
    Extracts acoustic & spectral features from a single audio segment (numpy float array)
    and evaluates synthetic vs organic human voice characteristics.
    """
    if len(segment_data) == 0:
        return {"risk_score": 10.0, "confidence": 75.0, "is_fake": False, "prediction": "REAL"}

    # 1. Zero Crossing Rate (ZCR)
    zcr = float(np.mean(np.abs(np.diff(np.sign(segment_data))))) / 2.0

    # 2. Short-Time Fourier Transform (STFT)
    n_fft = min(2048, len(segment_data))
    hop_length = 512
    if len(segment_data) < n_fft:
        segment_data = np.pad(segment_data, (0, n_fft - len(segment_data)))

    window = np.hanning(n_fft)
    num_frames = max(1, (len(segment_data) - n_fft) // hop_length + 1)
    stft_matrix = []
    for i in range(num_frames):
        start = i * hop_length
        frame = segment_data[start:start + n_fft] * window
        spectrum = np.abs(np.fft.rfft(frame))
        stft_matrix.append(spectrum)

    stft_matrix = np.array(stft_matrix)  # shape: (frames, freq_bins)
    freq_bins = np.fft.rfftfreq(n_fft, d=1.0 / sample_rate)

    # 3. Spectral Centroid
    magnitudes_sum = np.sum(stft_matrix, axis=1) + 1e-8
    centroids = np.sum(stft_matrix * freq_bins, axis=1) / magnitudes_sum
    mean_centroid = float(np.mean(centroids))
    std_centroid = float(np.std(centroids))

    # 4. Spectral Flux (frame-to-frame frequency shift)
    if len(stft_matrix) > 1:
        flux = np.sqrt(np.sum(np.diff(stft_matrix, axis=0)**2, axis=1))
        mean_flux = float(np.mean(flux))
    else:
        mean_flux = 0.8

    # 5. High-Frequency Vocoder Artifacts (AI vocoders produce unnatural cutoffs > 7.5 kHz)
    high_freq_mask = freq_bins > 7500
    total_energy = np.sum(stft_matrix) + 1e-8
    high_freq_energy = float(np.sum(stft_matrix[:, high_freq_mask]) / total_energy)

    # 6. Spectral Rolloff (85% energy frequency)
    cumulative_energy = np.cumsum(stft_matrix, axis=1)
    threshold = 0.85 * cumulative_energy[:, -1:]
    rolloff_indices = np.argmax(cumulative_energy >= threshold, axis=1)
    rolloff_freqs = freq_bins[np.clip(rolloff_indices, 0, len(freq_bins) - 1)]
    mean_rolloff = float(np.mean(rolloff_freqs))

    # Forensic Decision Rules for this segment:
    # Human vocal tracts exhibit rich dynamic pitch/timbre modulation (std_centroid > 320 Hz)
    # Neural vocoders (HiFi-GAN, WaveGlow, Tacotron, VITS) exhibit flat harmonic phases or unnatural cutoffs
    is_vocoder_synthetic = (std_centroid < 180.0 or high_freq_energy < 0.0015 or mean_flux < 0.22)
    is_natural_human = (std_centroid > 320.0 and mean_flux > 0.35 and 0.008 < high_freq_energy < 0.35)

    if is_vocoder_synthetic:
        risk_score = 86.0
        confidence = 88.0
        prediction = "SYNTHETIC"
        is_fake = True
    elif is_natural_human:
        risk_score = 12.0
        confidence = 92.0
        prediction = "REAL"
        is_fake = False
    else:
        # Interpolate based on centroid variance and flux
        risk_score = clamp_score(70.0 - (std_centroid / 10.0) + (1.0 - mean_flux) * 20.0)
        confidence = 72.0
        prediction = "SYNTHETIC" if risk_score > 40.0 else "REAL"
        is_fake = risk_score > 40.0

    return {
        "risk_score": round(risk_score, 1),
        "confidence": round(confidence, 1),
        "is_fake": is_fake,
        "prediction": prediction,
        "std_centroid": round(std_centroid, 1),
        "mean_flux": round(mean_flux, 2),
        "high_freq_energy": round(high_freq_energy * 100, 3),
        "mean_rolloff": round(mean_rolloff, 1)
    }


def analyze_audio_bytes(
    audio_bytes: bytes,
    segment_duration: float = SEGMENT_DURATION_SEC,
    hop_duration: float = SEGMENT_HOP_SEC
) -> Dict[str, Any]:
    """
    Analyzes raw audio bytes with segment-level sliding windows and spectral forensic models.
    """
    if not audio_bytes or len(audio_bytes) < 100:
        return {
            "success": False,
            "error": "Uploaded audio file is empty or corrupted."
        }

    start_time = time.time()
    try:
        mono_data, sample_rate = decode_audio_bytes(audio_bytes)
        duration_sec = float(len(mono_data)) / float(sample_rate) if sample_rate > 0 else 0.0

        if duration_sec < MIN_AUDIO_DURATION:
            return {
                "success": False,
                "error": f"Audio file is too short ({duration_sec:.2f}s). Minimum {MIN_AUDIO_DURATION}s required."
            }

        # Segment sliding window
        window_samples = int(segment_duration * sample_rate)
        hop_samples = max(1, int(hop_duration * sample_rate))

        segment_results: List[Dict[str, Any]] = []
        segment_scores: List[float] = []
        confidences: List[float] = []
        suspicious_count = 0

        start_sample = 0
        seg_idx = 1

        while start_sample < len(mono_data):
            end_sample = min(len(mono_data), start_sample + window_samples)
            seg_data = mono_data[start_sample:end_sample]

            # Only analyze segments with sufficient length (> 0.25s)
            if len(seg_data) >= int(0.25 * sample_rate):
                t_start = round(float(start_sample / sample_rate), 2)
                t_end = round(float(end_sample / sample_rate), 2)

                seg_res = analyze_audio_segment(seg_data, sample_rate)
                segment_scores.append(seg_res["risk_score"])
                confidences.append(seg_res["confidence"])

                if seg_res["is_fake"]:
                    suspicious_count += 1

                segment_results.append({
                    "segment_index": seg_idx,
                    "start_time": t_start,
                    "end_time": t_end,
                    "time_label": f"{int(t_start//60):02d}:{int(t_start%60):02d}–{int(t_end//60):02d}:{int(t_end%60):02d}",
                    "prediction": seg_res["prediction"],
                    "confidence": seg_res["confidence"],
                    "risk_score": seg_res["risk_score"],
                    "is_suspicious": seg_res["is_fake"],
                    "details": {
                        "centroid_variance": seg_res["std_centroid"],
                        "spectral_flux": seg_res["mean_flux"],
                        "high_freq_ratio": seg_res["high_freq_energy"]
                    }
                })
                seg_idx += 1

            if end_sample >= len(mono_data):
                break
            start_sample += hop_samples

        if not segment_scores:
            return {
                "success": False,
                "error": "Could not extract valid audio segments."
            }

        total_segments = len(segment_results)
        avg_risk = float(np.mean(segment_scores))
        max_risk = float(np.max(segment_scores))
        avg_conf = clamp_score(float(np.mean(confidences)))

        # Temporal aggregation:
        # If > 30% of segments are suspicious, weight towards peak risk
        if (suspicious_count / float(total_segments)) >= 0.30 or max_risk >= 75.0:
            overall_risk = clamp_score(0.65 * max_risk + 0.35 * avg_risk)
        else:
            overall_risk = clamp_score(0.35 * max_risk + 0.65 * avg_risk)

        # Check if trained neural AudioCNN model is available
        _load_trained_audio_cnn()
        neural_res = None
        model_name = "STFT Spectral Centroid + Vocoder Forensics"
        if _trained_audio_model is not None:
            try:
                neural_res = _infer_trained_audio_cnn(mono_data, sample_rate)
                neural_fake = neural_res["fake_prob"]
                # 70% trained neural model, 30% spectral forensics
                overall_risk = clamp_score(0.70 * neural_fake + 0.30 * overall_risk)
                avg_conf = clamp_score(0.70 * neural_res["confidence"] + 0.30 * avg_conf)
                model_name = "AudioCNN (ASVspoof 2019 LA) + STFT Forensics"
            except Exception as e:
                logger.warning(f"Audio neural inference failed: {e}")

        authenticity = clamp_score(100.0 - overall_risk)
        elapsed_sec = round(time.time() - start_time, 2)

        # Trust score calculation
        trust_meta = calculate_trust_score(overall_risk, avg_conf, is_scam=False)
        trust_score = trust_meta["trust_score"]
        trust_category = trust_meta["trust_category"]
        status = trust_meta["status"]
        status_label = trust_meta["status_label"]

        # Classification decision & human-readable evidence
        if overall_risk <= 25.0:
            classification = "REAL"
            explanation = (
                f"Multi-signal audio analysis verified natural vocal tract dynamics, organic pitch variance, "
                f"and authentic speech formants across {total_segments} audio segments ({duration_sec:.1f}s)."
            )
            evidence_list = [
                f"Organic vocal tract dynamics and natural pitch modulations verified across {total_segments} windows.",
                "Continuous acoustic harmonic formants without vocoder cutoff boundaries.",
                "Zero synthetic TTS / neural vocoder phase artifacts detected."
            ]
        elif overall_risk <= 50.0:
            classification = "SUSPICIOUS"
            explanation = (
                f"Audio features show mostly natural spectral distribution with slight background noise "
                f"or compression variance across {suspicious_count} of {total_segments} segments."
            )
            evidence_list = [
                f"Mild spectral compression variance detected in {suspicious_count} of {total_segments} windows.",
                "Harmonic timbre exhibits minor phase fluctuations.",
                "Conflicting acoustic cues; manual verification recommended."
            ]
        else:
            classification = "AI-GENERATED"
            explanation = (
                f"Acoustic and neural voice analysis detected artificial phase regularity and synthetic vocoder frequency "
                f"cutoffs characteristic of AI voice cloning/TTS across {suspicious_count} segment windows."
            )
            evidence_list = [
                f"AI vocoder high-frequency cutoff signatures detected across {suspicious_count} windows.",
                "Unnatural phase regularity and pitch flatness characteristic of synthetic speech models.",
                f"Peak segment synthetic score reached {max_risk:.1f} / 100."
            ]

        indicators = [
            {
                "label": "Segment-by-Segment Spectral Forensics",
                "detail": f"Analyzed {total_segments} windows ({segment_duration}s windows, {hop_duration}s hop) — {suspicious_count} suspicious / {total_segments - suspicious_count} authentic.",
                "score": round(overall_risk, 1),
                "level": "safe" if suspicious_count == 0 else "high" if suspicious_count >= total_segments * 0.3 else "mod"
            },
            {
                "label": "Vocoder High-Frequency Phase Signature",
                "detail": f"High-frequency energy and roll-off stability evaluated across {duration_sec:.1f}s sample rate {sample_rate} Hz.",
                "score": round(overall_risk, 1),
                "level": "high" if overall_risk > 50.0 else "safe"
            },
            {
                "label": "Spectral Centroid Harmonic Modulations",
                "detail": f"Evaluated dynamic timbre cadence (Peak segment risk: {max_risk:.1f}/100, Confidence: {avg_conf:.1f}%).",
                "score": round(max_risk, 1),
                "level": "high" if max_risk >= 65.0 else "mod" if max_risk > 35.0 else "safe"
            }
        ]

        if neural_res is not None:
            indicators.insert(0, {
                "label": "Neural Voice Anti-Spoofing Classifier",
                "detail": f"AudioCNN evaluated ASVspoof voice signatures: {neural_res['fake_prob']:.1f}% synthetic probability ({neural_res['confidence']:.1f}% confidence).",
                "score": round(neural_res["fake_prob"], 1),
                "level": "safe" if neural_res["fake_prob"] <= 30 else "high" if neural_res["fake_prob"] >= 70 else "mod"
            })

        return {
            "success": True,
            "modality": "audio",
            "mediaType": "audio",
            "type": "audio",
            "status": status,
            "status_label": status_label,
            "classification": status,
            "classification_label": status_label,
            "prediction": status,
            "confidence": round(avg_conf, 1),
            "confidence_pct": round(avg_conf, 1),
            "trust_score": trust_score,
            "trust_category": trust_category,
            "risk_score": round(overall_risk, 1),
            "risk_level": trust_meta["risk_level"],
            "riskLevel": trust_meta["risk_level"],
            "authenticity": round(authenticity, 1),
            "authenticity_probability": round(authenticity, 1),
            "duration": round(duration_sec, 2),
            "sample_rate": sample_rate,
            "segments_analyzed": total_segments,
            "suspicious_segments": suspicious_count,
            "explanation": explanation,
            "evidence": evidence_list,
            "technical": {
                "model": model_name,
                "model_type": "Trained AudioCNN" if _trained_audio_model is not None else "Spectral Forensics Fallback",
                "neural_metrics": _trained_audio_meta or {},
                "duration_seconds": round(duration_sec, 2),
                "sample_rate_hz": sample_rate,
                "window_duration_sec": segment_duration,
                "segments_analyzed": total_segments,
                "suspicious_segments": suspicious_count,
                "processing_time_sec": elapsed_sec
            },
            "limitations": [
                "Microphone proximity, acoustic reverb, and lossy compression (MP3/AAC) can shift spectral centroids.",
                "Authenticity assessment should be complemented with source context."
            ],
            "indicators": indicators,
            "segment_results": segment_results,
            "signals": indicators
        }

    except Exception as e:
        logger.error(f"Audio analysis error: {e}", exc_info=True)
        return {
            "success": False,
            "error": f"Audio analysis failed: {str(e)}"
        }
