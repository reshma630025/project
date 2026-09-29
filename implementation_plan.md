# Real Model & Backend Integration Plan for All TrustGuard AI Modules

Connect all TrustGuard AI detection modules directly to real backend detectors, pretrained AI models, and forensic analysis pipelines with unified risk scoring, SQLite scan history, dynamic dashboard statistics, and zero mock or randomized data.

---

## User Review Required

> [!IMPORTANT]
> **Key Architecture Decisions:**
> 1. **Zero Mock / Hardcoded Results:** All frontend modules (`Image`, `Video`, `Audio`, `Text/Scam`, `Job/Internship`, `URL`, `OCR`, `Company`, `Social Media`) will query the live FastAPI backend via `http://127.0.0.1:8000/api/analyze/*`.
> 2. **Unified Risk Scoring Contract:** Standardized to:
>    - `0–20`: **LOW**
>    - `21–40`: **MODERATE**
>    - `41–60`: **HIGH**
>    - `61–80`: **VERY HIGH**
>    - `81–100`: **CRITICAL**
> 3. **Dynamic History & Statistics:** SQLite database (`trustguard.db`) will store all scans and provide real-time counts for `GET /api/stats` and `GET /api/history` (starting at 0 for clean sessions).
> 4. **Preserved UI:** Retains all existing spatial grid styles, dark glassmorphism, animations, report export, and TTS voiceovers.

---

## Proposed Changes

### Backend Architecture

#### [NEW] [text_detector.py](file:///c:/Users/paruc/OneDrive/Desktop/git5/backend/detectors/text_detector.py)
- Analyzes text messages and emails for:
  - Financial fraud & payment solicitation (wire transfer, gift cards, crypto, UPI)
  - Urgency & psychological pressure (account suspension, legal threats, countdowns)
  - Credentials & OTP extraction (passwords, PINs, 2FA bypass)
  - Lottery / Prize / Reward scams
  - Impersonation of institutions (banks, government agencies, tech support)
- Computes deterministic confidence, risk score ($0..100$), risk level, explanation, and detected indicator list.

#### [NEW] [job_detector.py](file:///c:/Users/paruc/OneDrive/Desktop/git5/backend/detectors/job_detector.py)
- Analyzes job postings and internship listings for:
  - Mandatory registration fees, training charges, or security deposits
  - Unrealistic salary-to-experience ratios (e.g. $10k/week for entry-level data entry)
  - Suspicious / free recruiter emails (`@gmail.com`, `@yahoo.com` vs corporate domains)
  - Guaranteed employment claims and immediate hiring without interviews
  - Missing company identifiers or vague job scopes
- Returns `GENUINE`, `SUSPICIOUS`, or `FRAUDULENT` classifications with specific risk indicators.

#### [NEW] [url_detector.py](file:///c:/Users/paruc/OneDrive/Desktop/git5/backend/detectors/url_detector.py)
- Analyzes submitted URLs for:
  - IP address hostnames, excessive subdomains, character entropy, and homograph attacks
  - Suspicious / high-risk TLDs (`.top`, `.xyz`, `.fit`, `.work`, etc.)
  - Phishing path tokens (`/login-verify/`, `/update-billing/`, etc.)
  - SSL/HTTPS validation & redirect chains
- Returns `SAFE`, `SUSPICIOUS`, or `PHISHING / MALICIOUS` with risk level and breakdown.

#### [NEW] [audio_detector.py](file:///c:/Users/paruc/OneDrive/Desktop/git5/backend/detectors/audio_detector.py)
- Processes audio uploads using `librosa` / `soundfile` / `scipy`:
  - Extracts acoustic features: Spectral Centroid, Spectral Rolloff, Spectral Flux, Zero-Crossing Rate, and MFCC variance.
  - Detects voice cloning anomalies: unnatural phase continuity, spectral cutoff anomalies, and robotic pitch flattening.
  - Returns `REAL` / `GENUINE VOICE` vs `FAKE` / `AI-GENERATED / SYNTHETIC` with duration and indicators.

#### [NEW] [ocr_detector.py](file:///c:/Users/paruc/OneDrive/Desktop/git5/backend/detectors/ocr_detector.py)
- Receives uploaded posters/screenshots, extracts text, extracts structured entities (Company, Email, Phone, Website, Salary, Registration Fee), and evaluates scam indicators.

#### [NEW] [company_detector.py](file:///c:/Users/paruc/OneDrive/Desktop/git5/backend/detectors/company_detector.py)
- Performs real DNS lookup, domain MX validation, email domain cross-referencing, and brand authenticity heuristics.
- Returns `VERIFIED COMPANY`, `UNVERIFIED COMPANY`, or `SUSPICIOUS COMPANY`.

#### [NEW] [social_detector.py](file:///c:/Users/paruc/OneDrive/Desktop/git5/backend/detectors/social_detector.py)
- Evaluates social media posts and URLs for fake giveaways, crypto scams, account impersonation, and engagement bait.

#### [NEW] [history_db.py](file:///c:/Users/paruc/OneDrive/Desktop/git5/backend/utils/history_db.py)
- SQLite database (`trustguard.db`) managing scan logs and computing dynamic stats (`total_scans`, `threats_detected`, `deepfakes_detected`, `scams_prevented`).

#### [MODIFY] [main.py](file:///c:/Users/paruc/OneDrive/Desktop/git5/backend/main.py)
- Wire all endpoints:
  - `GET /api/health`
  - `GET /api/stats`
  - `GET /api/history`
  - `POST /api/analyze/image`
  - `POST /api/analyze/video`
  - `POST /api/analyze/audio`
  - `POST /api/analyze/text`
  - `POST /api/analyze/job`
  - `POST /api/analyze/internship`
  - `POST /api/analyze/url`
  - `POST /api/analyze/ocr`
  - `POST /api/analyze/company`
  - `POST /api/analyze/social`

---

### Frontend Architecture

#### [MODIFY] [index.html](file:///c:/Users/paruc/OneDrive/Desktop/git5/index.html)
- Centralize `API_BASE_URL = "http://127.0.0.1:8000"`.
- Implement unified `normalizeResult(apiRes, type)` and `renderResultCard(norm, title, duration)`.
- Connect all page buttons:
  - Image (`#imgAnalyzeBtn`)
  - Video (`#vidAnalyzeBtn`)
  - Audio (`#audAnalyzeBtn`)
  - Text / Scam (`#scamAnalyzeBtn`)
  - Job / Internship (`#jobAnalyzeBtn`)
  - URL (`#urlAnalyzeBtn`)
  - OCR (`#ocrRunBtn`)
  - Company (`#protectRunBtn`)
  - Social (`#socialAnalyzeBtn`)
  - Dashboard Universal Analyzer (`#dashAnalyzeBtn`)
- Wire real statistics loading from `GET /api/stats` on dashboard load.
- Remove all `Math.random()` and mock data generators.

---

## Verification Plan

### Automated Endpoint Testing
- Run test suite against every endpoint:
  ```powershell
  python verify_all_endpoints.py
  ```
- Run pytest suite:
  ```powershell
  python -m pytest backend/tests/
  ```

### Manual Verification
1. Test Image scanner with genuine and manipulated images.
2. Test Video scanner with sample video clip.
3. Test Audio scanner with voice audio file.
4. Test Text scanner with benign vs phishing/urgent scam messages.
5. Test Job scanner with genuine job listing vs fake registration fee scam.
6. Test URL scanner with legitimate domain vs suspicious IP/phishing URL.
7. Test OCR scanner with poster upload and verify extracted entity fields.
8. Test Company scanner with real vs invalid domain.
9. Test Social media scanner with fake giveaway text.
10. Verify dynamic dashboard counters update after each scan.
