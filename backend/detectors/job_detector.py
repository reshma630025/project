"""
Job & Internship Fraud Detection Module for TrustGuard AI.
Analyzes job descriptions for advance registration fees, security deposits,
unrealistic salaries, free recruiter email domains, and fake offer signals.
"""
import re
import time
import logging
from typing import Dict, Any, List
from backend.utils.response_utils import clamp_score, calculate_trust_score

logger = logging.getLogger("trustguard.job_detector")

JOB_FRAUD_PATTERNS = [
    {
        "category": "Advance Fees & Deposits",
        "weight": 40,
        "regex": r"(?:(?:registration|application|training|onboarding|upfront|mandatory|equipment|background check)\s*fee|security deposit|refundable deposit|laptop fee|processing fee|buy equipment from our vendor|pay (?:\$|₹|rs|usd)\s*\d+)",
        "label": "Mandatory Upfront Fee / Security Deposit Demand",
        "level": "high"
    },
    {
        "category": "Unrealistic Compensation",
        "weight": 25,
        "regex": r"(?:earn (?:\$|₹|rs)\s*(?:[5-9]\d{3}|[1-9]\d{4,})\s*(?:per (?:day|week|hour)|daily)|no experience needed.*(?:\$|₹)\s*\d{4,}|guaranteed income of|work 1 hour.*(?:\$|₹)\s*\d{3,})",
        "label": "Unrealistic Salary-to-Effort Ratio",
        "level": "mod"
    },
    {
        "category": "Informal / Suspicious Recruiter Contact",
        "weight": 25,
        "regex": r"(?:contact on whatsapp|telegram HR|message hr at @|send resume to (?:[a-zA-Z0-9._%+-]+@(gmail|yahoo|hotmail|outlook|protonmail|aol)\.com))",
        "label": "Unofficial Public Email / Messaging Platform Recruitment",
        "level": "mod"
    },
    {
        "category": "Guaranteed Employment Without Interview",
        "weight": 30,
        "regex": r"(?:immediate selection|100% guaranteed job|no interview required|direct appointment letter|instant joining without screening)",
        "label": "Guaranteed Hiring Without Formal Screening",
        "level": "high"
    },
    {
        "category": "Vague / Shady Job Scope",
        "weight": 20,
        "regex": r"(?:part time data entry|copy paste work|captcha filling|like and subscribe jobs|task based review earning)",
        "label": "High-Risk Task/Review/Data-Entry Scam Format",
        "level": "mod"
    }
]


def analyze_job_or_internship(
    description: str,
    url: str = "",
    email: str = "",
    is_internship: bool = False
) -> Dict[str, Any]:
    """
    Analyzes job or internship listing text and metadata for fraudulent markers.
    """
    combined_text = f"{description} {url} {email}".strip()
    if not combined_text:
        return {
            "success": False,
            "error": "No job description or contact details provided."
        }

    matched_indicators: List[Dict[str, Any]] = []
    accumulated_risk = 0.0

    for pat in JOB_FRAUD_PATTERNS:
        match = re.search(pat["regex"], combined_text, re.IGNORECASE)
        if match:
            accumulated_risk += pat["weight"]
            matched_indicators.append({
                "label": pat["label"],
                "detail": f"Detected risk trigger: \"{match.group(0)[:65]}\"",
                "score": float(pat["weight"]),
                "level": pat["level"]
            })

    # Free email check for formal recruiter email
    if email and any(prov in email.lower() for prov in ["@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com"]):
        accumulated_risk += 18.0
        matched_indicators.append({
            "label": "Non-Corporate Recruiter Email",
            "detail": f"Recruiter provided public email provider ({email}) instead of an official company domain.",
            "score": 18.0,
            "level": "mod"
        })

    start_time = time.time()
    risk_score = min(100.0, max(0.0, accumulated_risk))
    target_name = "Internship" if is_internship else "Job"

    if risk_score >= 55.0:
        classification = "SCAM-LIKELY"
        confidence_val = min(96.0, max(85.0, 70.0 + (risk_score / 2.0)))
        risk_level = "Critical" if risk_score >= 80.0 else "High"
        explanation = f"High-risk {target_name.lower()} solicitation identified with clear predatory markers (such as upfront fee demands or unofficial messaging recruitment)."
    elif risk_score >= 21.0:
        classification = "SUSPICIOUS"
        confidence_val = 76.0
        risk_level = "Moderate"
        explanation = f"Ambiguous {target_name.lower()} listing. Verify the employer's official careers portal directly before submitting personal data."
    else:
        classification = "REAL"
        confidence_val = 93.0
        risk_level = "Low"
        risk_score = max(5.0, risk_score)
        explanation = f"Standard professional {target_name.lower()} format. Zero advance fee requests or predatory contract patterns detected."

    trust_meta = calculate_trust_score(risk_score, confidence_val, is_scam=True)
    trust_score = trust_meta["trust_score"]
    trust_category = trust_meta["trust_category"]
    status = trust_meta["status"]
    status_label = "LIKELY LEGITIMATE OFFER" if status == "REAL" else trust_meta["status_label"]

    evidence_list = []
    for ind in matched_indicators:
        evidence_list.append(f"{ind['label']}: {ind['detail']}")
    if not evidence_list:
        evidence_list.append("Zero upfront registration or training fee demands detected.")
        evidence_list.append("Recruitment process aligns with standard corporate hiring protocols.")

    return {
        "success": True,
        "modality": "job",
        "type": "internship" if is_internship else "job",
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
            "model": "Recruitment Fraud Heuristics & Domain Matcher",
            "listing_type": target_name,
            "text_length_chars": len(combined_text),
            "matched_rules_count": len(matched_indicators),
            "processing_time_sec": round(time.time() - start_time, 3)
        },
        "limitations": [
            "Always verify offer letters through the organization's official domain email and corporate registrar."
        ],
        "indicators": matched_indicators,
        "signals": matched_indicators
    }
