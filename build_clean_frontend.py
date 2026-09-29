"""
Generator for the complete, refactored TrustGuard AI frontend (index.html).
Centers on: Content Authenticity, AI Generation Detection, Transparency, and Unified Trust Score.
"""
from pathlib import Path

def generate_index_html():
    html_content = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TrustGuard AI — AI Content Authenticity & Trust Detection Platform</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<!-- Tesseract OCR engine for client poster text extraction -->
<script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>
<style>
/* ============ MODERN DESIGN SYSTEM TOKENS ============ */
:root {
  --bg-base: #090d16;
  --bg-surface: #0f172a;
  --bg-card: rgba(18, 26, 44, 0.75);
  --bg-card-hover: rgba(28, 39, 64, 0.85);
  --border: rgba(148, 163, 184, 0.14);
  --border-focus: #38bdf8;
  
  --accent-cyan: #38bdf8;
  --accent-blue: #3b82f6;
  --accent-indigo: #6366f1;
  
  /* Semantic Status Colors */
  --trust-high: #10b981;      /* 90-100: High Trust / Real */
  --trust-likely: #059669;    /* 70-89: Likely Trustworthy */
  --trust-uncertain: #f59e0b; /* 40-69: Uncertain / Review */
  --trust-low: #ef4444;       /* 0-39: Low Trust / AI / Fake */
  --trust-danger: #dc2626;

  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --text-faint: #64748b;
  
  --font-display: 'Space Grotesk', -apple-system, sans-serif;
  --font-body: 'Inter', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;
  --sidebar-w: 260px;
}

[data-theme="light"] {
  --bg-base: #f1f5f9;
  --bg-surface: #ffffff;
  --bg-card: rgba(255, 255, 255, 0.9);
  --bg-card-hover: rgba(241, 245, 249, 0.95);
  --border: rgba(148, 163, 184, 0.25);
  --text-main: #0f172a;
  --text-muted: #475569;
  --text-faint: #94a3b8;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  background: var(--bg-base);
  color: var(--text-main);
  font-family: var(--font-body);
  min-height: 100vh;
  overflow-x: hidden;
  line-height: 1.5;
  transition: background 0.3s ease, color 0.3s ease;
}

/* Subtle background ambience */
.bg-ambient {
  position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background:
    radial-gradient(800px 500px at 15% 10%, rgba(56, 189, 248, 0.06), transparent 70%),
    radial-gradient(700px 600px at 85% 20%, rgba(99, 102, 241, 0.05), transparent 65%),
    radial-gradient(600px 600px at 50% 90%, rgba(16, 185, 129, 0.04), transparent 60%);
}

/* Layout container */
#app-root {
  display: flex;
  min-height: 100vh;
  position: relative;
  z-index: 1;
}

/* ============ SIDEBAR NAVIGATION ============ */
#sidebar {
  width: var(--sidebar-w);
  background: var(--bg-surface);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0; bottom: 0; left: 0;
  z-index: 100;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.brand-section {
  padding: 24px 20px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid var(--border);
}
.brand-logo {
  width: 38px; height: 38px; border-radius: 10px;
  background: linear-gradient(135deg, var(--accent-cyan), var(--accent-indigo));
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 20px; font-weight: 800;
  box-shadow: 0 4px 14px rgba(56, 189, 248, 0.3);
}
.brand-text h1 {
  font-family: var(--font-display);
  font-size: 17px; font-weight: 700; letter-spacing: -0.2px;
  color: var(--text-main);
}
.brand-text p {
  font-size: 11.5px; color: var(--text-muted);
}

.nav-menu {
  flex: 1;
  overflow-y: auto;
  padding: 18px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.nav-group-title {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-faint);
  padding: 12px 12px 6px;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  color: var(--text-muted);
  font-size: 13.5px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}
.nav-item:hover {
  background: var(--bg-card-hover);
  color: var(--text-main);
}
.nav-item.active {
  background: rgba(56, 189, 248, 0.12);
  color: var(--accent-cyan);
  font-weight: 600;
  border-color: rgba(56, 189, 248, 0.25);
}
.nav-icon {
  font-size: 16px;
  width: 20px;
  text-align: center;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.engine-status-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--text-muted);
  background: var(--bg-card);
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
}
.status-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--trust-high);
  box-shadow: 0 0 6px var(--trust-high);
}
.status-dot.offline {
  background: var(--trust-low);
  box-shadow: 0 0 6px var(--trust-low);
}

/* ============ MAIN CONTENT AREA ============ */
#main-content {
  flex: 1;
  margin-left: var(--sidebar-w);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Top Header Bar */
.top-bar {
  height: 64px;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border);
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(12px);
  position: sticky; top: 0; z-index: 90;
}
.top-left {
  display: flex;
  align-items: center;
  gap: 16px;
}
.menu-btn {
  display: none;
  background: none; border: none;
  color: var(--text-main); font-size: 22px; cursor: pointer;
}
.page-title-crumb {
  font-family: var(--font-display);
  font-size: 16px; font-weight: 600;
  color: var(--text-main);
}
.top-right {
  display: flex;
  align-items: center;
  gap: 14px;
}
.theme-btn {
  background: var(--bg-card); border: 1px solid var(--border);
  color: var(--text-muted); padding: 7px 12px; border-radius: var(--radius-sm);
  cursor: pointer; font-size: 14px; transition: all 0.2s ease;
}
.theme-btn:hover { color: var(--text-main); border-color: var(--border-focus); }
.user-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  background: var(--bg-card);
  border: 1px solid var(--border);
  font-size: 12.5px;
  color: var(--text-main);
  cursor: pointer;
}

/* Page Views Container */
.views-container {
  flex: 1;
  padding: 32px;
  max-width: 1240px;
  width: 100%;
  margin: 0 auto;
}
.page-view {
  display: none;
  animation: fadeIn 0.25s ease-out;
}
.page-view.active {
  display: block;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ============ OFFLINE BANNER ============ */
#offline-alert {
  display: none;
  background: linear-gradient(90deg, #b91c1c, #991b1b);
  color: #fff;
  padding: 10px 24px;
  font-size: 13px;
  font-weight: 500;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
#offline-alert.show { display: flex; align-items: center; justify-content: center; gap: 12px; }
.retry-btn {
  background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.4);
  color: #fff; padding: 3px 10px; border-radius: 4px; cursor: pointer; font-size: 12px;
}
.retry-btn:hover { background: rgba(255,255,255,0.35); }

/* ============ HERO & LANDING ============ */
.hero-section {
  text-align: center;
  padding: 40px 20px 48px;
  max-width: 820px;
  margin: 0 auto;
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border-radius: 9999px;
  background: rgba(56, 189, 248, 0.1);
  border: 1px solid rgba(56, 189, 248, 0.25);
  color: var(--accent-cyan);
  font-size: 12.5px;
  font-weight: 600;
  margin-bottom: 20px;
}
.hero-title {
  font-family: var(--font-display);
  font-size: 42px;
  font-weight: 800;
  letter-spacing: -1px;
  line-height: 1.15;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #ffffff 40%, var(--accent-cyan) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.hero-sub {
  font-size: 16.5px;
  color: var(--text-muted);
  line-height: 1.6;
  margin-bottom: 32px;
}
.hero-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  flex-wrap: wrap;
}
.btn-primary {
  background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
  color: #031525;
  border: none;
  padding: 13px 28px;
  border-radius: var(--radius-sm);
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(56, 189, 248, 0.35);
  transition: all 0.2s ease;
  display: inline-flex; align-items: center; gap: 8px;
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 22px rgba(56, 189, 248, 0.5);
}
.btn-secondary {
  background: var(--bg-card);
  color: var(--text-main);
  border: 1px solid var(--border);
  padding: 13px 24px;
  border-radius: var(--radius-sm);
  font-size: 14.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex; align-items: center; gap: 8px;
}
.btn-secondary:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-focus);
}

/* Modality Selector Grid */
.modality-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 18px;
  margin-top: 36px;
}
.modality-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 24px;
  cursor: pointer;
  transition: all 0.25s ease;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.modality-card:hover {
  background: var(--bg-card-hover);
  border-color: var(--accent-cyan);
  transform: translateY(-3px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
}
.mod-icon-wrap {
  width: 46px; height: 46px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px;
  background: rgba(56, 189, 248, 0.12);
  color: var(--accent-cyan);
}
.mod-title {
  font-family: var(--font-display);
  font-size: 17px; font-weight: 700;
  color: var(--text-main);
}
.mod-desc {
  font-size: 13px; color: var(--text-muted); line-height: 1.5;
}
.mod-footer {
  margin-top: auto;
  font-size: 12.5px; font-weight: 600;
  color: var(--accent-cyan);
  display: flex; align-items: center; gap: 4px;
}

/* How TrustGuard Works section */
.how-it-works-box {
  margin-top: 60px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 36px;
}
.section-heading {
  font-family: var(--font-display);
  font-size: 22px; font-weight: 700;
  color: var(--text-main);
  margin-bottom: 8px;
}
.section-sub {
  font-size: 14px; color: var(--text-muted); margin-bottom: 28px;
}
.steps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 20px;
}
.step-item {
  display: flex; flex-direction: column; gap: 8px;
}
.step-num {
  font-family: var(--font-mono);
  font-size: 12px; font-weight: 700;
  color: var(--accent-cyan);
  background: rgba(56, 189, 248, 0.1);
  padding: 4px 10px; border-radius: 4px;
  width: fit-content;
}
.step-title {
  font-size: 14.5px; font-weight: 600; color: var(--text-main);
}
.step-desc {
  font-size: 12.5px; color: var(--text-muted); line-height: 1.45;
}

/* ============ SCANNER LAYOUT: INPUT & UNIFIED RESULT ============ */
.scanner-split-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
  align-items: start;
}
@media (max-width: 960px) {
  .scanner-split-layout { grid-template-columns: 1fr; }
}

.panel-box {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 26px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.panel-header h2 {
  font-family: var(--font-display);
  font-size: 20px; font-weight: 700;
  color: var(--text-main);
}
.panel-header p {
  font-size: 13px; color: var(--text-muted); margin-top: 4px;
}

/* Drag & Drop Upload Box */
.dropzone {
  border: 2px dashed var(--border);
  border-radius: var(--radius-sm);
  padding: 36px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  background: rgba(15, 23, 42, 0.4);
}
.dropzone:hover, .dropzone.dragover {
  border-color: var(--accent-cyan);
  background: rgba(56, 189, 248, 0.05);
}
.drop-icon { font-size: 32px; margin-bottom: 10px; }
.drop-title { font-size: 14.5px; font-weight: 600; color: var(--text-main); margin-bottom: 4px; }
.drop-sub { font-size: 12px; color: var(--text-muted); }

/* Media Preview container */
.preview-box {
  border-radius: var(--radius-sm);
  overflow: hidden;
  border: 1px solid var(--border);
  background: #000;
  max-height: 280px;
  display: none;
  position: relative;
}
.preview-box img, .preview-box video {
  width: 100%; height: 280px; object-fit: contain; display: block;
}

/* Inputs & Form Controls */
.text-input-area {
  width: 100%;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 14px;
  color: var(--text-main);
  font-family: var(--font-body);
  font-size: 14px;
  resize: vertical;
  min-height: 140px;
  outline: none;
}
.text-input-area:focus { border-color: var(--border-focus); }

.form-group {
  display: flex; flex-direction: column; gap: 6px;
}
.form-label {
  font-size: 12px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px;
}
.form-input {
  width: 100%;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  color: var(--text-main);
  font-family: var(--font-body);
  font-size: 14px;
  outline: none;
}
.form-input:focus { border-color: var(--border-focus); }

/* ============ UNIFIED 5-PART RESULT COMPONENT ============ */
.result-placeholder {
  min-height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px;
  color: var(--text-faint);
}
.result-placeholder-icon { font-size: 40px; margin-bottom: 12px; opacity: 0.6; }

.unified-result-card {
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: fadeIn 0.3s ease-out;
}

/* Part 1: Status Hero Banner */
.result-status-banner {
  padding: 20px 24px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid transparent;
}
.result-status-banner.status-real {
  background: rgba(16, 185, 129, 0.12);
  border-color: rgba(16, 185, 129, 0.35);
  color: var(--trust-high);
}
.result-status-banner.status-fake {
  background: rgba(239, 68, 68, 0.12);
  border-color: rgba(239, 68, 68, 0.35);
  color: var(--trust-low);
}
.result-status-banner.status-suspicious {
  background: rgba(245, 158, 11, 0.12);
  border-color: rgba(245, 158, 11, 0.35);
  color: var(--trust-uncertain);
}
.result-status-banner.status-uncertain {
  background: rgba(148, 163, 184, 0.12);
  border-color: rgba(148, 163, 184, 0.35);
  color: #cbd5e1;
}

.status-title {
  font-family: var(--font-display);
  font-size: 22px; font-weight: 800; letter-spacing: -0.2px;
}
.status-desc {
  font-size: 13px; opacity: 0.9; margin-top: 3px; font-family: var(--font-body);
}

/* Part 2: Trust Score & Confidence Cards */
.result-scores-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.score-stat-box {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.score-stat-label {
  font-size: 11.5px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.6px; color: var(--text-muted);
}
.score-stat-val {
  font-family: var(--font-display);
  font-size: 32px; font-weight: 800; line-height: 1.1;
}
.score-stat-tag {
  font-family: var(--font-mono);
  font-size: 11.5px; font-weight: 700;
  width: fit-content;
  padding: 2px 8px; border-radius: 4px;
}
.tag-high { background: rgba(16, 185, 129, 0.15); color: var(--trust-high); }
.tag-likely { background: rgba(5, 150, 105, 0.15); color: #34d399; }
.tag-uncertain { background: rgba(245, 158, 11, 0.15); color: var(--trust-uncertain); }
.tag-low { background: rgba(239, 68, 68, 0.15); color: var(--trust-low); }

/* Part 3: What We Found (Evidence List) */
.evidence-section {
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 18px 20px;
}
.evidence-title {
  font-size: 12.5px; font-weight: 700; color: var(--text-main); text-transform: uppercase; letter-spacing: 0.6px;
  margin-bottom: 12px; display: flex; align-items: center; gap: 8px;
}
.evidence-list {
  display: flex; flex-direction: column; gap: 8px; list-style: none;
}
.evidence-item {
  font-size: 13.5px; color: var(--text-muted); line-height: 1.5;
  display: flex; align-items: flex-start; gap: 8px;
}
.evidence-item span {
  color: var(--accent-cyan); font-weight: bold;
}

/* Part 4: Why This Result? */
.why-section {
  padding: 16px 20px;
  border-left: 3px solid var(--accent-cyan);
  background: rgba(56, 189, 248, 0.04);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}
.why-title {
  font-size: 12.5px; font-weight: 700; color: var(--accent-cyan); text-transform: uppercase; letter-spacing: 0.6px;
  margin-bottom: 6px;
}
.why-text {
  font-size: 13.5px; color: var(--text-main); line-height: 1.55;
}

/* Part 5: Technical Details (Expandable) */
.tech-details-box {
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  overflow: hidden;
}
.tech-summary-btn {
  padding: 12px 18px;
  background: rgba(15, 23, 42, 0.6);
  display: flex; align-items: center; justify-content: space-between;
  cursor: pointer; font-size: 12.5px; font-weight: 600; color: var(--text-muted);
}
.tech-content {
  padding: 14px 18px;
  background: rgba(15, 23, 42, 0.3);
  border-top: 1px solid var(--border);
  display: grid; grid-template-columns: 1fr 1fr; gap: 10px;
  font-size: 12.5px;
}
.tech-row { display: flex; flex-direction: column; gap: 2px; }
.tech-key { color: var(--text-faint); font-size: 11px; text-transform: uppercase; }
.tech-val { color: var(--text-main); font-family: var(--font-mono); }

/* Part 6: Transparency & Limitations */
.limitations-box {
  padding: 14px 18px;
  border-radius: var(--radius-sm);
  background: rgba(245, 158, 11, 0.06);
  border: 1px solid rgba(245, 158, 11, 0.2);
  font-size: 12.5px; color: #fbbf24; line-height: 1.5;
}

/* ============ VIDEO TIMELINE ============ */
.timeline-container {
  margin-top: 14px;
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding: 10px 4px 14px;
}
.timeline-card {
  min-width: 100px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 10px;
  cursor: pointer;
  text-align: center;
  transition: all 0.2s ease;
}
.timeline-card:hover {
  border-color: var(--accent-cyan);
  transform: translateY(-2px);
}
.timeline-card.fake {
  border-color: rgba(239, 68, 68, 0.5);
  background: rgba(239, 68, 68, 0.08);
}
.timeline-time { font-family: var(--font-mono); font-size: 11px; color: var(--text-muted); }
.timeline-status { font-size: 11.5px; font-weight: 700; margin-top: 4px; }
.timeline-status.fake { color: var(--trust-low); }
.timeline-status.real { color: var(--trust-high); }

/* ============ WEBCAM / AUDIO RECORDER STYLES ============ */
.camera-view-container {
  width: 100%;
  border-radius: var(--radius-sm);
  overflow: hidden;
  background: #000;
  aspect-ratio: 16/9;
  position: relative;
  border: 1px solid var(--border);
}
.camera-video { width: 100%; height: 100%; object-fit: cover; }
.camera-controls {
  display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-top: 12px;
}

.recorder-box {
  padding: 32px 20px;
  text-align: center;
  border-radius: var(--radius-sm);
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid var(--border);
  display: flex; flex-direction: column; align-items: center; gap: 14px;
}
.record-pulse-btn {
  width: 68px; height: 68px; border-radius: 50%;
  background: #ef4444; border: none; color: #fff;
  font-size: 26px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
  transition: all 0.2s ease;
}
.record-pulse-btn.recording {
  animation: pulse 1.5s infinite;
  background: #dc2626;
}
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
  70% { box-shadow: 0 0 0 16px rgba(239, 68, 68, 0); }
  100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}
.record-timer {
  font-family: var(--font-mono); font-size: 22px; font-weight: 700; color: var(--text-main);
}

/* ============ SCAN HISTORY TABLE ============ */
.history-table-wrap {
  overflow-x: auto;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  background: var(--bg-card);
}
.clean-table {
  width: 100%; border-collapse: collapse; font-size: 13.5px;
}
.clean-table th {
  background: rgba(15, 23, 42, 0.8);
  padding: 14px 18px;
  text-align: left;
  font-size: 11.5px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.6px;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border);
}
.clean-table td {
  padding: 14px 18px;
  border-bottom: 1px solid var(--border);
  color: var(--text-main);
}
.clean-table tr:hover {
  background: var(--bg-card-hover);
}

/* Responsive collapse */
@media (max-width: 840px) {
  #sidebar { transform: translateX(-100%); }
  #sidebar.open { transform: translateX(0); }
  #main-content { margin-left: 0; }
  .menu-btn { display: block; }
  .views-container { padding: 20px 16px; }
  .hero-title { font-size: 30px; }
  .hero-sub { font-size: 15px; }
}
</style>
</head>
<body>

<div class="bg-ambient"></div>

<!-- Top Offline Alert Banner -->
<div id="offline-alert">
  <span>● TrustGuard AI Backend is offline (127.0.0.1:8000). Start the server to perform AI inferences.</span>
  <button class="retry-btn" onclick="checkBackendHealth()">Retry Connection</button>
</div>

<div id="app-root">
  <!-- SIDEBAR NAVIGATION -->
  <aside id="sidebar">
    <div class="brand-section">
      <div class="brand-logo">T</div>
      <div class="brand-text">
        <h1>TrustGuard AI</h1>
        <p>Content Authenticity Engine</p>
      </div>
    </div>

    <nav class="nav-menu">
      <div class="nav-group-title">Analysis Modules</div>
      <div class="nav-item active" data-page="home" onclick="navigateTo('home')">
        <span class="nav-icon">🏠</span> Home
      </div>
      <div class="nav-item" data-page="image" onclick="navigateTo('image')">
        <span class="nav-icon">🖼</span> Image
      </div>
      <div class="nav-item" data-page="video" onclick="navigateTo('video')">
        <span class="nav-icon">🎬</span> Video
      </div>
      <div class="nav-item" data-page="audio" onclick="navigateTo('audio')">
        <span class="nav-icon">🎙</span> Audio
      </div>
      <div class="nav-item" data-page="text" onclick="navigateTo('text')">
        <span class="nav-icon">✉️</span> Text Scam
      </div>
      <div class="nav-item" data-page="job" onclick="navigateTo('job')">
        <span class="nav-icon">💼</span> Job / Internship
      </div>
      <div class="nav-item" data-page="url" onclick="navigateTo('url')">
        <span class="nav-icon">🔗</span> URL Trust
      </div>

      <div class="nav-group-title">Live Capture</div>
      <div class="nav-item" data-page="camera" onclick="navigateTo('camera')">
        <span class="nav-icon">📷</span> Live Camera
      </div>
      <div class="nav-item" data-page="voice" onclick="navigateTo('voice')">
        <span class="nav-icon">🗣</span> Live Voice
      </div>

      <div class="nav-group-title">Records & System</div>
      <div class="nav-item" data-page="history" onclick="navigateTo('history')">
        <span class="nav-icon">📊</span> Scan History
      </div>
      <div class="nav-item" data-page="about" onclick="navigateTo('about')">
        <span class="nav-icon">ℹ️</span> About Platform
      </div>
    </nav>

    <div class="sidebar-footer">
      <div class="engine-status-pill">
        <span class="status-dot" id="engine-dot"></span>
        <span id="engine-status-text">Connecting to Engine...</span>
      </div>
    </div>
  </aside>

  <!-- MAIN VIEWPORT -->
  <main id="main-content">
    <header class="top-bar">
      <div class="top-left">
        <button class="menu-btn" onclick="toggleSidebar()">☰</button>
        <div class="page-title-crumb" id="current-page-title">Home Dashboard</div>
      </div>
      <div class="top-right">
        <button class="theme-btn" onclick="toggleTheme()" id="theme-toggle-btn" title="Toggle dark/light theme">🌓</button>
        <div class="user-badge" id="auth-badge" onclick="handleAuthBadgeClick()">
          <span>👤</span> <span id="user-display-name">Guest User</span>
        </div>
      </div>
    </header>

    <div class="views-container">
      
      <!-- ================= 1. HOME VIEW ================= -->
      <section id="view-home" class="page-view active">
        <div class="hero-section">
          <div class="hero-badge">✨ Multimodal Digital Authenticity & Forensics</div>
          <h1 class="hero-title">AI-Powered Digital Content Authenticity & Trust Detection</h1>
          <p class="hero-sub">Analyze images, videos, audio, text and digital offers to identify AI-generated, manipulated and suspicious content within seconds.</p>
          <div class="hero-actions">
            <button class="btn-primary" onclick="navigateTo('image')"><span>🔍</span> Analyze Content</button>
            <button class="btn-secondary" onclick="navigateTo('camera')"><span>📷</span> Live Camera</button>
            <button class="btn-secondary" onclick="navigateTo('voice')"><span>🎙</span> Live Voice</button>
          </div>
        </div>

        <div class="modality-grid">
          <div class="modality-card" onclick="navigateTo('image')">
            <div class="mod-icon-wrap">🖼</div>
            <div class="mod-title">Image Authenticity</div>
            <div class="mod-desc">Pretrained Vision Transformer (ViT) & Error Level Analysis (ELA) detects generative textures & synthetic smoothing.</div>
            <div class="mod-footer">Analyze Image ➔</div>
          </div>

          <div class="modality-card" onclick="navigateTo('video')">
            <div class="mod-icon-wrap">🎬</div>
            <div class="mod-title">Video Deepfake</div>
            <div class="mod-desc">OpenCV frame extraction with facial crop tracking & temporal consistency aggregation across keyframes.</div>
            <div class="mod-footer">Analyze Video ➔</div>
          </div>

          <div class="modality-card" onclick="navigateTo('audio')">
            <div class="mod-icon-wrap">🎙</div>
            <div class="mod-title">Audio / Voice Forensics</div>
            <div class="mod-desc">STFT spectral centroid variance, spectral flux, and vocoder roll-off signatures isolate AI voice clones.</div>
            <div class="mod-footer">Analyze Audio ➔</div>
          </div>

          <div class="modality-card" onclick="navigateTo('text')">
            <div class="mod-icon-wrap">✉️</div>
            <div class="mod-title">Text & Scam Detection</div>
            <div class="mod-desc">Identifies credential/OTP phishing, wire transfer & crypto solicitation, and coercive urgency patterns.</div>
            <div class="mod-footer">Analyze Message ➔</div>
          </div>

          <div class="modality-card" onclick="navigateTo('job')">
            <div class="mod-icon-wrap">💼</div>
            <div class="mod-title">Job & Internship Verifier</div>
            <div class="mod-desc">Flags upfront deposit demands, unrealistic salary claims, and unofficial recruiter email domains.</div>
            <div class="mod-footer">Verify Offer ➔</div>
          </div>

          <div class="modality-card" onclick="navigateTo('url')">
            <div class="mod-icon-wrap">🔗</div>
            <div class="mod-title">URL Trust Scanner</div>
            <div class="mod-desc">Shannon entropy analysis, suspicious TLD detection, typosquatting, and credential harvesting paths.</div>
            <div class="mod-footer">Scan URL ➔</div>
          </div>
        </div>

        <!-- How It Works -->
        <div class="how-it-works-box">
          <h2 class="section-heading">How TrustGuard Works</h2>
          <p class="section-sub">A transparent, multi-signal pipeline designed to give you clarity and confidence.</p>
          <div class="steps-grid">
            <div class="step-item">
              <span class="step-num">Step 01</span>
              <div class="step-title">Upload or Capture</div>
              <div class="step-desc">Provide your image, video, audio file, message, or use your live webcam/microphone.</div>
            </div>
            <div class="step-item">
              <span class="step-num">Step 02</span>
              <div class="step-title">AI Preprocessing</div>
              <div class="step-desc">Content is normalized, sampled into keyframes, or divided into spectral frequency windows.</div>
            </div>
            <div class="step-item">
              <span class="step-num">Step 03</span>
              <div class="step-title">Multimodal Inference</div>
              <div class="step-desc">Deep neural transformers and forensic heuristics inspect high-frequency anomalies.</div>
            </div>
            <div class="step-item">
              <span class="step-num">Step 04</span>
              <div class="step-title">Evidence Extraction</div>
              <div class="step-desc">Real detected signals are gathered into verifiable observations with zero hallucinations.</div>
            </div>
            <div class="step-item">
              <span class="step-num">Step 05</span>
              <div class="step-title">Unified Trust Score</div>
              <div class="step-desc">A deterministic 0–100 score indicates content authenticity and trustworthiness.</div>
            </div>
            <div class="step-item">
              <span class="step-num">Step 06</span>
              <div class="step-title">Transparent Result</div>
              <div class="step-desc">Clear classification (Real, AI, Manipulated, Suspicious, or Uncertain) with limitations stated.</div>
            </div>
          </div>
        </div>
      </section>

      <!-- ================= 2. IMAGE VIEW ================= -->
      <section id="view-image" class="page-view">
        <div class="scanner-split-layout">
          <div class="panel-box">
            <div class="panel-header">
              <h2>Image Authenticity Analyzer</h2>
              <p>Upload any picture to evaluate whether it is authentic, AI-generated, or manipulated.</p>
            </div>

            <div class="dropzone" id="image-dropzone" onclick="document.getElementById('image-file-input').click()">
              <div class="drop-icon">📁</div>
              <div class="drop-title">Click to upload or drag & drop</div>
              <div class="drop-sub">Supported formats: JPG, JPEG, PNG, WEBP (Max 15MB)</div>
              <input type="file" id="image-file-input" accept="image/jpeg,image/png,image/webp" style="display:none" onchange="handleImageSelected(this)">
            </div>

            <div class="preview-box" id="image-preview-wrap">
              <img id="image-preview-img" src="" alt="Image Preview">
            </div>

            <button class="btn-primary" id="btn-analyze-image" onclick="runImageAnalysis()" style="width:100%">
              <span>🔍</span> Analyze Image
            </button>
          </div>

          <!-- Result Container -->
          <div class="panel-box" id="image-result-panel">
            <div class="result-placeholder" id="image-placeholder">
              <div class="result-placeholder-icon">🖼</div>
              <div style="font-weight:600; margin-bottom:4px;">No image analyzed yet</div>
              <div style="font-size:13px;">Upload an image on the left and click Analyze Image to view the authenticity breakdown.</div>
            </div>
            <div id="image-result-content" style="display:none"></div>
          </div>
        </div>
      </section>

      <!-- ================= 3. VIDEO VIEW ================= -->
      <section id="view-video" class="page-view">
        <div class="scanner-split-layout">
          <div class="panel-box">
            <div class="panel-header">
              <h2>Video Authenticity Analyzer</h2>
              <p>Extracts temporal frames, performs ViT inference per frame, and tracks facial consistency.</p>
            </div>

            <div class="dropzone" id="video-dropzone" onclick="document.getElementById('video-file-input').click()">
              <div class="drop-icon">🎬</div>
              <div class="drop-title">Click to upload video file</div>
              <div class="drop-sub">Supported formats: MP4, AVI, MOV, WEBM</div>
              <input type="file" id="video-file-input" accept="video/mp4,video/quicktime,video/webm,video/x-msvideo" style="display:none" onchange="handleVideoSelected(this)">
            </div>

            <div class="preview-box" id="video-preview-wrap">
              <video id="video-preview-player" controls></video>
            </div>

            <button class="btn-primary" id="btn-analyze-video" onclick="runVideoAnalysis()" style="width:100%">
              <span>🎬</span> Analyze Video
            </button>
          </div>

          <!-- Result Container -->
          <div class="panel-box" id="video-result-panel">
            <div class="result-placeholder" id="video-placeholder">
              <div class="result-placeholder-icon">🎬</div>
              <div style="font-weight:600; margin-bottom:4px;">No video analyzed yet</div>
              <div style="font-size:13px;">Upload a video to evaluate keyframe consistency and deepfake indicators.</div>
            </div>
            <div id="video-result-content" style="display:none"></div>
          </div>
        </div>
      </section>

      <!-- ================= 4. AUDIO VIEW ================= -->
      <section id="view-audio" class="page-view">
        <div class="scanner-split-layout">
          <div class="panel-box">
            <div class="panel-header">
              <h2>Voice & Audio Authenticity</h2>
              <p>Inspects vocal tract spectral centroid variance, flux, and vocoder harmonic cutoffs.</p>
            </div>

            <div class="dropzone" id="audio-dropzone" onclick="document.getElementById('audio-file-input').click()">
              <div class="drop-icon">🎙</div>
              <div class="drop-title">Click to upload audio file</div>
              <div class="drop-sub">Supported formats: WAV, MP3, M4A, FLAC</div>
              <input type="file" id="audio-file-input" accept="audio/*" style="display:none" onchange="handleAudioSelected(this)">
            </div>

            <div id="audio-player-wrap" style="display:none; padding:12px; background:rgba(15,23,42,0.6); border-radius:var(--radius-sm); border:1px solid var(--border);">
              <audio id="audio-player" controls style="width:100%"></audio>
            </div>

            <button class="btn-primary" id="btn-analyze-audio" onclick="runAudioAnalysis()" style="width:100%">
              <span>🎙</span> Analyze Audio
            </button>
          </div>

          <!-- Result Container -->
          <div class="panel-box" id="audio-result-panel">
            <div class="result-placeholder" id="audio-placeholder">
              <div class="result-placeholder-icon">🎙</div>
              <div style="font-weight:600; margin-bottom:4px;">No audio analyzed yet</div>
              <div style="font-size:13px;">Upload a voice recording to check for AI cloning or synthetic vocoder artifacts.</div>
            </div>
            <div id="audio-result-content" style="display:none"></div>
          </div>
        </div>
      </section>

      <!-- ================= 5. TEXT VIEW ================= -->
      <section id="view-text" class="page-view">
        <div class="scanner-split-layout">
          <div class="panel-box">
            <div class="panel-header">
              <h2>Text Authenticity & Scam Analyzer</h2>
              <p>Paste suspicious messages, SMS, WhatsApp texts, or emails to detect fraudulent solicitation.</p>
            </div>

            <textarea class="text-input-area" id="text-input" placeholder="Paste SMS, WhatsApp message, email, or digital offer here..."></textarea>

            <button class="btn-primary" id="btn-analyze-text" onclick="runTextAnalysis()" style="width:100%">
              <span>✉️</span> Analyze Text
            </button>
          </div>

          <!-- Result Container -->
          <div class="panel-box" id="text-result-panel">
            <div class="result-placeholder" id="text-placeholder">
              <div class="result-placeholder-icon">✉️</div>
              <div style="font-weight:600; margin-bottom:4px;">No text analyzed yet</div>
              <div style="font-size:13px;">Paste a message on the left to inspect psychological coercion and scam vectors.</div>
            </div>
            <div id="text-result-content" style="display:none"></div>
          </div>
        </div>
      </section>

      <!-- ================= 6. JOB / INTERNSHIP VIEW ================= -->
      <section id="view-job" class="page-view">
        <div class="scanner-split-layout">
          <div class="panel-box">
            <div class="panel-header">
              <h2>Job & Internship Scam Verifier</h2>
              <p>Evaluates recruitment offers for advance fee demands, salary discrepancies, and recruiter email legitimacy.</p>
            </div>

            <div class="form-group">
              <label class="form-label">Job or Internship Description</label>
              <textarea class="text-input-area" id="job-desc-input" placeholder="Paste job advertisement description, requirements, or stipend details..."></textarea>
            </div>

            <div class="form-group">
              <label class="form-label">Recruiter Contact Email (Optional)</label>
              <input type="email" class="form-input" id="job-email-input" placeholder="e.g. hr@company.com or recruiter@gmail.com">
            </div>

            <div class="form-group">
              <label class="form-label">Application URL or Website (Optional)</label>
              <input type="text" class="form-input" id="job-url-input" placeholder="https://careers.example.com">
            </div>

            <div style="display:flex; gap:12px;">
              <button class="btn-primary" id="btn-analyze-job" onclick="runJobAnalysis(false)" style="flex:1">
                Verify Job
              </button>
              <button class="btn-secondary" id="btn-analyze-internship" onclick="runJobAnalysis(true)" style="flex:1">
                Verify Internship
              </button>
            </div>
          </div>

          <!-- Result Container -->
          <div class="panel-box" id="job-result-panel">
            <div class="result-placeholder" id="job-placeholder">
              <div class="result-placeholder-icon">💼</div>
              <div style="font-weight:600; margin-bottom:4px;">No offer analyzed yet</div>
              <div style="font-size:13px;">Enter job details to evaluate whether it represents a legitimate career opportunity.</div>
            </div>
            <div id="job-result-content" style="display:none"></div>
          </div>
        </div>
      </section>

      <!-- ================= 7. URL VIEW ================= -->
      <section id="view-url" class="page-view">
        <div class="scanner-split-layout">
          <div class="panel-box">
            <div class="panel-header">
              <h2>URL Trust Analyzer</h2>
              <p>Evaluates domain structure, typosquatting patterns, IP hosts, and phishing indicators.</p>
            </div>

            <div class="form-group">
              <label class="form-label">Target Web Address (URL)</label>
              <input type="text" class="form-input" id="url-input" placeholder="https://example.com/verify-account">
            </div>

            <button class="btn-primary" id="btn-analyze-url" onclick="runUrlAnalysis()" style="width:100%">
              <span>🔗</span> Analyze URL
            </button>
          </div>

          <!-- Result Container -->
          <div class="panel-box" id="url-result-panel">
            <div class="result-placeholder" id="url-placeholder">
              <div class="result-placeholder-icon">🔗</div>
              <div style="font-weight:600; margin-bottom:4px;">No URL analyzed yet</div>
              <div style="font-size:13px;">Enter a URL to evaluate its safety and domain trust characteristics.</div>
            </div>
            <div id="url-result-content" style="display:none"></div>
          </div>
        </div>
      </section>

      <!-- ================= 8. LIVE CAMERA VIEW ================= -->
      <section id="view-camera" class="page-view">
        <div class="scanner-split-layout">
          <div class="panel-box">
            <div class="panel-header">
              <h2>Live Camera Authenticity Check</h2>
              <p>Connect your camera to capture live frames and verify content authenticity using Vision Transformer.</p>
            </div>

            <div class="camera-view-container">
              <video class="camera-video" id="camera-feed" autoplay playsinline></video>
              <canvas id="camera-canvas" style="display:none;"></canvas>
            </div>

            <div class="camera-controls">
              <button class="btn-secondary" id="btn-start-camera" onclick="startCamera()"><span>📷</span> Start Camera</button>
              <button class="btn-secondary" id="btn-capture-frame" onclick="captureCameraSnapshot()" disabled><span>📸</span> Capture Frame</button>
              <button class="btn-primary" id="btn-analyze-camera" onclick="runCameraAnalysis()" disabled><span>🔍</span> Analyze Frame</button>
            </div>
          </div>

          <!-- Result Container -->
          <div class="panel-box" id="camera-result-panel">
            <div class="result-placeholder" id="camera-placeholder">
              <div class="result-placeholder-icon">📷</div>
              <div style="font-weight:600; margin-bottom:4px;">Camera standby</div>
              <div style="font-size:13px;">Start your camera, capture a frame, and analyze to inspect live content authenticity.</div>
            </div>
            <div id="camera-result-content" style="display:none"></div>
          </div>
        </div>
      </section>

      <!-- ================= 9. LIVE VOICE VIEW ================= -->
      <section id="view-voice" class="page-view">
        <div class="scanner-split-layout">
          <div class="panel-box">
            <div class="panel-header">
              <h2>Live Voice Authenticity</h2>
              <p>Record your voice through your browser microphone to detect synthetic voice cloning indicators.</p>
            </div>

            <div class="recorder-box">
              <button class="record-pulse-btn" id="voice-record-btn" onclick="toggleVoiceRecording()">
                🎙
              </button>
              <div class="record-timer" id="voice-timer">00:00</div>
              <div style="font-size:13px; color:var(--text-muted);" id="voice-status-note">Click the microphone to start recording</div>
            </div>

            <button class="btn-primary" id="btn-analyze-voice" onclick="runRecordedVoiceAnalysis()" disabled style="width:100%">
              <span>🗣</span> Stop & Analyze Voice
            </button>
          </div>

          <!-- Result Container -->
          <div class="panel-box" id="voice-result-panel">
            <div class="result-placeholder" id="voice-placeholder">
              <div class="result-placeholder-icon">🗣</div>
              <div style="font-weight:600; margin-bottom:4px;">Microphone standby</div>
              <div style="font-size:13px;">Record a brief voice sample to evaluate natural vocal tract characteristics.</div>
            </div>
            <div id="voice-result-content" style="display:none"></div>
          </div>
        </div>
      </section>

      <!-- ================= 10. SCAN HISTORY VIEW ================= -->
      <section id="view-history" class="page-view">
        <div class="panel-box" style="margin-bottom:20px;">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
            <div>
              <h2 style="font-family:var(--font-display); font-size:20px;">Verified Scan History</h2>
              <p style="font-size:13px; color:var(--text-muted);">Synchronized directly with local SQLite database records.</p>
            </div>
            <button class="btn-secondary" onclick="fetchScanHistory()" style="padding:8px 16px;"><span>🔄</span> Refresh</button>
          </div>
        </div>

        <div class="history-table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Modality</th>
                <th>Content / Subject</th>
                <th>Classification</th>
                <th>Trust Score</th>
                <th>Confidence</th>
              </tr>
            </thead>
            <tbody id="history-table-body">
              <tr><td colspan="6" style="text-align:center; padding:32px; color:var(--text-faint);">Loading history...</td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- ================= 11. ABOUT VIEW ================= -->
      <section id="view-about" class="page-view">
        <div class="panel-box" style="max-width:840px; margin:0 auto;">
          <div class="panel-header">
            <h2>About TrustGuard AI</h2>
            <p>Multimodal AI Content Authenticity & Digital Trust Platform</p>
          </div>

          <div style="font-size:14.5px; color:var(--text-muted); line-height:1.7; display:flex; flex-direction:column; gap:16px;">
            <p>
              TrustGuard AI is an AI-powered authenticity detection platform designed to evaluate images, videos, audio recordings, text messages, job offers, and web links. As generative AI models advance in realism, distinguishing between organic digital content and synthetic alterations has become essential for users, researchers, and organizations.
            </p>

            <h3 style="font-family:var(--font-display); font-size:17px; color:var(--text-main); margin-top:8px;">Core Design Principles</h3>
            <ul style="padding-left:20px; display:flex; flex-direction:column; gap:8px;">
              <li><strong>Transparency First:</strong> Rather than returning opaque judgments, TrustGuard exposes detected evidence, model architectures, and processing parameters.</li>
              <li><strong>Unified Trust Score:</strong> All modalities produce a standardized 0–100 Trust Score representing evidence-based authenticity.</li>
              <li><strong>Humility & Uncertainty:</strong> When model confidence is inconclusive, the system explicitly reports <em>UNCERTAIN</em> rather than forcing a misleading binary decision.</li>
            </ul>

            <h3 style="font-family:var(--font-display); font-size:17px; color:var(--text-main); margin-top:8px;">Supported AI Architectures</h3>
            <ul style="padding-left:20px; display:flex; flex-direction:column; gap:8px;">
              <li><strong>Vision:</strong> Pretrained Hugging Face Vision Transformer (ViT) paired with Error Level Analysis (ELA) and Laplacian gradient variance.</li>
              <li><strong>Video:</strong> OpenCV temporal keyframe extraction with facial bounding crops and temporal consistency scoring.</li>
              <li><strong>Audio:</strong> Short-Time Fourier Transform (STFT) spectral centroid analysis, spectral flux, and high-frequency vocoder harmonic forensics.</li>
              <li><strong>Language & Security:</strong> Multilingual regular expression heuristics for OTP harvesting, urgency coercion, and domain entropy scoring.</li>
            </ul>

            <div class="limitations-box" style="margin-top:10px;">
              <strong>Scientific & Ethical Disclaimer:</strong><br>
              AI-generated content detection is probabilistic. No automated detector can provide absolute certainty from visual or acoustic analysis alone. Results should be interpreted as evidence-based assessments to guide human review, not definitive legal proof.
            </div>
          </div>
        </div>
      </section>

    </div>
  </main>
</div>

<!-- ============================================================ -->
<!-- CENTRALIZED JAVASCRIPT CLIENT LOGIC -->
<!-- ============================================================ -->
<script>
/* ============ CONFIGURATION ============ */
// Dynamically resolve API base to support 127.0.0.1, localhost, or host headers
const API_BASE = window.location.origin.includes(':8000')
  ? `${window.location.origin}/api`
  : 'http://127.0.0.1:8000/api';

let activePage = 'home';
let currentUser = null;
let isBackendConnected = false;

/* ============ ROUTING ============ */
const PAGE_TITLES = {
  'home': 'Home Dashboard',
  'image': 'Image Authenticity Analyzer',
  'video': 'Video Deepfake Analyzer',
  'audio': 'Voice & Audio Forensics',
  'text': 'Text & Scam Detection',
  'job': 'Job & Internship Verifier',
  'url': 'URL Trust Analyzer',
  'camera': 'Live Camera Authenticity',
  'voice': 'Live Voice Authenticity',
  'history': 'Verified Scan History',
  'about': 'About Platform'
};

function navigateTo(pageId, pushState = true) {
  if (!PAGE_TITLES[pageId]) pageId = 'home';
  activePage = pageId;

  document.querySelectorAll('.page-view').forEach(el => el.classList.remove('active'));
  const targetView = document.getElementById(`view-${pageId}`);
  if (targetView) targetView.classList.add('active');

  document.querySelectorAll('.nav-item').forEach(el => {
    if (el.dataset.page === pageId) el.classList.add('active');
    else el.classList.remove('active');
  });

  const titleEl = document.getElementById('current-page-title');
  if (titleEl) titleEl.textContent = PAGE_TITLES[pageId];

  // Mobile sidebar auto-close
  const sidebar = document.getElementById('sidebar');
  if (window.innerWidth <= 840 && sidebar.classList.contains('open')) {
    sidebar.classList.remove('open');
  }

  if (pageId === 'history') {
    fetchScanHistory();
  }

  if (pushState) {
    try { history.pushState({ page: pageId }, '', pageId === 'home' ? '/' : `/${pageId}`); } catch(e) {}
  }
}

window.addEventListener('popstate', (e) => {
  const target = (e.state && e.state.page) ? e.state.page : 'home';
  navigateTo(target, false);
});

function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('tg_theme', next);
}

/* ============ HEALTH CHECK & TELEMETRY ============ */
async function checkBackendHealth() {
  const dot = document.getElementById('engine-dot');
  const txt = document.getElementById('engine-status-text');
  const alert = document.getElementById('offline-alert');

  try {
    const res = await fetch(`${API_BASE}/health`);
    if (res.ok) {
      isBackendConnected = true;
      if (dot) { dot.className = 'status-dot'; }
      if (txt) { txt.textContent = 'Authenticity Engine Ready'; }
      if (alert) { alert.classList.remove('show'); }
      return true;
    }
  } catch(err) {
    isBackendConnected = false;
    if (dot) { dot.className = 'status-dot offline'; }
    if (txt) { txt.textContent = 'Backend Offline'; }
    if (alert) { alert.classList.add('show'); }
    return false;
  }
}

/* ============ CENTRALIZED API HELPER ============ */
async function apiCall(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  try {
    const res = await fetch(url, options);
    if (!res.ok) {
      const errText = await res.text();
      let msg = errText;
      try { msg = JSON.parse(errText).detail || JSON.parse(errText).error || errText; } catch(e) {}
      throw new Error(msg);
    }
    return await res.json();
  } catch(err) {
    console.error(`API error at ${endpoint}:`, err);
    throw err;
  }
}

/* ============ UNIFIED 5-PART RESULT RENDERER ============ */
function renderUnifiedResult(containerId, placeholderId, res) {
  const container = document.getElementById(containerId);
  const placeholder = document.getElementById(placeholderId);
  if (placeholder) placeholder.style.display = 'none';
  if (!container) return;
  container.style.display = 'block';

  // Normalize fields
  const status = (res.status || res.classification || 'UNCERTAIN').toUpperCase();
  const statusLabel = res.status_label || res.classification_label || status;
  const trustScore = Math.round(res.trust_score !== undefined ? res.trust_score : (100.0 - (res.risk_score || 50)));
  const confidence = Math.round(res.confidence_pct || res.confidence || 80);
  const explanation = res.explanation || 'Authenticity evaluation completed.';
  const evidenceList = res.evidence || (res.indicators || []).map(i => `${i.label}: ${i.detail}`) || [];
  const technical = res.technical || {};
  const limitations = res.limitations || [
    "AI detection is probabilistic and may produce false positives or false negatives."
  ];

  // Map CSS classes & badges based on status & trust score
  let statusClass = 'status-uncertain';
  let tagClass = 'tag-uncertain';
  let trustTagText = res.trust_category || 'UNCERTAIN';

  if (status.includes('REAL') || status.includes('GENUINE') || trustScore >= 70) {
    statusClass = 'status-real';
    tagClass = trustScore >= 90 ? 'tag-high' : 'tag-likely';
  } else if (status.includes('AI') || status.includes('FAKE') || status.includes('SCAM') || trustScore < 40) {
    statusClass = 'status-fake';
    tagClass = 'tag-low';
  } else if (status.includes('SUSPICIOUS')) {
    statusClass = 'status-suspicious';
    tagClass = 'tag-uncertain';
  }

  // Evidence markup
  const evidenceMarkup = evidenceList.length > 0
    ? evidenceList.map(item => `<li class="evidence-item"><span>✓</span> ${item}</li>`).join('')
    : '<li class="evidence-item"><span>•</span> No specific anomalies detected.</li>';

  // Technical metadata markup
  const techRows = Object.entries(technical)
    .map(([k, v]) => `
      <div class="tech-row">
        <span class="tech-key">${k.replace(/_/g, ' ')}</span>
        <span class="tech-val">${v}</span>
      </div>
    `).join('');

  // Video frame timeline (if present)
  let timelineMarkup = '';
  if (res.frame_results && res.frame_results.length > 0) {
    timelineMarkup = `
      <div style="margin-top:14px;">
        <div style="font-size:12px; font-weight:700; color:var(--text-muted); text-transform:uppercase; margin-bottom:4px;">
          Sampled Frame Timeline (${res.frame_results.length} Frames)
        </div>
        <div class="timeline-container">
          ${res.frame_results.map(f => `
            <div class="timeline-card ${f.is_suspicious ? 'fake' : ''}" onclick="alert('Frame ${f.frame_number} at ${f.timestamp}s: ${f.prediction} (Risk: ${f.risk_score}/100, Confidence: ${f.confidence}%)')">
              <div class="timeline-time">${f.timestamp_label || f.timestamp + 's'}</div>
              <div class="timeline-status ${f.is_suspicious ? 'fake' : 'real'}">${f.prediction}</div>
              <div style="font-size:10.5px; color:var(--text-faint); margin-top:2px;">${f.confidence}%</div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  container.innerHTML = `
    <div class="unified-result-card">
      <!-- 1. Status Banner -->
      <div class="result-status-banner ${statusClass}">
        <div>
          <div class="status-title">${statusLabel}</div>
          <div class="status-desc">${status.includes('REAL') ? 'Verified authentic markers detected.' : status.includes('AI') ? 'Generative synthetic markers detected.' : 'Review detailed evidence below.'}</div>
        </div>
        <div style="font-size:32px;">
          ${status.includes('REAL') ? '✓' : status.includes('AI') || status.includes('SCAM') ? '⚠' : 'ℹ'}
        </div>
      </div>

      <!-- 2. Trust Score & Confidence -->
      <div class="result-scores-row">
        <div class="score-stat-box">
          <span class="score-stat-label">Trust Score</span>
          <div class="score-stat-val" style="color:${trustScore >= 70 ? 'var(--trust-high)' : trustScore < 40 ? 'var(--trust-low)' : 'var(--trust-uncertain)'};">
            ${trustScore} <span style="font-size:16px; color:var(--text-faint); font-weight:500;">/ 100</span>
          </div>
          <span class="score-stat-tag ${tagClass}">${trustTagText}</span>
        </div>

        <div class="score-stat-box">
          <span class="score-stat-label">Model Confidence</span>
          <div class="score-stat-val">${confidence}%</div>
          <span style="font-size:12px; color:var(--text-muted);">Inference certainty</span>
        </div>
      </div>

      <!-- 3. What We Found (Evidence) -->
      <div class="evidence-section">
        <div class="evidence-title">🔍 What We Found</div>
        <ul class="evidence-list">
          ${evidenceMarkup}
        </ul>
      </div>

      <!-- Video frame timeline if applicable -->
      ${timelineMarkup}

      <!-- 4. Why This Result? -->
      <div class="why-section">
        <div class="why-title">Why This Result?</div>
        <div class="why-text">${explanation}</div>
      </div>

      <!-- 5. Technical Details -->
      <div class="tech-details-box">
        <div class="tech-summary-btn" onclick="toggleTechDetails(this)">
          <span>⚙ Technical Analysis & Engine Details</span>
          <span class="chevron">▼</span>
        </div>
        <div class="tech-content" style="display:grid;">
          ${techRows || '<div class="tech-row"><span class="tech-key">Engine</span><span class="tech-val">TrustGuard Unified Pipeline</span></div>'}
        </div>
      </div>

      <!-- 6. Limitations & Disclaimer -->
      <div class="limitations-box">
        <strong>Transparency & Limitations:</strong><br>
        ${limitations.join(' ')}
      </div>
    </div>
  `;
}

function toggleTechDetails(btn) {
  const content = btn.nextElementSibling;
  const chevron = btn.querySelector('.chevron');
  if (content.style.display === 'none') {
    content.style.display = 'grid';
    chevron.textContent = '▼';
  } else {
    content.style.display = 'none';
    chevron.textContent = '▶';
  }
}

/* ============ 1. IMAGE ANALYZER ============ */
let currentImageFile = null;

function handleImageSelected(input) {
  if (input.files && input.files[0]) {
    currentImageFile = input.files[0];
    const preview = document.getElementById('image-preview-img');
    const wrap = document.getElementById('image-preview-wrap');
    preview.src = URL.createObjectURL(currentImageFile);
    wrap.style.display = 'block';
  }
}

async function runImageAnalysis() {
  if (!currentImageFile) {
    alert('Please select or drop an image file first.');
    return;
  }
  const btn = document.getElementById('btn-analyze-image');
  btn.disabled = true;
  btn.innerHTML = '<span>⏳</span> Analyzing Image Forensics...';

  try {
    const formData = new FormData();
    formData.append('file', currentImageFile);
    const res = await apiCall('/analyze/image', {
      method: 'POST',
      body: formData
    });
    renderUnifiedResult('image-result-content', 'image-placeholder', res);
  } catch(err) {
    alert(`Image Analysis Error: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>🔍</span> Analyze Image';
  }
}

/* ============ 2. VIDEO ANALYZER ============ */
let currentVideoFile = null;

function handleVideoSelected(input) {
  if (input.files && input.files[0]) {
    currentVideoFile = input.files[0];
    const player = document.getElementById('video-preview-player');
    const wrap = document.getElementById('video-preview-wrap');
    player.src = URL.createObjectURL(currentVideoFile);
    wrap.style.display = 'block';
  }
}

async function runVideoAnalysis() {
  if (!currentVideoFile) {
    alert('Please select a video file first.');
    return;
  }
  const btn = document.getElementById('btn-analyze-video');
  btn.disabled = true;
  btn.innerHTML = '<span>⏳</span> Extracting Frames & Analyzing...';

  try {
    const formData = new FormData();
    formData.append('file', currentVideoFile);
    const res = await apiCall('/analyze/video', {
      method: 'POST',
      body: formData
    });
    renderUnifiedResult('video-result-content', 'video-placeholder', res);
  } catch(err) {
    alert(`Video Analysis Error: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>🎬</span> Analyze Video';
  }
}

/* ============ 3. AUDIO ANALYZER ============ */
let currentAudioFile = null;

function handleAudioSelected(input) {
  if (input.files && input.files[0]) {
    currentAudioFile = input.files[0];
    const player = document.getElementById('audio-player');
    const wrap = document.getElementById('audio-player-wrap');
    player.src = URL.createObjectURL(currentAudioFile);
    wrap.style.display = 'block';
  }
}

async function runAudioAnalysis() {
  if (!currentAudioFile) {
    alert('Please select an audio file first.');
    return;
  }
  const btn = document.getElementById('btn-analyze-audio');
  btn.disabled = true;
  btn.innerHTML = '<span>⏳</span> Analyzing Acoustic Spectrum...';

  try {
    const formData = new FormData();
    formData.append('file', currentAudioFile);
    const res = await apiCall('/analyze/audio', {
      method: 'POST',
      body: formData
    });
    renderUnifiedResult('audio-result-content', 'audio-placeholder', res);
  } catch(err) {
    alert(`Audio Analysis Error: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>🎙</span> Analyze Audio';
  }
}

/* ============ 4. TEXT SCAM ANALYZER ============ */
async function runTextAnalysis() {
  const text = document.getElementById('text-input').value.trim();
  if (!text) {
    alert('Please paste message or text content first.');
    return;
  }
  const btn = document.getElementById('btn-analyze-text');
  btn.disabled = true;
  btn.innerHTML = '<span>⏳</span> Analyzing Text Markers...';

  try {
    const res = await apiCall('/analyze/text', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text })
    });
    renderUnifiedResult('text-result-content', 'text-placeholder', res);
  } catch(err) {
    alert(`Text Analysis Error: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>✉️</span> Analyze Text';
  }
}

/* ============ 5. JOB / INTERNSHIP VERIFIER ============ */
async function runJobAnalysis(isInternship = false) {
  const desc = document.getElementById('job-desc-input').value.trim();
  const email = document.getElementById('job-email-input').value.trim();
  const url = document.getElementById('job-url-input').value.trim();

  if (!desc && !email && !url) {
    alert('Please enter job description, recruiter email, or website.');
    return;
  }

  const btn = isInternship
    ? document.getElementById('btn-analyze-internship')
    : document.getElementById('btn-analyze-job');
  btn.disabled = true;
  btn.innerHTML = '<span>⏳</span> Verifying...';

  const endpoint = isInternship ? '/analyze/internship' : '/analyze/job';
  try {
    const res = await apiCall(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: desc, email: email, url: url })
    });
    renderUnifiedResult('job-result-content', 'job-placeholder', res);
  } catch(err) {
    alert(`Job Verification Error: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.innerHTML = isInternship ? 'Verify Internship' : 'Verify Job';
  }
}

/* ============ 6. URL ANALYZER ============ */
async function runUrlAnalysis() {
  const url = document.getElementById('url-input').value.trim();
  if (!url) {
    alert('Please enter a website or link URL.');
    return;
  }
  const btn = document.getElementById('btn-analyze-url');
  btn.disabled = true;
  btn.innerHTML = '<span>⏳</span> Inspecting Domain...';

  try {
    const res = await apiCall('/analyze/url', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: url })
    });
    renderUnifiedResult('url-result-content', 'url-placeholder', res);
  } catch(err) {
    alert(`URL Analysis Error: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>🔗</span> Analyze URL';
  }
}

/* ============ 7. LIVE CAMERA ============ */
let cameraStream = null;
let capturedBlob = null;

async function startCamera() {
  const video = document.getElementById('camera-feed');
  const startBtn = document.getElementById('btn-start-camera');
  const captureBtn = document.getElementById('btn-capture-frame');

  try {
    cameraStream = await navigator.mediaDevices.getUserMedia({
      video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: 'user' },
      audio: false
    });
    video.srcObject = cameraStream;
    startBtn.textContent = 'Camera Active';
    startBtn.disabled = true;
    captureBtn.disabled = false;
  } catch(err) {
    alert(`Could not access camera: ${err.message}. Please verify browser camera permissions.`);
  }
}

function captureCameraSnapshot() {
  const video = document.getElementById('camera-feed');
  const canvas = document.getElementById('camera-canvas');
  if (!video || !video.videoWidth) return;

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  canvas.toBlob((blob) => {
    capturedBlob = blob;
    document.getElementById('btn-analyze-camera').disabled = false;
    alert('Frame captured! Click "Analyze Frame" to evaluate content authenticity.');
  }, 'image/jpeg', 0.92);
}

async function runCameraAnalysis() {
  if (!capturedBlob) return;
  const btn = document.getElementById('btn-analyze-camera');
  btn.disabled = true;
  btn.innerHTML = '<span>⏳</span> Analyzing Frame...';

  try {
    const formData = new FormData();
    formData.append('file', capturedBlob, 'camera_frame.jpg');
    const res = await apiCall('/analyze/image', {
      method: 'POST',
      body: formData
    });
    renderUnifiedResult('camera-result-content', 'camera-placeholder', res);
  } catch(err) {
    alert(`Camera Frame Analysis Error: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>🔍</span> Analyze Frame';
  }
}

/* ============ 8. LIVE VOICE RECORDING ============ */
let mediaRecorder = null;
let recordedAudioChunks = [];
let voiceTimerInterval = null;
let voiceDurationSec = 0;
let recordedVoiceBlob = null;

async function toggleVoiceRecording() {
  const btn = document.getElementById('voice-record-btn');
  const note = document.getElementById('voice-status-note');
  const analyzeBtn = document.getElementById('btn-analyze-voice');

  if (!mediaRecorder || mediaRecorder.state === 'inactive') {
    // Start Recording
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      recordedAudioChunks = [];
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) recordedAudioChunks.push(e.data);
      };

      mediaRecorder.onstop = () => {
        recordedVoiceBlob = new Blob(recordedAudioChunks, { type: 'audio/wav' });
        analyzeBtn.disabled = false;
        note.textContent = `Recording complete (${voiceDurationSec}s). Click Analyze Voice.`;
      };

      mediaRecorder.start();
      btn.classList.add('recording');
      note.textContent = 'Listening... Speak into your microphone';

      voiceDurationSec = 0;
      voiceTimerInterval = setInterval(() => {
        voiceDurationSec++;
        const mins = String(Math.floor(voiceDurationSec / 60)).padStart(2, '0');
        const secs = String(voiceDurationSec % 60).padStart(2, '0');
        document.getElementById('voice-timer').textContent = `${mins}:${secs}`;
      }, 1000);

    } catch(err) {
      alert(`Microphone access error: ${err.message}. Please allow microphone permissions.`);
    }
  } else {
    // Stop Recording
    mediaRecorder.stop();
    mediaRecorder.stream.getTracks().forEach(t => t.stop());
    btn.classList.remove('recording');
    clearInterval(voiceTimerInterval);
  }
}

async function runRecordedVoiceAnalysis() {
  if (!recordedVoiceBlob) return;
  const btn = document.getElementById('btn-analyze-voice');
  btn.disabled = true;
  btn.innerHTML = '<span>⏳</span> Analyzing Recorded Voice...';

  try {
    const formData = new FormData();
    formData.append('file', recordedVoiceBlob, 'live_voice.wav');
    const res = await apiCall('/analyze/audio', {
      method: 'POST',
      body: formData
    });
    renderUnifiedResult('voice-result-content', 'voice-placeholder', res);
  } catch(err) {
    alert(`Voice Analysis Error: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>🗣</span> Stop & Analyze Voice';
  }
}

/* ============ 9. SCAN HISTORY ============ */
async function fetchScanHistory() {
  const tbody = document.getElementById('history-table-body');
  if (!tbody) return;

  try {
    const res = await apiCall('/history?limit=50');
    if (res.success && res.history && res.history.length > 0) {
      tbody.innerHTML = res.history.map(item => {
        const dateStr = item.timestamp ? new Date(item.timestamp * 1000).toLocaleString() : 'Recent';
        const ts = Math.round(item.trust_score !== undefined ? item.trust_score : (100 - item.risk_score));
        const conf = Math.round(item.confidence || 85);
        const tagClass = ts >= 70 ? 'tag-likely' : ts < 40 ? 'tag-low' : 'tag-uncertain';

        return `
          <tr>
            <td style="font-family:var(--font-mono); font-size:12px; color:var(--text-muted);">${dateStr}</td>
            <td><strong style="text-transform:uppercase; color:var(--accent-cyan); font-family:var(--font-mono); font-size:12px;">${item.scan_type}</strong></td>
            <td style="max-width:240px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${item.content_label || 'Direct Scan'}</td>
            <td><span class="score-stat-tag ${tagClass}">${item.classification || 'COMPLETED'}</span></td>
            <td><strong style="font-family:var(--font-mono); color:${ts >= 70 ? 'var(--trust-high)' : ts < 40 ? 'var(--trust-low)' : 'var(--trust-uncertain)'};">${ts} / 100</strong></td>
            <td style="font-family:var(--font-mono);">${conf}%</td>
          </tr>
        `;
      }).join('');
    } else {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:32px; color:var(--text-faint);">No scan records found in database yet.</td></tr>';
    }
  } catch(err) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:32px; color:var(--trust-low);">Could not fetch history: ${err.message}</td></tr>`;
  }
}

/* ============ AUTHENTICATION (OPTIONAL FOR GUESTS) ============ */
function handleAuthBadgeClick() {
  if (currentUser) {
    if (confirm(`Signed in as ${currentUser.email || currentUser.display_name}. Do you want to sign out?`)) {
      logout();
    }
  } else {
    const email = prompt('Enter your email to sign in / register (or click Cancel to continue as Guest):');
    if (email && email.includes('@')) {
      currentUser = { email: email, display_name: email.split('@')[0] };
      document.getElementById('user-display-name').textContent = currentUser.display_name;
      alert(`Welcome, ${currentUser.display_name}! Scans will be linked to your session.`);
    }
  }
}

function logout() {
  currentUser = null;
  document.getElementById('user-display-name').textContent = 'Guest User';
}

/* ============ INITIALIZATION ============ */
window.addEventListener('load', async () => {
  // Restore saved theme
  const savedTheme = localStorage.getItem('tg_theme');
  if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
  }

  // Initial backend health check
  await checkBackendHealth();

  // Periodic health polling every 12 seconds
  setInterval(checkBackendHealth, 12000);

  // Check URL route
  const path = window.location.pathname.replace(/^\/+|\/+$/g, '');
  if (PAGE_TITLES[path]) {
    navigateTo(path, false);
  } else {
    navigateTo('home', false);
  }
});
</script>
</body>
</html>
'''
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated index.html successfully ({len(html_content)} bytes)")

if __name__ == "__main__":
    generate_index_html()
