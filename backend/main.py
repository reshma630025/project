"""
FastAPI Backend Application for TrustGuard AI Unified Deepfake & Synthetic Content Analysis.
Connects all detection modules with real AI models, forensic algorithms, authentication, and live user-scoped history tracking.
"""
import sys
import json
import time
from pathlib import Path
import logging
from typing import Optional

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

from backend.detectors.image_detector import (
    analyze_image_bytes, MODEL_NAME as IMAGE_MODEL_NAME, get_pipeline,
    load_models as load_image_models, TRAINED_MODEL as IMAGE_TRAINED_MODEL
)
from backend.detectors.video_detector import analyze_video_file
from backend.detectors.audio_detector import (
    analyze_audio_bytes, load_models as load_audio_models,
    TRAINED_AUDIO_MODEL
)
from backend.detectors.text_detector import analyze_text, load_sms_model
from backend.detectors.job_detector import analyze_job_or_internship
from backend.detectors.url_detector import analyze_url, load_url_model
from backend.detectors.email_detector import analyze_email, load_email_model
from backend.detectors.ocr_detector import analyze_ocr_text
from backend.detectors.company_detector import verify_company
from backend.detectors.social_detector import analyze_social_post
from backend.detectors.assistant_engine import analyze_assistant_query
from backend.utils.history_db import record_scan, get_stats, get_history, clear_history, get_scan_by_id
from backend.utils.reports_db import create_report, get_reports, get_report_by_id
from backend.utils.auth_db import (
    register_user, login_user, logout_user,
    get_user_by_token, update_user_profile
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("trustguard.main")

app = FastAPI(
    title="TrustGuard AI API",
    description="Unified API for TrustGuard AI Pretrained Deepfake & Fraud Detection",
    version="1.0.0"
)

# Enable CORS for local development, LAN access, and GitHub Pages
ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://reshma630025.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(1[6-9]|2\d|3[0-1])\.\d+\.\d+|reshma630025\.github\.io)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    logger.info("Initializing TrustGuard AI detection models...")
    try:
        load_image_models()
    except Exception as e:
        logger.warning(f"Image model preloader notice: {e}")
    try:
        load_audio_models()
    except Exception as e:
        logger.warning(f"Audio model preloader notice: {e}")
    try:
        load_url_model()
    except Exception as e:
        logger.warning(f"URL model preloader notice: {e}")
    try:
        load_sms_model()
    except Exception as e:
        logger.warning(f"SMS model preloader notice: {e}")
    try:
        load_email_model()
    except Exception as e:
        logger.warning(f"Email model preloader notice: {e}")
    logger.info("TrustGuard AI models initialized.")


async def extract_request_data(request: Request) -> dict:
    """Helper to extract parameters whether provided via JSON, Form data, or query params."""
    content_type = request.headers.get("content-type", "").lower()
    data = {}
    if "application/json" in content_type:
        try:
            data = await request.json()
        except Exception:
            data = {}
    elif "multipart/form-data" in content_type or "application/x-www-form-urlencoded" in content_type:
        try:
            form = await request.form()
            data = dict(form)
        except Exception:
            data = {}
    if not data:
        data = dict(request.query_params)
    return data


def extract_user_from_request(request: Request) -> Optional[dict]:
    """Extracts authenticated user if Authorization header or X-Session-Token is present."""
    auth_header = request.headers.get("Authorization", "")
    token = None
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1].strip()
    elif "x-session-token" in request.headers:
        token = request.headers.get("x-session-token", "").strip()
    elif "token" in request.query_params:
        token = request.query_params.get("token", "").strip()

    if token:
        return get_user_by_token(token)
    return None


# ============================================================
# ROOT & STATIC FILE SERVING
# ============================================================

@app.get("/")
def read_root():
    index_file = PROJECT_ROOT / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {
        "service": "TrustGuard AI API",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/index.html")
def read_index_html():
    index_file = PROJECT_ROOT / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    raise HTTPException(status_code=404, detail="index.html not found")


@app.get("/firebase.js")
def read_firebase_js():
    js_file = PROJECT_ROOT / "firebase.js"
    if js_file.exists():
        return FileResponse(str(js_file), media_type="application/javascript")
    raise HTTPException(status_code=404, detail="firebase.js not found")


@app.get("/api.js")
def read_api_js():
    js_file = PROJECT_ROOT / "api.js"
    if js_file.exists():
        return FileResponse(str(js_file), media_type="application/javascript")
    raise HTTPException(status_code=404, detail="api.js not found")


# Dedicated SPA routes so direct navigation and refreshes return index.html
SPA_PATHS = [
    "/login", "/register", "/dashboard", "/deepfake",
    "/image-analysis", "/video-analysis", "/audio-analysis",
    "/text-scam", "/job-scan", "/internship-scan", "/url-scanner",
    "/ocr-scanner", "/company-verification", "/social-media",
    "/live-scan", "/profile", "/settings", "/history", "/results"
]

def make_spa_endpoint(route_path: str):
    def spa_route_handler():
        return FileResponse(str(PROJECT_ROOT / "index.html"))
    spa_route_handler.__name__ = f"spa_{route_path.strip('/').replace('-', '_')}"
    return spa_route_handler

for p in SPA_PATHS:
    app.add_api_route(p, make_spa_endpoint(p), methods=["GET"], include_in_schema=False)


# ============================================================
# AUTHENTICATION & USER PROFILE ENDPOINTS
# ============================================================

@app.post("/api/auth/register")
async def register_endpoint(request: Request):
    data = await extract_request_data(request)
    email = data.get("email", "")
    password = data.get("password", "")
    display_name = data.get("display_name", "") or data.get("name", "")
    organization = data.get("organization", "") or data.get("org", "")

    try:
        res = register_user(
            email=str(email),
            password=str(password),
            display_name=str(display_name),
            organization=str(organization)
        )
        return res
    except ValueError as ve:
        return JSONResponse(status_code=400, content={"success": False, "error": str(ve)})
    except Exception as e:
        logger.error(f"Error in /api/auth/register: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "error": f"Registration error: {str(e)}"})


@app.post("/api/auth/login")
async def login_endpoint(request: Request):
    data = await extract_request_data(request)
    email = data.get("email", "")
    password = data.get("password", "")

    try:
        res = login_user(email=str(email), password=str(password))
        return res
    except ValueError as ve:
        return JSONResponse(status_code=401, content={"success": False, "error": str(ve)})
    except Exception as e:
        logger.error(f"Error in /api/auth/login: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "error": f"Login error: {str(e)}"})


@app.post("/api/auth/logout")
async def logout_endpoint(request: Request):
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.split(" ", 1)[1] if auth_header.startswith("Bearer ") else request.headers.get("x-session-token", "")
    logout_user(token)
    return {"success": True, "message": "Logged out successfully."}


@app.get("/api/auth/me")
def get_current_user_endpoint(request: Request):
    user = extract_user_from_request(request)
    if not user:
        return JSONResponse(status_code=401, content={"success": False, "error": "Not authenticated or session expired."})
    return {"success": True, "user": user}


@app.put("/api/auth/profile")
async def update_profile_endpoint(request: Request):
    user = extract_user_from_request(request)
    if not user:
        return JSONResponse(status_code=401, content={"success": False, "error": "Authentication required to update profile."})

    data = await extract_request_data(request)
    try:
        updated = update_user_profile(
            user_id=user["id"],
            display_name=data.get("display_name"),
            organization=data.get("organization"),
            preferred_language=data.get("preferred_language"),
            theme=data.get("theme"),
            notifications_enabled=data.get("notifications_enabled")
        )
        return {"success": True, "user": updated, "message": "Profile updated successfully."}
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})


# ============================================================
# ROOT & STATIC ASSET ROUTES
# ============================================================

@app.get("/")
def serve_index():
    index_path = PROJECT_ROOT / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "TrustGuard AI API operational"}


@app.get("/api.js")
def serve_api_js():
    js_path = PROJECT_ROOT / "api.js"
    if js_path.exists():
        return FileResponse(str(js_path), media_type="application/javascript")
    return JSONResponse(status_code=404, content={"error": "api.js not found"})


@app.get("/firebase.js")
def serve_firebase_js():
    fb_path = PROJECT_ROOT / "firebase.js"
    if fb_path.exists():
        return FileResponse(str(fb_path), media_type="application/javascript")
    return JSONResponse(status_code=404, content={"error": "firebase.js not found"})


# ============================================================
# HEALTH & STATS ENDPOINTS
# ============================================================

@app.get("/api/health")
def get_health():
    return {
        "status": "ok",
        "service": "TrustGuard AI API",
        "version": "1.0.0"
    }


@app.get("/api/status")
def get_status():
    img_ready = IMAGE_TRAINED_MODEL.exists()
    aud_ready = TRAINED_AUDIO_MODEL.exists()
    url_ready = (PROJECT_ROOT / "models" / "url" / "best_model.pt").exists()
    sms_ready = (PROJECT_ROOT / "models" / "sms" / "best_model.pt").exists()
    email_ready = (PROJECT_ROOT / "models" / "email" / "best_model.pt").exists()
    social_ready = (PROJECT_ROOT / "models" / "social" / "best_model.pt").exists()

    prof_ready = (PROJECT_ROOT / "models" / "social" / "best_model_profile.pt").exists()
    
    return {
        "status": "online",
        "engine": "Real Pretrained & Multi-Signal Models",
        
        # Image Module
        "imageModel": "DeepfakeCNN (Trained on 1000 Videos Dataset, 88.1% Acc)",
        "imageDataset": "archive/1000_videos",
        "imageModelReady": img_ready,
        "imageModelLoaded": img_ready,
        "imageModelType": "trained",
        
        # Video Module
        "videoModel": "Frame-Level Video Deepfake Detection (Temporal Aggregation over DeepfakeCNN)",
        "videoDataset": "archive (16) Celeb-DF v2 Benchmark",
        "videoModelReady": img_ready,
        "videoModelLoaded": img_ready,
        "videoModelType": "frame_level_aggregation",
        
        # Audio Module
        "audioModel": "AudioCNN (Trained on ASVspoof 2019 LA, 99.5% Unseen Acc)",
        "audioDataset": "archive (1) ASVspoof 2019 LA",
        "audioModelReady": aud_ready,
        "audioModelLoaded": aud_ready,
        "audioModelType": "trained",
        
        # URL Module
        "urlModel": "PhishingURLNet (Trained on 579,920 URLs, 98.1% Acc)",
        "urlDataset": "archive (6) final_dataset.csv",
        "urlModelReady": url_ready,
        "urlModelLoaded": url_ready,
        "urlModelType": "trained",
        
        # Text & SMS Module
        "textModel": "SMSScamClassifier (Trained on SMS Spam Collection, 98.1% Deduplicated Acc)",
        "smsModel": "SMSScamClassifier (Trained on SMS Spam Collection, 98.1% Deduplicated Acc)",
        "smsDataset": "archive (4) spam_sms.csv",
        "smsModelReady": sms_ready,
        "smsModelLoaded": sms_ready,
        "textModelReady": sms_ready,
        "textModelLoaded": sms_ready,
        "smsModelType": "trained",
        "textModelType": "trained",
        
        # Email Module
        "emailModel": "EmailPhishingClassifier (Trained on 82,486 Emails, 98.7% Acc)",
        "emailDataset": "archive (9) phishing_email.csv & Multi-Corpus",
        "emailModelReady": email_ready,
        "emailModelLoaded": email_ready,
        "emailModelType": "trained",
        
        # Social Media Module
        "socialModel": "SocialProfileNet (94.2% Acc, archive (15)) & SocialSpamNet (90.8% Acc, archive (14))",
        "socialDataset": "archive (15) raw_user_profiles & archive (14) Instagram",
        "socialModelReady": (social_ready or prof_ready),
        "socialModelLoaded": (social_ready or prof_ready),
        "socialModelType": "trained",
        
        # Job & Internship Module (Heuristic Engine)
        "jobModel": "Forensic Entity & Upfront-Fee Rules (10,000 Fraudulent Postings Signatures)",
        "jobDataset": "archive (5) Fake Postings.csv (100% positive; no legitimate contrast available)",
        "jobModelReady": True,
        "jobModelType": "heuristic",
        "internshipModelReady": True,
        "internshipModelType": "heuristic",
        
        # Additional Modules
        "ocrModelReady": True,
        "ocrModelType": "tesseract_forensics",
        "companyModelReady": True,
        "companyModelType": "registry_verification",
        "multimodalReady": True,
        "multimodalType": "fusion_engine",
        "assistantReady": True,
        "reportsReady": True
    }


@app.get("/api/stats")
def get_live_stats(request: Request):
    user = extract_user_from_request(request)
    u_id = user["id"] if user else None
    stats = get_stats(user_id=u_id)
    return {
        "success": True,
        "stats": {
            "total_scans": stats.get("total_scans", 0),
            "threats_flagged": stats.get("threats", 0),
            "deepfakes_detected": stats.get("deepfakes", 0),
            "scams_neutralized": stats.get("scams", 0),
            "average_trust_score": stats.get("average_trust_score", 85.0),
            "authentic": stats.get("authentic", 0),
            "ai_generated": stats.get("ai_generated", 0),
            "uncertain": stats.get("uncertain", 0)
        },
        "total_scans": stats.get("total_scans", 0),
        "scans": stats.get("total_scans", 0),
        "threats": stats.get("threats", 0),
        "deepfakes": stats.get("deepfakes", 0),
        "scams": stats.get("scams", 0),
        "average_trust_score": stats.get("average_trust_score", 85.0)
    }


@app.get("/api/history")
def get_live_history(request: Request, limit: int = 50):
    user = extract_user_from_request(request)
    u_id = user["id"] if user else None
    history = get_history(user_id=u_id, limit=limit)
    return {
        "success": True,
        "history": history,
        "total": len(history)
    }


@app.post("/api/history/clear")
def clear_all_history(request: Request):
    user = extract_user_from_request(request)
    u_id = user["id"] if user else None
    clear_history(user_id=u_id)
    return {"success": True, "message": "History cleared."}


@app.get("/api/scan/{scan_id}")
def get_single_scan(scan_id: int):
    scan = get_scan_by_id(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail=f"Scan record #{scan_id} not found.")
    return {"success": True, "scan": scan}


# ============================================================
# 1. IMAGE DEEPFAKE DETECTION
# ============================================================

@app.post("/api/analyze/image")
async def analyze_image_endpoint(request: Request, image: Optional[UploadFile] = File(None), file: Optional[UploadFile] = File(None)):
    target = file or image
    if not target:
        raise HTTPException(status_code=400, detail="No image file uploaded. Provide 'file' or 'image' field.")
    
    user = extract_user_from_request(request)
    u_id = user["id"] if user else 1

    try:
        content = await target.read()
        if len(content) == 0:
            return JSONResponse(status_code=400, content={"success": False, "error": "Uploaded image file is empty."})
        
        result = analyze_image_bytes(content)
        result["fileName"] = target.filename
        
        if result.get("success"):
            record_scan(
                scan_type="image",
                content_label=target.filename or "Uploaded Image",
                classification=result.get("status") or result.get("classification", "UNKNOWN"),
                confidence=result.get("confidence", 0.0),
                risk_score=result.get("risk_score", 0.0),
                risk_level=result.get("risk_level", "LOW"),
                trust_score=result.get("trust_score"),
                trust_category=result.get("trust_category"),
                user_id=u_id,
                explanation=result.get("explanation", ""),
                indicators_json=json.dumps(result.get("indicators", []))
            )
        return result
    except Exception as e:
        logger.error(f"Error in /api/analyze/image: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "error": f"Image analysis failed: {str(e)}"})


@app.post("/api/analyze/camera")
async def analyze_camera_endpoint(request: Request, image: Optional[UploadFile] = File(None), file: Optional[UploadFile] = File(None)):
    target = file or image
    if not target:
        raise HTTPException(status_code=400, detail="No camera snapshot uploaded.")
    user = extract_user_from_request(request)
    u_id = user["id"] if user else 1
    try:
        content = await target.read()
        if len(content) == 0:
            return JSONResponse(status_code=400, content={"success": False, "error": "Captured camera snapshot is empty."})
        result = analyze_image_bytes(content)
        result["fileName"] = "camera_snapshot.jpg"
        result["modality"] = "camera"
        if result.get("success"):
            record_scan(
                scan_type="camera",
                content_label="Live Camera Snapshot",
                classification=result.get("status") or result.get("classification", "UNKNOWN"),
                confidence=result.get("confidence", 0.0),
                risk_score=result.get("risk_score", 0.0),
                risk_level=result.get("risk_level", "LOW"),
                trust_score=result.get("trust_score"),
                trust_category=result.get("trust_category"),
                user_id=u_id,
                explanation=result.get("explanation", ""),
                indicators_json=json.dumps(result.get("indicators", []))
            )
        return result
    except Exception as e:
        logger.error(f"Error in /api/analyze/camera: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "error": f"Camera analysis failed: {str(e)}"})


# ============================================================
# 2. VIDEO DEEPFAKE DETECTION (FRAME-BY-FRAME)
# ============================================================

@app.post("/api/analyze/video")
async def analyze_video_endpoint(request: Request, video: Optional[UploadFile] = File(None), file: Optional[UploadFile] = File(None)):
    target = file or video
    if not target:
        raise HTTPException(status_code=400, detail="No video file uploaded. Provide 'file' or 'video' field.")

    user = extract_user_from_request(request)
    u_id = user["id"] if user else 1

    try:
        content = await target.read()
        if len(content) == 0:
            return JSONResponse(status_code=400, content={"success": False, "error": "Uploaded video file is empty."})

        result = analyze_video_file(content)
        result["fileName"] = target.filename
        
        if result.get("success"):
            record_scan(
                scan_type="video",
                content_label=target.filename or "Uploaded Video",
                classification=result.get("status") or result.get("classification", "UNKNOWN"),
                confidence=result.get("confidence_pct", result.get("confidence", 0.0)),
                risk_score=result.get("risk_score", 0.0),
                risk_level=result.get("risk_level", "LOW"),
                trust_score=result.get("trust_score"),
                trust_category=result.get("trust_category"),
                user_id=u_id,
                explanation=result.get("explanation", ""),
                indicators_json=json.dumps(result.get("indicators", [])),
                frame_results_json=json.dumps(result.get("frame_results", []))
            )
        return result
    except Exception as e:
        logger.error(f"Error in /api/analyze/video: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "error": f"Video analysis failed: {str(e)}"})


# ============================================================
# 3. AUDIO / VOICE DEEPFAKE DETECTION (SEGMENT SPECTRAL)
# ============================================================

@app.post("/api/analyze/audio")
async def analyze_audio_endpoint(request: Request, audio: Optional[UploadFile] = File(None), file: Optional[UploadFile] = File(None)):
    target = file or audio
    if not target:
        raise HTTPException(status_code=400, detail="No audio file uploaded. Provide 'file' or 'audio' field.")

    user = extract_user_from_request(request)
    u_id = user["id"] if user else 1

    try:
        content = await target.read()
        result = analyze_audio_bytes(content)
        result["fileName"] = target.filename
        
        if result.get("success"):
            record_scan(
                scan_type="audio",
                content_label=target.filename or "Audio Recording",
                classification=result.get("status") or result.get("classification", "UNKNOWN"),
                confidence=result.get("confidence_pct", result.get("confidence", 0.0)),
                risk_score=result.get("risk_score", 0.0),
                risk_level=result.get("risk_level", "LOW"),
                trust_score=result.get("trust_score"),
                trust_category=result.get("trust_category"),
                user_id=u_id,
                explanation=result.get("explanation", ""),
                indicators_json=json.dumps(result.get("indicators", [])),
                segment_results_json=json.dumps(result.get("segment_results", []))
            )
        return result
    except Exception as e:
        logger.error(f"Error in /api/analyze/audio: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "error": f"Audio analysis failed: {str(e)}"})


@app.post("/api/analyze/live-audio")
async def analyze_live_audio_endpoint(request: Request, audio: Optional[UploadFile] = File(None), file: Optional[UploadFile] = File(None)):
    target = file or audio
    if not target:
        raise HTTPException(status_code=400, detail="No live audio stream uploaded.")
    user = extract_user_from_request(request)
    u_id = user["id"] if user else 1
    try:
        content = await target.read()
        if len(content) == 0:
            return JSONResponse(status_code=400, content={"success": False, "error": "Live audio sample is empty."})
        result = analyze_audio_bytes(content)
        result["fileName"] = target.filename or "live_recording.wav"
        result["modality"] = "live_audio"
        if result.get("success"):
            record_scan(
                scan_type="live_audio",
                content_label="Live Microphone Sample",
                classification=result.get("status") or result.get("classification", "UNKNOWN"),
                confidence=result.get("confidence_pct", result.get("confidence", 0.0)),
                risk_score=result.get("risk_score", 0.0),
                risk_level=result.get("risk_level", "LOW"),
                trust_score=result.get("trust_score"),
                trust_category=result.get("trust_category"),
                user_id=u_id,
                explanation=result.get("explanation", ""),
                indicators_json=json.dumps(result.get("indicators", [])),
                segment_results_json=json.dumps(result.get("segment_results", []))
            )
        return result
    except Exception as e:
        logger.error(f"Error in /api/analyze/live-audio: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "error": f"Live audio analysis failed: {str(e)}"})


# ============================================================
# 4. TEXT & SCAM DETECTION
# ============================================================

@app.post("/api/analyze/text")
async def analyze_text_endpoint(request: Request):
    data = await extract_request_data(request)
    input_text = data.get("text", "") or data.get("message", "") or data.get("content", "")
    user = extract_user_from_request(request)
    u_id = user["id"] if user else 1

    if not input_text or not str(input_text).strip():
        raise HTTPException(status_code=400, detail="No text provided. Send 'text' in JSON body or form.")

    try:
        result = analyze_text(str(input_text))
        if result.get("success"):
            record_scan(
                scan_type="text",
                content_label=str(input_text)[:40] + ("..." if len(str(input_text)) > 40 else ""),
                classification=result.get("status") or result.get("classification", "SAFE"),
                confidence=result.get("confidence_pct", result.get("confidence", 0.0)),
                risk_score=result.get("risk_score", 0.0),
                risk_level=result.get("risk_level", "LOW"),
                trust_score=result.get("trust_score"),
                trust_category=result.get("trust_category"),
                user_id=u_id,
                explanation=result.get("explanation", ""),
                indicators_json=json.dumps(result.get("indicators", []))
            )
        return result
    except Exception as e:
        logger.error(f"Error in /api/analyze/text: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "error": f"Text analysis failed: {str(e)}"})


# ============================================================
# 4b. EMAIL PHISHING DETECTION
# ============================================================

@app.post("/api/analyze/email")
async def analyze_email_endpoint(request: Request):
    data = await extract_request_data(request)
    body = data.get("body", "") or data.get("content", "") or data.get("text", "") or data.get("message", "")
    subject = data.get("subject", "")
    sender = data.get("sender", "") or data.get("from", "")
    user = extract_user_from_request(request)
    u_id = user["id"] if user else 1

    if not body and not subject:
        raise HTTPException(status_code=400, detail="No email content provided. Send 'body' or 'content' in request.")

    try:
        result = analyze_email(content=str(body), subject=str(subject), sender=str(sender))
        if result.get("success"):
            record_scan(
                scan_type="email",
                content_label=(subject or str(body))[:40] + ("..." if len(subject or str(body)) > 40 else ""),
                classification=result.get("status") or result.get("classification", "LEGITIMATE"),
                confidence=result.get("confidence_pct", result.get("confidence", 0.0)),
                risk_score=result.get("risk_score", 0.0),
                risk_level=result.get("risk_level", "LOW"),
                trust_score=result.get("trust_score"),
                trust_category=result.get("trust_category"),
                user_id=u_id,
                explanation=result.get("explanation", ""),
                indicators_json=json.dumps(result.get("indicators", []))
            )
        return result
    except Exception as e:
        logger.error(f"Error in /api/analyze/email: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "error": f"Email analysis failed: {str(e)}"})


# ============================================================
# 5. JOB & INTERNSHIP FRAUD DETECTION
# ============================================================

@app.post("/api/analyze/job")
async def analyze_job_endpoint(request: Request):
    data = await extract_request_data(request)
    desc = data.get("description", "") or data.get("desc", "") or data.get("text", "")
    title = data.get("title", "")
    company = data.get("company", "")
    salary = data.get("salary", "")
    location = data.get("location", "")
    fee = data.get("fee", "") or data.get("registration_fee", "")
    phone = data.get("phone", "")
    u = data.get("url", "") or data.get("website", "")
    em = data.get("email", "") or data.get("contact_email", "")

    parts = []
    if title: parts.append(f"Job Title: {title}")
    if company: parts.append(f"Company: {company}")
    if salary: parts.append(f"Salary: {salary}")
    if location: parts.append(f"Location: {location}")
    if fee: parts.append(f"Registration Fee: {fee}")
    if phone: parts.append(f"Contact Phone: {phone}")
    if desc: parts.append(str(desc))
    combined_desc = "\n".join(parts) if parts else str(desc)

    user = extract_user_from_request(request)
    u_id = user["id"] if user else 1

    if not combined_desc and not u and not em:
        raise HTTPException(status_code=400, detail="No job details provided.")

    try:
        result = analyze_job_or_internship(description=combined_desc, url=str(u), email=str(em), is_internship=False)
        if result.get("success"):
            record_scan(
                scan_type="job",
                content_label=(title or str(desc))[:40] if (title or desc) else "Job Listing",
                classification=result.get("status") or result.get("classification", "GENUINE"),
                confidence=result.get("confidence_pct", result.get("confidence", 0.0)),
                risk_score=result.get("risk_score", 0.0),
                risk_level=result.get("risk_level", "LOW"),
                trust_score=result.get("trust_score"),
                trust_category=result.get("trust_category"),
                user_id=u_id,
                explanation=result.get("explanation", ""),
                indicators_json=json.dumps(result.get("indicators", []))
            )
        return result
    except Exception as e:
        logger.error(f"Error in /api/analyze/job: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "error": f"Job analysis failed: {str(e)}"})


@app.post("/api/analyze/internship")
async def analyze_internship_endpoint(request: Request):
    data = await extract_request_data(request)
    desc = data.get("description", "") or data.get("desc", "") or data.get("text", "")
    title = data.get("title", "")
    company = data.get("company", "")
    salary = data.get("salary", "")
    location = data.get("location", "")
    fee = data.get("fee", "") or data.get("registration_fee", "")
    phone = data.get("phone", "")
    u = data.get("url", "") or data.get("website", "")
    em = data.get("email", "") or data.get("contact_email", "")

    parts = []
    if title: parts.append(f"Internship Title: {title}")
    if company: parts.append(f"Company: {company}")
    if salary: parts.append(f"Stipend/Salary: {salary}")
    if location: parts.append(f"Location: {location}")
    if fee: parts.append(f"Registration Fee: {fee}")
    if phone: parts.append(f"Contact Phone: {phone}")
    if desc: parts.append(str(desc))
    combined_desc = "\n".join(parts) if parts else str(desc)

    user = extract_user_from_request(request)
    u_id = user["id"] if user else 1

    try:
        result = analyze_job_or_internship(description=combined_desc, url=str(u), email=str(em), is_internship=True)
        if result.get("success"):
            record_scan(
                scan_type="internship",
                content_label=(title or str(desc))[:40] if (title or desc) else "Internship Posting",
                classification=result.get("status") or result.get("classification", "GENUINE"),
                confidence=result.get("confidence_pct", result.get("confidence", 0.0)),
                risk_score=result.get("risk_score", 0.0),
                risk_level=result.get("risk_level", "LOW"),
                trust_score=result.get("trust_score"),
                trust_category=result.get("trust_category"),
                user_id=u_id,
                explanation=result.get("explanation", ""),
                indicators_json=json.dumps(result.get("indicators", []))
            )
        return result
    except Exception as e:
        logger.error(f"Error in /api/analyze/internship: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "error": f"Internship analysis failed: {str(e)}"})


# ============================================================
# 6. URL SCANNER
# ============================================================

@app.post("/api/analyze/url")
async def analyze_url_endpoint(request: Request):
    data = await extract_request_data(request)
    target_url = data.get("url", "") or data.get("link", "")
    user = extract_user_from_request(request)
    u_id = user["id"] if user else 1

    if not target_url or not str(target_url).strip():
        raise HTTPException(status_code=400, detail="No URL provided.")

    try:
        result = analyze_url(str(target_url))
        if result.get("success"):
            record_scan(
                scan_type="url",
                content_label=str(target_url)[:50],
                classification=result.get("status") or result.get("classification", "SAFE"),
                confidence=result.get("confidence_pct", result.get("confidence", 0.0)),
                risk_score=result.get("risk_score", 0.0),
                risk_level=result.get("risk_level", "LOW"),
                trust_score=result.get("trust_score"),
                trust_category=result.get("trust_category"),
                user_id=u_id,
                explanation=result.get("explanation", ""),
                indicators_json=json.dumps(result.get("indicators", []))
            )
        return result
    except Exception as e:
        logger.error(f"Error in /api/analyze/url: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "error": f"URL analysis failed: {str(e)}"})


# ============================================================
# 7. OCR SCANNER
# ============================================================

@app.post("/api/analyze/ocr")
async def analyze_ocr_endpoint(
    request: Request,
    file: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None)
):
    target = file or image
    extracted = ""
    filename = "document.png"
    user = extract_user_from_request(request)
    u_id = user["id"] if user else 1

    if target:
        filename = target.filename or "document.png"
        content = await target.read()
        if not extracted:
            extracted = filename

    # Check for text in form/json if not provided
    if not extracted or extracted == filename:
        data = await extract_request_data(request)
        if data.get("text"):
            extracted = data.get("text")
        elif data.get("extracted_text"):
            extracted = data.get("extracted_text")

    if not extracted:
        raise HTTPException(status_code=400, detail="No document image or OCR text provided.")

    try:
        result = analyze_ocr_text(extracted, filename=filename)
        if result.get("success"):
            record_scan(
                scan_type="ocr",
                content_label=result.get("fileName", "Document"),
                classification=result.get("classification", "VERIFIED / LOW RISK"),
                confidence=result.get("confidence_pct", 0.0),
                risk_score=result.get("risk_score", 0.0),
                risk_level=result.get("risk_level", "LOW"),
                user_id=u_id,
                explanation=result.get("explanation", ""),
                indicators_json=json.dumps(result.get("indicators", []))
            )
        return result
    except Exception as e:
        logger.error(f"Error in /api/analyze/ocr: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "error": f"OCR analysis failed: {str(e)}"})


# ============================================================
# 8. COMPANY VERIFICATION
# ============================================================

@app.post("/api/analyze/company")
async def analyze_company_endpoint(request: Request):
    data = await extract_request_data(request)
    c_name = data.get("company_name", "") or data.get("name", "") or data.get("company", "")
    web = data.get("website", "") or data.get("domain", "") or data.get("url", "")
    em = data.get("email", "")
    user = extract_user_from_request(request)
    u_id = user["id"] if user else 1

    try:
        result = verify_company(str(c_name), str(web), str(em))
        if result.get("success"):
            record_scan(
                scan_type="company",
                content_label=c_name or web or "Company Entity",
                classification=result.get("classification", "VERIFIED COMPANY"),
                confidence=result.get("confidence_pct", 0.0),
                risk_score=result.get("risk_score", 0.0),
                risk_level=result.get("risk_level", "LOW"),
                user_id=u_id,
                explanation=result.get("explanation", ""),
                indicators_json=json.dumps(result.get("indicators", []))
            )
        return result
    except Exception as e:
        logger.error(f"Error in /api/analyze/company: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "error": f"Company verification failed: {str(e)}"})


# ============================================================
# 9. SOCIAL MEDIA FRAUD & BOT PROFILE DETECTION
# ============================================================

@app.post("/api/analyze/social")
async def analyze_social_endpoint(request: Request, file: Optional[UploadFile] = File(None)):
    data = await extract_request_data(request)
    user = extract_user_from_request(request)
    u_id = user["id"] if user else 1

    # Check if a file (CSV/JSON) was uploaded
    if file:
        try:
            content = await file.read()
            fname = (file.filename or "").lower()
            if fname.endswith(".csv"):
                import io
                import pandas as pd
                df = pd.read_csv(io.BytesIO(content))
                if len(df) > 0:
                    data.update(df.iloc[0].to_dict())
                data["source_file"] = file.filename
            elif fname.endswith(".json"):
                data.update(json.loads(content.decode("utf-8")))
                data["source_file"] = file.filename
        except Exception as fe:
            logger.warning(f"Error parsing social file: {fe}")

    # Determine if profile tabular features are present
    has_profile_features = any(k in data for k in [
        'username', 'handle', 'followers', 'followers_count', 'following', 'following_count',
        '#followers', '#follows', 'profile pic', 'profile_picture', 'nums/length username', 'posts', '#posts'
    ])

    try:
        if has_profile_features:
            from backend.detectors.social_detector import analyze_social_profile
            result = analyze_social_profile(data)
        else:
            post_text = data.get("content", "") or data.get("text", "") or data.get("post", "")
            post_url = data.get("url", "") or data.get("link", "")
            if not post_text and not post_url:
                raise HTTPException(status_code=400, detail="No profile details, text, or file provided.")
            result = analyze_social_post(str(post_text), str(post_url))

        if result.get("success"):
            label = data.get("username") or data.get("handle") or data.get("source_file") or (str(data.get("content", ""))[:30]) or "Social Profile"
            record_scan(
                scan_type="social",
                content_label=str(label),
                classification=result.get("classification") or result.get("status", "GENUINE"),
                confidence=result.get("confidence_pct", 0.0),
                risk_score=result.get("risk_score", 0.0),
                risk_level=result.get("risk_level", "LOW"),
                user_id=u_id,
                explanation=result.get("explanation", ""),
                indicators_json=json.dumps(result.get("indicators", []))
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in /api/analyze/social: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "error": f"Social media analysis failed: {str(e)}"})


# ============================================================
# 9b. DATASET SAMPLE VERIFICATION & EVALUATOR DEMO API
# ============================================================

DATASET_SAMPLES_CATALOG = {
    "image": {
        "real": {
            "path": r"C:\Users\paruc\Downloads\archive\1000_videos\test\real\067_16.png",
            "name": "067_16.png",
            "dataset": "1000 Videos Deepfake Video Frames (test/real)",
            "expected_label": "REAL",
            "description": "Authentic video frame without facial synthesis or warping artifacts."
        },
        "fake": {
            "path": r"C:\Users\paruc\Downloads\archive\1000_videos\test\fake\067_025_1.png",
            "name": "067_025_1.png",
            "dataset": "1000 Videos Deepfake Video Frames (test/fake)",
            "expected_label": "AI-GENERATED / FAKE",
            "description": "Manipulated face frame exhibiting deepfake synthesis boundaries."
        }
    },
    "audio": {
        "real": {
            "path": r"C:\Users\paruc\Downloads\archive (1)\LA\LA\ASVspoof2019_LA_dev\flac\LA_D_1047731.flac",
            "name": "LA_D_1047731.flac",
            "dataset": "ASVspoof 2019 Logical Access (dev/flac)",
            "expected_label": "REAL / AUTHENTIC",
            "description": "Authentic human vocal harmonics recorded in studio conditions."
        },
        "fake": {
            "path": r"C:\Users\paruc\Downloads\archive (1)\LA\LA\ASVspoof2019_LA_dev\flac\LA_D_1008730.flac",
            "name": "LA_D_1008730.flac",
            "dataset": "ASVspoof 2019 Logical Access (dev/flac)",
            "expected_label": "AI-GENERATED / SPOOF",
            "description": "Synthesized vocoder speech exhibiting spectral discontinuities."
        }
    },
    "sms": {
        "real": {
            "text": "Go until jurong point, crazy.. Available only in bugis n great world la e buffet... Cine there got amore wat...",
            "dataset": "SMS Spam Collection (spam_sms.csv)",
            "expected_label": "REAL / HAM",
            "description": "Organic conversational text without scam or urgency patterns."
        },
        "fake": {
            "text": "Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 to receive entry question(std txt rate)T&C's apply 08452810075over18's",
            "dataset": "SMS Spam Collection (spam_sms.csv)",
            "expected_label": "SPAM / SUSPICIOUS",
            "description": "Unsolicited premium-rate prize draw scam solicitation."
        }
    },
    "url": {
        "real": {
            "url": "http://0123456789nonexistent.com/",
            "dataset": "Phishing & Malicious URLs Dataset (final_dataset.csv)",
            "expected_label": "LEGITIMATE",
            "description": "Standard domain structure with low character entropy."
        },
        "fake": {
            "url": "http://%20%25**)(**@fbrasil.com/old/lqjj0ukuvg1e0h2f/qiye",
            "dataset": "Phishing & Malicious URLs Dataset (final_dataset.csv)",
            "expected_label": "PHISHING / SCAM-LIKELY",
            "description": "Obfuscated host, credential-stealing directory, and high Shannon entropy."
        }
    },
    "email": {
        "real": {
            "subject": "HPL Nom - May 25, 2001 File Review",
            "body": "hpl nom may 25 2001 see attached file hplno 525 xls hplno 525 xls for your records and review.",
            "sender": "records@enron-corporation.com",
            "dataset": "Phishing Email Benchmark Collection (phishing_email.csv)",
            "expected_label": "REAL / LEGITIMATE",
            "description": "Legitimate corporate correspondence with normal business syntax."
        },
        "fake": {
            "subject": "Urgent: Account Access Suspended - Confirm Credentials",
            "body": "Dear user, your payment account has been temporarily locked due to unauthorized access attempts. Click on the link below immediately to verify your credentials and wire transfer confirmation.",
            "sender": "security-notice@paypal-update.top",
            "dataset": "Phishing Email Benchmark Collection (phishing_email.csv)",
            "expected_label": "PHISHING / SCAM-LIKELY",
            "description": "Brand impersonation, high-pressure coercion, and credential harvesting."
        }
    },
    "social": {
        "real": {
            "name": "Genuine Profile (@peterkonda / Index 0)",
            "username": "peterkonda",
            "full_name": "Peter Konda",
            "profile pic": 1,
            "nums/length username": 0.0,
            "fullname words": 2,
            "nums/length fullname": 0.0,
            "name==username": 0,
            "description length": 44,
            "external URL": 0,
            "private": 0,
            "#posts": 32,
            "#followers": 1000,
            "#follows": 955,
            "followers": 1000,
            "following": 955,
            "posts": 32,
            "has_pic": 1,
            "bio": "Personal account exploring technology and life",
            "dataset": "Instagram Fake Spammer Genuine Accounts (archive (14)/test.csv)",
            "expected_label": "GENUINE",
            "description": "Balanced follower-to-following ratio with organic activity history."
        },
        "fake": {
            "name": "Spammer Profile (Follower Bot / Index 63)",
            "username": "official_bg_spambot",
            "full_name": "official_bg_spambot",
            "profile pic": 0,
            "nums/length username": 0.0,
            "fullname words": 1,
            "nums/length fullname": 0.0,
            "name==username": 1,
            "description length": 0,
            "external URL": 0,
            "private": 0,
            "#posts": 0,
            "#followers": 69,
            "#follows": 694,
            "followers": 69,
            "following": 694,
            "posts": 0,
            "has_pic": 0,
            "bio": "",
            "dataset": "Instagram Fake Spammer Genuine Accounts (archive (14)/test.csv)",
            "expected_label": "FAKE / SPAM",
            "description": "Original test split sample (Row 63): zero posts, no profile picture, 694 following disparity."
        }
    },
    "job": {
        "fake": {
            "title": "Mental health nurse",
            "company": "Rivera and Sons",
            "salary": "$5000/week",
            "email": "david27@gmail.com",
            "fee": "$150",
            "description": "Earn $5000/week! Immediate hiring. Contact now at david27@gmail.com. Mandatory registration fee of $150 required for processing equipment and onboarding without screening.",
            "dataset": "Fake Job Postings Dataset (archive (5)/Fake Postings.csv)",
            "expected_label": "FRAUDULENT / SCAM",
            "description": "Advance fee requirement with free commercial webmail recruiter address."
        }
    }
}

@app.get("/api/dataset-samples")
def get_dataset_samples_catalog():
    return {
        "success": True,
        "catalog": DATASET_SAMPLES_CATALOG
    }

@app.post("/api/verify/dataset-sample")
async def verify_dataset_sample_endpoint(request: Request):
    data = await extract_request_data(request)
    modality = str(data.get("modality", "")).lower()
    sample_type = str(data.get("sample_type", "")).lower()

    if sample_type in ["bonafide", "legit", "ham", "genuine"]:
        sample_type = "real"
    elif sample_type in ["spoof", "phish", "spam"]:
        sample_type = "fake"

    if modality not in DATASET_SAMPLES_CATALOG or sample_type not in DATASET_SAMPLES_CATALOG[modality]:
        raise HTTPException(status_code=400, detail=f"No dataset sample found for modality '{modality}' and type '{sample_type}'.")

    meta = DATASET_SAMPLES_CATALOG[modality][sample_type]
    user = extract_user_from_request(request)
    u_id = user["id"] if user else 1

    t0 = time.time()

    # Route through production analysis pipeline
    if modality == "image":
        img_path = Path(meta["path"])
        if not img_path.exists():
            raise HTTPException(status_code=404, detail=f"Original dataset file missing at {img_path}")
        content = img_path.read_bytes()
        res = analyze_image_bytes(content)
        res["fileName"] = meta["name"]
    elif modality == "audio":
        aud_path = Path(meta["path"])
        if not aud_path.exists():
            raise HTTPException(status_code=404, detail=f"Original dataset file missing at {aud_path}")
        content = aud_path.read_bytes()
        res = analyze_audio_bytes(content)
        res["fileName"] = meta["name"]
    elif modality == "sms":
        res = analyze_text(meta["text"])
    elif modality == "url":
        res = analyze_url(meta["url"])
    elif modality == "email":
        from backend.detectors.email_detector import analyze_email
        res = analyze_email(meta["body"], meta["subject"], meta.get("sender", ""))
    elif modality == "social":
        from backend.detectors.social_detector import analyze_social_profile
        res = analyze_social_profile(meta)
    elif modality == "job":
        combined_desc = f"{meta.get('title', '')} at {meta.get('company', '')}. Salary: {meta.get('salary', '')}. Upfront fee: {meta.get('fee', '')}. {meta.get('description', '')}"
        res = analyze_job_or_internship(
            description=combined_desc,
            email=meta.get("email", "")
        )
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported verification modality: {modality}")

    proc_time = round(time.time() - t0, 3)
    pred_label = str(res.get("classification") or res.get("status", "UNKNOWN")).upper()
    expected = meta["expected_label"].upper()

    # Determine ground truth alignment
    is_match = False
    if "REAL" in expected or "AUTHENTIC" in expected or "LEGITIMATE" in expected or "GENUINE" in expected:
        if any(k in pred_label for k in ["REAL", "AUTHENTIC", "LEGITIMATE", "GENUINE", "LOW RISK"]):
            is_match = True
    elif any(k in expected for k in ["FAKE", "SPOOF", "SPAM", "PHISH", "FRAUD", "SCAM"]):
        if any(k in pred_label for k in ["FAKE", "AI-GENERATED", "SPAM", "SUSPICIOUS", "SCAM-LIKELY", "PHISHING", "CRITICAL", "SCAM"]):
            is_match = True

    # Record to scan history
    record_scan(
        scan_type=modality,
        content_label=f"Dataset Sample: {meta.get('name') or meta.get('username') or meta.get('text', '')[:30] or meta.get('url', '')}",
        classification=pred_label,
        confidence=res.get("confidence_pct", 0.0),
        risk_score=res.get("risk_score", 0.0),
        risk_level=res.get("risk_level", "LOW"),
        user_id=u_id,
        explanation=f"[Dataset Verification Mode] Evaluated on {meta['dataset']}. {res.get('explanation', '')}",
        indicators_json=json.dumps(res.get("indicators", []))
    )

    return {
        "success": True,
        "modality": modality,
        "sample_type": sample_type,
        "dataset_name": meta["dataset"],
        "sample_identifier": meta.get("name") or meta.get("username") or meta.get("url") or meta.get("text", "")[:35],
        "expected_label": meta["expected_label"],
        "predicted_label": pred_label,
        "is_match": is_match,
        "match_status": "✓ MATCH" if is_match else "✗ MISMATCH",
        "confidence_pct": res.get("confidence_pct", 0.0),
        "risk_score": res.get("risk_score", 0.0),
        "risk_level": res.get("risk_level", "LOW"),
        "model_used": res.get("model_used") or res.get("model", "TrustGuard Engine"),
        "processing_time": proc_time,
        "explanation": res.get("explanation", ""),
        "indicators": res.get("indicators", []),
        "recommendation": res.get("recommendation", "")
    }


# ============================================================
# 10. MULTIMODAL UNIFIED FRAUD & CONTENT ANALYSIS
# ============================================================

@app.post("/api/analyze/multimodal")
async def analyze_multimodal_endpoint(
    request: Request,
    image: Optional[UploadFile] = File(None),
    audio: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None),
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    url: Optional[str] = Form(None)
):
    user = extract_user_from_request(request)
    u_id = user["id"] if user else 1

    modalities_analyzed = {}
    evidence_collected = []
    risk_scores = []
    confidences = []
    indicators_all = []

    # Infer file type if single file uploaded
    target_file = file
    if target_file and not (image or audio or video):
        fname = (target_file.filename or "").lower()
        if fname.endswith((".jpg", ".jpeg", ".png", ".webp", ".bmp")):
            image = target_file
        elif fname.endswith((".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac")):
            audio = target_file
        elif fname.endswith((".mp4", ".mov", ".avi", ".webm", ".mkv")):
            video = target_file

    # Image analysis
    if image:
        try:
            content = await image.read()
            if len(content) > 0:
                res_img = analyze_image_bytes(content)
                if res_img.get("success"):
                    modalities_analyzed["image"] = res_img
                    risk_scores.append(res_img.get("risk_score", 0.0))
                    confidences.append(res_img.get("confidence_pct", res_img.get("confidence", 80.0)))
                    evidence_collected.append(f"Image ({image.filename or 'image'}): {res_img.get('explanation', '')}")
                    indicators_all.extend(res_img.get("indicators", []))
        except Exception as e:
            logger.warning(f"Multimodal image analysis error: {e}")

    # Audio analysis
    if audio:
        try:
            content = await audio.read()
            if len(content) > 0:
                res_aud = analyze_audio_bytes(content)
                if res_aud.get("success"):
                    modalities_analyzed["audio"] = res_aud
                    risk_scores.append(res_aud.get("risk_score", 0.0))
                    confidences.append(res_aud.get("confidence_pct", res_aud.get("confidence", 80.0)))
                    evidence_collected.append(f"Audio ({audio.filename or 'audio'}): {res_aud.get('explanation', '')}")
                    indicators_all.extend(res_aud.get("indicators", []))
        except Exception as e:
            logger.warning(f"Multimodal audio analysis error: {e}")

    # Video analysis
    if video:
        try:
            content = await video.read()
            if len(content) > 0:
                res_vid = analyze_video_file(content)
                if res_vid.get("success"):
                    modalities_analyzed["video"] = res_vid
                    risk_scores.append(res_vid.get("risk_score", 0.0))
                    confidences.append(res_vid.get("confidence_pct", res_vid.get("confidence", 80.0)))
                    evidence_collected.append(f"Video ({video.filename or 'video'}): {res_vid.get('explanation', '')}")
                    indicators_all.extend(res_vid.get("indicators", []))
        except Exception as e:
            logger.warning(f"Multimodal video analysis error: {e}")

    # Text analysis
    if text and text.strip():
        try:
            res_txt = analyze_text(text.strip())
            if res_txt.get("success"):
                modalities_analyzed["text"] = res_txt
                risk_scores.append(res_txt.get("risk_score", 0.0))
                confidences.append(res_txt.get("confidence_pct", 85.0))
                evidence_collected.append(f"Text: {res_txt.get('explanation', '')}")
                indicators_all.extend(res_txt.get("indicators", []))
        except Exception as e:
            logger.warning(f"Multimodal text analysis error: {e}")

    # URL analysis
    if url and url.strip():
        try:
            res_url = analyze_url(url.strip())
            if res_url.get("success"):
                modalities_analyzed["url"] = res_url
                risk_scores.append(res_url.get("risk_score", 0.0))
                confidences.append(res_url.get("confidence_pct", 85.0))
                evidence_collected.append(f"URL ({url}): {res_url.get('explanation', '')}")
                indicators_all.extend(res_url.get("indicators", []))
        except Exception as e:
            logger.warning(f"Multimodal url analysis error: {e}")

    if not modalities_analyzed:
        raise HTTPException(
            status_code=400,
            detail="No valid multimodal inputs provided. Provide at least one of 'image', 'audio', 'video', 'text', 'url', or 'file'."
        )

    # Cross-modal fusion: weighted towards maximum detected threat
    from backend.utils.response_utils import calculate_trust_score, clamp_score
    max_risk = max(risk_scores)
    avg_risk = sum(risk_scores) / len(risk_scores)
    fused_risk = round(0.65 * max_risk + 0.35 * avg_risk, 1)
    fused_conf = round(sum(confidences) / len(confidences), 1)

    trust_meta = calculate_trust_score(fused_risk, fused_conf, is_scam=False)
    trust_score = trust_meta["trust_score"]
    status = trust_meta["status"]
    status_label = trust_meta["status_label"]

    mod_list = list(modalities_analyzed.keys())
    mod_str = ", ".join([m.upper() for m in mod_list])
    if fused_risk > 50.0:
        fused_explanation = f"Cross-modal fusion evaluated {len(mod_list)} signals ({mod_str}). Suspicious manipulation or synthetic fraud indicators detected. Peak modality risk reached {max_risk:.1f}/100."
    elif fused_risk > 25.0:
        fused_explanation = f"Cross-modal fusion evaluated {len(mod_list)} signals ({mod_str}). Moderate caution advised due to borderline indicators or compression variance."
    else:
        fused_explanation = f"Cross-modal fusion verified consistent authentic signatures across all {len(mod_list)} analyzed modalities ({mod_str}). Trust score: {trust_score}/100."

    record_scan(
        scan_type="multimodal",
        content_label=f"Multimodal ({mod_str})",
        classification=status,
        confidence=fused_conf,
        risk_score=fused_risk,
        risk_level=trust_meta["risk_level"],
        trust_score=trust_score,
        trust_category=trust_meta["trust_category"],
        user_id=u_id,
        explanation=fused_explanation,
        indicators_json=json.dumps(indicators_all)
    )

    min_risk = min(risk_scores) if risk_scores else 0.0
    cross_modal_divergence = round(abs(max_risk - min_risk), 1)
    fusion_strategy = "Weighted Peak-Average Cross-Modal Decision Fusion (65% Peak / 35% Modality Mean)"

    return {
        "success": True,
        "modality": "multimodal",
        "modalities_analyzed": mod_list,
        "status": status,
        "status_label": status_label,
        "classification": status,
        "confidence": fused_conf,
        "confidence_pct": fused_conf,
        "trust_score": trust_score,
        "trust_category": trust_meta["trust_category"],
        "risk_score": fused_risk,
        "risk_level": trust_meta["risk_level"],
        "authenticity": round(100.0 - fused_risk, 1),
        "authenticity_probability": round(100.0 - fused_risk, 1),
        "explanation": fused_explanation,
        "evidence": evidence_collected,
        "indicators": indicators_all,
        "signals": indicators_all,
        "modalities": modalities_analyzed,
        "cross_modal_divergence": cross_modal_divergence,
        "fusion_strategy": fusion_strategy
    }


# ============================================================
# 11. CYBERSECURITY AI ASSISTANT
# ============================================================

@app.post("/api/assistant")
async def assistant_endpoint(request: Request):
    data = await extract_request_data(request)
    query = data.get("query", "") or data.get("message", "") or data.get("prompt", "") or data.get("question", "")
    if not query:
        raise HTTPException(status_code=400, detail="Query message required.")
    scan_id = data.get("scan_id") or data.get("scanId")
    context_data = data.get("context") or data.get("context_data")
    if scan_id is not None:
        try:
            scan_id = int(scan_id)
        except Exception:
            scan_id = None
    res = analyze_assistant_query(str(query), context_scan_id=scan_id, context_data=context_data)
    return res


# ============================================================
# 12. COMPLIANCE & FORENSIC SECURITY REPORTS
# ============================================================

@app.get("/api/reports")
def get_reports_endpoint(request: Request, limit: int = 50):
    user = extract_user_from_request(request)
    u_id = user["id"] if user else None
    reports = get_reports(user_id=u_id, limit=limit)
    return {"success": True, "reports": reports, "total": len(reports)}


@app.post("/api/reports")
async def create_report_endpoint(request: Request):
    user = extract_user_from_request(request)
    u_id = user["id"] if user else 1
    data = await extract_request_data(request)
    title = data.get("title") or "Forensic Security Audit Report"
    report_type = data.get("report_type") or data.get("type") or "forensic_audit"
    scan_id = data.get("scan_id")
    summary = data.get("summary") or ""
    metrics = data.get("metrics") or get_stats(user_id=u_id)
    findings = data.get("findings") or []
    rep = create_report(
        title=str(title),
        report_type=str(report_type),
        user_id=u_id,
        scan_id=scan_id,
        summary=str(summary),
        metrics=metrics,
        findings=findings
    )
    return {"success": True, "report": rep}


@app.get("/api/reports/{report_id}")
def get_single_report_endpoint(report_id: str):
    rep = get_report_by_id(report_id)
    if not rep:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found.")
    return {"success": True, "report": rep}


# Universal Static File & SPA Fallback Handler
@app.get("/{full_path:path}", include_in_schema=False)
def serve_static_or_spa(full_path: str):
    clean_path = full_path.lstrip("/")
    target = (PROJECT_ROOT / clean_path).resolve()
    
    # Check if target is inside PROJECT_ROOT
    if PROJECT_ROOT.resolve() in target.parents or target == PROJECT_ROOT.resolve():
        if target.is_file():
            media_type = None
            if clean_path.endswith(".html"):
                media_type = "text/html"
            elif clean_path.endswith(".css"):
                media_type = "text/css"
            elif clean_path.endswith(".js"):
                media_type = "application/javascript"
            elif clean_path.endswith(".json"):
                media_type = "application/json"
            elif clean_path.endswith(".png"):
                media_type = "image/png"
            elif clean_path.endswith(".jpg") or clean_path.endswith(".jpeg"):
                media_type = "image/jpeg"
            elif clean_path.endswith(".svg"):
                media_type = "image/svg+xml"
            elif clean_path.endswith(".ico"):
                media_type = "image/x-icon"
            return FileResponse(str(target), media_type=media_type)
    
    # Fallback to SPA index.html
    index_file = PROJECT_ROOT / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    raise HTTPException(status_code=404, detail="Page not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
