# TrustGuard AI - Offline & Online Verification

## Offline-First Architecture Compliance
TrustGuard AI has been fully validated to operate 100% locally on the host machine. 

### Dependencies & Local Processing
- **No Cloud API Reliance**: The FastAPI backend completely bypasses external SaaS calls for core functionality. Image, Video, Audio, SMS, Email, URL, Social, and Job verification occurs directly inside the local `uvicorn` Python process.
- **Model Storage**: All required AI models are successfully checked out in the `models/` directory. 
- **Graceful Offline Degradation**: The Image detector automatically triggers local `ELA` forensics combined with Hugging Face caching. 

## Local vs LAN Routing Fixes
### GitHub Pages / Frontend Hardcoding Bug
The critical error `Unexpected token '<'` was caused by GitHub Pages returning an HTML 404 page when the static JS requested `/api/...`. 

**The Fix:**
- The frontend `api.js` explicitly traps `<!doctype html>` injections and halts execution with a detailed error: "The local TrustGuard AI backend is not running."
- The UI differentiates the backend topology, ensuring users know if they are connecting via `localhost` (127.0.0.1) or `LAN IP`.
- `window.location.origin` is safely parsed to prevent the UI from calling `localhost` on external LAN devices.

## One-Click Startup Script (`start_trustguard.bat`)
A comprehensive batch script has been implemented to handle all connectivity automation:
1. Validates Python environment paths.
2. Checks pip for `fastapi`, `torch`, `uvicorn`, `pandas`.
3. Auto-detects the machine's local IPv4 LAN address (e.g., `192.168.x.x`).
4. Binds the backend to `0.0.0.0:8000`.
5. Checks if the port is already occupied (prevents double-startup crashes).
6. Tests the `/api/status` endpoint to confirm the ML models loaded successfully.
7. Opens Google Chrome to the dynamically detected LAN IP URL.
