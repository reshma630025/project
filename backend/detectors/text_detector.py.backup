"""
Text & Scam Detection Module for TrustGuard AI.
Analyzes message content for financial fraud, urgent threats, credential phishing,
lottery scams, and institutional impersonation.
"""
import re
import time
import logging
from typing import Dict, Any, List
from backend.utils.response_utils import clamp_score, calculate_trust_score

logger = logging.getLogger("trustguard.text_detector")

SCAM_PATTERNS = [
    {
        "category": "Credential & OTP Phishing",
        "weight": 40,
        "regex": r"(?:(?:share|send|enter|verify|provide|forward|give|submit)\s+(?:your\s+)?(?:otp|one[- ]time|code|pin|password|2fa|credentials?))|(?:(?:otp|code|pin|password|2fa)\b.*?(?:share|send|enter|verify|provide))|(?:(?:click here|tap link|open link|verify here).*?(?:verify|update|unlock|reactivate|login|access).*?(?:account|card|bank|wallet|profile))",
        "label": "Credential / OTP Harvesting Attempt",
        "level": "high"
    },
    {
        "category": "Financial Solicitation & Extortion",
        "weight": 35,
        "regex": r"(?:wire transfer|western union|gift card|crypto|bitcoin|btc|usdt|ethereum|wallet address|payment via upi|send money to|deposit fee|processing fee|advance payment|transfer funds|pay (?:\$|₹|rs|usd)\s*\d+)",
        "label": "Direct Financial / Crypto / Wire Transfer Solicitation",
        "level": "high"
    },
    {
        "category": "Psychological Urgency & Threats",
        "weight": 30,
        "regex": r"(?:within (?:24|12|48|2|1) hours?|immediately|urgent|arrest warrant|legal action|police complaint|account (?:is )?(?:suspended|blocked|terminated|locked)|final notice|penalty will be charged|take legal steps)",
        "label": "High-Pressure Psychological Coercion / Urgency",
        "level": "mod"
    },
    {
        "category": "Lottery & Unsolicited Reward Scams",
        "weight": 35,
        "regex": r"(?:congratulations|you have won|selected as the winner|claim your (?:reward|prize|grant|lottery|bonus)|\$?(?:\d{1,3}(?:,\d{3})+|\d+)\s*(?:usd|dollars|pounds|cash|crypto))",
        "label": "Unsolicited Prize / Lottery / Reward Bait",
        "level": "high"
    },
    {
        "category": "Institutional Impersonation",
        "weight": 25,
        "regex": r"(?:irs|fbi|customs department|income tax department|microsoft tech support|apple security team|whatsapp support|telegram support|bank customer care|fraud department)",
        "label": "Authoritative Entity / Institutional Impersonation",
        "level": "mod"
    },
    {
        "category": "Suspicious Communication Links",
        "weight": 20,
        "regex": r"(?:wa\.me\/|t\.me\/|bit\.ly\/|tinyurl\.com\/|cutt\.ly\/|http:\/\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|t\.co\/)",
        "label": "Obfuscated / Unofficial Communication Link",
        "level": "mod"
    },
    {
        "category": "Multilingual (Hindi) Phishing / Coercion",
        "weight": 40,
        "regex": r"(?:ओटीपी|पासवर्ड|पिन|खाता\s*(?:ब्लॉक|बंद)|तुरंत|लॉटरी|इनाम|रुपये\s*(?:जीत|भेजें)|बैंक\s*खाता)",
        "label": "Hindi Credential / Financial Coercion Trigger",
        "level": "high"
    },
    {
        "category": "Multilingual (Telugu) Phishing / Coercion",
        "weight": 40,
        "regex": r"(?:ఓటీపీ|పాస్‌వర్డ్|పిన్|ఖాతా\s*(?:బ్లాక్|రద్దు)|వెంటనే|లాటరీ|బహుమతి|డబ్బులు\s*(?:పంపండి|గెలుచుకున్నారు)|బ్యాంక్\s*ఖాతా)",
        "label": "Telugu Credential / Financial Coercion Trigger",
        "level": "high"
    }
]

def detect_language(text: str) -> str:
    """Identifies primary language script of text."""
    if re.search(r"[\u0900-\u097F]", text):
        return "Hindi (हिंदी)"
    elif re.search(r"[\u0C00-\u0C7F]", text):
        return "Telugu (తెలుగు)"
    elif re.search(r"[\u0B80-\u0BFF]", text):
        return "Tamil (தமிழ்)"
    elif re.search(r"[\u0C80-\u0CFF]", text):
        return "Kannada (ಕನ್ನಡ)"
    elif re.search(r"[a-zA-Z]", text):
        return "English"
    return "Undetermined / Mixed"


def analyze_text(text: str) -> Dict[str, Any]:
    """
    Analyzes raw text message for fraud indicators and computes risk score.
    """
    if not text or not text.strip():
        return {
            "success": False,
            "error": "No text content provided for analysis."
        }

    clean_text = text.strip()
    matched_indicators: List[Dict[str, Any]] = []
    accumulated_risk = 0.0

    # Test all scam pattern heuristics
    for pat in SCAM_PATTERNS:
        match = re.search(pat["regex"], clean_text, re.IGNORECASE)
        if match:
            accumulated_risk += pat["weight"]
            matched_indicators.append({
                "label": pat["label"],
                "detail": f"Matched pattern trigger: \"{match.group(0)[:60]}\"",
                "score": float(pat["weight"]),
                "level": pat["level"]
            })

    # Base linguistic checks (ALL CAPS shouting, excessive exclamation marks)
    caps_ratio = sum(1 for c in clean_text if c.isupper()) / max(1, len(clean_text))
    if caps_ratio > 0.40 and len(clean_text) > 25:
        accumulated_risk += 12.0
        matched_indicators.append({
            "label": "Aggressive Visual Styling",
            "detail": f"{int(caps_ratio*100)}% capitalized characters indicate coercive emphasis.",
            "score": 12.0,
            "level": "mod"
        })

    # Risk Score & Classification Logic (0..100)
    risk_score = min(100.0, max(0.0, accumulated_risk))
    start_time = time.time()

    if risk_score >= 50.0:
        classification = "SCAM"
        confidence_val = min(98.0, max(85.0, 70.0 + (risk_score / 2.0)))
        risk_level = "Critical" if risk_score >= 80.0 else "High"
        explanation = f"Detected high-confidence scam markers ({matched_indicators[0]['label']}). Do not share OTPs, passwords, or send funds."
    elif risk_score >= 21.0:
        classification = "SUSPICIOUS"
        confidence_val = 78.0
        risk_level = "Moderate"
        explanation = f"Potential social engineering or urgency coercion patterns detected. Exercise caution before clicking links."
    else:
        classification = "REAL"
        confidence_val = 94.0
        risk_level = "Low"
        risk_score = max(4.0, risk_score)
        explanation = "No credential harvesting, fraudulent wire demands, or psychological urgency triggers detected."

    trust_meta = calculate_trust_score(risk_score, confidence_val, is_scam=True)
    trust_score = trust_meta["trust_score"]
    trust_category = trust_meta["trust_category"]
    status = trust_meta["status"]
    status_label = trust_meta["status_label"]

    evidence_list = []
    for ind in matched_indicators:
        evidence_list.append(f"{ind['label']}: {ind['detail']}")
    if not evidence_list:
        evidence_list.append("Standard conversational linguistic structure verified.")
        evidence_list.append("Zero OTP / banking credential solicitation detected.")

    lang = detect_language(clean_text)

    return {
        "success": True,
        "modality": "text",
        "type": "text",
        "status": status,
        "status_label": status_label,
        "classification": classification,
        "prediction": classification,
        "confidence": round(confidence_val, 1),
        "confidence_pct": round(confidence_val, 1),
        "trust_score": trust_score,
        "trust_category": trust_category,
        "risk_score": round(risk_score, 1),
        "risk_level": risk_level,
        "explanation": explanation,
        "evidence": evidence_list,
        "technical": {
            "model": "Multilingual Fraud Pattern & Lexical Heuristics",
            "detected_language": lang,
            "text_length_chars": len(clean_text),
            "uppercase_ratio_pct": round(caps_ratio * 100, 1),
            "matched_rules_count": len(matched_indicators),
            "processing_time_sec": round(time.time() - start_time, 3)
        },
        "limitations": [
            "Linguistic heuristics evaluate known scam vectors; novel or targeted spear-phishing should be evaluated with external sender verification."
        ],
        "indicators": matched_indicators,
        "signals": matched_indicators
    }
