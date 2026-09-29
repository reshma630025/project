# TrustGuard AI — Permanent Local Server & LAN Setup Guide

This document explains how TrustGuard AI runs permanently as a local service on your Windows PC, how other devices on the same Wi-Fi connect, and how to operate and manage the platform completely offline.

---

## 1. System Architecture & URLs

The TrustGuard AI backend is built on FastAPI and binds to `0.0.0.0:8000`, allowing access from both the host machine and any local network device.

```
                  +----------------------------------------------+
                  |               Host Windows PC                |
                  |                                              |
                  |  FastAPI Backend (0.0.0.0:8000)             |
                  |  PyTorch / Scikit-Learn Local Models         |
                  |  SQLite Database (trustguard.db)             |
                  +----------------------+-----------------------+
                                         |
               +-------------------------+-------------------------+
               |                                                   |
       [ Local Host Access ]                               [ LAN Wi-Fi Access ]
   http://127.0.0.1:8000/                              http://192.168.58.105:8000/
   http://localhost:8000/                              (Accessible from Phone, Laptop,
                                                        Tablet, Smart TV on same Wi-Fi)
```

### Active URLs:
- **Localhost (Host PC Only):** `http://127.0.0.1:8000/` or `http://localhost:8000/`
- **Dynamic LAN URL (Other Devices):** `http://192.168.58.105:8000/`
- **API Status Endpoint:** `http://192.168.58.105:8000/api/status`

> [!IMPORTANT]
> **Why `127.0.0.1` and `localhost` only work on the host PC:**
> `127.0.0.1` is the loopback address referring to the *current device itself*. If you type `127.0.0.1` into a mobile phone's browser, the phone attempts to connect to a web server running on the phone, not on your PC. To access TrustGuard AI from a phone, laptop, or tablet, use your PC's active LAN IPv4 address (`http://192.168.58.105:8000/`).

---

## 2. Automatic Startup After Windows Restart

TrustGuard AI is configured to start automatically every time your Windows PC starts or when you log in.

### Installed Startup Mechanism:
- **User Startup Launcher:** `C:\Users\paruc\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\TrustGuardAI-AutoStart.vbs`
- **Background Runner:** `start_trustguard_background.vbs`
- **Execution Script:** `start_trustguard.bat`

### What happens after a Windows restart:
1. Windows logs in and immediately triggers `TrustGuardAI-AutoStart.vbs`.
2. The script changes working directory to the project folder and executes `start_trustguard.bat` silently in the background (no intrusive black terminal windows remain open).
3. The script verifies whether port 8000 is already active (preventing duplicate processes).
4. Uvicorn starts on `0.0.0.0:8000` using the project's Python runtime (`Python 3.13`).
5. A health check polls `http://127.0.0.1:8000/api/status` until HTTP 200 is confirmed.
6. The startup timestamp and detected LAN IP are recorded into `logs/server.log`.

---

## 3. How Other Devices Connect (Phone / Laptop / Tablet)

To connect from an iPhone, Android phone, iPad, or another computer:
1. Ensure the device is connected to the **SAME Wi-Fi or Ethernet network** as the host PC.
2. Open any web browser (Chrome, Safari, Firefox, Edge).
3. Enter your host PC's current LAN address:
   ```
   http://192.168.58.105:8000/
   ```
4. The complete TrustGuard AI dashboard loads immediately. You can upload media (images, audio, videos, text, URLs) directly from your phone/tablet and receive instant AI analysis.

---

## 4. Frontend Dynamic Relative Routing

All API requests in TrustGuard AI use relative API routing (`/api/...` or `window.location.origin`):
```javascript
window.API_BASE_URL = window.location.origin;
```
When a phone loads `http://192.168.58.105:8000/`, all fetch requests (`/api/analyze/image`, `/api/analyze/video`, `/api/status`, etc.) automatically route to `http://192.168.58.105:8000/api/...`. No phone configuration or hardcoded IPs are required.

---

## 5. Offline-First & No-Internet Reliability

TrustGuard AI is 100% offline-first. **Internet access is NOT required for core AI detection.**

| Component / Detection Module | Requires Internet? | Local Execution Engine |
|---|---|---|
| **Image Deepfake ViT** | **NO (100% Offline)** | PyTorch `DeepfakeCNN` (`models/image/best_model.pt`) |
| **Audio Deepfake & STFT** | **NO (100% Offline)** | PyTorch `AudioCNN` (`models/audio/best_model.pt`) |
| **Video Deepfake (16 Keyframes)** | **NO (100% Offline)** | OpenCV + `DeepfakeCNN` Temporal Aggregator |
| **SMS Scam & Text Analyzer** | **NO (100% Offline)** | TF-IDF Vectorizer + `SMSScamClassifier` |
| **Email Phishing Scanner** | **NO (100% Offline)** | TF-IDF Vectorizer + `EmailPhishingClassifier` |
| **URL Phishing ML Scanner** | **NO (100% Offline)** | PyTorch `PhishingURLNet` (74 Lexical/Host Features) |
| **Social Media Profile/Spam** | **NO (100% Offline)** | PyTorch `SocialProfileNet` (14 Profile Features) |
| **Job / Internship Forensics** | **NO (100% Offline)** | Local Entity & Upfront-Fee Signature Engine |
| **Database / History / Stats** | **NO (100% Offline)** | Local SQLite Database (`backend/trustguard.db`) |

> [!NOTE]
> When public Internet is disconnected, `/api/status` continues returning `status: "online"`, and the web UI displays `● Online (Local AI Ready)` with `ONLINE / LOCAL`. It will NEVER display "Backend Offline" solely because WAN Internet is disconnected.

---

## 6. Windows Firewall Configuration

For devices on your local Wi-Fi to connect, Windows Firewall must allow inbound connections on TCP Port 8000 for Private networks.

### Automated Setup Script:
Right-click and select **"Run as administrator"**:
```
scripts\configure_firewall.bat
```

### Manual Command (PowerShell as Administrator):
```powershell
netsh advfirewall firewall add rule name="TrustGuard AI Server (Port 8000)" dir=in action=allow protocol=TCP localport=8000 profile=private,domain
```

---

## 7. Manual Server Control Commands

All control scripts are located in the root directory:

| Action | Script to Run | Description |
|---|---|---|
| **Start Server** | `start_trustguard.bat` | Checks port 8000, starts Uvicorn if stopped, polls `/api/status`, displays LAN URL, and opens browser. |
| **Stop Server** | `stop_trustguard.bat` | Gracefully terminates all processes listening on port 8000. |
| **Restart Server** | `restart_trustguard.bat` | Stops existing process and launches a fresh server instance. |
| **Install Auto-Start** | `setup_autostart_task.bat` | Registers Windows Task Scheduler and Startup folder shortcuts. |
| **Remove Auto-Start** | `remove_autostart_task.bat` | Removes Windows Startup shortcut and Task Scheduler entries. |

---

## 8. Server Activity & Startup Logging

All server startup events, shutdowns, port bindings, and IP detections are logged to:
```
logs/server.log
```
Example log entry:
```
[15-09-2026 14:53:45] Server started/verified on 0.0.0.0:8000 (LAN: 192.168.58.105)
```
