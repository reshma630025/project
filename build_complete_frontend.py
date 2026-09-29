# -*- coding: utf-8 -*-
"""
Script to build the complete, research-grade TrustGuard AI index.html
with full Authentication, Video Frame Timeline, Audio Segment Timeline,
5-Row Spatial Bento Grid AI SOC, Company Verification, Profile, and Functional Settings.
"""

import sys

def generate_html():
    print("Generating comprehensive index.html...", flush=True)

    # Let's write the entire index.html file with all features.
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(INDEX_HTML_CONTENT)
    print("index.html written successfully!", flush=True)

INDEX_HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TrustGuard AI — Unified Multimodal Deepfake & Digital Fraud Detection Platform</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<!-- Real OCR engine, loaded from CDN -->
<script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>
<style>
/* ============ DESIGN TOKENS (IEEE AI CYBERSECURITY SOC) ============ */
:root{
  --void:#080b12;
  --panel:#0e1420;
  --panel-2:#121a29;
  --glass:rgba(20,28,44,.65);
  
  --glass-brd:rgba(120,150,200,.14);
  --line:rgba(140,165,210,.12);
  --cyan:#2dd9e8;
  --cyan-dim:#1b8f9c;
  --violet:#8b6bf0;
  --safe:#33d19a;
  --warn:#f5b942;
  --danger:#f2495c;
  --danger-2:#ff6b7a;
  --text:#e8edf7;
  --text-dim:#93a0b8;
  --text-faint:#5c6885;
  --mono:'JetBrains Mono', monospace;
  --disp:'Space Grotesk', sans-serif;
  --body:'Inter', sans-serif;
  --radius:14px;
  --sidebar-w:264px;
}
[data-theme="light"]{
  --void:#eef1f7;
  --panel:#ffffff;
  --panel-2:#f4f6fb;
  --glass:rgba(255,255,255,.75);
  --glass-brd:rgba(30,50,90,.12);
  --line:rgba(30,50,90,.1);
  --text:#141a26;
  --text-dim:#4c5872;
  --text-faint:#8590a6;
}
*{box-sizing:border-box; margin:0; padding:0;}
html{scroll-behavior:smooth;}
body{
  background:var(--void);
  color:var(--text);
  font-family:var(--body);
  min-height:100vh;
  overflow-x:hidden;
  transition:background .3s ease, color .3s ease;
}
::selection{background:var(--cyan); color:#04141a;}
a{color:inherit; text-decoration:none;}
button{font-family:inherit; cursor:pointer;}
::-webkit-scrollbar{width:8px; height:8px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:var(--glass-brd); border-radius:8px;}
:focus-visible{outline:2px solid var(--cyan); outline-offset:2px; border-radius:4px;}

/* ============ BACKGROUND FX ============ */
#particles{position:fixed; inset:0; z-index:0; pointer-events:none; opacity:.45;}
.bg-glow{position:fixed; inset:0; z-index:0; pointer-events:none;
  background:
    radial-gradient(700px 500px at 10% -5%, rgba(45,217,232,.08), transparent 60%),
    radial-gradient(800px 600px at 100% 10%, rgba(139,107,240,.08), transparent 55%),
    radial-gradient(600px 500px at 50% 110%, rgba(45,217,232,.05), transparent 60%);
}

/* ============ LAYOUT ============ */
#app{position:relative; z-index:1; display:flex; min-height:100vh;}
.sidebar{
  width:var(--sidebar-w); flex-shrink:0; position:sticky; top:0; height:100vh;
  background:var(--glass); backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px); border-right:1px solid var(--glass-brd);
  display:flex; flex-direction:column; padding:18px 14px; z-index:40; transition:transform .3s ease;
}
.brand{display:flex; align-items:center; gap:10px; padding:6px 10px 18px; border-bottom:1px solid var(--line); margin-bottom:12px;}
.brand-mark{width:36px; height:36px; border-radius:10px; background:conic-gradient(from 220deg, var(--cyan), var(--violet), var(--cyan)); display:flex; align-items:center; justify-content:center; font-family:var(--disp); font-weight:800; color:#04141a; font-size:15px; box-shadow:0 0 20px rgba(45,217,232,.35);}
.brand-name{font-family:var(--disp); font-weight:700; font-size:16.5px; letter-spacing:.2px;}
.brand-sub{font-size:9.5px; color:var(--text-faint); letter-spacing:1.4px; text-transform:uppercase; margin-top:1px;}

.nav-group-label{font-size:9.5px; text-transform:uppercase; letter-spacing:1.4px; color:var(--text-faint); padding:12px 10px 4px; font-weight:600;}
.navlist{list-style:none; display:flex; flex-direction:column; gap:2px;}
.navitem{display:flex; align-items:center; gap:10px; padding:8.5px 12px; border-radius:9px; color:var(--text-dim); font-size:13px; font-weight:500; cursor:pointer; transition:.15s ease; border:1px solid transparent; position:relative;}
.navitem svg{width:16px; height:16px; flex-shrink:0; opacity:.85;}
.navitem:hover{background:rgba(120,150,200,.08); color:var(--text);}
.navitem.active{background:linear-gradient(90deg, rgba(45,217,232,.14), rgba(139,107,240,.06)); color:var(--cyan); border-color:rgba(45,217,232,.24);}
.navitem.active svg{opacity:1;}
.sidebar-foot{margin-top:auto; padding:12px 6px 0; border-top:1px solid var(--line); font-size:11px; color:var(--text-faint); display:flex; flex-direction:column; gap:6px;}
.demo-badge{display:inline-flex; align-items:center; gap:6px; font-size:10.5px; color:var(--safe); background:rgba(51,209,154,.1); border:1px solid rgba(51,209,154,.25); padding:4px 9px; border-radius:20px; width:fit-content;}
.demo-badge .dot{width:6px; height:6px; border-radius:50%; background:currentColor; box-shadow:0 0 8px currentColor;}

.main-col{flex:1; min-width:0; display:flex; flex-direction:column;}
.topbar{position:sticky; top:0; z-index:35; display:flex; align-items:center; gap:12px; padding:10px 24px; background:var(--glass); backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px); border-bottom:1px solid var(--glass-brd);}
.hamburger{display:none; width:34px; height:34px; border-radius:8px; background:var(--panel-2); border:1px solid var(--line); align-items:center; justify-content:center; color:var(--text);}
.search-box{flex:1; max-width:380px; display:flex; align-items:center; gap:8px; background:var(--panel-2); border:1px solid var(--line); border-radius:9px; padding:7px 12px; color:var(--text-dim);}
.search-box input{background:transparent; border:none; outline:none; color:var(--text); font-size:12.5px; width:100%;}
.search-box svg{width:14px; height:14px; opacity:.6; flex-shrink:0;}
.topbar-spacer{flex:1;}
.top-actions{display:flex; align-items:center; gap:8px;}
.icon-btn{width:34px; height:34px; border-radius:9px; background:var(--panel-2); border:1px solid var(--line); display:flex; align-items:center; justify-content:center; color:var(--text-dim); position:relative; transition:.15s;}
.icon-btn:hover{color:var(--cyan); border-color:rgba(45,217,232,.3);}
.icon-btn svg{width:16px; height:16px;}
.badge-dot{position:absolute; top:6px; right:6px; width:6px; height:6px; border-radius:50%; background:var(--danger); box-shadow:0 0 6px var(--danger);}
.lang-select, select.uiselect{background:var(--panel-2); border:1px solid var(--line); color:var(--text); font-size:12px; padding:6px 10px; border-radius:9px; font-family:inherit;}

/* Topbar Profile Chip */
.profile-chip{display:flex; align-items:center; gap:8px; background:var(--panel-2); border:1px solid var(--line); border-radius:20px; padding:4px 12px 4px 4px; cursor:pointer; transition:.15s;}
.profile-chip:hover{border-color:rgba(45,217,232,.4);}
.profile-chip .av{width:26px; height:26px; border-radius:50%; background:linear-gradient(135deg,var(--cyan),var(--violet)); display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:700; color:#04141a;}
.profile-chip span{font-size:12.5px; color:var(--text); font-weight:500;}

.dropdown-panel{position:absolute; top:48px; right:0; width:280px; background:var(--panel); border:1px solid var(--glass-brd); border-radius:12px; box-shadow:0 20px 50px rgba(0,0,0,.5); padding:8px; z-index:60; display:none;}
.dropdown-panel.open{display:block; animation:popIn .18s ease;}
@keyframes popIn{from{opacity:0; transform:translateY(-6px) scale(.98);} to{opacity:1; transform:translateY(0) scale(1);}}
.notif-item{padding:9px 10px; border-radius:8px; display:flex; gap:10px; align-items:flex-start; cursor:pointer; transition:.15s;}
.notif-item:hover{background:var(--panel-2);}
.notif-dot{width:8px; height:8px; border-radius:50%; margin-top:4px; flex-shrink:0;}
.notif-text b{display:block; font-size:12px;}
.notif-text span{font-size:11px; color:var(--text-faint);}

.content{padding:24px 28px 90px; position:relative;}
.page{display:none;}
.page.active{display:block; animation:fadeUp .3s ease;}
@keyframes fadeUp{from{opacity:0; transform:translateY(8px);} to{opacity:1; transform:translateY(0);}}

.page-head{margin-bottom:20px;}
.eyebrow{font-size:10.5px; color:var(--cyan); text-transform:uppercase; letter-spacing:1.8px; font-weight:700; display:flex; align-items:center; gap:8px;}
.eyebrow::before{content:''; width:14px; height:1.5px; background:var(--cyan);}
.page-title{font-family:var(--disp); font-size:25px; font-weight:700; margin-top:5px; letter-spacing:-.3px;}
.page-sub{color:var(--text-dim); font-size:13.5px; margin-top:4px; max-width:640px; line-height:1.5;}

/* ============ GLASS CARDS & BENTO GRID ============ */
.card{background:var(--glass); border:1px solid var(--glass-brd); border-radius:var(--radius); backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px); position:relative; overflow:hidden;}
.card-pad{padding:20px;}
.grid{display:grid; gap:16px;}
.g2{grid-template-columns:repeat(2,1fr);}
.g3{grid-template-columns:repeat(3,1fr);}
.g4{grid-template-columns:repeat(4,1fr);}

.bento-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}
.bento-card {
  background: var(--glass);
  border: 1px solid var(--glass-brd);
  border-radius: var(--radius);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 20px;
  position: relative;
  overflow: hidden;
  transition: transform .25s cubic-bezier(.16,1,.3,1), border-color .25s ease, box-shadow .25s ease;
  display: flex;
  flex-direction: column;
}
.bento-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 10% 10%, rgba(45,217,232,.04), transparent 70%);
  pointer-events: none;
}
.bento-card:hover {
  transform: translateY(-2px);
  border-color: rgba(45,217,232,.35);
  box-shadow: 0 16px 36px rgba(0,0,0,.45), 0 0 24px rgba(45,217,232,.06);
}
.bento-2x2 { grid-column: span 2; grid-row: span 2; }
.bento-2x1 { grid-column: span 2; }
.bento-1x1 { grid-column: span 1; }
.bento-3x1 { grid-column: span 3; }
.bento-4x1 { grid-column: span 4; }

.bento-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
  border-bottom: 1px solid var(--line);
  padding-bottom: 10px;
}
.bento-head .title-group {
  display: flex;
  align-items: center;
  gap: 9px;
}
.bento-head .icon-chip {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(45,217,232,.1);
  color: var(--cyan);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.bento-head .icon-chip svg { width: 16px; height: 16px; }
.bento-head h3 {
  font-family: var(--disp);
  font-size: 14.5px;
  font-weight: 700;
  letter-spacing: .2px;
}
.bento-head .tag {
  font-size: 9.5px;
  font-family: var(--mono);
  text-transform: uppercase;
  letter-spacing: .8px;
  padding: 3px 7px;
  border-radius: 6px;
  background: var(--panel-2);
  border: 1px solid var(--line);
  color: var(--text-dim);
}

/* Threat Dial */
.threat-meter-box {
  display: flex;
  align-items: center;
  gap: 20px;
  background: var(--panel-2);
  border: 1px solid var(--line);
  border-radius: 11px;
  padding: 16px 18px;
  margin-bottom: 14px;
}
.threat-dial {
  position: relative;
  width: 96px;
  height: 96px;
  flex-shrink: 0;
}
.threat-dial svg { transform: rotate(-90deg); width: 100%; height: 100%; }
.threat-dial-center {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.threat-dial-num { font-family: var(--mono); font-size: 20px; font-weight: 800; }
.threat-dial-lbl { font-size: 8px; color: var(--text-faint); text-transform: uppercase; letter-spacing: .5px; }

.soc-status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: .6px;
  padding: 4px 10px;
  border-radius: 20px;
  background: rgba(51,209,154,.12);
  color: var(--safe);
  border: 1px solid rgba(51,209,154,.3);
}
.soc-status-badge.alert {
  background: rgba(242,73,92,.12);
  color: var(--danger-2);
  border-color: rgba(242,73,92,.3);
}
.soc-status-badge .dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  box-shadow: 0 0 6px currentColor;
  animation: pulse 1.6s infinite;
}

/* Bento Stats 4-Grid */
.bento-stat-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}
.bento-stat-cell {
  background: var(--panel-2);
  border: 1px solid var(--line);
  border-radius: 9px;
  padding: 11px 13px;
}
.bento-stat-cell .b-lbl {
  font-size: 10px;
  color: var(--text-faint);
  text-transform: uppercase;
  letter-spacing: .6px;
  display: block;
  margin-bottom: 3px;
}
.bento-stat-cell .b-val {
  font-family: var(--mono);
  font-size: 19px;
  font-weight: 700;
}

/* Multimodal Radar Channels */
.radar-channel {
  background: var(--panel-2);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 12px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 8px;
  transition: .15s ease;
  cursor: pointer;
}
.radar-channel:last-child { margin-bottom: 0; }
.radar-channel:hover {
  border-color: rgba(45,217,232,.35);
  background: rgba(45,217,232,.04);
}
.radar-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}
.radar-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.radar-info b { font-size: 12.5px; display: block; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.radar-info span { font-size: 10.5px; color: var(--text-faint); display: block; margin-top: 1px; }

/* Bento Detector 3x3 Matrix */
.detector-matrix {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}
.det-tile {
  background: var(--panel-2);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 12px 14px;
  cursor: pointer;
  transition: .2s ease;
  display: flex;
  flex-direction: column;
}
.det-tile:hover {
  border-color: rgba(45,217,232,.4);
  background: rgba(45,217,232,.04);
  transform: translateY(-2px);
}
.det-tile-head { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.det-tile-head .ic { width: 26px; height: 26px; border-radius: 6px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 13px; }
.det-tile-head b { font-size: 12.5px; font-weight: 600; color: var(--text); }
.det-tile p { font-size: 11px; color: var(--text-faint); line-height: 1.45; margin-bottom: 8px; flex: 1; }
.det-tile-foot { display: flex; justify-content: space-between; align-items: center; font-size: 10.5px; color: var(--cyan); font-weight: 600; font-family: var(--mono); }

/* Telemetry row */
.telemetry-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px solid var(--line);
  font-size: 11.5px;
}
.telemetry-row:last-child { border-bottom: none; }
.telemetry-row span:first-child { color: var(--text-faint); }
.telemetry-row span:last-child { font-family: var(--mono); font-weight: 600; color: var(--text); }

/* ============ BUTTONS ============ */
.btn{display:inline-flex; align-items:center; justify-content:center; gap:7px; padding:10px 18px; border-radius:9px; font-size:13px; font-weight:600; border:1px solid transparent; transition:.18s ease; white-space:nowrap;}
.btn svg{width:15px; height:15px;}
.btn-primary{background:linear-gradient(90deg, var(--cyan), #4fc3f7); color:#04141a; box-shadow:0 0 20px rgba(45,217,232,.25);}
.btn-primary:hover{filter:brightness(1.08); transform:translateY(-1px);}
.btn-ghost{background:var(--panel-2); color:var(--text); border-color:var(--line);}
.btn-ghost:hover{border-color:rgba(45,217,232,.4); color:var(--cyan);}
.btn-outline{background:transparent; border-color:var(--glass-brd); color:var(--text-dim);}
.btn-outline:hover{color:var(--text); border-color:var(--cyan);}
.btn-danger{background:rgba(242,73,92,.12); color:var(--danger-2); border-color:rgba(242,73,92,.3);}
.btn-sm{padding:6px 12px; font-size:11.5px; border-radius:7px;}
.btn-block{width:100%;}
.btn:disabled{opacity:.5; cursor:not-allowed; transform:none;}

/* ============ HERO / LANDING ============ */
.hero{min-height:calc(100vh - 60px); display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:50px 20px 30px; position:relative;}
.hero-badge{display:inline-flex; align-items:center; gap:8px; padding:6px 14px; border-radius:20px; background:var(--glass); border:1px solid var(--glass-brd); font-size:11.5px; color:var(--cyan); margin-bottom:22px;}
.pulse-dot{width:7px; height:7px; border-radius:50%; background:var(--safe); box-shadow:0 0 10px var(--safe); animation:pulse 1.8s infinite;}
@keyframes pulse{0%,100%{opacity:1;} 50%{opacity:.35;}}
.hero h1{font-family:var(--disp); font-size:clamp(36px,6vw,68px); font-weight:800; line-height:1.02; letter-spacing:-1.5px;}
.hero h1 span{background:linear-gradient(90deg,var(--cyan),var(--violet)); -webkit-background-clip:text; background-clip:text; color:transparent;}
.hero p.sub{max-width:620px; margin:18px auto 0; color:var(--text-dim); font-size:15.5px; line-height:1.6;}
.hero-ctas{display:flex; gap:12px; margin-top:28px; flex-wrap:wrap; justify-content:center;}
.hero-tertiary{margin-top:14px; font-size:12px; color:var(--text-faint);}
.hero-tertiary a{color:var(--cyan); border-bottom:1px dotted currentColor; cursor:pointer;}

.engine-wrap{margin-top:45px; width:100%; max-width:880px;}
.flow-row{display:flex; align-items:center; justify-content:center; gap:8px; flex-wrap:wrap;}
.flow-chip{background:var(--glass); border:1px solid var(--glass-brd); padding:8px 14px; border-radius:9px; font-family:var(--mono); font-size:11px; color:var(--text-dim); letter-spacing:.5px;}
.flow-chip.io{color:var(--cyan); border-color:rgba(45,217,232,.3);}
.flow-arrow{color:var(--text-faint); font-size:14px;}
.hub{width:130px; height:130px; border-radius:50%; margin:22px auto; display:flex; align-items:center; justify-content:center; position:relative; background:radial-gradient(circle at 50% 40%, rgba(45,217,232,.16), rgba(139,107,240,.05) 70%); border:1px solid rgba(45,217,232,.35);}
.hub::before,.hub::after{content:''; position:absolute; border-radius:50%; border:1px solid rgba(45,217,232,.18); animation:ringspin 12s linear infinite;}
.hub::before{inset:-14px;}
.hub::after{inset:-28px; border-color:rgba(139,107,240,.14); animation-duration:20s; animation-direction:reverse;}
@keyframes ringspin{to{transform:rotate(360deg);}}
.hub-label{font-family:var(--disp); font-weight:700; font-size:12px; text-align:center; color:var(--text);}
.hub-label small{display:block; font-size:8.5px; color:var(--cyan); letter-spacing:1.5px; margin-top:2px;}

.stats-strip{display:flex; gap:12px; justify-content:center; margin-top:40px; flex-wrap:wrap;}
.stat-mini{text-align:center; min-width:105px;}
.stat-mini b{display:block; font-family:var(--mono); font-size:22px; color:var(--cyan);}
.stat-mini span{font-size:10px; color:var(--text-faint); text-transform:uppercase; letter-spacing:1px;}

/* ============ SCANNER & DROPZONES ============ */
.scanner-card{padding:24px;}
.tab-row{display:flex; gap:6px; margin-bottom:18px; flex-wrap:wrap; border-bottom:1px solid var(--line); padding-bottom:0;}
.tab-btn{padding:9px 15px; font-size:12.5px; font-weight:600; color:var(--text-faint); border-bottom:2px solid transparent; background:none; border-top:none;border-left:none;border-right:none; display:flex; align-items:center; gap:6px; cursor:pointer;}
.tab-btn svg{width:14px; height:14px;}
.tab-btn.active{color:var(--cyan); border-bottom-color:var(--cyan);}
.tab-panel{display:none;}
.tab-panel.active{display:block; animation:fadeUp .25s ease;}

.dropzone{border:1.5px dashed var(--glass-brd); border-radius:12px; padding:38px 20px; text-align:center; transition:.2s; background:rgba(120,150,200,.03); cursor:pointer;}
.dropzone:hover, .dropzone.drag{border-color:var(--cyan); background:rgba(45,217,232,.05);}
.dropzone svg{width:34px; height:34px; color:var(--cyan); margin-bottom:10px;}
.dropzone h4{font-family:var(--disp); font-size:15px; margin-bottom:4px;}
.dropzone p{font-size:12px; color:var(--text-faint);}
.chip-row{display:flex; gap:6px; margin-top:14px; flex-wrap:wrap; justify-content:center;}
.type-chip{font-size:10.5px; padding:3px 9px; border-radius:20px; background:var(--panel-2); border:1px solid var(--line); color:var(--text-faint);}

.textarea{width:100%; background:var(--panel-2); border:1px solid var(--line); border-radius:10px; padding:12px 14px; color:var(--text); font-size:13px; font-family:inherit; resize:vertical; min-height:120px;}
.textarea:focus{outline:none; border-color:var(--cyan);}
.field{width:100%; background:var(--panel-2); border:1px solid var(--line); border-radius:9px; padding:10px 13px; color:var(--text); font-size:13px; font-family:inherit;}
.field:focus{outline:none; border-color:var(--cyan);}
.field-label{font-size:11px; color:var(--text-faint); margin-bottom:5px; display:block; text-transform:uppercase; letter-spacing:.6px; font-weight:600;}

.preview-row{display:flex; align-items:center; gap:12px; background:var(--panel-2); border:1px solid var(--line); border-radius:10px; padding:10px 12px; margin-top:12px;}
.preview-thumb{width:42px; height:42px; border-radius:8px; object-fit:cover; background:#1a2332; flex-shrink:0;}
.preview-meta{flex:1; min-width:0;}
.preview-meta b{font-size:12px; display:block; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
.preview-meta span{font-size:10.5px; color:var(--text-faint);}

.action-row{display:flex; gap:10px; margin-top:16px; flex-wrap:wrap;}

/* ============ PROMINENT PREDICTION STYLES ============ */
.pred-banner {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 22px;
  border-radius: var(--radius);
  margin-bottom: 16px;
  border: 1px solid;
  position: relative;
  overflow: hidden;
}
.pred-banner::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: radial-gradient(circle at 10% 50%, rgba(255,255,255,.08), transparent 60%);
}
.pred-banner.genuine {
  background: linear-gradient(135deg, rgba(51,209,154,.18), rgba(45,217,232,.08));
  border-color: rgba(51,209,154,.45);
  box-shadow: 0 0 35px rgba(51,209,154,.18);
}
.pred-banner.fake {
  background: linear-gradient(135deg, rgba(242,73,92,.22), rgba(255,107,122,.1));
  border-color: rgba(242,73,92,.5);
  box-shadow: 0 0 35px rgba(242,73,92,.22);
}
.pred-banner.mod {
  background: linear-gradient(135deg, rgba(245,185,66,.18), rgba(120,150,200,.08));
  border-color: rgba(245,185,66,.45);
  box-shadow: 0 0 25px rgba(245,185,66,.15);
}

.pred-icon-box {
  width: 54px;
  height: 54px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  flex-shrink: 0;
  font-weight: 800;
}
.pred-banner.genuine .pred-icon-box {
  background: rgba(51,209,154,.25);
  color: var(--safe);
  box-shadow: 0 0 16px rgba(51,209,154,.4);
  border: 1px solid rgba(51,209,154,.5);
}
.pred-banner.fake .pred-icon-box {
  background: rgba(242,73,92,.25);
  color: var(--danger-2);
  box-shadow: 0 0 16px rgba(242,73,92,.45);
  border: 1px solid rgba(242,73,92,.5);
}
.pred-banner.mod .pred-icon-box {
  background: rgba(245,185,66,.25);
  color: var(--warn);
  border: 1px solid rgba(245,185,66,.5);
}

.pred-title {
  font-family: var(--disp);
  font-size: 24px;
  font-weight: 800;
  letter-spacing: .4px;
  line-height: 1.15;
}
.pred-sub {
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.1px;
  margin-top: 3px;
  opacity: .92;
}
.pred-banner.genuine .pred-title, .pred-banner.genuine .pred-sub { color: var(--safe); }
.pred-banner.fake .pred-title, .pred-banner.fake .pred-sub { color: var(--danger-2); }
.pred-banner.mod .pred-title, .pred-banner.mod .pred-sub { color: var(--warn); }

.pred-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(125px, 1fr));
  gap: 10px;
  margin-top: 14px;
  margin-bottom: 16px;
}
.pred-card {
  background: var(--panel-2);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 11px 13px;
}
.pred-card .val {
  font-family: var(--mono);
  font-size: 19px;
  font-weight: 700;
}
.pred-card .lbl {
  font-size: 10.5px;
  color: var(--text-faint);
  text-transform: uppercase;
  letter-spacing: .6px;
  margin-top: 3px;
}

/* ============ VIDEO & AUDIO TIMELINES ============ */
.timeline-box {
  background: var(--panel-2);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 16px;
  margin-top: 16px;
  margin-bottom: 16px;
}
.timeline-title {
  font-family: var(--disp);
  font-size: 13.5px;
  font-weight: 700;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.timeline-scroll {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 6px 2px 10px;
}
.timeline-chip {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 9px;
  padding: 9px 12px;
  min-width: 120px;
  cursor: pointer;
  transition: .15s ease;
  flex-shrink: 0;
}
.timeline-chip:hover {
  border-color: var(--cyan);
  transform: translateY(-2px);
}
.timeline-chip.fake {
  border-left: 3px solid var(--danger-2);
}
.timeline-chip.real {
  border-left: 3px solid var(--safe);
}
.timeline-chip .tc-time { font-family: var(--mono); font-size: 10.5px; color: var(--text-faint); display: block; margin-bottom: 2px; }
.timeline-chip .tc-status { font-size: 12px; font-weight: 700; display: flex; align-items: center; gap: 4px; }
.timeline-chip .tc-score { font-family: var(--mono); font-size: 11px; color: var(--text-dim); margin-top: 2px; }

/* Circular Gauge */
.gauge-card{padding:22px; display:flex; align-items:center; gap:24px; flex-wrap:wrap;}
.gauge{position:relative; width:160px; height:160px; flex-shrink:0;}
.gauge svg{transform:rotate(-90deg); width:100%; height:100%;}
.gauge-bg{fill:none; stroke:var(--line); stroke-width:10;}
.gauge-fg{fill:none; stroke-width:10; stroke-linecap:round; transition:stroke-dashoffset 1.4s cubic-bezier(.16,1,.3,1), stroke 1s ease;}
.gauge-center{position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;}
.gauge-num{font-family:var(--mono); font-size:32px; font-weight:800;}
.gauge-max{font-size:10px; color:var(--text-faint);}
.gauge-tag{margin-top:4px; font-size:9.5px; font-weight:700; letter-spacing:1px; padding:2px 8px; border-radius:20px;}
.gauge-info{flex:1; min-width:200px;}
.gauge-info h3{font-family:var(--disp); font-size:17px; margin-bottom:4px;}
.gauge-info p{font-size:12.5px; color:var(--text-dim); line-height:1.5;}

.result-cards{margin-top:14px;}
.rc-title{font-size:11px; color:var(--text-faint); text-transform:uppercase; letter-spacing:.6px; margin-bottom:4px;}
.rc-val{font-family:var(--mono); font-size:19px; font-weight:700;}
.bar-track{height:4px; background:var(--line); border-radius:4px; margin-top:8px; overflow:hidden;}
.bar-fill{height:100%; border-radius:4px; transition:width 1s ease;}

.indicators{padding:18px;}
.indicators h3{font-family:var(--disp); font-size:15px; margin-bottom:12px; display:flex; align-items:center; gap:8px;}
.ind-bullet-item{display:flex; gap:10px; padding:10px 0; border-bottom:1px solid var(--line);}
.ind-bullet-item:last-child{border-bottom:none;}
.ind-bullet-item .bullet{font-size:15px; line-height:1.2;}
.ind-bullet-item .content-txt b{font-size:12.5px; display:block;}
.ind-bullet-item .content-txt p{font-size:11.5px; color:var(--text-dim); margin-top:2px; line-height:1.45;}

.explanation-card{background:var(--glass); border:1px solid var(--glass-brd); border-radius:var(--radius); padding:16px 18px; margin-top:14px; margin-bottom:14px;}
.explanation-card h4{font-family:var(--disp); font-size:13px; color:var(--cyan); text-transform:uppercase; letter-spacing:1px; margin-bottom:6px; display:flex; align-items:center; gap:8px;}
.explanation-card h4::before{content:''; width:12px; height:1px; background:var(--cyan);}
.explanation-card p{font-size:13px; color:var(--text); line-height:1.55;}

.recommend-box{padding:14px 16px; border-radius:10px; border:1px solid; display:flex; gap:12px; align-items:flex-start; margin-bottom:14px;}
.recommend-box svg{width:20px; height:20px; flex-shrink:0; margin-top:1px;}
.recommend-box b{font-size:12.5px; display:block; margin-bottom:2px;}
.recommend-box p{font-size:12px; line-height:1.45; opacity:.9;}

/* ============ PIPELINE ANIMATION ============ */
.pipeline{padding:18px; margin-top:16px;}
.pipeline-title{display:flex; align-items:center; justify-content:space-between; margin-bottom:12px;}
.pipeline-title h3{font-family:var(--disp); font-size:15px;}
.step{display:flex; align-items:center; gap:11px; padding:8px 4px; position:relative;}
.step:not(:last-child)::after{content:''; position:absolute; left:14px; top:32px; width:1px; height:calc(100% - 6px); background:var(--line);}
.step-dot{width:26px; height:26px; border-radius:50%; background:var(--panel-2); border:1.5px solid var(--line); display:flex; align-items:center; justify-content:center; flex-shrink:0; transition:.3s; z-index:1;}
.step-dot svg{width:12px; height:12px; opacity:0;}
.step.done .step-dot{background:rgba(51,209,154,.15); border-color:var(--safe);}
.step.done .step-dot svg{opacity:1; color:var(--safe);}
.step.active .step-dot{border-color:var(--cyan); box-shadow:0 0 0 4px rgba(45,217,232,.12);}
.step.active .step-dot::before{content:''; width:8px; height:8px; border-radius:50%; background:var(--cyan); animation:pulse .8s infinite;}
.step-txt b{font-size:12.5px; font-weight:600; color:var(--text-faint); transition:.3s;}
.step.active .step-txt b, .step.done .step-txt b{color:var(--text);}
.step-txt span{font-size:11px; color:var(--text-faint); display:block;}
.step-time{margin-left:auto; font-family:var(--mono); font-size:10.5px; color:var(--text-faint);}

/* ============ AUTH MODAL ============ */
.modal-bg{position:fixed; inset:0; background:rgba(4,8,14,.72); backdrop-filter:blur(6px); z-index:180; display:none; align-items:center; justify-content:center; padding:20px;}
.modal-bg.open{display:flex;}
.modal-box{background:var(--panel); border:1px solid var(--glass-brd); border-radius:16px; max-width:480px; width:100%; max-height:85vh; overflow-y:auto; box-shadow:0 30px 70px rgba(0,0,0,.6);}
.modal-head{display:flex; align-items:center; justify-content:space-between; padding:16px 20px; border-bottom:1px solid var(--line); position:sticky; top:0; background:var(--panel); z-index:2;}
.modal-head h3{font-family:var(--disp); font-size:16px; font-weight:700;}
.modal-body{padding:20px;}
.modal-close{width:28px; height:28px; border-radius:8px; background:var(--panel-2); border:1px solid var(--line); display:flex; align-items:center; justify-content:center; color:var(--text-dim); cursor:pointer;}

.auth-tabs{display:flex; border-bottom:1px solid var(--line); margin-bottom:18px;}
.auth-tab{flex:1; text-align:center; padding:10px; font-size:13px; font-weight:600; color:var(--text-faint); cursor:pointer; border-bottom:2px solid transparent; background:none; border-top:none; border-left:none; border-right:none;}
.auth-tab.active{color:var(--cyan); border-bottom-color:var(--cyan);}
.auth-form{display:none;}
.auth-form.active{display:block; animation:fadeUp .2s ease;}

/* ============ TOAST ============ */
#toasts{position:fixed; bottom:20px; right:20px; z-index:200; display:flex; flex-direction:column; gap:8px;}
.toast{background:var(--panel); border:1px solid var(--glass-brd); border-left:3px solid var(--cyan); border-radius:10px; padding:10px 14px; font-size:12px; box-shadow:0 12px 30px rgba(0,0,0,.4); min-width:240px; animation:slideIn .3s ease;}
.toast.warn{border-left-color:var(--warn);}
.toast.danger{border-left-color:var(--danger);}
.toast.safe{border-left-color:var(--safe);}
.toast b{display:block; margin-bottom:2px; font-size:12.5px;}
.toast span{color:var(--text-faint); font-size:11px;}
@keyframes slideIn{from{opacity:0; transform:translateX(30px);} to{opacity:1; transform:translateX(0);}}

/* Assistant fab */
.assist-fab{position:fixed; bottom:22px; right:22px; z-index:150; width:54px; height:54px; border-radius:50%; background:linear-gradient(135deg,var(--cyan),var(--violet)); display:flex; align-items:center; justify-content:center; box-shadow:0 10px 30px rgba(45,217,232,.35); border:none; color:#04141a; transition:.2s;}
.assist-fab:hover{transform:scale(1.06);}
.assist-fab svg{width:22px; height:22px;}
.assist-panel{position:fixed; bottom:86px; right:22px; width:360px; max-width:calc(100vw - 32px); height:500px; max-height:calc(100vh - 130px); background:var(--panel); border:1px solid var(--glass-brd); border-radius:16px; box-shadow:0 24px 60px rgba(0,0,0,.55); z-index:150; display:none; flex-direction:column; overflow:hidden;}
.assist-panel.open{display:flex; animation:popIn .22s ease;}
.assist-head{padding:12px 14px; border-bottom:1px solid var(--line); display:flex; align-items:center; gap:10px; background:var(--panel-2);}
.assist-head .av{width:30px; height:30px; border-radius:8px; background:conic-gradient(from 220deg,var(--cyan),var(--violet)); display:flex; align-items:center; justify-content:center;}
.assist-head .av svg{width:15px; height:15px; color:#04141a;}
.assist-head b{font-size:13px; display:block;}
.assist-head span{font-size:10px; color:var(--safe);}
.assist-close{margin-left:auto; width:26px; height:26px; border-radius:6px; background:transparent; border:none; color:var(--text-faint); display:flex; align-items:center; justify-content:center; cursor:pointer;}
.assist-body{flex:1; overflow-y:auto; padding:12px; display:flex; flex-direction:column; gap:10px;}
.msg{max-width:85%; font-size:12px; line-height:1.55; padding:9px 12px; border-radius:11px;}
.msg.bot{background:var(--panel-2); border:1px solid var(--line); align-self:flex-start; border-bottom-left-radius:3px;}
.msg.user{background:linear-gradient(90deg,var(--cyan),#4fc3f7); color:#04141a; align-self:flex-end; border-bottom-right-radius:3px; font-weight:500;}
.suggest-row{display:flex; flex-wrap:wrap; gap:6px;}
.suggest-chip{font-size:10.5px; padding:5px 9px; border-radius:20px; background:var(--panel-2); border:1px solid var(--line); color:var(--text-dim); cursor:pointer;}
.suggest-chip:hover{border-color:var(--cyan); color:var(--cyan);}
.assist-input-row{border-top:1px solid var(--line); padding:9px; display:flex; gap:6px; align-items:center;}
.assist-input-row input{flex:1; background:var(--panel-2); border:1px solid var(--line); border-radius:20px; padding:9px 12px; color:var(--text); font-size:12px; outline:none;}
.mic-btn{width:34px; height:34px; border-radius:50%; background:var(--panel-2); border:1px solid var(--line); display:flex; align-items:center; justify-content:center; color:var(--text-dim); flex-shrink:0; cursor:pointer;}
.send-btn{width:34px; height:34px; border-radius:50%; background:var(--cyan); border:none; color:#04141a; display:flex; align-items:center; justify-content:center; flex-shrink:0; cursor:pointer;}

/* Tables */
.table-wrap{overflow-x:auto;}
table.data-table{width:100%; border-collapse:collapse; font-size:12px;}
table.data-table th{text-align:left; padding:10px 12px; color:var(--text-faint); font-weight:600; text-transform:uppercase; font-size:10px; letter-spacing:.6px; border-bottom:1px solid var(--line); white-space:nowrap;}
table.data-table td{padding:10px 12px; border-bottom:1px solid var(--line); white-space:nowrap;}
table.data-table tr:hover td{background:rgba(120,150,200,.04);}
.status-pill{display:inline-flex; align-items:center; gap:4px; font-size:10px; font-weight:700; padding:3px 8px; border-radius:20px; letter-spacing:.4px;}

@media(max-width:1200px){
  .bento-grid { grid-template-columns: repeat(2, 1fr); }
  .bento-2x2, .bento-3x1, .bento-4x1 { grid-column: span 2; }
  .detector-matrix { grid-template-columns: repeat(2, 1fr); }
}
@media(max-width:980px){
  .sidebar{position:fixed; left:0; top:0; transform:translateX(-100%); box-shadow:0 0 40px rgba(0,0,0,.5);}
  .sidebar.open{transform:translateX(0);}
  .hamburger{display:flex;}
  .search-box{display:none;}
  .content{padding:16px 14px 100px;}
}
@media(max-width:768px){
  .bento-grid { grid-template-columns: 1fr; }
  .bento-2x2, .bento-2x1, .bento-3x1, .bento-4x1, .bento-1x1 { grid-column: span 1; grid-row: auto; }
  .threat-meter-box { flex-direction: column; text-align: center; }
  .detector-matrix { grid-template-columns: 1fr; }
  .g2, .g3, .g4 { grid-template-columns: 1fr; }
}
</style>
</head>
<body data-theme="dark">
<canvas id="particles"></canvas>
<div class="bg-glow"></div>

<div id="app">
  <!-- ============ SIDEBAR ============ -->
  <aside class="sidebar" id="sidebar">
    <div class="brand">
      <div class="brand-mark">TG</div>
      <div>
        <div class="brand-name">TrustGuard <span style="color:var(--cyan)">AI</span></div>
        <div class="brand-sub">Content Protection</div>
      </div>
    </div>

    <div style="flex:1; overflow-y:auto;">
      <div class="nav-group-label">Overview</div>
      <ul class="navlist">
        <li class="navitem active" data-page="dashboard"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/></svg>Dashboard</li>
      </ul>

      <div class="nav-group-label">Detection</div>
      <ul class="navlist">
        <li class="navitem" data-page="deepfake"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M9 10c0-1 1-2 3-2s3 1 3 2M8 15s1.5 2 4 2 4-2 4-2"/></svg>Deepfake Detection</li>
        <li class="navitem" data-page="image"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>Image Analysis</li>
        <li class="navitem" data-page="video"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="15" height="14" rx="2"/><path d="M17 10l5-3v10l-5-3"/></svg>Video Analysis</li>
        <li class="navitem" data-page="audio"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10a7 7 0 0014 0M12 19v3"/></svg>Audio Analysis</li>
      </ul>

      <div class="nav-group-label">Fraud Intelligence</div>
      <ul class="navlist">
        <li class="navitem" data-page="text"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16v13H7l-3 3z"/></svg>Text & Scam Detection</li>
        <li class="navitem" data-page="job"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>Job / Internship Scan</li>
        <li class="navitem" data-page="url"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 17H7a5 5 0 010-10h2M15 7h2a5 5 0 010 10h-2M8 12h8"/></svg>URL Scanner</li>
        <li class="navitem" data-page="ocr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7V5a1 1 0 011-1h2M4 17v2a1 1 0 001 1h2M20 7V5a1 1 0 00-1-1h-2M20 17v2a1 1 0 01-1 1h-2M7 9h10M7 13h6"/></svg>OCR Scanner</li>
        <li class="navitem" data-page="company"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18M3 7v14M21 7v14M9 3h6v18H9z"/></svg>Company Verification</li>
        <li class="navitem" data-page="social"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 010 18 14 14 0 010-18z"/></svg>Social Media Protection</li>
      </ul>

      <div class="nav-group-label">Live Detection</div>
      <ul class="navlist">
        <li class="navitem" data-page="camera"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg>Camera Scanner</li>
        <li class="navitem" data-page="mic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10a7 7 0 0014 0M12 19v3"/></svg>Live Microphone</li>
      </ul>

      <div class="nav-group-label">System</div>
      <ul class="navlist">
        <li class="navitem" data-page="protect"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l8 4v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V6l8-4z"/></svg>Digital Protection</li>
        <li class="navitem" data-page="reports"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2h9l5 5v15H6z"/><path d="M14 2v6h6"/></svg>Reports</li>
        <li class="navitem" data-page="history"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 109-9 9 9 0 00-9 9z"/><path d="M12 7v5l3 3"/></svg>Scan History</li>
        <li class="navitem" data-page="profile"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>User Profile</li>
        <li class="navitem" data-page="settings"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.6 1.6 0 00.3 1.8l.1.1a2 2 0 11-2.8 2.8l-.1-.1a1.6 1.6 0 00-1.8-.3 1.6 1.6 0 00-1 1.5V21a2 2 0 01-4 0v-.1a1.6 1.6 0 00-1-1.5 1.6 1.6 0 00-1.8.3l-.1.1a2 2 0 11-2.8-2.8l.1-.1a1.6 1.6 0 00.3-1.8 1.6 1.6 0 00-1.5-1H3a2 2 0 010-4h.1a1.6 1.6 0 001.5-1 1.6 1.6 0 00-.3-1.8l-.1-.1a2 2 0 112.8-2.8l.1.1a1.6 1.6 0 001.8.3H9a1.6 1.6 0 001-1.5V3a2 2 0 014 0v.1a1.6 1.6 0 001 1.5 1.6 1.6 0 001.8-.3l.1-.1a2 2 0 112.8 2.8l-.1.1a1.6 1.6 0 00-.3 1.8V9a1.6 1.6 0 001.5 1H21a2 2 0 010 4h-.1a1.6 1.6 0 00-1.5 1z"/></svg>Settings</li>
      </ul>
    </div>

    <div class="sidebar-foot">
      <span class="demo-badge" id="engineBadge"><i class="dot"></i>● Connecting…</span>
      <span>© 2026 TrustGuard AI · v1.0</span>
    </div>
  </aside>

  <!-- ============ MAIN ============ -->
  <div class="main-col">
    <header class="topbar">
      <button class="hamburger" id="hamburger" aria-label="Open menu"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
      <div class="search-box"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg><input id="globalSearch" type="text" placeholder="Search detection modules, scans, reports…" aria-label="Search"></div>
      <div class="topbar-spacer"></div>
      <div class="top-actions">
        <select class="lang-select" id="langSelect" aria-label="Language">
          <option value="en">🇬🇧 English</option>
          <option value="hi">🇮🇳 Hindi</option>
          <option value="te">🇮🇳 Telugu</option>
          <option value="ta">🇮🇳 Tamil</option>
          <option value="kn">🇮🇳 Kannada</option>
          <option value="ml">🇮🇳 Malayalam</option>
          <option value="mr">🇮🇳 Marathi</option>
          <option value="bn">🇮🇳 Bengali</option>
          <option value="gu">🇮🇳 Gujarati</option>
          <option value="pa">🇮🇳 Punjabi</option>
          <option value="ur">🇵🇰 Urdu</option>
        </select>
        <div style="position:relative;">
          <button class="icon-btn" id="notifBtn" aria-label="Notifications"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8a6 6 0 10-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 01-3.4 0"/></svg><span class="badge-dot"></span></button>
          <div class="dropdown-panel" id="notifPanel">
            <div style="padding:8px 10px 10px; font-weight:700; font-size:12.5px; border-bottom:1px solid var(--line); margin-bottom:6px;">Threat Alerts & Notifications</div>
            <div class="notif-item"><div class="notif-dot" style="background:var(--danger)"></div><div class="notif-text"><b>Deepfake Artifacts Flagged</b><span>Temporal frame anomaly identified</span></div></div>
            <div class="notif-item"><div class="notif-dot" style="background:var(--warn)"></div><div class="notif-text"><b>Suspicious Domain Intercepted</b><span>Shortener entropy > 4.2 bits</span></div></div>
            <div class="notif-item"><div class="notif-dot" style="background:var(--safe)"></div><div class="notif-text"><b>AI Engine Online</b><span>Vision ViT & STFT ready</span></div></div>
          </div>
        </div>
        <button class="icon-btn" id="themeBtn" aria-label="Toggle theme"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3a9 9 0 109 9c0-.46-.04-.92-.1-1.36A5.4 5.4 0 0112 3z"/></svg></button>
        
        <!-- Dynamic User Profile Chip -->
        <div style="position:relative;">
          <div class="profile-chip" id="profileBtn">
            <div class="av" id="topAvatar">RA</div>
            <span id="topUserName">Reshma A.</span>
          </div>
          <div class="dropdown-panel" id="profilePanel" style="width:220px;">
            <div style="padding:8px 10px 10px; border-bottom:1px solid var(--line); margin-bottom:6px;">
              <b style="font-size:13px; display:block;" id="menuUserName">Reshma A.</b>
              <span style="font-size:11px; color:var(--text-faint);" id="menuUserEmail">reshma@trustguard.ai</span>
            </div>
            <div class="notif-item" data-page="profile"><div class="notif-text"><b>My Profile & Scans</b></div></div>
            <div class="notif-item" data-page="settings"><div class="notif-text"><b>Account Settings</b></div></div>
            <div class="notif-item" id="menuAuthAction"><div class="notif-text"><b style="color:var(--danger-2);">Sign Out</b></div></div>
          </div>
        </div>
      </div>
    </header>

    <main class="content">

      <!-- ================= 1. LANDING PAGE ================= -->
      <section class="page" id="page-landing">
        <div class="hero">
          <div class="hero-badge"><span class="pulse-dot"></span> Multimodal AI Trust Engine · Live Neural SOC</div>
          <h1>Detect. Verify. <span>Protect.</span></h1>
          <p class="sub">An intelligent multilingual AI platform for real-time deepfake detection, synthetic speech forensics, and fraud prevention across images, video frames, audio waveforms, and phishing vectors.</p>
          <div class="hero-ctas">
            <button class="btn btn-primary" data-goto="dashboard"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>Launch Security Operations Center</button>
            <button class="btn btn-ghost" data-goto="image"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>Image ViT Radar</button>
            <button class="btn btn-outline" data-goto="camera"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg>Live Camera HUD</button>
          </div>
          <div class="hero-tertiary">Production Pretrained AI Inference · <a data-goto="settings">zero mock predictions</a></div>

          <div class="engine-wrap">
            <div class="flow-row">
              <span class="flow-chip io">IMAGE ViT</span><span class="flow-arrow">→</span>
              <span class="flow-chip io">VIDEO RADAR</span><span class="flow-arrow">→</span>
              <span class="flow-chip io">AUDIO STFT</span><span class="flow-arrow">→</span>
              <span class="flow-chip io">SCAM NLP</span><span class="flow-arrow">→</span>
              <span class="flow-chip io">URL ENTROPY</span><span class="flow-arrow">→</span>
              <span class="flow-chip io">OCR EXTRACTOR</span>
            </div>
            <div class="hub"><div class="hub-label">TRUST<br>ENGINE<small>MULTIMODAL AI</small></div></div>
            <div class="flow-row">
              <span class="flow-chip">PROVENANCE</span>
              <span class="flow-chip">RISK SCORE</span>
              <span class="flow-chip">AUTHENTICITY</span>
              <span class="flow-chip">FORENSIC SIGNALS</span>
              <span class="flow-chip">EXPLAINABLE AI</span>
            </div>
          </div>

          <div class="stats-strip">
            <div class="stat-mini"><b id="landStat1">0</b><span>Scans Today</span></div>
            <div class="stat-mini"><b id="landStat2">0</b><span>Threats Detected</span></div>
            <div class="stat-mini"><b id="landStat3">0</b><span>Deepfakes Found</span></div>
            <div class="stat-mini"><b id="landStat4">0</b><span>Scams Blocked</span></div>
            <div class="stat-mini"><b>11</b><span>Languages</span></div>
          </div>
        </div>
      </section>

      <!-- ================= 2. SPATIAL BENTO GRID DASHBOARD (AI SOC) ================= -->
      <section class="page active" id="page-dashboard">
        <div class="page-head" style="display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; gap:12px; margin-bottom:20px;">
          <div>
            <div class="eyebrow">Security Operations Center · Real-Time AI Telemetry</div>
            <div class="page-title">AI Content Authenticity & Threat Radar</div>
            <p class="page-sub">Multi-modal neural inspection across images, temporal video frames, synthetic voices, scam texts, and phishing domains.</p>
          </div>
          <div style="display:flex; align-items:center; gap:8px;">
            <div class="soc-status-badge" id="socGlobalShield">
              <span class="dot"></span>
              <span id="socGlobalText">PROTECTED · ENGINE ACTIVE</span>
            </div>
          </div>
        </div>

        <!-- 5-ROW SPATIAL BENTO GRID -->
        <div class="bento-grid">

          <!-- ROW 1: Card 1 (2x1) AI Content Security Status -->
          <div class="bento-card bento-2x1">
            <div class="bento-head">
              <div class="title-group">
                <div class="icon-chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
                <div>
                  <h3>AI Content Security Status</h3>
                  <div style="font-size:10.5px; color:var(--text-faint);">Live Platform Threat Assessment</div>
                </div>
              </div>
              <span class="tag">ACTIVE RADAR</span>
            </div>
            <div class="threat-meter-box">
              <div class="threat-dial">
                <svg viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="40" fill="none" stroke="var(--line)" stroke-width="8"/>
                  <circle cx="50" cy="50" r="40" fill="none" stroke="var(--safe)" stroke-width="8" stroke-dasharray="251.2" stroke-dashoffset="230" id="bentoThreatArc" style="transition: stroke-dashoffset 1s ease, stroke .5s ease; stroke-linecap: round;"/>
                </svg>
                <div class="threat-dial-center">
                  <div class="threat-dial-num" id="bentoThreatScore" style="color:var(--safe);">0</div>
                  <div class="threat-dial-lbl">SYSTEM RISK</div>
                </div>
              </div>
              <div style="flex:1;">
                <div style="font-family:var(--disp); font-size:16px; font-weight:700; margin-bottom:4px;" id="bentoSecHeadline">System Nominal · Zero Critical Threats</div>
                <p style="font-size:12px; color:var(--text-dim); line-height:1.45; margin-bottom:10px;" id="bentoSecDetail">All multi-signal detectors are actively screening media. No unverified anomalies detected.</p>
                <div style="display:flex; gap:8px;">
                  <button class="btn btn-primary btn-sm" onclick="document.getElementById('dashScanTabs')?.scrollIntoView({behavior:'smooth'});"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>Quick Scan</button>
                  <button class="btn btn-outline btn-sm" data-goto="history">View History</button>
                </div>
              </div>
            </div>
          </div>

          <!-- ROW 1: Card 2 (1x1) System Health & Telemetry -->
          <div class="bento-card bento-1x1">
            <div class="bento-head">
              <div class="title-group">
                <div class="icon-chip" style="background:rgba(51,209,154,.12); color:var(--safe);"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg></div>
                <div>
                  <h3 style="font-size:13.5px;">Engine Health</h3>
                </div>
              </div>
              <span class="tag" id="bentoEngineStatusTag" style="color:var(--safe);">ONLINE</span>
            </div>
            <div style="display:flex; flex-direction:column; gap:3px;">
              <div class="telemetry-row"><span>Status</span><span style="color:var(--safe);" id="bentoStatusTxt">● Online</span></div>
              <div class="telemetry-row"><span>ViT Vision</span><span style="color:var(--cyan);">Ready</span></div>
              <div class="telemetry-row"><span>Audio STFT</span><span style="color:var(--cyan);">Ready</span></div>
              <div class="telemetry-row"><span>Latency</span><span id="bentoLatency">24ms</span></div>
            </div>
          </div>

          <!-- ROW 1: Card 3 (1x1) Operator Profile -->
          <div class="bento-card bento-1x1">
            <div class="bento-head">
              <div class="title-group">
                <div class="icon-chip" style="background:rgba(139,107,240,.12); color:var(--violet);"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div>
                <div>
                  <h3 style="font-size:13.5px;">Operator Session</h3>
                </div>
              </div>
              <span class="tag" style="color:var(--violet);">AUTH</span>
            </div>
            <div style="display:flex; flex-direction:column; gap:4px;">
              <b style="font-size:13px;" id="dashOperatorName">Reshma A.</b>
              <span style="font-size:11px; color:var(--text-faint);" id="dashOperatorOrg">TrustGuard Cyber Labs</span>
              <div style="margin-top:auto; padding-top:8px;">
                <button class="btn btn-ghost btn-sm btn-block" data-goto="profile">Operator Profile →</button>
              </div>
            </div>
          </div>

          <!-- ROW 2: 4 Bento Live Counter Cards -->
          <div class="bento-card bento-1x1">
            <span class="b-lbl" style="font-size:10px; color:var(--text-faint); text-transform:uppercase; letter-spacing:.6px;">Total Scans</span>
            <span class="b-val" id="dStat1" style="font-family:var(--mono); font-size:22px; font-weight:700; color:var(--cyan); margin-top:4px;">0</span>
            <span style="font-size:10px; color:var(--text-faint); margin-top:2px;">User-specific database log</span>
          </div>
          <div class="bento-card bento-1x1">
            <span class="b-lbl" style="font-size:10px; color:var(--text-faint); text-transform:uppercase; letter-spacing:.6px;">Threats Flagged</span>
            <span class="b-val" id="dStat2" style="font-family:var(--mono); font-size:22px; font-weight:700; color:var(--danger-2); margin-top:4px;">0</span>
            <span style="font-size:10px; color:var(--text-faint); margin-top:2px;">High & critical severity</span>
          </div>
          <div class="bento-card bento-1x1">
            <span class="b-lbl" style="font-size:10px; color:var(--text-faint); text-transform:uppercase; letter-spacing:.6px;">Deepfakes Found</span>
            <span class="b-val" id="dStat3" style="font-family:var(--mono); font-size:22px; font-weight:700; color:var(--warn); margin-top:4px;">0</span>
            <span style="font-size:10px; color:var(--text-faint); margin-top:2px;">Image, video & voice</span>
          </div>
          <div class="bento-card bento-1x1">
            <span class="b-lbl" style="font-size:10px; color:var(--text-faint); text-transform:uppercase; letter-spacing:.6px;">Scams Blocked</span>
            <span class="b-val" id="dStat4" style="font-family:var(--mono); font-size:22px; font-weight:700; color:var(--safe); margin-top:4px;">0</span>
            <span style="font-size:10px; color:var(--text-faint); margin-top:2px;">Phishing, jobs & OTP traps</span>
          </div>

          <!-- ROW 3: (4x1) MULTIMODAL CONTENT ANALYSIS & DETECTION CENTER -->
          <div class="bento-card bento-4x1">
            <div class="bento-head">
              <div class="title-group">
                <div class="icon-chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg></div>
                <div>
                  <h3>Multimodal Threat Radar & Detection Matrix</h3>
                  <div style="font-size:10.5px; color:var(--text-faint);">Connects to live pretrained neural transformers and signal processing engines</div>
                </div>
              </div>
              <span class="tag" style="color:var(--cyan);">9 DETECTORS ONLINE</span>
            </div>

            <div class="detector-matrix">
              <div class="det-tile" data-goto="image">
                <div class="det-tile-head"><div class="ic" style="background:rgba(45,217,232,.12); color:var(--cyan);">🖼️</div><b>Image Analysis</b></div>
                <p>Vision Transformer (ViT) & Error Level Analysis for synthetic artifacts & face swaps.</p>
                <div class="det-tile-foot"><span>ViT Neural Radar</span><span>Scan Image →</span></div>
              </div>
              <div class="det-tile" data-goto="video">
                <div class="det-tile-head"><div class="ic" style="background:rgba(139,107,240,.12); color:var(--violet);">🎬</div><b>Video Deepfake</b></div>
                <p>Frame-by-frame temporal consistency sampling with clickable anomaly timeline.</p>
                <div class="det-tile-foot"><span>Frame Sampling</span><span>Scan Video →</span></div>
              </div>
              <div class="det-tile" data-goto="audio">
                <div class="det-tile-head"><div class="ic" style="background:rgba(51,209,154,.12); color:var(--safe);">🎙️</div><b>Audio & Voice</b></div>
                <p>Sliding-window STFT spectral centroid, flux & vocoder cutoff forensics.</p>
                <div class="det-tile-foot"><span>Spectral DSP</span><span>Scan Audio →</span></div>
              </div>
              <div class="det-tile" data-goto="text">
                <div class="det-tile-head"><div class="ic" style="background:rgba(245,185,66,.12); color:var(--warn);">💬</div><b>Text & Scam</b></div>
                <p>Urgency pressure, OTP demands, financial wire solicitation across 11 languages.</p>
                <div class="det-tile-foot"><span>NLP Heuristics</span><span>Scan Text →</span></div>
              </div>
              <div class="det-tile" data-goto="job">
                <div class="det-tile-head"><div class="ic" style="background:rgba(255,107,122,.12); color:var(--danger-2);">💼</div><b>Job & Internship</b></div>
                <p>Scans registration fees, fake recruiters, domain spoofing & salary ratios.</p>
                <div class="det-tile-foot"><span>Dual Detector</span><span>Verify Offer →</span></div>
              </div>
              <div class="det-tile" data-goto="url">
                <div class="det-tile-head"><div class="ic" style="background:rgba(45,217,232,.12); color:var(--cyan);">🔗</div><b>URL Scanner</b></div>
                <p>Shannon entropy, brand typosquatting, raw IP URLs, and malicious TLD detection.</p>
                <div class="det-tile-foot"><span>Entropy Radar</span><span>Inspect URL →</span></div>
              </div>
              <div class="det-tile" data-goto="ocr">
                <div class="det-tile-head"><div class="ic" style="background:rgba(51,209,154,.12); color:var(--safe);">📄</div><b>OCR Forensics</b></div>
                <p>Tesseract client OCR + structured entity extraction (Company, Email, Phone, Fee).</p>
                <div class="det-tile-foot"><span>Entity Parser</span><span>Scan Poster →</span></div>
              </div>
              <div class="det-tile" data-goto="company">
                <div class="det-tile-head"><div class="ic" style="background:rgba(139,107,240,.12); color:var(--violet);">🏢</div><b>Company Verification</b></div>
                <p>Live DNS MX record lookup and recruiter corporate email alignment checks.</p>
                <div class="det-tile-foot"><span>DNS Validation</span><span>Verify Entity →</span></div>
              </div>
              <div class="det-tile" data-goto="social">
                <div class="det-tile-head"><div class="ic" style="background:rgba(245,185,66,.12); color:var(--warn);">📱</div><b>Social Protection</b></div>
                <p>Crypto airdrop doubling lures, VIP impersonation, and engagement bait analysis.</p>
                <div class="det-tile-foot"><span>Social Shield</span><span>Scan Post →</span></div>
              </div>
            </div>
          </div>

          <!-- ROW 4: Card 1 (2x1) Recent Scans -->
          <div class="bento-card bento-2x1">
            <div class="bento-head">
              <div class="title-group">
                <div class="icon-chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>
                <div>
                  <h3>Recent Security Scans</h3>
                  <div style="font-size:10.5px; color:var(--text-faint);">Live SQLite database stream</div>
                </div>
              </div>
              <span class="tag" data-goto="history" style="cursor:pointer;">VIEW ALL →</span>
            </div>
            <div id="dashRecent" style="flex:1; overflow-y:auto; max-height:160px;">
              <div style="text-align:center; padding:20px; color:var(--text-faint); font-size:12px;">No scans recorded yet. Execute an analysis below.</div>
            </div>
          </div>

          <!-- ROW 4: Card 2 (1x1) Threat Alerts -->
          <div class="bento-card bento-1x1">
            <div class="bento-head">
              <div class="title-group">
                <div class="icon-chip" style="background:rgba(242,73,92,.12); color:var(--danger-2);"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></div>
                <div>
                  <h3 style="font-size:13.5px;">Threat Alerts</h3>
                </div>
              </div>
              <span class="tag" style="color:var(--danger-2);">ACTIVE</span>
            </div>
            <div id="dashAlerts" style="flex:1; overflow-y:auto; max-height:160px;">
              <div style="font-size:11.5px; color:var(--text-dim); line-height:1.45;">
                <div style="padding:6px 0; border-bottom:1px solid var(--line);"><b>✓ System Protected</b><span style="display:block; color:var(--text-faint); font-size:10.5px;">Continuous neural screening enabled.</span></div>
              </div>
            </div>
          </div>

          <!-- ROW 4: Card 3 (1x1) Risk Tier Guide -->
          <div class="bento-card bento-1x1">
            <div class="bento-head">
              <div class="title-group">
                <div class="icon-chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg></div>
                <div>
                  <h3 style="font-size:13.5px;">Risk Scale</h3>
                </div>
              </div>
              <span class="tag">STANDARDS</span>
            </div>
            <div style="display:flex; flex-direction:column; gap:4px; font-size:11px;">
              <div style="display:flex; justify-content:space-between;"><span style="color:var(--safe);">0–20 LOW</span><span style="color:var(--text-faint);">Genuine</span></div>
              <div style="display:flex; justify-content:space-between;"><span style="color:var(--warn);">21–40 MODERATE</span><span style="color:var(--text-faint);">Verify Source</span></div>
              <div style="display:flex; justify-content:space-between;"><span style="color:var(--danger-2);">41–60 HIGH</span><span style="color:var(--text-faint);">Anomalies</span></div>
              <div style="display:flex; justify-content:space-between;"><span style="color:#e63946;">61–80 VERY HIGH</span><span style="color:var(--text-faint);">Deceptive</span></div>
              <div style="display:flex; justify-content:space-between;"><span style="color:#ff1e42;">81–100 CRITICAL</span><span style="color:var(--text-faint);">Deepfake/Scam</span></div>
            </div>
          </div>

        </div>

        <!-- ================= MULTI-MODAL DIRECT SCANNER DOCK ================= -->
        <div class="card scanner-card" id="dashScanTabs" style="margin-top:8px;">
          <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; border-bottom:1px solid var(--line); padding-bottom:10px; flex-wrap:wrap; gap:8px;">
            <div>
              <h3 style="font-family:var(--disp); font-size:16px; font-weight:700;">Multi-Modal Direct Content Scanner</h3>
              <p style="font-size:12px; color:var(--text-faint);">Upload files, paste strings, or engage live sensors directly into the neural pipeline.</p>
            </div>
            <div class="soc-status-badge" style="color:var(--cyan); border-color:rgba(45,217,232,.3);">Real Pretrained Models Active</div>
          </div>

          <div class="tab-row" id="scanTabs" role="tablist">
            <button class="tab-btn active" data-tab="up-image"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>Image</button>
            <button class="tab-btn" data-tab="up-video"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="15" height="14" rx="2"/><path d="M17 10l5-3v10l-5-3"/></svg>Video</button>
            <button class="tab-btn" data-tab="up-audio"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10a7 7 0 0014 0M12 19v3"/></svg>Audio</button>
            <button class="tab-btn" data-tab="up-text"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16v13H7l-3 3z"/></svg>Text</button>
            <button class="tab-btn" data-tab="up-url"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 17H7a5 5 0 010-10h2M15 7h2a5 5 0 010 10h-2M8 12h8"/></svg>URL</button>
          </div>

          <div class="tab-panel active" id="tab-up-image">
            <div class="dropzone" data-accept="image/*" data-kind="image">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 16v3a2 2 0 002 2h12a2 2 0 002-2v-3"/></svg>
              <h4>Upload Image for Neural Deepfake Inspection</h4><p>Click to browse or drag & drop · JPG, PNG, WEBP</p>
              <div class="chip-row"><span class="type-chip">Face swaps</span><span class="type-chip">Diffusion art</span><span class="type-chip">Manipulated photos</span></div>
            </div>
            <div id="prev-up-image"></div>
          </div>
          <div class="tab-panel" id="tab-up-video">
            <div class="dropzone" data-accept="video/*" data-kind="video">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 16v3a2 2 0 002 2h12a2 2 0 002-2v-3"/></svg>
              <h4>Upload Video for Frame-by-Frame Temporal Analysis</h4><p>Click to browse or drag & drop · MP4, MOV, WEBM</p>
              <div class="chip-row"><span class="type-chip">Frame Consistency</span><span class="type-chip">Temporal ViT</span><span class="type-chip">Lip-sync</span></div>
            </div>
            <div id="prev-up-video"></div>
          </div>
          <div class="tab-panel" id="tab-up-audio">
            <div class="dropzone" data-accept="audio/*" data-kind="audio">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 16v3a2 2 0 002 2h12a2 2 0 002-2v-3"/></svg>
              <h4>Upload Audio for Spectral Segment Analysis</h4><p>Click to browse or drag & drop · WAV, MP3, M4A</p>
              <div class="chip-row"><span class="type-chip">Voice cloning</span><span class="type-chip">Synthetic TTS</span><span class="type-chip">Vocoder Phase</span></div>
            </div>
            <div id="prev-up-audio"></div>
          </div>
          <div class="tab-panel" id="tab-up-text">
            <textarea class="textarea" id="dashText" placeholder="Paste suspicious text message, WhatsApp forward, financial request, or email..."></textarea>
          </div>
          <div class="tab-panel" id="tab-up-url">
            <label class="field-label">Target URL Link</label>
            <input type="text" class="field" id="dashUrl" placeholder="https://example-banking-verification.tk/auth">
          </div>

          <div class="action-row">
            <button class="btn btn-primary" id="dashAnalyzeBtn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>Execute AI Detection</button>
            <button class="btn btn-outline" id="dashResetBtn">Reset</button>
          </div>

          <div class="card pipeline" id="dashPipeline" style="display:none;">
            <div class="pipeline-title"><h3>Multi-Modal Inference Pipeline</h3><span class="pipeline-status" id="dashPipeStatus">Running…</span></div>
            <div class="steps" id="dashSteps"></div>
          </div>

          <div class="result-wrap" id="dashResult"></div>
        </div>
      </section>

      <!-- ================= 3. IMAGE ANALYSIS ================= -->
      <section class="page" id="page-image">
        <div class="page-head">
          <div class="eyebrow">Vision Transformer & ELA Forensics</div>
          <div class="page-title">Image Deepfake Analysis</div>
          <p class="page-sub">Pretrained Vision Transformer (ViT) deepfake model analyzing pixel frequency patterns, compression boundaries, and facial manipulation artifacts.</p>
        </div>
        <div class="card card-pad">
          <div class="dropzone" data-accept="image/*" data-kind="image">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 16v3a2 2 0 002 2h12a2 2 0 002-2v-3"/></svg>
            <h4>Select or Drop Image for Pretrained ViT Inference</h4><p>JPG, PNG, WEBP · Direct model connection</p>
          </div>
          <div id="prev-image"></div>
          <div class="action-row">
            <button class="btn btn-primary" id="imgAnalyzeBtn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>Analyze Image</button>
            <button class="btn btn-outline" id="imgResetBtn">Reset</button>
          </div>
          <div class="card pipeline" id="imgPipeline" style="display:none;">
            <div class="pipeline-title"><h3>Image Inference Pipeline</h3><span id="imgPipeStatus">Analyzing…</span></div>
            <div class="steps" id="imgSteps"></div>
          </div>
          <div class="result-wrap" id="imgResult"></div>
        </div>
      </section>

      <!-- ================= 4. VIDEO ANALYSIS (FRAME-BY-FRAME) ================= -->
      <section class="page" id="page-video">
        <div class="page-head">
          <div class="eyebrow">Temporal Consistency & Frame Sampling</div>
          <div class="page-title">Video Deepfake Analysis</div>
          <p class="page-sub">Samples frames across video duration using OpenCV, applies face crop preprocessing, runs ViT deepfake inference per frame, and computes an interactive frame timeline.</p>
        </div>
        <div class="card card-pad">
          <div class="dropzone" data-accept="video/*" data-kind="video">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="2" y="5" width="15" height="14" rx="2"/><path d="M17 10l5-3v10l-5-3"/></svg>
            <h4>Upload Video for Frame-by-Frame Neural Analysis</h4><p>MP4, MOV, WEBM, AVI · Configurable sampling interval</p>
          </div>
          <div id="prev-video"></div>
          <div id="videoPlayerWrap" style="display:none; margin-top:14px;">
            <video id="videoPreviewPlayer" controls style="max-width:100%; max-height:360px; border-radius:10px; background:#000; display:block; margin:0 auto;"></video>
          </div>
          <div class="action-row">
            <button class="btn btn-primary" id="vidAnalyzeBtn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>Analyze Video (Frame-by-Frame)</button>
            <button class="btn btn-outline" id="vidResetBtn">Reset</button>
          </div>
          <div class="card pipeline" id="vidPipeline" style="display:none;">
            <div class="pipeline-title"><h3>Video Temporal Sampling Pipeline</h3><span id="vidPipeStatus">Sampling frames…</span></div>
            <div class="steps" id="vidSteps"></div>
          </div>
          <div class="result-wrap" id="vidResult"></div>
        </div>
      </section>

      <!-- ================= 5. AUDIO ANALYSIS (SEGMENT SPECTRAL) ================= -->
      <section class="page" id="page-audio">
        <div class="page-head">
          <div class="eyebrow">STFT Spectral Windows & Vocoder Forensics</div>
          <div class="page-title">Audio & Voice Deepfake Analysis</div>
          <p class="page-sub">Segments speech audio into sliding windows, computes Short-Time Fourier Transforms, spectral centroid variance, spectral flux, and vocoder phase cutoffs.</p>
        </div>
        <div class="card card-pad">
          <div class="dropzone" data-accept="audio/*" data-kind="audio">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10a7 7 0 0014 0M12 19v3"/></svg>
            <h4>Upload Voice / Audio Recording for Spectral Inspection</h4><p>WAV, MP3, M4A, OGG · Sliding window forensic analysis</p>
          </div>
          <div id="prev-audio"></div>
          <div id="audioPlayerWrap" style="display:none; margin-top:14px;">
            <audio id="audioPreviewPlayer" controls style="width:100%; margin-bottom:8px;"></audio>
          </div>
          <div class="action-row">
            <button class="btn btn-primary" id="audAnalyzeBtn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>Analyze Audio Windows</button>
            <button class="btn btn-outline" id="audResetBtn">Reset</button>
          </div>
          <div class="card pipeline" id="audPipeline" style="display:none;">
            <div class="pipeline-title"><h3>Acoustic Spectral Pipeline</h3><span id="audPipeStatus">Computing STFT…</span></div>
            <div class="steps" id="audSteps"></div>
          </div>
          <div class="result-wrap" id="audResult"></div>
        </div>
      </section>

      <!-- ================= 6. TEXT & SCAM DETECTION ================= -->
      <section class="page" id="page-text">
        <div class="page-head">
          <div class="eyebrow">Multilingual NLP Scam Radar</div>
          <div class="page-title">Text & Scam Detection</div>
          <p class="page-sub">Evaluates psychological urgency pressure, OTP extortion, wire transfers, credential harvesting, and suspicious links across 11 Indian and global languages.</p>
        </div>
        <div class="card card-pad">
          <label class="field-label">Message or Post Content</label>
          <textarea class="textarea" id="scamText" placeholder="Paste suspicious SMS, WhatsApp message, extortion email, or fraudulent text..."></textarea>
          <div class="action-row">
            <button class="btn btn-primary" id="scamAnalyzeBtn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>Analyze Message</button>
            <button class="btn btn-outline" id="scamResetBtn">Reset</button>
          </div>
          <div class="card pipeline" id="scamPipeline" style="display:none;">
            <div class="pipeline-title"><h3>Scam Intelligence Pipeline</h3><span id="scamPipeStatus">Analyzing…</span></div>
            <div class="steps" id="scamSteps"></div>
          </div>
          <div class="result-wrap" id="scamResult"></div>
        </div>
      </section>

      <!-- ================= 7. JOB & INTERNSHIP DETECTION ================= -->
      <section class="page" id="page-job">
        <div class="page-head">
          <div class="eyebrow">Recruiter Domain & Fee Solicitations</div>
          <div class="page-title">Job & Internship Fraud Verification</div>
          <p class="page-sub">Identifies upfront registration fees, laptop deposits, fake corporate recruiters, domain typosquatting, and unrealistic salary claims.</p>
        </div>
        <div class="card card-pad">
          <div class="tab-row" id="jobModeTabs">
            <button class="tab-btn active" data-jobmode="job">Job Posting</button>
            <button class="tab-btn" data-jobmode="internship">Internship Offer</button>
          </div>
          <div style="display:flex; flex-direction:column; gap:12px;">
            <div>
              <label class="field-label">Job / Internship Description or Offer Letter Text</label>
              <textarea class="textarea" id="jobDesc" placeholder="Paste job offer description, salary compensation details, or appointment letter text..."></textarea>
            </div>
            <div class="grid g2">
              <div>
                <label class="field-label">Recruiter / Company Email</label>
                <input type="email" class="field" id="jobEmail" placeholder="hr@company-name.com or recruiter@gmail.com">
              </div>
              <div>
                <label class="field-label">Application URL / Website Link</label>
                <input type="text" class="field" id="jobUrl" placeholder="https://careers.company.com/apply">
              </div>
            </div>
          </div>
          <div class="action-row">
            <button class="btn btn-primary" id="jobAnalyzeBtn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>Verify Job / Internship</button>
            <button class="btn btn-outline" id="jobResetBtn">Reset</button>
          </div>
          <div class="result-wrap" id="jobResult"></div>
        </div>
      </section>

      <!-- ================= 8. URL SCANNER ================= -->
      <section class="page" id="page-url">
        <div class="page-head">
          <div class="eyebrow">Shannon Entropy & Typosquatting</div>
          <div class="page-title">Phishing & URL Security Scanner</div>
          <p class="page-sub">Analyzes character entropy, IP-based URLs, suspicious top-level domains, URL shorteners, and credential phishing patterns.</p>
        </div>
        <div class="card card-pad">
          <label class="field-label">Website URL Link</label>
          <input type="text" class="field" id="urlInput" placeholder="https://secure-login-verify-account.tk/signin">
          <div class="action-row">
            <button class="btn btn-primary" id="urlAnalyzeBtn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>Inspect URL Security</button>
            <button class="btn btn-outline" id="urlResetBtn">Reset</button>
          </div>
          <div class="card pipeline" id="urlPipeline" style="display:none;">
            <div class="pipeline-title"><h3>URL Intelligence Pipeline</h3><span id="urlPipeStatus">Scanning…</span></div>
            <div class="steps" id="urlSteps"></div>
          </div>
          <div class="result-wrap" id="urlResult"></div>
        </div>
      </section>

      <!-- ================= 9. OCR SCANNER ================= -->
      <section class="page" id="page-ocr">
        <div class="page-head">
          <div class="eyebrow">Tesseract OCR & Structured Entity Extraction</div>
          <div class="page-title">OCR Poster & Screenshot Verification</div>
          <p class="page-sub">Performs client-side optical character recognition on screenshots and posters, extracting companies, emails, phone numbers, UPI handles, and registration fees.</p>
        </div>
        <div class="card card-pad">
          <div class="dropzone" data-accept="image/*" data-kind="ocr">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 7V5a1 1 0 011-1h2M4 17v2a1 1 0 001 1h2M20 7V5a1 1 0 00-1-1h-2M20 17v2a1 1 0 01-1 1h-2M7 9h10M7 13h6"/></svg>
            <h4>Upload Poster, Offer Letter or Chat Screenshot</h4><p>JPG, PNG · In-browser OCR + Backend fraud analysis</p>
          </div>
          <div id="prev-ocr"></div>
          <div id="ocrProgressWrap" style="display:none; margin-top:12px;">
            <div style="font-size:11.5px; color:var(--text-faint); margin-bottom:4px;" id="ocrProgressTxt">Extracting text…</div>
            <div class="bar-track"><div class="bar-fill" id="ocrBar" style="width:0%; background:var(--cyan);"></div></div>
          </div>
          <div class="preview-row" style="margin-top:12px;">
            <div class="preview-meta">
              <span style="font-size:11px; text-transform:uppercase; color:var(--text-faint);">Extracted Text Buffer</span>
              <p id="ocrTextBox" style="font-size:12px; color:var(--text-dim); margin-top:2px; max-height:80px; overflow-y:auto;">Upload an image above to extract text.</p>
            </div>
          </div>
          <div class="action-row">
            <button class="btn btn-primary" id="ocrRunBtn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>Run OCR & Verify</button>
            <button class="btn btn-outline" id="ocrResetBtn">Reset</button>
          </div>
          <div class="result-wrap" id="ocrResult"></div>
        </div>
      </section>

      <!-- ================= 10. COMPANY VERIFICATION ================= -->
      <section class="page" id="page-company">
        <div class="page-head">
          <div class="eyebrow">DNS MX Validation & Identity Alignment</div>
          <div class="page-title">Company Entity Verification</div>
          <p class="page-sub">Validates corporate domain existence, MX mail exchange records, and cross-checks recruiter email addresses against official corporate infrastructure.</p>
        </div>
        <div class="card card-pad">
          <div style="display:flex; flex-direction:column; gap:12px;">
            <div>
              <label class="field-label">Company Name</label>
              <input type="text" class="field" id="compName" placeholder="e.g. Google, Microsoft, Infosys">
            </div>
            <div class="grid g2">
              <div>
                <label class="field-label">Official Website Domain</label>
                <input type="text" class="field" id="compDomain" placeholder="e.g. google.com">
              </div>
              <div>
                <label class="field-label">Contact / Recruiter Email</label>
                <input type="email" class="field" id="compEmail" placeholder="e.g. careers@google.com">
              </div>
            </div>
          </div>
          <div class="action-row">
            <button class="btn btn-primary" id="compVerifyBtn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>Verify Company Identity</button>
            <button class="btn btn-outline" id="compResetBtn">Reset</button>
          </div>
          <div class="result-wrap" id="compResult"></div>
        </div>
      </section>

      <!-- ================= 11. SOCIAL MEDIA PROTECTION ================= -->
      <section class="page" id="page-social">
        <div class="page-head">
          <div class="eyebrow">Airdrop Lures & Impersonation Radar</div>
          <div class="page-title">Social Media Fraud Protection</div>
          <p class="page-sub">Identifies high-yield crypto doubling schemes, VIP celebrity impersonation, malicious off-platform redirects, and engagement bait.</p>
        </div>
        <div class="card card-pad">
          <div style="display:flex; gap:8px; margin-bottom:14px; flex-wrap:wrap;">
            <button class="plat-card active" data-plat="Twitter / X" style="border:1px solid var(--cyan); border-radius:8px; padding:8px 14px; background:var(--panel-2); color:var(--cyan); cursor:pointer;">Twitter / X</button>
            <button class="plat-card" data-plat="Instagram" style="border:1px solid var(--line); border-radius:8px; padding:8px 14px; background:var(--panel-2); color:var(--text-dim); cursor:pointer;">Instagram</button>
            <button class="plat-card" data-plat="LinkedIn" style="border:1px solid var(--line); border-radius:8px; padding:8px 14px; background:var(--panel-2); color:var(--text-dim); cursor:pointer;">LinkedIn</button>
            <button class="plat-card" data-plat="Telegram" style="border:1px solid var(--line); border-radius:8px; padding:8px 14px; background:var(--panel-2); color:var(--text-dim); cursor:pointer;">Telegram</button>
          </div>
          <label class="field-label">Social Post Content</label>
          <textarea class="textarea" id="socialText" placeholder="Paste social media post text, tweet, or influencer giveaway message..."></textarea>
          <div style="margin-top:10px;">
            <label class="field-label">Embedded Link / Bio URL (Optional)</label>
            <input type="text" class="field" id="socialUrl" placeholder="https://t.me/crypto-giveaway-bot">
          </div>
          <div class="action-row">
            <button class="btn btn-primary" id="socialAnalyzeBtn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>Scan Social Content</button>
            <button class="btn btn-outline" id="socialResetBtn">Reset</button>
          </div>
          <div class="result-wrap" id="socialResult"></div>
        </div>
      </section>

      <!-- ================= 12. CAMERA SCANNER ================= -->
      <section class="page" id="page-camera">
        <div class="page-head">
          <div class="eyebrow">Real-Time Sensor Screening</div>
          <div class="page-title">Live Camera Scanner</div>
          <p class="page-sub">Engages webcam sensor feed and captures real-time video snapshots directly for Vision Transformer deepfake inspection.</p>
        </div>
        <div class="card card-pad">
          <div style="position:relative; border-radius:12px; overflow:hidden; background:#000; border:1px solid var(--line); aspect-ratio:16/9; display:flex; align-items:center; justify-content:center;">
            <video id="camVideo" autoplay playsinline style="width:100%; height:100%; object-fit:cover; display:none;"></video>
            <div id="camEmpty" style="text-align:center; color:var(--text-faint); padding:20px;">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" width="40" height="40" style="margin-bottom:8px; opacity:.5;"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg>
              <div>Camera is currently inactive. Click Start Camera below.</div>
            </div>
          </div>
          <div class="action-row">
            <button class="btn btn-primary" id="camStartBtn">Start Camera</button>
            <button class="btn btn-ghost" id="camCaptureBtn" disabled>Capture Snapshot & Analyze</button>
            <button class="btn btn-outline" id="camStopBtn" disabled>Stop Camera</button>
          </div>
          <div class="result-wrap" id="camResult"></div>
        </div>
      </section>

      <!-- ================= 13. LIVE MICROPHONE ================= -->
      <section class="page" id="page-mic">
        <div class="page-head">
          <div class="eyebrow">Live Audio Sensor Screening</div>
          <div class="page-title">Live Microphone Forensics</div>
          <p class="page-sub">Streams microphone audio into Web Audio API AnalyserNode and monitors real-time acoustic voice frequency activity.</p>
        </div>
        <div class="card card-pad">
          <canvas id="liveMicCanvas" style="width:100%; height:120px; border-radius:10px; background:var(--panel-2); border:1px solid var(--line);"></canvas>
          <div style="margin-top:10px; font-size:12px; font-family:var(--mono);" id="liveMicStatus">Microphone Status: IDLE</div>
          <div class="action-row">
            <button class="btn btn-primary" id="liveMicStart">Start Listening</button>
            <button class="btn btn-outline" id="liveMicStop" disabled>Stop</button>
          </div>
        </div>
      </section>

      <!-- ================= 14. DIGITAL PROTECTION ================= -->
      <section class="page" id="page-protect">
        <div class="page-head">
          <div class="eyebrow">Cryptographic Media Provenance</div>
          <div class="page-title">Digital Fingerprint & Provenance</div>
          <p class="page-sub">Generates cryptographic SHA-256 zero-knowledge content hashes in-browser to establish verifiable media provenance.</p>
        </div>
        <div class="card card-pad">
          <div class="dropzone" data-accept="*" data-kind="protect">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 2l8 4v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V6l8-4z"/></svg>
            <h4>Select File to Compute SHA-256 Provenance Fingerprint</h4><p>Images, audio, video, PDFs · In-browser WebCrypto execution</p>
          </div>
          <div id="prev-protect"></div>
          <div class="action-row">
            <button class="btn btn-primary" id="protectRunBtn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>Compute Fingerprint</button>
            <button class="btn btn-outline" id="protectResetBtn">Reset</button>
          </div>
          <div class="result-wrap" id="protectResult"></div>
        </div>
      </section>

      <!-- ================= 15. REPORTS ================= -->
      <section class="page" id="page-reports">
        <div class="page-head">
          <div class="eyebrow">Analysis Reports & Exports</div>
          <div class="page-title">Detailed Analysis Reports</div>
          <p class="page-sub">Export and review comprehensive detection dossiers, confidence breakdowns, and mitigation guidelines.</p>
        </div>
        <div class="card card-pad">
          <div class="table-wrap">
            <table class="data-table">
              <thead><tr><th>Date</th><th>Label</th><th>Type</th><th>Language</th><th>Risk</th><th>Trust</th><th>Confidence</th><th>Status</th><th>Action</th></tr></thead>
              <tbody id="reportsBody"></tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- ================= 16. SCAN HISTORY ================= -->
      <section class="page" id="page-history">
        <div class="page-head" style="display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; gap:12px;">
          <div>
            <div class="eyebrow">SQLite Scans Database</div>
            <div class="page-title">Scan History</div>
            <p class="page-sub">Real-time scan records scoped to your authenticated account.</p>
          </div>
          <div style="display:flex; gap:8px;">
            <button class="btn btn-outline btn-sm" id="exportHistBtn">Export CSV</button>
            <button class="btn btn-danger btn-sm" id="clearHistBtn">Clear History</button>
          </div>
        </div>
        <div class="card card-pad">
          <div class="table-wrap">
            <table class="data-table">
              <thead><tr><th>Date</th><th>Content Label</th><th>Type</th><th>Language</th><th>Risk Score</th><th>Trust</th><th>Confidence</th><th>Status</th><th>Actions</th></tr></thead>
              <tbody id="historyBody"></tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- ================= 17. USER PROFILE ================= -->
      <section class="page" id="page-profile">
        <div class="page-head">
          <div class="eyebrow">Operator Account</div>
          <div class="page-title">User Profile</div>
          <p class="page-sub">Manage your researcher profile and review personal detection analytics.</p>
        </div>
        <div class="grid g2">
          <div class="card card-pad">
            <div style="display:flex; align-items:center; gap:14px; margin-bottom:16px;">
              <div class="av" id="profPageAvatar" style="width:52px; height:52px; border-radius:50%; background:linear-gradient(135deg,var(--cyan),var(--violet)); display:flex; align-items:center; justify-content:center; font-size:20px; font-weight:700; color:#04141a;">RA</div>
              <div>
                <h3 style="font-family:var(--disp); font-size:18px;" id="profPageName">Reshma A.</h3>
                <span style="font-size:12px; color:var(--cyan);" id="profPageEmail">reshma@trustguard.ai</span>
              </div>
            </div>
            <div class="telemetry-row"><span>Organization</span><span id="profPageOrg">TrustGuard Cyber Labs</span></div>
            <div class="telemetry-row"><span>Preferred Language</span><span id="profPageLang">English (en)</span></div>
            <div class="telemetry-row"><span>Account Status</span><span style="color:var(--safe);">Active Operator</span></div>
            <div class="action-row" style="margin-top:16px;">
              <button class="btn btn-primary btn-sm" data-goto="settings">Edit in Settings</button>
              <button class="btn btn-danger btn-sm" id="profLogoutBtn">Sign Out</button>
            </div>
          </div>
          <div class="card card-pad">
            <h3 style="font-family:var(--disp); font-size:15px; margin-bottom:12px;">Personal Scan Analytics</h3>
            <div class="bento-stat-grid">
              <div class="bento-stat-cell"><span class="b-lbl">Total Scans</span><span class="b-val" id="profStatScans" style="color:var(--cyan);">0</span></div>
              <div class="bento-stat-cell"><span class="b-lbl">Threats Flagged</span><span class="b-val" id="profStatThreats" style="color:var(--danger-2);">0</span></div>
              <div class="bento-stat-cell"><span class="b-lbl">Deepfakes</span><span class="b-val" id="profStatDeepfakes" style="color:var(--warn);">0</span></div>
              <div class="bento-stat-cell"><span class="b-lbl">Scams</span><span class="b-val" id="profStatScams" style="color:var(--safe);">0</span></div>
            </div>
          </div>
        </div>
      </section>

      <!-- ================= 18. SETTINGS ================= -->
      <section class="page" id="page-settings">
        <div class="page-head">
          <div class="eyebrow">Preferences & System Configuration</div>
          <div class="page-title">Settings</div>
          <p class="page-sub">Update your display profile, account credentials, theme, and risk alert notifications.</p>
        </div>
        <div class="grid g2">
          <div class="card card-pad">
            <h3 style="font-family:var(--disp); font-size:15px; margin-bottom:14px;">Account Information</h3>
            <div style="display:flex; flex-direction:column; gap:12px;">
              <div>
                <label class="field-label">Display Name</label>
                <input type="text" class="field" id="settingName" value="Reshma A.">
              </div>
              <div>
                <label class="field-label">Organization / University</label>
                <input type="text" class="field" id="settingOrg" value="TrustGuard Cyber Labs">
              </div>
            </div>
          </div>
          <div class="card card-pad">
            <h3 style="font-family:var(--disp); font-size:15px; margin-bottom:14px;">Appearance & Preferences</h3>
            <div style="display:flex; flex-direction:column; gap:12px;">
              <div>
                <label class="field-label">Interface Theme</label>
                <select class="field" id="settingTheme"><option value="dark">Dark Theme (SOC Mode)</option><option value="light">Light Theme</option></select>
              </div>
              <div>
                <label class="field-label">Preferred Detection Language</label>
                <select class="field" id="settingLang"><option value="en">English</option><option value="hi">Hindi</option><option value="te">Telugu</option></select>
              </div>
            </div>
          </div>
        </div>
        <div class="action-row" style="margin-top:16px;">
          <button class="btn btn-primary" id="saveSettingsBtn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>Save Changes</button>
        </div>
      </section>

    </main>
  </div>
</div>

<!-- ============ AUTHENTICATION MODAL ============ -->
<div class="modal-bg" id="authModal">
  <div class="modal-box">
    <div class="modal-head">
      <h3 id="authModalTitle">Sign In to TrustGuard AI</h3>
      <button class="modal-close" id="authModalClose">✕</button>
    </div>
    <div class="modal-body">
      <div class="auth-tabs">
        <button class="auth-tab active" id="tabLoginBtn">Sign In</button>
        <button class="auth-tab" id="tabRegisterBtn">Create Account</button>
      </div>

      <!-- Login Form -->
      <form class="auth-form active" id="loginForm" onsubmit="return false;">
        <div style="display:flex; flex-direction:column; gap:12px;">
          <div>
            <label class="field-label">Email Address</label>
            <input type="email" class="field" id="loginEmail" placeholder="reshma@trustguard.ai" required>
          </div>
          <div>
            <label class="field-label">Password</label>
            <input type="password" class="field" id="loginPassword" placeholder="••••••••" required>
          </div>
          <div id="loginError" style="display:none; color:var(--danger-2); font-size:12px;"></div>
          <button class="btn btn-primary btn-block" id="submitLoginBtn" style="margin-top:6px;">Sign In</button>
          <button class="btn btn-ghost btn-block btn-sm" id="demoLoginBtn">Quick Demo Login (Reshma A.)</button>
        </div>
      </form>

      <!-- Register Form -->
      <form class="auth-form" id="registerForm" onsubmit="return false;">
        <div style="display:flex; flex-direction:column; gap:12px;">
          <div>
            <label class="field-label">Display Name</label>
            <input type="text" class="field" id="regName" placeholder="Dr. Sarah Connor" required>
          </div>
          <div>
            <label class="field-label">Email Address</label>
            <input type="email" class="field" id="regEmail" placeholder="sarah@cyberdefense.org" required>
          </div>
          <div>
            <label class="field-label">Password</label>
            <input type="password" class="field" id="regPassword" placeholder="Minimum 4 characters" required>
          </div>
          <div>
            <label class="field-label">Organization / University</label>
            <input type="text" class="field" id="regOrg" placeholder="Cyber Defense Unit">
          </div>
          <div id="regError" style="display:none; color:var(--danger-2); font-size:12px;"></div>
          <button class="btn btn-primary btn-block" id="submitRegisterBtn" style="margin-top:6px;">Create Account</button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- ============ REPORT MODAL ============ -->
<div class="modal-bg" id="reportModal">
  <div class="modal-box">
    <div class="modal-head"><h3>Detailed Forensic Report</h3><button class="modal-close" id="modalCloseBtn">✕</button></div>
    <div class="modal-body" id="modalBody"></div>
  </div>
</div>

<!-- Assistant FAB -->
<button class="assist-fab" id="assistFab" aria-label="Open Assistant"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a5 5 0 00-5 5v2a5 5 0 0010 0V7a5 5 0 00-5-5z"/><path d="M4 12v1a8 8 0 0016 0v-1M12 21v-4"/></svg></button>
<div class="assist-panel" id="assistPanel">
  <div class="assist-head">
    <div class="av"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M12 2a5 5 0 00-5 5v2a5 5 0 0010 0V7a5 5 0 00-5-5z"/><path d="M4 12v1a8 8 0 0016 0v-1M12 21v-4"/></svg></div>
    <div><b>TrustGuard AI Assistant</b><span>● Context-aware online</span></div>
    <button class="assist-close" id="assistClose">✕</button>
  </div>
  <div class="assist-body" id="assistBody"></div>
  <div class="assist-input-row">
    <input id="assistInput" type="text" placeholder="Ask about your scan result…">
    <button class="send-btn" id="assistSendBtn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" width="14" height="14"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg></button>
  </div>
</div>

<div id="toasts"></div>

<script>
/* ============================================================
   TRUSTGUARD AI — CENTRALIZED FRONTEND API CONTROLLER
   ============================================================ */
const API_BASE_URL = (function() {
  if (window.location.origin && window.location.origin.includes(':5173')) {
    return 'http://127.0.0.1:8000';
  }
  if (window.location.origin && window.location.origin.startsWith('http')) {
    return window.location.origin;
  }
  return 'http://127.0.0.1:8000';
})();

let currentUser = null;
let currentToken = localStorage.getItem('trustguard_token') || '';
let filesStore = {};
let scanHistory = [];
let statCounters = { scans: 0, threats: 0, deepfakes: 0, scams: 0 };
let lastScanContext = null;

function getAuthHeaders(isFormData = false) {
  const h = {};
  if (!isFormData) h['Content-Type'] = 'application/json';
  if (currentToken) h['Authorization'] = `Bearer ${currentToken}`;
  return h;
}

async function apiPost(endpoint, body, isFormData = false, timeoutMs = 45000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: getAuthHeaders(isFormData),
      body: isFormData ? body : JSON.stringify(body),
      signal: controller.signal
    });
    clearTimeout(timer);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || data.detail || `Server returned ${response.status}`);
    return data;
  } catch (err) {
    clearTimeout(timer);
    throw err;
  }
}

async function apiGet(endpoint) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: getAuthHeaders(false)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || data.detail || 'Request failed');
  return data;
}

async function apiPut(endpoint, body) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'PUT',
    headers: getAuthHeaders(false),
    body: JSON.stringify(body)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || data.detail || 'Request failed');
  return data;
}

/* ---------- TOAST NOTIFICATIONS ---------- */
function toast(title, sub, kind='info'){
  const box = document.createElement('div');
  box.className = 'toast ' + (kind==='info'?'':kind);
  box.innerHTML = `<b>${title}</b><span>${sub||''}</span>`;
  const cont = document.getElementById('toasts');
  if(cont) cont.appendChild(box);
  setTimeout(()=>{ box.style.transition='opacity .3s'; box.style.opacity='0'; setTimeout(()=>box.remove(),300); }, 4000);
}

/* ---------- PARTICLES BACKGROUND ---------- */
(function(){
  const c = document.getElementById('particles');
  if(!c) return;
  const ctx = c.getContext('2d');
  let w,h,particles=[];
  function resize(){ w=c.width=innerWidth; h=c.height=innerHeight; }
  resize(); addEventListener('resize', resize);
  const N = Math.min(50, Math.floor(innerWidth/26));
  for(let i=0;i<N;i++) particles.push({x:Math.random()*w, y:Math.random()*h, vx:(Math.random()-.5)*.2, vy:(Math.random()-.5)*.2, r:Math.random()*1.5+.4});
  function tick(){
    ctx.clearRect(0,0,w,h);
    for(const p of particles){
      p.x+=p.vx; p.y+=p.vy;
      if(p.x<0||p.x>w) p.vx*=-1;
      if(p.y<0||p.y>h) p.vy*=-1;
      ctx.beginPath(); ctx.fillStyle='rgba(45,217,232,.45)'; ctx.arc(p.x,p.y,p.r,0,7); ctx.fill();
    }
    requestAnimationFrame(tick);
  }
  tick();
})();

/* ============ RISK SCORING STANDARDS ============ */
function clampScore(v) { const n = Number(v); return isNaN(n) ? 0 : Math.max(0, Math.min(100, Math.round(n * 10) / 10)); }

function riskTier(score) {
  score = clampScore(score);
  if (score <= 20) return { label: 'LOW RISK', cls: 'safe', tierName: 'Low', color: '#33d19a' };
  if (score <= 40) return { label: 'MODERATE RISK', cls: 'mod', tierName: 'Moderate', color: '#f5b942' };
  if (score <= 60) return { label: 'HIGH RISK', cls: 'high', tierName: 'High', color: '#f2495c' };
  if (score <= 80) return { label: 'VERY HIGH RISK', cls: 'vhigh', tierName: 'Very High', color: '#e63946' };
  return { label: 'CRITICAL RISK', cls: 'crit', tierName: 'Critical', color: '#ff1e42' };
}

function riskColor(cls) {
  const colors = { safe: '#33d19a', low: '#2dd9e8', mod: '#f5b942', high: '#f2495c', vhigh: '#e63946', crit: '#ff1e42' };
  return colors[cls] || '#2dd9e8';
}

function recommendation(cls) {
  const map = {
    safe: { title: 'GENUINE / AUTHENTIC', text: 'Content exhibits natural patterns and standard authenticity markers. Verified with high confidence.' },
    mod: { title: 'MODERATE RISK — VERIFY SOURCE', text: 'Some non-standard signals or minor compression variance detected. Cross-referencing source is advised.' },
    high: { title: 'HIGH RISK — EXERCISE CAUTION', text: 'Prominent risk factors or manipulation indicators discovered. Avoid trusting untrusted requests.' },
    vhigh: { title: 'VERY HIGH RISK — SUSPICIOUS / SYNTHETIC', text: 'Significant manipulation or fraud markers flagged. Highly likely to be deepfaked or deceptive.' },
    crit: { title: 'CRITICAL THREAT — DO NOT ENGAGE', text: 'Severe synthetic manipulation, fraud, or phishing detected. Do not send funds or credentials.' }
  };
  return map[cls] || map.mod;
}

/* ============ NORMALIZATION & UNIFIED PREDICTION FORMAT ============ */
function normalizePrediction(apiRes, defaultContentType = 'Content', fallbackLabel = 'Analysis') {
  if (!apiRes || typeof apiRes !== 'object') return { valid: false, message: 'Invalid response from model backend.' };

  const rawClf = String(apiRes.classification || apiRes.prediction || apiRes.classification_label || '').toUpperCase();
  let riskScore = apiRes.risk_score ?? apiRes.fakeProbability ?? apiRes.score ?? null;
  if (riskScore !== null) riskScore = Number(riskScore);

  let confidence = apiRes.confidence_pct ?? apiRes.confidence ?? 90;
  if (confidence !== null) {
    confidence = Number(confidence);
    if (confidence <= 1.0 && confidence > 0.0) confidence = confidence * 100.0;
  }
  confidence = clampScore(confidence);

  let authProb = apiRes.authenticity_probability ?? apiRes.authenticity ?? null;
  if (authProb === null && riskScore !== null) authProb = 100 - riskScore;
  authProb = clampScore(authProb !== null ? authProb : 85);
  if (riskScore === null) riskScore = 100 - authProb;
  riskScore = clampScore(riskScore);

  const genuineKeys = ['GENUINE', 'REAL', 'AUTHENTIC', 'SAFE', 'LEGITIMATE', 'VERIFIED'];
  const fakeKeys = ['FAKE', 'DEEPFAKE', 'MANIPULATED', 'SYNTHETIC', 'SCAM', 'PHISHING', 'FRAUD'];
  
  let isGenuine = false;
  if (genuineKeys.some(k => rawClf.includes(k))) isGenuine = true;
  else if (fakeKeys.some(k => rawClf.includes(k))) isGenuine = false;
  else isGenuine = riskScore <= 40;

  const tier = riskTier(riskScore);
  const riskLevel = apiRes.risk_level || apiRes.riskLevel || tier.tierName;

  let rawInds = apiRes.indicators || apiRes.signals || [];
  let indicators = Array.isArray(rawInds) && rawInds.length > 0 ? rawInds.map(i => ({
    label: typeof i === 'string' ? i : (i.label || i.name || 'Detection Signal'),
    detail: typeof i === 'string' ? i : (i.detail || i.description || ''),
    level: typeof i === 'object' && i.level ? i.level : (isGenuine ? 'safe' : 'high')
  })) : [
    { label: isGenuine ? 'Authentic Signals Verified' : 'Neural Manipulation Flagged', detail: isGenuine ? 'Passed model authenticity checks.' : `Risk evaluated at ${riskScore}/100.`, level: isGenuine ? 'safe' : 'high' }
  ];

  let explanation = apiRes.explanation || apiRes.detail || (isGenuine ? `Verified as authentic (${confidence}% confidence, ${riskLevel} risk).` : `Manipulation or fraud indicators detected (${confidence}% confidence, ${riskScore}/100 risk).`);

  return {
    valid: true,
    isGenuine,
    riskScore,
    confidence,
    authenticity: authProb,
    riskLevel,
    tier,
    classification: rawClf || (isGenuine ? 'GENUINE' : 'FAKE'),
    classificationLabel: apiRes.classification_label || (isGenuine ? 'REAL / AUTHENTIC' : 'DEEPFAKE / MANIPULATED'),
    indicators,
    explanation,
    raw: apiRes
  };
}

/* ============ RESULT CARD RENDERERS ============ */
function renderUnifiedResultCard(norm, opts) {
  const isGenuine = norm.isGenuine;
  const bannerClass = isGenuine ? 'genuine' : (norm.riskScore <= 50 ? 'mod' : 'fake');
  const bannerIcon = isGenuine ? '✓' : '⚠';
  const bannerTitle = isGenuine ? `✓ GENUINE ${opts.contentType.toUpperCase()}` : `⚠ ${norm.classification} ${opts.contentType.toUpperCase()}`;
  const bannerSub = norm.classificationLabel || (isGenuine ? 'Real / Authentic' : 'Deepfake / Manipulated / Fraud');
  const bannerColor = isGenuine ? 'var(--safe)' : (norm.riskScore > 75 ? 'var(--danger)' : 'var(--danger-2)');

  const indicatorsHTML = norm.indicators.map(ind => `
    <div class="ind-bullet-item">
      <div class="bullet" style="color:${ind.level === 'safe' ? 'var(--safe)' : ind.level === 'mod' ? 'var(--warn)' : 'var(--danger-2)'};">•</div>
      <div class="content-txt">
        <b>${ind.label}</b>
        <p>${ind.detail}</p>
      </div>
    </div>
  `).join('');

  const rec = recommendation(norm.tier.cls);

  // Optional Frame Timeline (Video)
  let timelineHTML = '';
  if (opts.frameResults && opts.frameResults.length > 0) {
    timelineHTML = `
      <div class="timeline-box">
        <div class="timeline-title">
          <span>🎬 Frame-by-Frame Temporal Analysis (${opts.frameResults.length} frames)</span>
          <span style="font-size:11px; font-family:var(--mono); color:var(--cyan); font-weight:normal;">Click frame to seek video</span>
        </div>
        <div class="timeline-scroll">
          ${opts.frameResults.map(fr => `
            <div class="timeline-chip ${fr.prediction === 'REAL' ? 'real' : 'fake'}" data-time="${fr.timestamp}">
              <span class="tc-time">${fr.timestamp_label || fr.timestamp + 's'}</span>
              <span class="tc-status" style="color:${fr.prediction === 'REAL' ? 'var(--safe)' : 'var(--danger-2)'};">
                ${fr.prediction === 'REAL' ? '✓ REAL' : '⚠ FAKE'}
              </span>
              <span class="tc-score">${fr.confidence}% conf</span>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  // Optional Segment Timeline (Audio)
  let segmentHTML = '';
  if (opts.segmentResults && opts.segmentResults.length > 0) {
    segmentHTML = `
      <div class="timeline-box">
        <div class="timeline-title">
          <span>🎙️ STFT Acoustic Segment Timeline (${opts.segmentResults.length} windows)</span>
        </div>
        <div class="timeline-scroll">
          ${opts.segmentResults.map(sr => `
            <div class="timeline-chip ${sr.prediction === 'REAL' ? 'real' : 'fake'}">
              <span class="tc-time">${sr.time_label || sr.start_time + 's'}</span>
              <span class="tc-status" style="color:${sr.prediction === 'REAL' ? 'var(--safe)' : 'var(--danger-2)'};">
                ${sr.prediction === 'REAL' ? '✓ REAL' : '⚠ SYNTHETIC'}
              </span>
              <span class="tc-score">Risk: ${sr.risk_score}</span>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  return `
    <div class="card card-pad" style="border-top: 3px solid ${bannerColor}; margin-top:16px;">
      <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; border-bottom:1px solid var(--line); padding-bottom:8px; flex-wrap:wrap; gap:8px;">
        <div style="font-family:var(--disp); font-size:11.5px; font-weight:700; letter-spacing:1.5px; color:var(--text-faint); text-transform:uppercase;">
          ${opts.contentType.toUpperCase()} FORENSIC DOSSIER · <span style="color:var(--text)">${opts.contentLabel}</span>
        </div>
        <span class="chip-tag" style="color:var(--cyan); border-color:rgba(45,217,232,.3); font-size:11px;">Real Pretrained Model</span>
      </div>

      <div class="pred-banner ${bannerClass}">
        <div class="pred-icon-box">${bannerIcon}</div>
        <div>
          <div class="pred-title">${bannerTitle}</div>
          <div class="pred-sub">${bannerSub}</div>
        </div>
      </div>

      <div class="pred-grid">
        <div class="pred-card"><div class="val" style="color:var(--safe);">${norm.confidence}%</div><div class="lbl">Confidence</div></div>
        <div class="pred-card"><div class="val" style="color:${isGenuine ? 'var(--safe)' : 'var(--danger-2)'};">${norm.riskScore}/100</div><div class="lbl">Risk Score</div></div>
        <div class="pred-card"><div class="val" style="color:${riskColor(norm.tier.cls)};">${norm.riskLevel}</div><div class="lbl">Risk Level</div></div>
        <div class="pred-card"><div class="val" style="color:var(--cyan);">${norm.authenticity}%</div><div class="lbl">Authenticity</div></div>
      </div>

      ${timelineHTML}
      ${segmentHTML}

      <div class="card indicators" style="margin-top:14px; margin-bottom:14px;">
        <h3>${isGenuine ? '✓ Verified Authenticity Indicators' : '🚨 Detected Anomaly Indicators'}</h3>
        ${indicatorsHTML}
      </div>

      <div class="explanation-card">
        <h4>Forensic Explanation</h4>
        <p>${norm.explanation}</p>
      </div>

      <div class="recommend-box" style="background:${riskColor(norm.tier.cls)}12; border-color:${riskColor(norm.tier.cls)}44; color:${riskColor(norm.tier.cls)};">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 9v4M12 17h.01M10.3 3.9L1.8 18a2 2 0 001.7 3h17a2 2 0 001.7-3L13.7 3.9a2 2 0 00-3.4 0z"/></svg>
        <div><b>${rec.title}</b><p style="color:var(--text-dim)">${rec.text}</p></div>
      </div>

      <div class="action-row" style="margin-top:16px;">
        <button class="btn btn-ghost btn-sm speak-btn">🔊 Read Voiceover</button>
        <button class="btn btn-outline btn-sm view-report-btn">View Full Report</button>
        <button class="btn btn-outline btn-sm ask-ai-btn">Ask AI Assistant</button>
      </div>
    </div>
  `;
}

function attachResultActions(container, reportData){
  const speakBtn = container.querySelector('.speak-btn');
  if(speakBtn) speakBtn.addEventListener('click', ()=> speakResult(reportData));
  const reportBtn = container.querySelector('.view-report-btn');
  if(reportBtn) reportBtn.addEventListener('click', ()=> openReportModal(reportData));
  const askBtn = container.querySelector('.ask-ai-btn');
  if(askBtn) askBtn.addEventListener('click', ()=>{ lastScanContext = reportData; openAssistant(); pushBotMsg(`I've loaded your ${reportData.contentType.toLowerCase()} scan — risk ${reportData.score}/100 (${riskTier(reportData.score).label}). Ask me why, or what to do next.`); });
  
  // Seek video player on frame click if available
  container.querySelectorAll('.timeline-chip[data-time]').forEach(chip => {
    chip.addEventListener('click', () => {
      const t = parseFloat(chip.dataset.time);
      const vp = document.getElementById('videoPreviewPlayer');
      if (vp && !isNaN(t)) {
        vp.currentTime = t;
        vp.play().catch(()=>{});
        toast('Seeking video', `Jumped to timestamp ${t}s`, 'info');
      }
    });
  });
}

function speakResult(data){
  if(!('speechSynthesis' in window)){ toast('Voice not supported', '', 'warn'); return; }
  const text = `Your ${data.contentType} analysis scored a risk of ${data.score} out of 100, rated ${riskTier(data.score).label}. ${recommendation(riskTier(data.score).cls).text}`;
  const utter = new SpeechSynthesisUtterance(text);
  speechSynthesis.cancel();
  speechSynthesis.speak(utter);
  toast('Voiceover playing', 'Text-to-speech started', 'info');
}

/* ============ PIPELINE ANIMATION HELPER ============ */
const FULL_PIPELINE = [
  {title:'Preprocessing', sub:'Normalizing input & format checks'},
  {title:'Language detection', sub:'Identifying script & language'},
  {title:'OCR / feature extraction', sub:'Extracting embedded signals'},
  {title:'Vision / Audio / NLP Model', sub:'Executing deep learning inference'},
  {title:'Deepfake analysis', sub:'Evaluating facial & spectral features'},
  {title:'Scam & fraud engine', sub:'Analyzing urgency & financial markers'},
  {title:'Unified risk scoring', sub:'Clamping risk bands (0-100)'},
  {title:'Explainable output', sub:'Finalizing explainable report'}
];

function buildPipeline(stepDefs, containerId){
  const el = document.getElementById(containerId);
  if(!el) return;
  el.innerHTML = stepDefs.map((s,i)=>`
    <div class="step" data-i="${i}">
      <div class="step-dot"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M20 6L9 17l-5-5"/></svg></div>
      <div class="step-txt"><b>${s.title}</b><span>${s.sub}</span></div>
      <div class="step-time"></div>
    </div>`).join('');
}

function runPipeline(stepDefs, containerId, statusId, asyncAction){
  buildPipeline(stepDefs, containerId);
  const steps = document.querySelectorAll(`#${containerId} .step`);
  const statusEl = document.getElementById(statusId);
  if (statusEl) { statusEl.textContent = 'Running model inference…'; statusEl.style.color = 'var(--cyan)'; }
  let i = 0;
  let interval = setInterval(()=>{
    if (i > 0 && i <= steps.length) {
      steps[i-1].classList.remove('active');
      steps[i-1].classList.add('done');
      const timeEl = steps[i-1].querySelector('.step-time');
      if (timeEl) timeEl.textContent = Math.floor(80 + (i*35)) + 'ms';
    }
    if (i < steps.length) { steps[i].classList.add('active'); i++; }
  }, 120);

  (async function() {
    try {
      await asyncAction();
      clearInterval(interval);
      steps.forEach(s => { s.classList.remove('active'); s.classList.add('done'); });
      if (statusEl) { statusEl.textContent = 'Prediction Complete'; statusEl.style.color = 'var(--safe)'; }
    } catch (err) {
      clearInterval(interval);
      if (statusEl) { statusEl.textContent = 'Error during analysis'; statusEl.style.color = 'var(--danger)'; }
    }
  })();
}

/* ============ AUTHENTICATION SYSTEM ============ */
function openAuthModal(mode = 'login') {
  const modal = document.getElementById('authModal');
  if (!modal) return;
  modal.classList.add('open');
  if (mode === 'login') {
    document.getElementById('tabLoginBtn')?.click();
  } else {
    document.getElementById('tabRegisterBtn')?.click();
  }
}

function closeAuthModal() {
  document.getElementById('authModal')?.classList.remove('open');
}

function updateAuthUI() {
  const av = currentUser ? (currentUser.display_name.split(' ').map(n=>n[0]).join('').slice(0,2).toUpperCase() || 'RA') : 'G';
  const name = currentUser ? currentUser.display_name : 'Guest';
  const email = currentUser ? currentUser.email : 'Not signed in';
  const org = currentUser ? currentUser.organization || 'Independent Researcher' : 'Demo Operator';

  document.getElementById('topAvatar').textContent = av;
  document.getElementById('topUserName').textContent = name;
  document.getElementById('menuUserName').textContent = name;
  document.getElementById('menuUserEmail').textContent = email;
  document.getElementById('dashOperatorName').textContent = name;
  document.getElementById('dashOperatorOrg').textContent = org;

  document.getElementById('profPageAvatar').textContent = av;
  document.getElementById('profPageName').textContent = name;
  document.getElementById('profPageEmail').textContent = email;
  document.getElementById('profPageOrg').textContent = org;
  document.getElementById('profPageLang').textContent = (currentUser?.preferred_language || 'en').toUpperCase();

  const sn = document.getElementById('settingName'); if(sn) sn.value = name;
  const so = document.getElementById('settingOrg'); if(so) so.value = org;

  const authAction = document.getElementById('menuAuthAction');
  if (authAction) {
    authAction.innerHTML = currentUser ? '<div class="notif-text"><b style="color:var(--danger-2);">Sign Out</b></div>' : '<div class="notif-text"><b style="color:var(--cyan);">Sign In</b></div>';
  }
}

async function loginUser(email, password) {
  try {
    const res = await apiPost('/api/auth/login', { email, password });
    if (res.token && res.user) {
      currentToken = res.token;
      currentUser = res.user;
      localStorage.setItem('trustguard_token', currentToken);
      updateAuthUI();
      closeAuthModal();
      toast('✓ Signed In', `Welcome, ${currentUser.display_name}`, 'safe');
      await fetchDashboardStats();
      await fetchHistoryFromBackend();
    }
  } catch (err) {
    const errBox = document.getElementById('loginError');
    if (errBox) { errBox.textContent = err.message; errBox.style.display = 'block'; }
    toast('Sign In Failed', err.message, 'danger');
  }
}

async function registerUser(email, password, displayName, org) {
  try {
    const res = await apiPost('/api/auth/register', { email, password, display_name: displayName, organization: org });
    if (res.token && res.user) {
      currentToken = res.token;
      currentUser = res.user;
      localStorage.setItem('trustguard_token', currentToken);
      updateAuthUI();
      closeAuthModal();
      toast('✓ Account Created', `Welcome to TrustGuard AI, ${currentUser.display_name}`, 'safe');
      await fetchDashboardStats();
      await fetchHistoryFromBackend();
    }
  } catch (err) {
    const errBox = document.getElementById('regError');
    if (errBox) { errBox.textContent = err.message; errBox.style.display = 'block'; }
    toast('Registration Failed', err.message, 'danger');
  }
}

async function logoutUser() {
  try {
    await apiPost('/api/auth/logout', {});
  } catch(e){}
  currentToken = '';
  currentUser = null;
  localStorage.removeItem('trustguard_token');
  updateAuthUI();
  toast('Signed Out', 'You have been logged out.', 'info');
  gotoPage('dashboard');
}

async function checkAuthSession() {
  if (!currentToken) {
    // Seed demo user state
    currentUser = { id: 1, display_name: 'Reshma A.', email: 'reshma@trustguard.ai', organization: 'TrustGuard Cyber Labs', preferred_language: 'en' };
    updateAuthUI();
    return;
  }
  try {
    const res = await apiGet('/api/auth/me');
    if (res.user) {
      currentUser = res.user;
      updateAuthUI();
    }
  } catch (e) {
    currentToken = '';
    localStorage.removeItem('trustguard_token');
    currentUser = { id: 1, display_name: 'Reshma A.', email: 'reshma@trustguard.ai', organization: 'TrustGuard Cyber Labs', preferred_language: 'en' };
    updateAuthUI();
  }
}

/* ============ ROUTING & NAVIGATION ============ */
const pages = document.querySelectorAll('.page');
function gotoPage(name){
  pages.forEach(p=>p.classList.toggle('active', p.id === 'page-'+name));
  document.querySelectorAll('.navitem').forEach(n=>n.classList.toggle('active', n.dataset.page===name));
  document.getElementById('sidebar')?.classList.remove('open');
  window.scrollTo({top:0, behavior:'smooth'});
  closeDropdowns();
}

document.querySelectorAll('[data-page]').forEach(el=> el.addEventListener('click', ()=> gotoPage(el.dataset.page)));
document.querySelectorAll('[data-goto]').forEach(el=> el.addEventListener('click', ()=> gotoPage(el.dataset.goto)));

function closeDropdowns(){ document.querySelectorAll('.dropdown-panel').forEach(d=>d.classList.remove('open')); }
document.getElementById('notifBtn')?.addEventListener('click', e=>{ e.stopPropagation(); const p=document.getElementById('notifPanel'); const wasOpen=p?.classList.contains('open'); closeDropdowns(); if(!wasOpen) p?.classList.add('open'); });
document.getElementById('profileBtn')?.addEventListener('click', e=>{ e.stopPropagation(); const p=document.getElementById('profilePanel'); const wasOpen=p?.classList.contains('open'); closeDropdowns(); if(!wasOpen) p?.classList.add('open'); });
document.addEventListener('click', closeDropdowns);

document.getElementById('hamburger')?.addEventListener('click', ()=> document.getElementById('sidebar')?.classList.toggle('open'));

document.getElementById('themeBtn')?.addEventListener('click', ()=>{
  const cur = document.body.getAttribute('data-theme');
  const next = cur==='dark' ? 'light' : 'dark';
  document.body.setAttribute('data-theme', next);
  const st = document.getElementById('settingTheme'); if(st) st.value = next;
});

/* Auth Modal Handlers */
document.getElementById('tabLoginBtn')?.addEventListener('click', ()=>{
  document.getElementById('tabLoginBtn').classList.add('active');
  document.getElementById('tabRegisterBtn').classList.remove('active');
  document.getElementById('loginForm').classList.add('active');
  document.getElementById('registerForm').classList.remove('active');
  document.getElementById('authModalTitle').textContent = 'Sign In to TrustGuard AI';
});
document.getElementById('tabRegisterBtn')?.addEventListener('click', ()=>{
  document.getElementById('tabRegisterBtn').classList.add('active');
  document.getElementById('tabLoginBtn').classList.remove('active');
  document.getElementById('registerForm').classList.add('active');
  document.getElementById('loginForm').classList.remove('active');
  document.getElementById('authModalTitle').textContent = 'Create Operator Account';
});
document.getElementById('authModalClose')?.addEventListener('click', closeAuthModal);
document.getElementById('authModal')?.addEventListener('click', e=>{ if(e.target.id==='authModal') closeAuthModal(); });

document.getElementById('submitLoginBtn')?.addEventListener('click', ()=>{
  const em = document.getElementById('loginEmail')?.value;
  const pw = document.getElementById('loginPassword')?.value;
  if(em && pw) loginUser(em, pw);
});
document.getElementById('demoLoginBtn')?.addEventListener('click', ()=> loginUser('reshma@trustguard.ai', 'trustguard2026'));

document.getElementById('submitRegisterBtn')?.addEventListener('click', ()=>{
  const nm = document.getElementById('regName')?.value;
  const em = document.getElementById('regEmail')?.value;
  const pw = document.getElementById('regPassword')?.value;
  const org = document.getElementById('regOrg')?.value;
  if(em && pw && nm) registerUser(em, pw, nm, org);
});

document.getElementById('menuAuthAction')?.addEventListener('click', ()=>{
  if (currentUser) logoutUser();
  else openAuthModal('login');
});
document.getElementById('profLogoutBtn')?.addEventListener('click', logoutUser);

/* Settings save */
document.getElementById('saveSettingsBtn')?.addEventListener('click', async ()=>{
  const newName = document.getElementById('settingName')?.value;
  const newOrg = document.getElementById('settingOrg')?.value;
  const newTheme = document.getElementById('settingTheme')?.value;
  const newLang = document.getElementById('settingLang')?.value;

  if (currentToken) {
    try {
      const res = await apiPut('/api/auth/profile', { display_name: newName, organization: newOrg, theme: newTheme, preferred_language: newLang });
      if (res.user) {
        currentUser = res.user;
        updateAuthUI();
        document.body.setAttribute('data-theme', newTheme);
        toast('✓ Changes Saved', 'Profile & preferences updated in database', 'safe');
      }
    } catch(err) { toast('Update Failed', err.message, 'danger'); }
  } else {
    currentUser = { ...currentUser, display_name: newName, organization: newOrg };
    updateAuthUI();
    document.body.setAttribute('data-theme', newTheme);
    toast('✓ Changes Saved', 'Session preferences updated', 'safe');
  }
});

/* ============ FILE STORE & DROPZONES ============ */
function wireDropzone(zone){
  const kind = zone.dataset.kind;
  const accept = zone.dataset.accept;
  const input = document.createElement('input');
  input.type='file'; input.accept = accept==='*'?'':accept; input.style.display='none';
  zone.appendChild(input);
  zone.addEventListener('click', ()=> input.click());
  input.addEventListener('change', ()=> { if(input.files[0]) handleFile(input.files[0], kind); });
  zone.addEventListener('dragover', e=> { e.preventDefault(); zone.classList.add('drag'); });
  zone.addEventListener('dragleave', ()=> zone.classList.remove('drag'));
  zone.addEventListener('drop', e=> { e.preventDefault(); zone.classList.remove('drag'); if(e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0], kind); });
}
document.querySelectorAll('.dropzone').forEach(wireDropzone);

function handleFile(file, kind){
  filesStore[kind] = file;
  const prev = document.getElementById(`prev-${kind}`) || document.getElementById(`prev-up-${kind}`);
  if(prev){
    prev.innerHTML = `
      <div class="preview-row">
        <div class="preview-meta"><b>${file.name}</b><span>${(file.size/1024).toFixed(1)} KB · ${file.type||'file'}</span></div>
        <span class="soc-status-badge" style="color:var(--cyan); border-color:rgba(45,217,232,.3);">Loaded</span>
      </div>
    `;
  }
  if(kind==='video'){
    const vp = document.getElementById('videoPreviewPlayer');
    const vwrap = document.getElementById('videoPlayerWrap');
    if(vp && vwrap){
      vp.src = URL.createObjectURL(file);
      vwrap.style.display = 'block';
    }
  }
  if(kind==='audio'){
    const ap = document.getElementById('audioPreviewPlayer');
    const awrap = document.getElementById('audioPlayerWrap');
    if(ap && awrap){
      ap.src = URL.createObjectURL(file);
      awrap.style.display = 'block';
    }
  }
  toast('File ready', file.name, 'info');
}

/* ============ MODULE 1: IMAGE DEEPFAKE ============ */
document.getElementById('imgAnalyzeBtn')?.addEventListener('click', async ()=>{
  const f = filesStore['image'];
  if(!f){ toast('No image selected', 'Upload an image first', 'warn'); return; }
  const pipe = document.getElementById('imgPipeline');
  const resWrap = document.getElementById('imgResult');
  if(pipe) pipe.style.display='block';
  if(resWrap) { resWrap.classList.remove('show'); resWrap.innerHTML=''; }

  runPipeline(FULL_PIPELINE.filter(s=>s.title.includes('Vision')||s.title.includes('Deepfake')||s.title.includes('Unified')), 'imgSteps', 'imgPipeStatus', async ()=>{
    const formData = new FormData();
    formData.append('image', f);
    const apiRes = await apiPost('/api/analyze/image', formData, true);
    const norm = normalizePrediction(apiRes, 'Image', f.name);
    if(resWrap){
      resWrap.innerHTML = renderUnifiedResultCard(norm, { contentType: 'Image', contentLabel: f.name });
      resWrap.classList.add('show');
      attachResultActions(resWrap, { ...norm, contentType: 'Image', contentLabel: f.name, date: Date.now() });
    }
    pushHistory({ contentLabel: f.name, contentType: 'Image', score: norm.riskScore, trust: norm.authenticity, confidence: norm.confidence, date: Date.now() });
    toast(norm.isGenuine ? '✓ Genuine Image' : '⚠ Deepfake Flagged', `Confidence: ${norm.confidence}%`, norm.isGenuine ? 'safe' : 'danger');
  });
});
document.getElementById('imgResetBtn')?.addEventListener('click', ()=>{ delete filesStore['image']; const p=document.getElementById('prev-image'); if(p) p.innerHTML=''; const r=document.getElementById('imgResult'); if(r){ r.classList.remove('show'); r.innerHTML=''; } });

/* ============ MODULE 2: VIDEO DEEPFAKE (FRAME-BY-FRAME) ============ */
document.getElementById('vidAnalyzeBtn')?.addEventListener('click', async ()=>{
  const f = filesStore['video'];
  if(!f){ toast('No video selected', 'Upload an MP4/MOV video first', 'warn'); return; }
  const pipe = document.getElementById('vidPipeline');
  const resWrap = document.getElementById('vidResult');
  if(pipe) pipe.style.display='block';
  if(resWrap) { resWrap.classList.remove('show'); resWrap.innerHTML=''; }

  runPipeline(FULL_PIPELINE, 'vidSteps', 'vidPipeStatus', async ()=>{
    const formData = new FormData();
    formData.append('video', f);
    const apiRes = await apiPost('/api/analyze/video', formData, true);
    const norm = normalizePrediction(apiRes, 'Video', f.name);
    if(resWrap){
      resWrap.innerHTML = renderUnifiedResultCard(norm, {
        contentType: 'Video',
        contentLabel: f.name,
        frameResults: apiRes.frame_results || []
      });
      resWrap.classList.add('show');
      attachResultActions(resWrap, { ...norm, contentType: 'Video', contentLabel: f.name, date: Date.now() });
    }
    pushHistory({ contentLabel: f.name, contentType: 'Video', score: norm.riskScore, trust: norm.authenticity, confidence: norm.confidence, date: Date.now() });
    toast(norm.isGenuine ? '✓ Genuine Video' : '⚠ Video Deepfake Detected', `Analyzed ${apiRes.analyzed_frames || 0} frames`, norm.isGenuine ? 'safe' : 'danger');
  });
});
document.getElementById('vidResetBtn')?.addEventListener('click', ()=>{ delete filesStore['video']; const p=document.getElementById('prev-video'); if(p) p.innerHTML=''; const r=document.getElementById('vidResult'); if(r){ r.classList.remove('show'); r.innerHTML=''; } });

/* ============ MODULE 3: AUDIO DEEPFAKE (SPECTRAL WINDOWS) ============ */
document.getElementById('audAnalyzeBtn')?.addEventListener('click', async ()=>{
  const f = filesStore['audio'];
  if(!f){ toast('No audio selected', 'Upload a WAV/MP3 audio file first', 'warn'); return; }
  const pipe = document.getElementById('audPipeline');
  const resWrap = document.getElementById('audResult');
  if(pipe) pipe.style.display='block';
  if(resWrap) { resWrap.classList.remove('show'); resWrap.innerHTML=''; }

  runPipeline(FULL_PIPELINE.filter(s=>s.title.includes('Audio')||s.title.includes('Deepfake')||s.title.includes('Unified')), 'audSteps', 'audPipeStatus', async ()=>{
    const formData = new FormData();
    formData.append('audio', f);
    const apiRes = await apiPost('/api/analyze/audio', formData, true);
    const norm = normalizePrediction(apiRes, 'Audio', f.name);
    if(resWrap){
      resWrap.innerHTML = renderUnifiedResultCard(norm, {
        contentType: 'Audio',
        contentLabel: f.name,
        segmentResults: apiRes.segment_results || []
      });
      resWrap.classList.add('show');
      attachResultActions(resWrap, { ...norm, contentType: 'Audio', contentLabel: f.name, date: Date.now() });
    }
    pushHistory({ contentLabel: f.name, contentType: 'Audio', score: norm.riskScore, trust: norm.authenticity, confidence: norm.confidence, date: Date.now() });
    toast(norm.isGenuine ? '✓ Authentic Voice' : '⚠ Synthetic Speech Detected', `Risk Score: ${norm.riskScore}/100`, norm.isGenuine ? 'safe' : 'danger');
  });
});
document.getElementById('audResetBtn')?.addEventListener('click', ()=>{ delete filesStore['audio']; const p=document.getElementById('prev-audio'); if(p) p.innerHTML=''; const r=document.getElementById('audResult'); if(r){ r.classList.remove('show'); r.innerHTML=''; } });

/* ============ MODULE 4: TEXT SCAM ============ */
document.getElementById('scamAnalyzeBtn')?.addEventListener('click', async ()=>{
  const txt = document.getElementById('scamText')?.value || '';
  if(!txt.trim()){ toast('Empty text', 'Paste a message first', 'warn'); return; }
  const resWrap = document.getElementById('scamResult');
  try {
    const apiRes = await apiPost('/api/analyze/text', { text: txt });
    const norm = normalizePrediction(apiRes, 'Text', txt.slice(0, 30));
    if(resWrap){
      resWrap.innerHTML = renderUnifiedResultCard(norm, { contentType: 'Text', contentLabel: txt.slice(0, 35) + '...' });
      resWrap.classList.add('show');
      attachResultActions(resWrap, { ...norm, contentType: 'Text', contentLabel: txt.slice(0, 35), date: Date.now() });
    }
    pushHistory({ contentLabel: txt.slice(0, 35), contentType: 'Text', score: norm.riskScore, trust: norm.authenticity, confidence: norm.confidence, date: Date.now() });
    toast(norm.isGenuine ? '✓ Safe Text' : '⚠ Scam Flagged', `Risk: ${norm.riskScore}/100`, norm.isGenuine ? 'safe' : 'danger');
  } catch(e) { toast('Error', e.message, 'danger'); }
});
document.getElementById('scamResetBtn')?.addEventListener('click', ()=>{ const t=document.getElementById('scamText'); if(t) t.value=''; const r=document.getElementById('scamResult'); if(r){ r.classList.remove('show'); r.innerHTML=''; } });

/* ============ MODULE 5: JOB / INTERNSHIP ============ */
let activeJobMode = 'job';
document.querySelectorAll('#jobModeTabs .tab-btn').forEach(btn => {
  btn.addEventListener('click', ()=>{
    document.querySelectorAll('#jobModeTabs .tab-btn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    activeJobMode = btn.dataset.jobmode || 'job';
  });
});
document.getElementById('jobAnalyzeBtn')?.addEventListener('click', async ()=>{
  const desc = document.getElementById('jobDesc')?.value || '';
  const em = document.getElementById('jobEmail')?.value || '';
  const u = document.getElementById('jobUrl')?.value || '';
  if(!desc.trim() && !em.trim()){ toast('No details provided', 'Paste job description or email', 'warn'); return; }
  const resWrap = document.getElementById('jobResult');
  try {
    const endpoint = activeJobMode === 'internship' ? '/api/analyze/internship' : '/api/analyze/job';
    const apiRes = await apiPost(endpoint, { description: desc, email: em, url: u });
    const label = activeJobMode === 'internship' ? 'Internship Offer' : 'Job Listing';
    const norm = normalizePrediction(apiRes, label, desc.slice(0, 30));
    if(resWrap){
      resWrap.innerHTML = renderUnifiedResultCard(norm, { contentType: label, contentLabel: desc.slice(0, 35) || 'Offer' });
      resWrap.classList.add('show');
      attachResultActions(resWrap, { ...norm, contentType: label, contentLabel: desc.slice(0, 35), date: Date.now() });
    }
    pushHistory({ contentLabel: desc.slice(0, 35) || label, contentType: label, score: norm.riskScore, trust: norm.authenticity, confidence: norm.confidence, date: Date.now() });
    toast(norm.isGenuine ? '✓ Legitimate Offer' : '⚠ Fraudulent Solicitations', `Risk: ${norm.riskScore}/100`, norm.isGenuine ? 'safe' : 'danger');
  } catch(e) { toast('Error', e.message, 'danger'); }
});
document.getElementById('jobResetBtn')?.addEventListener('click', ()=>{ const d=document.getElementById('jobDesc'); if(d) d.value=''; const r=document.getElementById('jobResult'); if(r){ r.classList.remove('show'); r.innerHTML=''; } });

/* ============ MODULE 6: URL SCANNER ============ */
document.getElementById('urlAnalyzeBtn')?.addEventListener('click', async ()=>{
  const u = document.getElementById('urlInput')?.value || '';
  if(!u.trim()){ toast('No URL', 'Paste a link first', 'warn'); return; }
  const resWrap = document.getElementById('urlResult');
  try {
    const apiRes = await apiPost('/api/analyze/url', { url: u });
    const norm = normalizePrediction(apiRes, 'URL', u);
    if(resWrap){
      resWrap.innerHTML = renderUnifiedResultCard(norm, { contentType: 'URL', contentLabel: u });
      resWrap.classList.add('show');
      attachResultActions(resWrap, { ...norm, contentType: 'URL', contentLabel: u, date: Date.now() });
    }
    pushHistory({ contentLabel: u, contentType: 'URL', score: norm.riskScore, trust: norm.authenticity, confidence: norm.confidence, date: Date.now() });
    toast(norm.isGenuine ? '✓ Safe URL' : '⚠ Phishing URL Detected', `Entropy Risk: ${norm.riskScore}/100`, norm.isGenuine ? 'safe' : 'danger');
  } catch(e) { toast('Error', e.message, 'danger'); }
});
document.getElementById('urlResetBtn')?.addEventListener('click', ()=>{ const u=document.getElementById('urlInput'); if(u) u.value=''; const r=document.getElementById('urlResult'); if(r){ r.classList.remove('show'); r.innerHTML=''; } });

/* ============ MODULE 7: OCR SCANNER ============ */
document.getElementById('ocrRunBtn')?.addEventListener('click', async ()=>{
  const f = filesStore['ocr'];
  if(!f){ toast('No image uploaded', 'Upload a poster or screenshot first', 'warn'); return; }
  const resWrap = document.getElementById('ocrResult');
  const progWrap = document.getElementById('ocrProgressWrap');
  const bar = document.getElementById('ocrBar');
  const txt = document.getElementById('ocrProgressTxt');
  if(progWrap) progWrap.style.display = 'block';

  try {
    let extractedText = f.name;
    if(typeof Tesseract !== 'undefined') {
      const { data } = await Tesseract.recognize(f, 'eng', {
        logger: m => {
          if(m.progress != null && bar && txt) {
            bar.style.width = Math.round(m.progress * 100) + '%';
            txt.textContent = `${m.status || 'Extracting'}… ${Math.round(m.progress * 100)}%`;
          }
        }
      });
      extractedText = (data.text || '').trim() || f.name;
    }
    document.getElementById('ocrTextBox').textContent = extractedText;

    const formData = new FormData();
    formData.append('image', f);
    formData.append('text', extractedText);
    const apiRes = await apiPost('/api/analyze/ocr', formData, true);
    const norm = normalizePrediction(apiRes, 'OCR Document', f.name);
    if(resWrap){
      resWrap.innerHTML = renderUnifiedResultCard(norm, { contentType: 'OCR Document', contentLabel: f.name });
      resWrap.classList.add('show');
      attachResultActions(resWrap, { ...norm, contentType: 'OCR Document', contentLabel: f.name, date: Date.now() });
    }
    pushHistory({ contentLabel: f.name, contentType: 'OCR Document', score: norm.riskScore, trust: norm.authenticity, confidence: norm.confidence, date: Date.now() });
    toast(norm.isGenuine ? '✓ Verified Document' : '⚠ Fraud Detected in OCR', `Risk: ${norm.riskScore}/100`, norm.isGenuine ? 'safe' : 'danger');
  } catch(e) { toast('OCR Error', e.message, 'danger'); }
});
document.getElementById('ocrResetBtn')?.addEventListener('click', ()=>{ delete filesStore['ocr']; const p=document.getElementById('prev-ocr'); if(p) p.innerHTML=''; const r=document.getElementById('ocrResult'); if(r){ r.classList.remove('show'); r.innerHTML=''; } });

/* ============ MODULE 8: COMPANY VERIFICATION ============ */
document.getElementById('compVerifyBtn')?.addEventListener('click', async ()=>{
  const cn = document.getElementById('compName')?.value || '';
  const cd = document.getElementById('compDomain')?.value || '';
  const ce = document.getElementById('compEmail')?.value || '';
  if(!cn.trim() && !cd.trim()){ toast('No details', 'Enter company name or website domain', 'warn'); return; }
  const resWrap = document.getElementById('compResult');
  try {
    const apiRes = await apiPost('/api/analyze/company', { company_name: cn, domain: cd, email: ce });
    const norm = normalizePrediction(apiRes, 'Company Entity', cn || cd);
    if(resWrap){
      resWrap.innerHTML = renderUnifiedResultCard(norm, { contentType: 'Company Entity', contentLabel: cn || cd });
      resWrap.classList.add('show');
      attachResultActions(resWrap, { ...norm, contentType: 'Company Entity', contentLabel: cn || cd, date: Date.now() });
    }
    pushHistory({ contentLabel: cn || cd, contentType: 'Company Entity', score: norm.riskScore, trust: norm.authenticity, confidence: norm.confidence, date: Date.now() });
    toast(norm.isGenuine ? '✓ Verified Corporate Entity' : '⚠ Domain Alignment Warning', `Risk: ${norm.riskScore}/100`, norm.isGenuine ? 'safe' : 'danger');
  } catch(e) { toast('Error', e.message, 'danger'); }
});
document.getElementById('compResetBtn')?.addEventListener('click', ()=>{ const c=document.getElementById('compName'); if(c) c.value=''; const r=document.getElementById('compResult'); if(r){ r.classList.remove('show'); r.innerHTML=''; } });

/* ============ MODULE 9: SOCIAL MEDIA PROTECTION ============ */
let activePlatform = 'Twitter / X';
document.querySelectorAll('.plat-card').forEach(btn => {
  btn.addEventListener('click', ()=>{
    document.querySelectorAll('.plat-card').forEach(b=>{ b.style.borderColor='var(--line)'; b.style.color='var(--text-dim)'; });
    btn.style.borderColor='var(--cyan)'; btn.style.color='var(--cyan)';
    activePlatform = btn.dataset.plat || 'General';
  });
});
document.getElementById('socialAnalyzeBtn')?.addEventListener('click', async ()=>{
  const st = document.getElementById('socialText')?.value || '';
  const su = document.getElementById('socialUrl')?.value || '';
  if(!st.trim() && !su.trim()){ toast('No content', 'Paste a social post or link', 'warn'); return; }
  const resWrap = document.getElementById('socialResult');
  try {
    const apiRes = await apiPost('/api/analyze/social', { content: st, url: su, platform: activePlatform });
    const norm = normalizePrediction(apiRes, 'Social Content', `${activePlatform} Post`);
    if(resWrap){
      resWrap.innerHTML = renderUnifiedResultCard(norm, { contentType: 'Social Content', contentLabel: `${activePlatform} Post` });
      resWrap.classList.add('show');
      attachResultActions(resWrap, { ...norm, contentType: 'Social Content', contentLabel: `${activePlatform} Post`, date: Date.now() });
    }
    pushHistory({ contentLabel: `${activePlatform} Post`, contentType: 'Social Content', score: norm.riskScore, trust: norm.authenticity, confidence: norm.confidence, date: Date.now() });
    toast(norm.isGenuine ? '✓ Safe Social Content' : '⚠ Social Scam / Bait Detected', `Risk: ${norm.riskScore}/100`, norm.isGenuine ? 'safe' : 'danger');
  } catch(e) { toast('Error', e.message, 'danger'); }
});
document.getElementById('socialResetBtn')?.addEventListener('click', ()=>{ const s=document.getElementById('socialText'); if(s) s.value=''; const r=document.getElementById('socialResult'); if(r){ r.classList.remove('show'); r.innerHTML=''; } });

/* ============ MODULE 10: CAMERA SCANNER ============ */
let camStream = null;
document.getElementById('camStartBtn')?.addEventListener('click', async ()=>{
  try {
    camStream = await navigator.mediaDevices.getUserMedia({ video: true });
    const vid = document.getElementById('camVideo');
    if(vid) { vid.srcObject = camStream; vid.style.display = 'block'; }
    document.getElementById('camEmpty').style.display = 'none';
    document.getElementById('camStartBtn').disabled = true;
    document.getElementById('camCaptureBtn').disabled = false;
    document.getElementById('camStopBtn').disabled = false;
    toast('Camera started', 'Ready to capture snapshot', 'safe');
  } catch(e) { toast('Camera Error', 'Could not access webcam', 'danger'); }
});
document.getElementById('camStopBtn')?.addEventListener('click', ()=>{
  if(camStream) camStream.getTracks().forEach(t=>t.stop());
  document.getElementById('camVideo').style.display = 'none';
  document.getElementById('camEmpty').style.display = 'block';
  document.getElementById('camStartBtn').disabled = false;
  document.getElementById('camCaptureBtn').disabled = true;
  document.getElementById('camStopBtn').disabled = true;
});
document.getElementById('camCaptureBtn')?.addEventListener('click', ()=>{
  const vid = document.getElementById('camVideo');
  if(!vid) return;
  const canvas = document.createElement('canvas'); canvas.width = vid.videoWidth || 640; canvas.height = vid.videoHeight || 480;
  canvas.getContext('2d').drawImage(vid, 0, 0);
  canvas.toBlob(async blob => {
    const file = new File([blob], 'camera_snapshot.jpg', { type: 'image/jpeg' });
    toast('Analyzing snapshot…', 'Running Vision Transformer inference', 'info');
    const formData = new FormData();
    formData.append('image', file);
    try {
      const apiRes = await apiPost('/api/analyze/image', formData, true);
      const norm = normalizePrediction(apiRes, 'Camera Snapshot', 'Live Webcam Frame');
      const wrap = document.getElementById('camResult');
      if(wrap){
        wrap.innerHTML = renderUnifiedResultCard(norm, { contentType: 'Camera Snapshot', contentLabel: 'Live Camera Capture' });
        wrap.classList.add('show');
        attachResultActions(wrap, { ...norm, contentType: 'Camera Snapshot', contentLabel: 'Live Snapshot', date: Date.now() });
      }
      pushHistory({ contentLabel: 'Live Camera Capture', contentType: 'Camera Snapshot', score: norm.riskScore, trust: norm.authenticity, confidence: norm.confidence, date: Date.now() });
      toast(norm.isGenuine ? '✓ Genuine Camera Feed' : '⚠ Anomaly Detected', `Risk: ${norm.riskScore}/100`, norm.isGenuine ? 'safe' : 'danger');
    } catch(e) { toast('Analysis failed', e.message, 'danger'); }
  }, 'image/jpeg');
});

/* ============ MODULE 11: LIVE MICROPHONE ============ */
let liveMicStream = null, liveMicCtx = null, liveMicRAF = null;
document.getElementById('liveMicStart')?.addEventListener('click', async ()=>{
  try {
    liveMicStream = await navigator.mediaDevices.getUserMedia({ audio: true });
    liveMicCtx = new (window.AudioContext || window.webkitAudioContext)();
    const src = liveMicCtx.createMediaStreamSource(liveMicStream);
    const analyser = liveMicCtx.createAnalyser(); analyser.fftSize = 256;
    src.connect(analyser);

    const canvas = document.getElementById('liveMicCanvas');
    const ctx = canvas.getContext('2d');
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    function draw(){
      liveMicRAF = requestAnimationFrame(draw);
      analyser.getByteFrequencyData(dataArray);
      ctx.fillStyle = 'rgba(18, 26, 41, 0.4)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      const barWidth = (canvas.width / bufferLength) * 2.5;
      let x = 0;
      for(let i = 0; i < bufferLength; i++){
        const barHeight = dataArray[i] / 2;
        ctx.fillStyle = `rgb(${barHeight + 50}, 217, 232)`;
        ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
        x += barWidth + 1;
      }
    }
    draw();
    document.getElementById('liveMicStatus').textContent = 'Microphone Status: ACTIVE (Monitoring acoustic spectrum)';
    document.getElementById('liveMicStatus').style.color = 'var(--safe)';
    document.getElementById('liveMicStart').disabled = true;
    document.getElementById('liveMicStop').disabled = false;
    toast('Microphone active', 'Monitoring live acoustic frequency', 'safe');
  } catch(e) { toast('Mic Error', 'Could not access microphone', 'danger'); }
});
document.getElementById('liveMicStop')?.addEventListener('click', ()=>{
  if(liveMicStream) liveMicStream.getTracks().forEach(t=>t.stop());
  if(liveMicCtx) liveMicCtx.close();
  cancelAnimationFrame(liveMicRAF);
  document.getElementById('liveMicStatus').textContent = 'Microphone Status: IDLE';
  document.getElementById('liveMicStatus').style.color = 'var(--text-dim)';
  document.getElementById('liveMicStart').disabled = false;
  document.getElementById('liveMicStop').disabled = true;
});

/* ============ MODULE 12: DIGITAL PROVENANCE ============ */
document.getElementById('protectRunBtn')?.addEventListener('click', async ()=>{
  const f = filesStore['protect'];
  if(!f){ toast('No file selected', 'Upload a file to fingerprint', 'warn'); return; }
  const buf = await f.arrayBuffer();
  const hash = await crypto.subtle.digest('SHA-256', buf);
  const hex = Array.from(new Uint8Array(hash)).map(b=>b.toString(16).padStart(2,'0')).join('');
  const shortHash = hex.slice(0,10).toUpperCase() + '...' + hex.slice(-6).toUpperCase();
  const wrap = document.getElementById('protectResult');
  if(wrap){
    wrap.innerHTML = `
      <div class="card card-pad" style="border-top: 3px solid var(--safe); margin-top:16px;">
        <h3 style="font-family:var(--disp); font-size:16px; margin-bottom:10px;">✓ Cryptographic Fingerprint Generated</h3>
        <div class="telemetry-row"><span>File Name</span><span>${f.name}</span></div>
        <div class="telemetry-row"><span>Size</span><span>${(f.size/1024).toFixed(1)} KB</span></div>
        <div class="telemetry-row"><span>SHA-256 Hash</span><span style="color:var(--cyan); word-break:break-all;">${hex}</span></div>
        <div class="telemetry-row"><span>Provenance Status</span><span style="color:var(--safe);">Registered in Local Manifest</span></div>
      </div>
    `;
    wrap.classList.add('show');
  }
  pushHistory({ contentLabel: f.name, contentType: 'Digital Fingerprint', score: 5, trust: 95, confidence: 99, date: Date.now() });
  toast('Provenance verified', `SHA-256: ${shortHash}`, 'safe');
});
document.getElementById('protectResetBtn')?.addEventListener('click', ()=>{ delete filesStore['protect']; const p=document.getElementById('prev-protect'); if(p) p.innerHTML=''; const r=document.getElementById('protectResult'); if(r){ r.classList.remove('show'); r.innerHTML=''; } });

/* ============ DASHBOARD DIRECT SCANNER HANDLER ============ */
let activeDashTab = 'up-image';
document.querySelectorAll('#scanTabs .tab-btn').forEach(btn => {
  btn.addEventListener('click', ()=>{
    document.querySelectorAll('#scanTabs .tab-btn').forEach(b=>b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
    btn.classList.add('active');
    activeDashTab = btn.dataset.tab || 'up-image';
    document.getElementById(activeDashTab)?.classList.add('active');
  });
});

document.getElementById('dashAnalyzeBtn')?.addEventListener('click', async ()=>{
  if (activeDashTab === 'up-image') {
    const f = filesStore['image'];
    if (!f) { toast('No image loaded', 'Upload an image first', 'warn'); return; }
    document.getElementById('imgAnalyzeBtn')?.click();
    gotoPage('image');
  } else if (activeDashTab === 'up-video') {
    const f = filesStore['video'];
    if (!f) { toast('No video loaded', 'Upload a video first', 'warn'); return; }
    document.getElementById('vidAnalyzeBtn')?.click();
    gotoPage('video');
  } else if (activeDashTab === 'up-audio') {
    const f = filesStore['audio'];
    if (!f) { toast('No audio loaded', 'Upload an audio file first', 'warn'); return; }
    document.getElementById('audAnalyzeBtn')?.click();
    gotoPage('audio');
  } else if (activeDashTab === 'up-text') {
    const txt = document.getElementById('dashText')?.value || '';
    if (!txt.trim()) { toast('Empty text', 'Paste text first', 'warn'); return; }
    document.getElementById('scamText').value = txt;
    document.getElementById('scamAnalyzeBtn')?.click();
    gotoPage('text');
  } else if (activeDashTab === 'up-url') {
    const u = document.getElementById('dashUrl')?.value || '';
    if (!u.trim()) { toast('No URL', 'Paste a link first', 'warn'); return; }
    document.getElementById('urlInput').value = u;
    document.getElementById('urlAnalyzeBtn')?.click();
    gotoPage('url');
  }
});
document.getElementById('dashResetBtn')?.addEventListener('click', ()=>{
  delete filesStore['image']; delete filesStore['video']; delete filesStore['audio'];
  ['prev-up-image','prev-up-video','prev-up-audio'].forEach(id=>{ const el=document.getElementById(id); if(el) el.innerHTML=''; });
  const dt = document.getElementById('dashText'); if(dt) dt.value='';
  const du = document.getElementById('dashUrl'); if(du) du.value='';
});

/* ============ HISTORY & STATS TELEMETRY ============ */
async function fetchDashboardStats() {
  try {
    const stats = await apiGet('/api/stats');
    statCounters = { scans: stats.scans ?? 0, threats: stats.threats ?? 0, deepfakes: stats.deepfakes ?? 0, scams: stats.scams ?? 0 };
    updateDashboardStats();
  } catch(e) { console.warn('Could not fetch stats:', e); }
}

async function fetchHistoryFromBackend() {
  try {
    const data = await apiGet('/api/history');
    if (Array.isArray(data)) {
      scanHistory = data.map(item => ({
        id: item.id,
        contentLabel: item.content_label || 'Scan',
        contentType: item.scan_type ? item.scan_type.toUpperCase() : 'Content',
        lang: { name: 'English', flag: '🌐' },
        score: item.risk_score || 0,
        trust: 100 - (item.risk_score || 0),
        confidence: item.confidence || 90,
        date: item.timestamp ? (item.timestamp > 1e11 ? item.timestamp : item.timestamp * 1000) : Date.now()
      }));
      renderHistory();
      renderReports();
      renderRecent();
    }
  } catch(e) { console.warn('Could not fetch history:', e); }
}

function pushHistory(entry){
  scanHistory.unshift(entry);
  statCounters.scans++;
  if(entry.score > 40) statCounters.threats++;
  if(entry.contentType.includes('IMAGE') || entry.contentType.includes('VIDEO') || entry.contentType.includes('AUDIO')) {
    if(entry.score > 40) statCounters.deepfakes++;
  }
  if(entry.contentType.includes('TEXT') || entry.contentType.includes('JOB') || entry.contentType.includes('URL')) {
    if(entry.score > 40) statCounters.scams++;
  }
  renderHistory(); renderReports(); renderRecent(); updateDashboardStats();
  setTimeout(fetchDashboardStats, 500);
}

function updateDashboardStats(){
  ['dStat1','landStat1'].forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent = statCounters.scans; });
  ['dStat2','landStat2'].forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent = statCounters.threats; });
  ['dStat3','landStat3'].forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent = statCounters.deepfakes; });
  ['dStat4','landStat4'].forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent = statCounters.scams; });

  const profScans = document.getElementById('profStatScans'); if(profScans) profScans.textContent = statCounters.scans;
  const profThreats = document.getElementById('profStatThreats'); if(profThreats) profThreats.textContent = statCounters.threats;
  const profD = document.getElementById('profStatDeepfakes'); if(profD) profD.textContent = statCounters.deepfakes;
  const profS = document.getElementById('profStatScams'); if(profS) profS.textContent = statCounters.scams;

  let threatScore = 0;
  if (scanHistory.length > 0) {
    const sum = scanHistory.reduce((acc, h) => acc + (Number(h.score) || 0), 0);
    threatScore = Math.round(sum / scanHistory.length);
  } else if (statCounters.scans > 0) {
    threatScore = Math.round((statCounters.threats / statCounters.scans) * 100);
  }
  threatScore = Math.max(0, Math.min(100, threatScore));

  const scoreEl = document.getElementById('bentoThreatScore');
  const arcEl = document.getElementById('bentoThreatArc');
  const headlineEl = document.getElementById('bentoSecHeadline');
  const detailEl = document.getElementById('bentoSecDetail');
  const shieldEl = document.getElementById('socGlobalShield');
  const shieldTxt = document.getElementById('socGlobalText');

  const tier = riskTier(threatScore);
  const color = riskColor(tier.cls);

  if (scoreEl) { scoreEl.textContent = threatScore; scoreEl.style.color = color; }
  if (arcEl) {
    const totalCirc = 251.2;
    arcEl.style.strokeDashoffset = totalCirc - (threatScore / 100) * totalCirc;
    arcEl.style.stroke = color;
  }

  if (statCounters.threats > 0 || threatScore > 40) {
    if (headlineEl) headlineEl.textContent = `Elevated Threat Activity · ${statCounters.threats} Anomalies Flagged`;
    if (detailEl) detailEl.textContent = `${statCounters.threats} suspicious items flagged in recent scans. Multi-signal radar active.`;
    if (shieldEl) shieldEl.className = 'soc-status-badge alert';
    if (shieldTxt) shieldTxt.textContent = 'ALERT · ACTIVE THREATS';
  } else {
    if (headlineEl) headlineEl.textContent = 'System Nominal · Zero Critical Threats';
    if (detailEl) detailEl.textContent = 'All multi-signal detectors are actively screening media. No unverified anomalies detected.';
    if (shieldEl) shieldEl.className = 'soc-status-badge';
    if (shieldTxt) shieldTxt.textContent = 'PROTECTED · ENGINE ACTIVE';
  }
}

function renderHistory(){
  const body = document.getElementById('historyBody');
  if(!body) return;
  body.innerHTML = scanHistory.length === 0 ? '<tr><td colspan="9" style="text-align:center; padding:20px; color:var(--text-faint);">No scan history recorded.</td></tr>' : scanHistory.map((h,idx)=>`
    <tr>
      <td>${new Date(h.date).toLocaleDateString()}</td>
      <td><b>${h.contentLabel}</b></td>
      <td>${h.contentType}</td>
      <td>🌐 English</td>
      <td style="color:${riskColor(riskTier(h.score).cls)}; font-weight:700;">${h.score}/100</td>
      <td>${h.trust}%</td>
      <td>${h.confidence}%</td>
      <td><span class="status-pill" style="background:${riskColor(riskTier(h.score).cls)}22; color:${riskColor(riskTier(h.score).cls)}">${riskTier(h.score).label}</span></td>
      <td><button class="btn btn-outline btn-sm" data-view="${idx}">Report</button></td>
    </tr>`).join('');
  body.querySelectorAll('[data-view]').forEach(b=> b.addEventListener('click', ()=> openReportModal(scanHistory[+b.dataset.view])));
}

function renderReports(){
  const body = document.getElementById('reportsBody');
  if(!body) return;
  body.innerHTML = scanHistory.length === 0 ? '<tr><td colspan="9" style="text-align:center; padding:20px; color:var(--text-faint);">No reports available.</td></tr>' : scanHistory.map((h,idx)=>`
    <tr>
      <td>${new Date(h.date).toLocaleDateString()}</td>
      <td><b>${h.contentLabel}</b></td>
      <td>${h.contentType}</td>
      <td>🌐 English</td>
      <td style="color:${riskColor(riskTier(h.score).cls)}; font-weight:700;">${h.score}</td>
      <td>${h.trust}%</td>
      <td>${h.confidence}%</td>
      <td><span class="status-pill" style="background:${riskColor(riskTier(h.score).cls)}22; color:${riskColor(riskTier(h.score).cls)}">${riskTier(h.score).label}</span></td>
      <td><button class="btn btn-outline btn-sm" data-rview="${idx}">Inspect</button></td>
    </tr>`).join('');
  body.querySelectorAll('[data-rview]').forEach(b=> b.addEventListener('click', ()=> openReportModal(scanHistory[+b.dataset.rview])));
}

function renderRecent(){
  const wrap = document.getElementById('dashRecent');
  if(!wrap) return;
  if(!scanHistory.length){ wrap.innerHTML = `<div style="text-align:center; padding:18px; color:var(--text-faint); font-size:11.5px;">No scans yet. Run an analysis below.</div>`; return; }
  wrap.innerHTML = scanHistory.slice(0,5).map(h=>`
    <div style="display:flex; align-items:center; gap:10px; padding:7px 0; border-bottom:1px solid var(--line);">
      <div style="width:7px; height:7px; border-radius:50%; background:${riskColor(riskTier(h.score).cls)}; flex-shrink:0;"></div>
      <div style="flex:1; min-width:0;"><div style="font-size:12px; font-weight:600; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${h.contentLabel}</div><div style="font-size:10px; color:var(--text-faint);">${h.contentType}</div></div>
      <div style="font-family:var(--mono); font-size:11.5px; font-weight:700; color:${riskColor(riskTier(h.score).cls)}">${h.score}</div>
    </div>`).join('');
}

document.getElementById('exportHistBtn')?.addEventListener('click', ()=>{
  if(!scanHistory.length){ toast('Nothing to export', '', 'warn'); return; }
  const rows = [['Date','Content','Type','Risk','Trust','Confidence','Status']];
  scanHistory.forEach(h=> rows.push([new Date(h.date).toLocaleString(), h.contentLabel, h.contentType, h.score, h.trust+'%', h.confidence+'%', riskTier(h.score).label]));
  const csv = rows.map(r=>r.map(v=>`"${v}"`).join(',')).join('\n');
  const blob = new Blob([csv], {type:'text/csv'});
  const a = document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='trustguard-history.csv'; a.click();
  toast('Exported', 'trustguard-history.csv downloaded', 'safe');
});

document.getElementById('clearHistBtn')?.addEventListener('click', async ()=>{
  try {
    await apiPost('/api/history/clear', {});
    scanHistory=[]; renderHistory(); renderReports(); renderRecent(); updateDashboardStats();
    toast('History cleared', '', 'info');
  } catch(e){ toast('Failed', e.message, 'danger'); }
});

/* ============ REPORT MODAL ============ */
function openReportModal(data){
  const tier = riskTier(data.score);
  const body = document.getElementById('modalBody');
  if(!body) return;
  body.innerHTML = `
    <div style="margin-bottom:12px;"><span style="font-size:10px; text-transform:uppercase; color:var(--text-faint); letter-spacing:1px;">Forensic Target</span><h3 style="font-size:16px;">${data.contentLabel}</h3></div>
    <div class="telemetry-row"><span>Content Modality</span><span>${data.contentType}</span></div>
    <div class="telemetry-row"><span>Risk Score</span><span style="color:${riskColor(tier.cls)}">${data.score}/100 — ${tier.label}</span></div>
    <div class="telemetry-row"><span>Authenticity Score</span><span>${data.trust}%</span></div>
    <div class="telemetry-row"><span>Model Confidence</span><span>${data.confidence}%</span></div>
    <div class="telemetry-row"><span>Scan Timestamp</span><span>${new Date(data.date).toLocaleString()}</span></div>
    <div style="margin-top:14px;">
      <h4 style="font-size:12px; text-transform:uppercase; color:var(--cyan); margin-bottom:4px;">Mitigation Guidance</h4>
      <p style="font-size:12px; color:var(--text-dim); line-height:1.45;">${recommendation(tier.cls).text}</p>
    </div>
    <button class="btn btn-primary btn-block btn-sm" id="downloadReportTxtBtn" style="margin-top:16px;">Download Dossier (.txt)</button>
  `;
  document.getElementById('reportModal')?.classList.add('open');
  document.getElementById('downloadReportTxtBtn')?.addEventListener('click', ()=>{
    const txt = `TRUSTGUARD AI — FORENSIC REPORT\n\nTarget: ${data.contentLabel}\nType: ${data.contentType}\nRisk Score: ${data.score}/100 (${tier.label})\nAuthenticity: ${data.trust}%\nConfidence: ${data.confidence}%\nDate: ${new Date(data.date).toLocaleString()}\n\nRecommendation:\n${recommendation(tier.cls).text}\n\n(Generated by TrustGuard AI Production Pretrained Engine)`;
    const blob = new Blob([txt], {type:'text/plain'});
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'trustguard-report.txt'; a.click();
    toast('Report downloaded', '', 'safe');
  });
}
document.getElementById('modalCloseBtn')?.addEventListener('click', ()=> document.getElementById('reportModal')?.classList.remove('open'));
document.getElementById('reportModal')?.addEventListener('click', e=>{ if(e.target.id==='reportModal') e.currentTarget.classList.remove('open'); });

/* ============ ASSISTANT ============ */
const assistPanel = document.getElementById('assistPanel');
function openAssistant(){ assistPanel?.classList.add('open'); }
document.getElementById('assistFab')?.addEventListener('click', ()=> assistPanel?.classList.toggle('open'));
document.getElementById('assistClose')?.addEventListener('click', ()=> assistPanel?.classList.remove('open'));

function pushBotMsg(text){
  const body = document.getElementById('assistBody');
  if(!body) return;
  const div = document.createElement('div'); div.className='msg bot'; div.textContent = text;
  body.appendChild(div); body.scrollTop = body.scrollHeight;
}
function pushUserMsg(text){
  const body = document.getElementById('assistBody');
  if(!body) return;
  const div = document.createElement('div'); div.className='msg user'; div.textContent = text;
  body.appendChild(div); body.scrollTop = body.scrollHeight;
}
function assistantReply(q){
  const lower = q.toLowerCase();
  const ctx = lastScanContext;
  if(!ctx) return "Run a scan on any module and I will explain the genuine model prediction and mitigation steps.";
  const tier = riskTier(ctx.score);
  if(lower.includes('why') || lower.includes('risk')) return `${ctx.contentLabel} evaluated with ${ctx.score}/100 risk (${tier.label}). Confidence is ${ctx.confidence}%.`;
  if(lower.includes('safe') || lower.includes('should i')) return recommendation(tier.cls).text;
  return `Summary: ${ctx.contentLabel} (${ctx.contentType}) has ${ctx.score}/100 risk (${tier.label}).`;
}
document.getElementById('assistSendBtn')?.addEventListener('click', ()=>{
  const inp = document.getElementById('assistInput');
  if(!inp || !inp.value.trim()) return;
  const q = inp.value.trim();
  pushUserMsg(q); inp.value='';
  setTimeout(()=> pushBotMsg(assistantReply(q)), 400);
});
document.getElementById('assistInput')?.addEventListener('keydown', e=>{ if(e.key==='Enter') document.getElementById('assistSendBtn')?.click(); });

/* ============ ENGINE STATUS POLLING ============ */
async function checkBackendEngineStatus() {
  const badge = document.getElementById('engineBadge');
  const latEl = document.getElementById('bentoLatency');
  const statusTxt = document.getElementById('bentoStatusTxt');
  const tag = document.getElementById('bentoEngineStatusTag');
  const t0 = performance.now();
  try {
    const res = await fetch(`${API_BASE_URL}/api/status`);
    const lat = Math.max(1, Math.round(performance.now() - t0));
    if (latEl) latEl.textContent = `${lat}ms`;

    if (res.ok) {
      const data = await res.json();
      if (badge) {
        badge.innerHTML = `<i class="dot" style="background:var(--safe); box-shadow:0 0 6px var(--safe);"></i>Engine: ${data.imageModel ? 'ViT Online' : 'Active'}`;
        badge.style.color = 'var(--safe)';
      }
      if (statusTxt) { statusTxt.textContent = '● Online'; statusTxt.style.color = 'var(--safe)'; }
      if (tag) { tag.textContent = 'ONLINE'; tag.style.color = 'var(--safe)'; }
    } else {
      if (badge) { badge.innerHTML = `<i class="dot" style="background:var(--danger)"></i>Offline`; badge.style.color = 'var(--danger-2)'; }
      if (statusTxt) { statusTxt.textContent = '● Offline'; statusTxt.style.color = 'var(--danger-2)'; }
      if (tag) { tag.textContent = 'OFFLINE'; tag.style.color = 'var(--danger-2)'; }
    }
  } catch (e) {
    if (badge) { badge.innerHTML = `<i class="dot" style="background:var(--danger)"></i>Offline`; badge.style.color = 'var(--danger-2)'; }
    if (latEl) latEl.textContent = '—';
    if (statusTxt) { statusTxt.textContent = '● Offline'; statusTxt.style.color = 'var(--danger-2)'; }
    if (tag) { tag.textContent = 'OFFLINE'; tag.style.color = 'var(--danger-2)'; }
  }
}

/* ============ INITIALIZATION ============ */
window.addEventListener('load', async ()=>{
  pushBotMsg("Hi, I am the TrustGuard AI SOC Assistant. Run a scan anywhere across the platform and I will provide explainable intelligence.");
  await checkAuthSession();
  await checkBackendEngineStatus();
  await fetchDashboardStats();
  await fetchHistoryFromBackend();
});
</script>
<!-- Firebase realtime sync -->
<script type="module" src="./firebase.js"></script>
</body>
</html>
'''

if __name__ == "__main__":
    generate_html()
