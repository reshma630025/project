"""
Response formatting and score normalization utilities for TrustGuard AI.
Implements the Unified Trust Score (0–100), 5-category authenticity classification,
and transparent evidence/limitations schema.
"""
from typing import Dict, Any, List, Optional

def clamp_score(value: float) -> float:
    """Clamp score between 0.0 and 100.0 with float precision rounding."""
    try:
        val = float(value)
    except (TypeError, ValueError):
        return 0.0
    return round(max(0.0, min(100.0, val)), 1)


def authenticity_classification(fake_prob: float) -> dict:
    """Returns classification dictionary for backward compatibility."""
    score = clamp_score(fake_prob)
    if score <= 30.0:
        return {
            "label": "LIKELY GENUINE",
            "status": "safe",
            "classification": "LIKELY_GENUINE"
        }
    elif score < 70.0:
        return {
            "label": "UNCERTAIN — VERIFY MANUALLY",
            "status": "warning",
            "classification": "UNCERTAIN"
        }
    else:
        return {
            "label": "LIKELY FAKE / MANIPULATED",
            "status": "danger",
            "classification": "LIKELY_FAKE"
        }


def calculate_trust_score(fake_prob: float, confidence: float, is_scam: bool = False) -> Dict[str, Any]:
    """
    Computes unified Trust Score (0–100) and 5-tier Authenticity Classification.
    
    Higher Trust Score = Higher confidence that content is authentic / trustworthy.
    0–39   : LOW TRUST (Severe risk, AI-generated, manipulated, scam)
    40–69  : UNCERTAIN / REVIEW (Inconclusive, conflicting signals)
    70–89  : LIKELY TRUSTWORTHY (Strong authenticity markers, low risk)
    90–100 : HIGH TRUST (Verified authentic characteristics)
    """
    fp = clamp_score(fake_prob)
    conf = clamp_score(confidence)
    if conf <= 1.0 and conf > 0.0:
        conf = clamp_score(conf * 100.0)

    # 1. Authentic / Real Content (low fake probability <= 30%)
    if fp <= 30.0:
        # Trust score correlates directly with authenticity confidence
        trust_score = clamp_score(max(70.0, 100.0 - (fp * 0.8) - ((100.0 - conf) * 0.15)))
        status = "REAL"
        status_label = "LIKELY AUTHENTIC"
        risk_level = "Low Risk"
        theme = "safe"
        
        if trust_score >= 90.0:
            trust_category = "HIGH TRUST"
        else:
            trust_category = "LIKELY TRUSTWORTHY"

    # 2. AI-Generated / Manipulated / Scam (high fake probability >= 70%)
    elif fp >= 70.0:
        # Trust score is severely penalized by detected synthetic / scam signals
        trust_score = clamp_score(max(2.0, (100.0 - fp) * 0.6))
        status = "AI-GENERATED" if not is_scam else "SCAM-LIKELY"
        status_label = "AI-GENERATED CONTENT" if not is_scam else "HIGH RISK / SCAM DETECTED"
        risk_level = "Critical Risk" if fp >= 88.0 else "High Risk"
        trust_category = "LOW TRUST"
        theme = "danger"

    # 3. Suspicious / Borderline (fake probability 51% to 69%)
    elif fp > 50.0:
        trust_score = clamp_score(max(30.0, min(48.0, 100.0 - fp)))
        status = "SUSPICIOUS"
        status_label = "SUSPICIOUS CONTENT"
        risk_level = "Moderate Risk"
        trust_category = "UNCERTAIN / REVIEW"
        theme = "warn"

    # 4. Uncertain / Inconclusive (fake probability 31% to 50%)
    else:
        trust_score = clamp_score(50.0 + (50.0 - fp) * 0.3)
        status = "UNCERTAIN"
        status_label = "UNCERTAIN — REQUIRES REVIEW"
        risk_level = "Inconclusive"
        trust_category = "UNCERTAIN / REVIEW"
        theme = "neutral"

    return {
        "trust_score": trust_score,
        "trust_category": trust_category,
        "status": status,
        "status_label": status_label,
        "risk_level": risk_level,
        "theme": theme,
        "confidence": conf
    }


def normalize_fake_probability(probabilities: dict, id2label: dict) -> float:
    """
    Explicitly normalizes model class probabilities into a single `fakeProbability` score (0.0 to 100.0).
    0   = very likely genuine / real
    100 = very likely fake / synthetic / manipulated
    """
    if not probabilities:
        return 50.0

    prob_lookup = {}
    for k, v in probabilities.items():
        prob_lookup[str(k).strip().lower()] = float(v)

    fake_val = None
    real_val = None

    for k, v in prob_lookup.items():
        if any(term in k for term in ["fake", "synthetic", "manipulated", "generated", "deepfake"]):
            fake_val = v
        elif any(term in k for term in ["real", "genuine", "authentic", "human", "original"]):
            real_val = v

    if fake_val is not None:
        return clamp_score(fake_val * 100.0)
    if real_val is not None:
        return clamp_score((1.0 - real_val) * 100.0)

    if id2label:
        for class_id, label_name in id2label.items():
            lbl = str(label_name).strip().lower()
            cid = str(class_id).strip().lower()
            score = prob_lookup.get(cid, prob_lookup.get(lbl, 0.0))

            if any(term in lbl for term in ["fake", "synthetic", "manipulated", "generated", "deepfake"]):
                return clamp_score(score * 100.0)
            elif any(term in lbl for term in ["real", "genuine", "authentic", "human", "original"]):
                return clamp_score((1.0 - score) * 100.0)

    return 50.0


def build_unified_result(
    modality: str,
    status: str,
    status_label: str,
    confidence: float,
    trust_score: float,
    trust_category: str,
    explanation: str,
    evidence: List[str],
    technical: Dict[str, Any],
    limitations: Optional[List[str]] = None,
    extra: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Constructs the standard 6-part transparent analysis result schema.
    """
    default_limits = [
        "AI detection is probabilistic and may produce false positives or false negatives.",
        "Assess content alongside verifiable provenance and independent sources."
    ]
    
    res = {
        "success": True,
        "modality": modality,
        "status": status,
        "status_label": status_label,
        "classification": status,
        "confidence": clamp_score(confidence),
        "confidence_pct": clamp_score(confidence),
        "trust_score": clamp_score(trust_score),
        "trust_category": trust_category,
        "risk_score": clamp_score(100.0 - trust_score),
        "explanation": explanation,
        "evidence": evidence,
        "technical": technical,
        "limitations": limitations or default_limits
    }
    if extra:
        res.update(extra)
    return res
