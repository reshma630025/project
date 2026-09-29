"""
TrustGuard AI — Cybersecurity & Fraud Analysis Assistant Engine
Provides contextual fraud analysis, deepfake verification guidance, and actionable security recommendations.
"""

import time
import re
from typing import Dict, Any, Optional, List
from backend.utils.history_db import get_scan_by_id, get_stats

# Curated knowledge base patterns for cybersecurity fraud detection
FRAUD_PATTERNS = [
    {
        "keywords": ["voice", "audio", "call", "cloned", "voice clone", "mimic", "phone"],
        "category": "Voice Cloning & Audio Deepfakes",
        "threat_level": "HIGH",
        "guidance": (
            "Modern generative voice clones require only 3–5 seconds of sample audio. "
            "To verify an urgent or suspicious caller claiming to be a family member, colleague, or executive: "
            "1. Hang up immediately and call back using a trusted, verified contact number. "
            "2. Establish an out-of-band mutual passphrase that AI voice synthesizers cannot anticipate. "
            "3. Listen for unnatural cadence, metallic vocoder frequency cutoffs, or absence of breathing sounds."
        ),
        "actions": [
            "Initiate a callback on a known verified phone number.",
            "Ask a private question only the real individual could answer.",
            "Never transfer funds or provide 2FA codes over an incoming voice call."
        ]
    },
    {
        "keywords": ["video", "face", "zoom", "teams", "webcam", "deepfake video", "glitch"],
        "category": "Video & Face Synthesis Deepfakes",
        "threat_level": "HIGH",
        "guidance": (
            "Real-time video deepfakes often reveal visual seams during side-profile movement or lighting changes. "
            "Verification techniques for live video calls: "
            "1. Ask the participant to turn their head 90 degrees or pass a hand across their face; "
            "real-time GAN/diffusion overlays frequently blur or distort around fingers and jawlines. "
            "2. Inspect earlobe alignment, eye blink cadence, and teeth consistency. "
            "3. Verify through a secondary authenticated corporate channel."
        ),
        "actions": [
            "Request the participant to wave their hand in front of their face.",
            "Check for unnatural edge blur around hair, collars, and spectacles.",
            "Confirm identity via corporate directory or multi-factor authentication challenge."
        ]
    },
    {
        "keywords": ["job", "offer", "interview", "telegram", "whatsapp", "hr", "recruiter", "upfront", "equipment"],
        "category": "Employment & Internship Fraud",
        "threat_level": "CRITICAL",
        "guidance": (
            "Employment scams frequently solicit immediate interviews via unverified messaging apps (Telegram, Signal, WhatsApp) "
            "and offer above-market compensation without video or technical evaluation. "
            "Crucial red flags include requests for advance equipment fees, fake check reimbursements, "
            "or sending sensitive PII/banking details before formal onboarding contracts are signed."
        ),
        "actions": [
            "Verify the recruiter on LinkedIn and directly contact the official corporate HR desk.",
            "Check that emails originate from the company's official registered domain, not generic webmail (Gmail/Hotmail).",
            "Never deposit checks sent for 'home office equipment setup'."
        ]
    },
    {
        "keywords": ["url", "link", "domain", "phish", "typo", "login", "reset", "password", "bank"],
        "category": "Phishing & Malicious Domains",
        "threat_level": "HIGH",
        "guidance": (
            "Phishing URLs utilize typosquatting, IDN homograph characters (Cyrillic lookalikes), "
            "and subdomain trickery (e.g., login.bank.com-verify.security) to harvest credentials. "
            "Always inspect the apex domain (the last two segments before the first forward slash) "
            "and look for EV SSL certificates matching the exact legal entity."
        ),
        "actions": [
            "Do not click links inside unsolicited emails or SMS alerts.",
            "Navigate directly to the service by typing the official URL into your browser.",
            "Check the URL with TrustGuard's URL Scanner module for domain reputation and age."
        ]
    },
    {
        "keywords": ["otp", "code", "pin", "verify", "2fa", "mfa", "sms"],
        "category": "Credential & OTP Interception",
        "threat_level": "CRITICAL",
        "guidance": (
            "No legitimate bank, employer, or service will EVER ask you to read back or text an SMS One-Time Passcode. "
            "Any prompt requesting your 2FA code is an active session takeover or account recovery attempt."
        ),
        "actions": [
            "Never disclose 2FA or OTP codes to any caller, chatbot, or email recipient.",
            "If an unexpected OTP arrives, assume credentials have been compromised and change your password immediately.",
            "Migrate from SMS OTP to hardware security keys (FIDO2/WebAuthn) or authenticator apps."
        ]
    },
    {
        "keywords": ["crypto", "investment", "guaranteed", "returns", "wallet", "binance", "deposit"],
        "category": "Crypto & High-Yield Investment Fraud",
        "threat_level": "CRITICAL",
        "guidance": (
            "Guaranteed returns in cryptocurrency or forex trading do not exist. Fraudulent platforms display "
            "fabricated trading dashboards showing rapid profit accumulation, but block withdrawals while demanding "
            "'taxes', 'liquidity fees', or 'insurance deposits' before funds can be released."
        ),
        "actions": [
            "Cease all additional transfers to the platform immediately.",
            "Check the regulatory registry (SEC, FCA, FinCEN) to see if the platform is licensed.",
            "Report fraudulent wallet addresses to law enforcement and blockchain analytics platforms."
        ]
    }
]

def analyze_assistant_query(
    query: str,
    context_scan_id: Optional[int] = None,
    context_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Processes an end-user query with cybersecurity intelligence and optional scan context.
    """
    q_lower = query.lower().strip()
    
    # 1. Inspect scan context if provided
    scan_context_info = None
    if context_scan_id:
        scan = get_scan_by_id(context_scan_id)
        if scan:
            scan_context_info = {
                "scan_id": scan["id"],
                "scan_type": scan["scan_type"],
                "classification": scan["classification"],
                "trust_score": scan["trust_score"],
                "risk_score": scan["risk_score"],
                "content_label": scan["content_label"],
                "explanation": scan.get("explanation", "")
            }
    elif context_data and isinstance(context_data, dict):
        scan_context_info = {
            "scan_id": context_data.get("id") or context_data.get("scanId") or 1,
            "scan_type": context_data.get("contentType") or context_data.get("scan_type") or "asset",
            "classification": context_data.get("classification") or ("SUSPICIOUS" if float(context_data.get("score", 0)) > 50 else "AUTHENTIC"),
            "trust_score": context_data.get("trustScore") or context_data.get("trust_score") or (100 - int(context_data.get("score", 0))),
            "risk_score": context_data.get("score") or context_data.get("risk_score", 0),
            "content_label": context_data.get("contentLabel") or context_data.get("contentType", "Asset Scan"),
            "explanation": context_data.get("explanation") or ("; ".join([i.get("detail", i.get("label", "")) for i in context_data.get("indicators", [])]))
        }

    # 2. Pattern match query against cybersecurity threat knowledge base
    best_match = None
    max_score = 0
    for pat in FRAUD_PATTERNS:
        score = sum(1 for kw in pat["keywords"] if kw in q_lower)
        if score > max_score:
            max_score = score
            best_match = pat

    # 3. Generate response
    if scan_context_info:
        # Contextual response referring to specific scan
        stype = scan_context_info["scan_type"].upper()
        sclass = scan_context_info["classification"]
        srisk = scan_context_info["risk_score"]
        strust = scan_context_info["trust_score"]

        intro = (
            f"Reviewing your Scan #{scan_context_info['scan_id']} ({stype} - {scan_context_info['content_label']}): "
            f"The detection engine classified this asset as **{sclass}** with a Trust Score of **{strust}/100** "
            f"and Risk Score of **{srisk}/100**.\n\n"
        )
        
        if srisk > 50.0:
            assessment = (
                "**Urgent Security Assessment**: Significant synthetic artifacts or fraud indicators were detected. "
                "Do NOT trust this content, authorize financial disbursements, or release credentials based on it."
            )
            threat_level = "CRITICAL" if srisk > 75.0 else "HIGH"
        elif srisk > 25.0:
            assessment = (
                "**Moderate Caution Advised**: Mixed or borderline signals were detected. "
                "The asset contains compression or spectral variations that warrant secondary out-of-band verification."
            )
            threat_level = "MODERATE"
        else:
            assessment = (
                "**Verified Authentic**: Sensor noise, acoustic dynamics, and forensic signatures are consistent with organic media. "
                "Risk is minimal, though standard operational security practices still apply."
            )
            threat_level = "LOW"

        if best_match:
            reply = f"{intro}{assessment}\n\n**Cybersecurity Guidance ({best_match['category']})**:\n{best_match['guidance']}"
            actions = best_match["actions"]
        else:
            reply = f"{intro}{assessment}\n\n**Technical Details**: {scan_context_info['explanation']}"
            actions = [
                "Preserve original file metadata for forensic chain-of-custody.",
                "Cross-verify identity using out-of-band communication.",
                "Report confirmed threats to security operations."
            ]

        confidence = 94.0

    elif best_match and max_score > 0:
        reply = (
            f"**TrustGuard Intelligence — {best_match['category']}**\n\n"
            f"{best_match['guidance']}"
        )
        threat_level = best_match["threat_level"]
        actions = best_match["actions"]
        confidence = 91.0

    else:
        # General guidance
        stats = get_stats()
        reply = (
            "I am TrustGuard AI's Cybersecurity & Threat Intelligence Assistant. "
            "I can analyze deepfakes, synthetic voices, phishing links, job scams, and social media fraud.\n\n"
            f"Our platform has processed **{stats.get('total_scans', 0)} scans** with an average trust score of "
            f"**{stats.get('average_trust_score', 85.0)}/100**.\n\n"
            "You can upload any file to our detectors or ask questions like:\n"
            "• *'How do I detect an AI-cloned voice on a phone call?'*\n"
            "• *'What are the signs of a fake Zoom job interview?'*\n"
            "• *'How can I verify if an urgent wire transfer request is legitimate?'*"
        )
        threat_level = "INFO"
        actions = [
            "Run an asset through TrustGuard's multimodal detectors.",
            "Verify caller identity through out-of-band channels.",
            "Enable hardware-backed multi-factor authentication on all accounts."
        ]
        confidence = 88.0

    return {
        "success": True,
        "query": query,
        "reply": reply,
        "answer": reply,
        "threat_level": threat_level,
        "confidence": confidence,
        "category": best_match["category"] if best_match else "General Threat Advisory",
        "suggested_actions": actions,
        "context_scan": scan_context_info,
        "timestamp": time.time()
    }
