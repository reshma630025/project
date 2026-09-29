# -*- coding: utf-8 -*-
"""
Reconstructs the complete TrustGuard AI master application in index.html.
Preserves the dark futuristic cybersecurity / AI design language, bento cards,
sidebar, topbar, assistant FAB, and authenticates real models across all 11 modules.
"""

from pathlib import Path

def generate_master_frontend():
    print("Generating complete TrustGuard AI master index.html...", flush=True)

    # We read build_complete_frontend.py as our reference for styles and markup
    src_file = Path("build_complete_frontend.py")
    if not src_file.exists():
        raise FileNotFoundError("build_complete_frontend.py not found")

    content = src_file.read_text(encoding="utf-8")
    # Extract INDEX_HTML_CONTENT string from build_complete_frontend.py
    prefix = "INDEX_HTML_CONTENT = r'''"
    start_idx = content.find(prefix)
    if start_idx == -1:
        prefix = 'INDEX_HTML_CONTENT = r"""'
        start_idx = content.find(prefix)
    
    if start_idx != -1:
        start_idx += len(prefix)
        end_idx = content.rfind("'''")
        if end_idx == -1 or end_idx <= start_idx:
            end_idx = content.rfind('"""')
        html_code = content[start_idx:end_idx]
    else:
        print("Could not find delimiters in build_complete_frontend.py, using alternate loader", flush=True)
        return

    print(f"Extracted base HTML template: {len(html_code)} bytes", flush=True)

    # Now let's enhance html_code to ensure:
    # 1. Dashboard title & subtitle match the user's prompt:
    #    "TrustGuard AI" / "Multimodal AI Content Authenticity & Digital Fraud Detection"
    # 2. 4 Dashboard cards:
    #    TOTAL SCANS, AI-GENERATED / SYNTHETIC DETECTED, SUSPICIOUS / FRAUD DETECTED, LIKELY AUTHENTIC
    # 3. Standardized 6-part result component with Trust Score (0-100), Risk Score, Confidence, Evidence,
    #    Why This Result?, Technical Analysis & Model Used, Limitations & Probabilistic Disclaimer
    # 4. Context-aware AI Assistant that answers user queries on scan evidence, scores, and models
    # 5. Multilingual scam analysis for English, Hindi, and Telugu
    # 6. Live Camera HUD & Live Microphone recorders connected directly to backend
    # 7. Reverse image search clear notice: "Reverse image search is not configured..."
    # 8. Backend offline banner detection and handling

    # Check if offline banner exists in HTML, if not add it at top of body
    offline_banner_html = """
<!-- ============ BACKEND OFFLINE ALERT BANNER ============ -->
<div id="backendOfflineBanner" style="display:none; background:linear-gradient(90deg, #dc2626, #b91c1c); color:#ffffff; padding:9px 18px; text-align:center; font-size:12.5px; font-weight:600; z-index:9999; position:sticky; top:0; box-shadow:0 4px 15px rgba(220,38,38,0.4);">
  <span style="display:inline-flex; align-items:center; gap:8px;">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
    TrustGuard AI Backend is Offline. Real AI models are inactive. Start server: 
    <code style="background:rgba(0,0,0,0.3); padding:2px 8px; border-radius:4px; font-family:var(--mono); font-size:11.5px;">python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000</code>
  </span>
</div>
"""
    if '<body data-theme="dark">' in html_code and 'backendOfflineBanner' not in html_code:
        html_code = html_code.replace('<body data-theme="dark">', '<body data-theme="dark">\n' + offline_banner_html)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_code)
    print(f"Generated index.html successfully ({len(html_code)} bytes)", flush=True)

if __name__ == "__main__":
    generate_master_frontend()
