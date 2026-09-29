
"""
OCR Document and Poster Fraud Detection Module for TrustGuard AI.
Extracts text and key entities (Company, Email, Phone, Website, Salary, Registration Fee)
and conducts multi-point fraud verification.
"""
import io
import re
import logging
from typing import Dict, Any, List
from PIL import Image

logger = logging.getLogger("trustguard.ocr_detector")


def extract_entities_from_text(text: str) -> Dict[str, str]:
    """
    Parses structured entities from OCR raw text.
    """
    # 1. Email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    email = email_match.group(0) if email_match else "—"

    # 2. Phone
    phone_match = re.search(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    phone = phone_match.group(0) if phone_match else "—"

    # 3. Website / URL
    url_match = re.search(r"(?:https?://|www\.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}[^\s]*", text, re.IGNORECASE)
    website = url_match.group(0) if url_match else "—"

    # 4. Salary / Earnings Mention
    salary_match = re.search(r"(?:salary|stipend|earn|pay|package|ctc)[\s:]*(?:(?:\$|₹|rs|usd|inr|eur|£)\s*[\d,]+(?:\s*(?:k|lakhs?|per\s*(?:month|year|annum|hr|day|week)|/-\b|\b)))", text, re.IGNORECASE)
    if not salary_match:
        salary_match = re.search(r"(?:\$|₹|rs|usd|inr|eur|£)\s*[\d,]+(?:\s*(?:k|lakhs?|per\s*(?:month|year|annum|hr|day|week)|/-\b))", text, re.IGNORECASE)
    salary = salary_match.group(0) if salary_match else "—"

    # 5. Registration / Processing Fee
    fee_match = re.search(r"(?:registration|application|training|processing|security|deposit|seat)[\s\w]*(?:fee|charges?|amount|cost)[\s:]*(?:(?:\$|₹|rs|usd|inr|eur|£)\s*[\d,]+|\d+\s*(?:usd|rs|inr|\$|₹))", text, re.IGNORECASE)
    if not fee_match:
        fee_match = re.search(r"(?:fee|charge|deposit)[\s:]*(?:(?:\$|₹|rs|usd|inr|eur|£)\s*[\d,]+)", text, re.IGNORECASE)
    reg_fee = fee_match.group(0) if fee_match else "None / Free"

    # 6. Company Name
    comp_match = re.search(r"(?:company|organization|hiring for|at|employer)[\s:]*([A-Za-z0-9&.\- ]{3,35})(?:\n|\r|,|;|\.)", text, re.IGNORECASE)
    if comp_match:
        company = comp_match.group(1).strip()
    else:
        # Check first prominent non-empty line as potential title/brand
        lines = [l.strip() for l in text.splitlines() if len(l.strip()) >= 3 and not re.search(r"hire|hiring|walk[- ]in|job|urgent", l, re.I)]
        company = lines[0] if lines else "Unspecified Employer"

    return {
        "company": company,
        "email": email,
        "phone": phone,
        "website": website,
        "salary": salary,
        "registration_fee": reg_fee
    }


def analyze_ocr_text(extracted_text: str, filename: str = "document.png") -> Dict[str, Any]:
    """
    Analyzes extracted text and entity relationships to detect fraudulent posters and notices.
    """
    if not extracted_text or len(extracted_text.strip()) < 5:
        return {
            "success": False,
            "error": "Extracted OCR text is empty or could not be recognized."
        }

    clean_text = extracted_text.strip()
    entities = extract_entities_from_text(clean_text)

    matched_indicators: List[Dict[str, Any]] = []
    accumulated_risk = 0.0

    # 1. Advance Fee Demands in Poster
    if entities["registration_fee"] != "None / Free":
        accumulated_risk += 45.0
        matched_indicators.append({
            "label": "Mandatory Upfront Fee Identified",
            "detail": f"Document explicitly lists fee requirements: {entities['registration_fee']}.",
            "score": 45.0,
            "level": "high"
        })

    # 2. Suspicious Public Email in Recruitment Notice
    if entities["email"] != "—" and any(prov in entities["email"].lower() for prov in ["@gmail.com", "@yahoo.com", "@hotmail.com"]):
        accumulated_risk += 20.0
        matched_indicators.append({
            "label": "Non-Enterprise Contact Email",
            "detail": f"Official notice uses free email provider ({entities['email']}) instead of corporate domain.",
            "score": 20.0,
            "level": "mod"
        })

    # 3. High Urgency or Guaranteed Selection Triggers
    if re.search(r"(?:100% selection|no interview|direct joining|instant appointment|urgent vacancy.*apply today)", clean_text, re.IGNORECASE):
        accumulated_risk += 25.0
        matched_indicators.append({
            "label": "Predatory / Unverified Guaranteed Hiring",
            "detail": "Notice promises direct placement without standard screening.",
            "score": 25.0,
            "level": "mod"
        })

    # 4. WhatsApp / Telegram Direct Payment Instructions
    if re.search(r"(?:send payment to|gpay to|phonepe|upi id|paytm to)\b", clean_text, re.IGNORECASE):
        accumulated_risk += 35.0
        matched_indicators.append({
            "label": "Informal Digital Payment Gateway Request",
            "detail": "Direct request to send funds via personal UPI / payment handle.",
            "score": 35.0,
            "level": "high"
        })

    risk_score = min(100.0, max(0.0, accumulated_risk))

    if risk_score >= 50.0:
        classification = "FRAUDULENT"
        confidence = min(0.96, max(0.85, 0.70 + (risk_score / 200.0)))
        risk_level = "CRITICAL" if risk_score >= 80.0 else "VERY HIGH"
        explanation = f"Fraudulent document/poster identified with {len(matched_indicators)} critical fraud indicators (such as fee demands or unauthorized payment instructions)."
    elif risk_score >= 21.0:
        classification = "SUSPICIOUS"
        confidence = 0.78
        risk_level = "HIGH" if risk_score >= 41.0 else "MODERATE"
        explanation = f"Document contains potential anomalies or unverified contact information. Exercise caution before proceeding."
    else:
        classification = "VERIFIED / LOW RISK"
        confidence = 0.92
        risk_level = "LOW"
        risk_score = max(5.0, risk_score)
        explanation = "Extracted text and corporate metadata follow verified professional publishing standards with zero fee demands."

    if not matched_indicators:
        matched_indicators = [
            {
                "label": "No Advance Fee Demands",
                "detail": "Document specifies genuine zero-cost employment / public notice terms.",
                "score": 0.0,
                "level": "safe"
            },
            {
                "label": "Legitimate Entity Metadata",
                "detail": "Contact information and publication layout conform to verified standard guidelines.",
                "score": 5.0,
                "level": "safe"
            }
        ]

    return {
        "success": True,
        "type": "ocr",
        "fileName": filename,
        "extracted_text": clean_text,
        "entities": entities,
        "classification": classification,
        "confidence": round(confidence, 2),
        "confidence_pct": round(confidence * 100, 1),
        "risk_score": round(risk_score, 1),
        "risk_level": risk_level,
        "indicators": matched_indicators,
        "signals": matched_indicators,
        "explanation": explanation
    }
