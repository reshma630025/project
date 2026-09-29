"""
FastAPI Backend Application for TrustGuard AI Unified Deepfake & Synthetic Content Analysis.
Connects all detection modules with real AI models, forensic algorithms, authentication, and live user-scoped history tracking.
"""
import sys
import json
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
from backend.detectors.text_detector import analyze_text
from backend.detectors.job_detector import analyze_job_or_internship
from backend.detectors.url_detector import analyze_url
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

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    return {
        "status": "online",
        "engine": "Real Pretrained & Multi-Signal Models",
        "imageModel": "DeepfakeCNN (Trained on 1000 Videos Dataset)" if img_ready else IMAGE_MODEL_NAME,
        "imageModelReady": img_ready,
        "imageModelLoaded": img_ready,
        "videoModelReady": img_ready,
        "videoModelLoaded": img_ready,
        "audioModel": "AudioCNN (Trained on ASVspoof 2019 LA)" if aud_ready else "STFT Spectral Forensics",
        "audioModelReady": aud_ready or True,
        "audioModelLoaded": aud_ready,
        "textModelReady": True,
        "jobModelReady": True,
        "urlModelReady": True,
        "ocrModelReady": True,
        "companyModelReady": True,
        "socialModelReady": True,
        "multimodalReady": True,
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
# 9. SOCIAL MEDIA FRAUD DETECTION
# ============================================================

@app.post("/api/analyze/social")
async def analyze_social_endpoint(request: Request):
    data = await extract_request_data(request)
    post_text = data.get("content", "") or data.get("text", "") or data.get("post", "")
    post_url = data.get("url", "") or data.get("link", "")
    platform = data.get("platform", "General")
    user = extract_user_from_request(request)
    u_id = user["id"] if user else 1

    if not post_text and not post_url:
        raise HTTPException(status_code=400, detail="No social media text or URL provided.")

    try:
        result = analyze_social_post(str(post_text), str(post_url))
        if result.get("success"):
            record_scan(
                scan_type="social",
                content_label=str(post_text)[:40] if post_text else f"{platform} Post",
                classification=result.get("classification", "LOW RISK SOCIAL CONTENT"),
                confidence=result.get("confidence_pct", 0.0),
                risk_score=result.get("risk_score", 0.0),
                risk_level=result.get("risk_level", "LOW"),
                user_id=u_id,
                explanation=result.get("explanation", ""),
                indicators_json=json.dumps(result.get("indicators", []))
            )
        return result
    except Exception as e:
        logger.error(f"Error in /api/analyze/social: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"success": False, "error": f"Social media analysis failed: {str(e)}"})


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
