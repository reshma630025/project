# -*- coding: utf-8 -*-
"""
Script to build the comprehensive TrustGuard AI index.html
with dedicated Login Page, Protected Route Guards, Session Restore,
5-Row Spatial Bento Grid AI SOC, Frame-by-Frame Video Timeline,
Audio STFT Segment Timeline, Multilingual Assistant, and Live Backend Sync.
"""

import sys

def build_frontend():
    print("Writing index.html...", flush=True)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(INDEX_HTML_CONTENT)
    print("index.html written successfully!", flush=True)

INDEX_HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TrustGuard AI — Unified Multimodal Deepfake & AI SOC Platform</title>
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
  --glass:rgba(20,28,44,.72);
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
  --glass:rgba(255,255,255,.82);
  --glass-brd:rgba(30,50,90,.14);
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

/* ============ FULL-SCREEN LOADING OVERLAY ============ */
#app-loader{
  position:fixed; inset:0; z-index:9999;
  background:var(--void);
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  gap:20px; transition:opacity .4s ease, visibility .4s ease;
}
#app-loader.hide{opacity:0; visibility:hidden; pointer-events:none;}
.loader-spinner{
  width:64px; height:64px; border-radius:50%;
  border:3px solid rgba(45,217,232,.15);
  border-top-color:var(--cyan);
  border-right-color:var(--violet);
  animation:spin 1s linear infinite;
}
@keyframes spin{to{transform:rotate(360deg);}}
.loader-title{font-family:var(--disp); font-size:18px; font-weight:700; letter-spacing:.5px; color:var(--text);}
.loader-sub{font-size:12.5px; color:var(--text-dim); font-family:var(--mono);}

/* ============ OFFLINE NOTIFICATION BANNER ============ */
#offline-banner{
  display:none; position:fixed; top:0; left:0; right:0; z-index:5000;
  background:linear-gradient(90deg, #991b1b, #7f1d1d);
  color:#fff; padding:10px 16px; font-size:12.5px; font-weight:600;
  text-align:center; box-shadow:0 4px 16px rgba(0,0,0,.4);
  border-bottom:1px solid rgba(255,255,255,.2);
}
#offline-banner code{background:rgba(0,0,0,.3); padding:2px 6px; border-radius:4px; font-family:var(--mono); margin:0 4px;}

/* ============ LAYOUT ============ */
#app{position:relative; z-index:1; display:flex; min-height:100vh;}
.sidebar{
  width:var(--sidebar-w); flex-shrink:0; position:sticky; top:0; height:100vh;
  background:var(--glass); backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px); border-right:1px solid var(--glass-brd);
  display:flex; flex-direction:column; padding:18px 14px; z-index:40; transition:transform .3s ease;
}
.sidebar.hidden{display:none;}
.brand{display:flex; align-items:center; gap:10px; padding:6px 10px 18px; border-bottom:1px solid var(--line); margin-bottom:12px; cursor:pointer;}
.brand-mark{width:36px; height:36px; border-radius:10px; background:conic-gradient(from 220deg, var(--cyan), var(--violet), var(--cyan)); display:flex; align-items:center; justify-content:center; font-family:var(--disp); font-weight:800; color:#04141a; font-size:15px; box-shadow:0 0 20px rgba(45,217,232,.35);}
.brand-name{font-family:var(--disp); font-weight:700; font-size:16.5px; letter-spacing:.2px;}
.brand-tag{font-size:9.5px; font-family:var(--mono); color:var(--cyan); letter-spacing:1px; text-transform:uppercase;}

.nav-sec-title{font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1.2px; color:var(--text-faint); padding:12px 10px 6px; font-family:var(--mono);}
.nav-list{display:flex; flex-direction:column; gap:3px;}
.nav-item{
  display:flex; align-items:center; gap:11px; padding:9px 12px; border-radius:9px;
  color:var(--text-dim); font-size:13px; font-weight:500; transition:all .18s ease; cursor:pointer;
}
.nav-item i{font-size:15px; width:18px; text-align:center; color:var(--text-faint); transition:color .18s;}
.nav-item:hover{background:rgba(255,255,255,.05); color:var(--text);}
.nav-item:hover i{color:var(--cyan);}
.nav-item.active{background:linear-gradient(90deg, rgba(45,217,232,.12), rgba(139,107,240,.06)); color:var(--cyan); font-weight:600; border-left:3px solid var(--cyan);}
.nav-item.active i{color:var(--cyan);}
.nav-badge{margin-left:auto; font-size:9.5px; font-family:var(--mono); padding:2px 6px; border-radius:6px; background:rgba(45,217,232,.12); color:var(--cyan); font-weight:600;}

.sidebar-foot{margin-top:auto; padding-top:14px; border-top:1px solid var(--line); display:flex; flex-direction:column; gap:10px;}
.engine-chip{
  background:rgba(14,20,32,.7); border:1px solid var(--glass-brd); border-radius:9px;
  padding:8px 10px; display:flex; align-items:center; justify-content:space-between; font-size:11.5px;
}
.engine-dot{width:7px; height:7px; border-radius:50%; background:var(--safe); box-shadow:0 0 8px var(--safe); animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1;} 50%{opacity:.4;}}

/* MAIN WRAPPER */
.main-wrap{flex:1; display:flex; flex-direction:column; min-width:0;}
.topbar{
  height:60px; position:sticky; top:0; z-index:30; background:var(--glass);
  backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px); border-bottom:1px solid var(--glass-brd);
  display:flex; align-items:center; justify-content:space-between; padding:0 24px;
}
.topbar-left{display:flex; align-items:center; gap:14px;}
.menu-btn{display:none; background:transparent; border:none; color:var(--text); font-size:18px; cursor:pointer;}
.crumb{font-size:12.5px; color:var(--text-dim); display:flex; align-items:center; gap:6px; font-family:var(--mono);}
.crumb span{color:var(--cyan); font-weight:600;}

.topbar-right{display:flex; align-items:center; gap:12px;}
.topbar-btn{
  background:rgba(255,255,255,.05); border:1px solid var(--glass-brd); color:var(--text-dim);
  padding:6px 12px; border-radius:8px; font-size:12.5px; display:flex; align-items:center; gap:7px; transition:all .2s ease;
}
.topbar-btn:hover{background:rgba(255,255,255,.1); color:var(--text); border-color:var(--cyan-dim);}
.status-pill{
  display:flex; align-items:center; gap:7px; padding:5px 11px; border-radius:20px;
  background:rgba(51,209,154,.1); border:1px solid rgba(51,209,154,.25); color:var(--safe);
  font-size:11.5px; font-weight:600; font-family:var(--mono);
}
.status-dot{width:6px; height:6px; border-radius:50%; background:var(--safe); box-shadow:0 0 6px var(--safe);}

.user-profile-badge{
  display:flex; align-items:center; gap:9px; padding:4px 10px 4px 6px;
  background:rgba(14,20,32,.8); border:1px solid var(--glass-brd); border-radius:22px; cursor:pointer;
  transition:all .2s;
}
.user-profile-badge:hover{border-color:var(--cyan); background:rgba(45,217,232,.08);}
.user-avatar{
  width:28px; height:28px; border-radius:50%; background:linear-gradient(135deg, var(--cyan), var(--violet));
  display:flex; align-items:center; justify-content:center; font-family:var(--disp); font-weight:700; font-size:11px; color:#04141a;
}
.user-name{font-size:12px; font-weight:600; max-width:110px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}

.content{padding:24px; max-width:1480px; width:100%; margin:0 auto; flex:1;}
.page-view{display:none;}
.page-view.active{display:block;}

/* ============ DEDICATED LOGIN / REGISTER FULL PAGE ============ */
.auth-page-container{
  display:flex; align-items:center; justify-content:center; min-height:calc(100vh - 120px);
  padding:20px;
}
.auth-card{
  width:100%; max-width:480px; background:var(--panel); border:1px solid var(--glass-brd);
  border-radius:18px; padding:32px 28px; box-shadow:0 12px 40px rgba(0,0,0,.6), 0 0 30px rgba(45,217,232,.08);
  position:relative; overflow:hidden;
}
.auth-card::before{
  content:''; position:absolute; top:0; left:0; right:0; height:3px;
  background:linear-gradient(90deg, var(--cyan), var(--violet), var(--safe));
}
.auth-header{text-align:center; margin-bottom:24px;}
.auth-header .brand-mark{margin:0 auto 12px; width:46px; height:46px; font-size:18px;}
.auth-header h1{font-family:var(--disp); font-size:22px; font-weight:700;}
.auth-header p{font-size:13px; color:var(--text-dim); margin-top:4px;}

.auth-tabs{
  display:flex; background:rgba(0,0,0,.3); padding:4px; border-radius:10px;
  border:1px solid var(--line); margin-bottom:20px; gap:4px;
}
.auth-tab{
  flex:1; padding:8px 12px; font-size:12.5px; font-weight:600; text-align:center;
  border-radius:7px; border:none; background:transparent; color:var(--text-dim); cursor:pointer;
  transition:all .2s ease;
}
.auth-tab.active{background:rgba(45,217,232,.14); color:var(--cyan); border:1px solid rgba(45,217,232,.3);}

.auth-form{display:flex; flex-direction:column; gap:16px;}
.form-field{display:flex; flex-direction:column; gap:6px;}
.form-field label{font-size:12px; font-weight:600; color:var(--text-dim); font-family:var(--mono);}
.input-with-icon{position:relative; display:flex; align-items:center;}
.input-with-icon input{
  width:100%; padding:10px 14px 10px 38px; background:rgba(0,0,0,.35);
  border:1px solid var(--glass-brd); border-radius:8px; color:var(--text); font-size:13.5px;
  font-family:inherit; transition:border-color .2s;
}
.input-with-icon input:focus{border-color:var(--cyan); background:rgba(0,0,0,.5);}
.input-icon{position:absolute; left:12px; font-size:14px; color:var(--text-faint); pointer-events:none;}
.toggle-pwd-btn{
  position:absolute; right:10px; background:none; border:none; color:var(--text-faint);
  font-size:13px; cursor:pointer; padding:4px;
}
.toggle-pwd-btn:hover{color:var(--text);}

.auth-options{display:flex; align-items:center; justify-content:space-between; font-size:12px; color:var(--text-dim);}
.auth-options label{display:flex; align-items:center; gap:6px; cursor:pointer;}
.auth-options input[type="checkbox"]{accent-color:var(--cyan);}

.auth-msg{
  display:none; padding:10px 14px; border-radius:8px; font-size:12.5px; font-weight:500;
}
.auth-msg.error{display:block; background:rgba(242,73,92,.15); border:1px solid var(--danger); color:var(--danger-2);}
.auth-msg.success{display:block; background:rgba(51,209,154,.15); border:1px solid var(--safe); color:var(--safe);}
.auth-msg.warn{display:block; background:rgba(245,185,66,.15); border:1px solid var(--warn); color:var(--warn);}

.auth-btn-primary{
  background:linear-gradient(135deg, var(--cyan), var(--cyan-dim));
  color:#04141a; font-weight:700; font-size:13.5px; border:none; padding:11px;
  border-radius:8px; cursor:pointer; transition:transform .15s, box-shadow .15s;
  box-shadow:0 0 16px rgba(45,217,232,.3); display:flex; align-items:center; justify-content:center; gap:8px;
}
.auth-btn-primary:hover{transform:translateY(-1px); box-shadow:0 0 24px rgba(45,217,232,.5);}

.auth-demo-box{
  margin-top:20px; padding:14px; border-radius:10px; background:rgba(0,0,0,.25);
  border:1px dashed var(--line); font-size:12px;
}
.auth-demo-box .demo-title{font-weight:700; color:var(--cyan); margin-bottom:6px; font-family:var(--mono); display:flex; align-items:center; justify-content:space-between;}
.auth-demo-box code{background:rgba(255,255,255,.08); padding:2px 5px; border-radius:4px; font-family:var(--mono); color:var(--text);}
.demo-quick-btn{
  width:100%; margin-top:10px; background:rgba(139,107,240,.15); border:1px solid rgba(139,107,240,.35);
  color:var(--text); padding:7px; border-radius:6px; font-size:11.5px; font-weight:600; cursor:pointer;
  transition:all .2s;
}
.demo-quick-btn:hover{background:rgba(139,107,240,.28); border-color:var(--violet);}

/* ============ 5-ROW SPATIAL BENTO GRID SOC DASHBOARD ============ */
.dashboard-grid{display:flex; flex-direction:column; gap:20px;}

/* ROW 1: AI SECURITY STATUS BANNER */
.soc-hero-banner{
  background:linear-gradient(135deg, rgba(20,28,44,.85), rgba(14,20,32,.95));
  border:1px solid var(--glass-brd); border-radius:var(--radius); padding:22px 28px;
  display:flex; align-items:center; justify-content:space-between; gap:24px; flex-wrap:wrap;
  box-shadow:0 8px 30px rgba(0,0,0,.4); position:relative; overflow:hidden;
}
.soc-hero-banner::before{
  content:''; position:absolute; inset:0; pointer-events:none;
  background:radial-gradient(500px 200px at 0% 0%, rgba(45,217,232,.08), transparent 70%);
}
.soc-hero-left h2{font-family:var(--disp); font-size:22px; font-weight:700; margin-bottom:4px;}
.soc-hero-left p{color:var(--text-dim); font-size:13.5px; max-width:580px;}

.soc-hero-metrics{display:flex; align-items:center; gap:24px;}
.soc-dial-wrap{display:flex; align-items:center; gap:14px;}
.soc-dial{width:68px; height:68px; position:relative; display:flex; align-items:center; justify-content:center;}
.soc-dial svg{transform:rotate(-90deg); width:100%; height:100%;}
.soc-dial circle{fill:none; stroke-width:6; stroke-linecap:round;}
.soc-dial .bg{stroke:rgba(255,255,255,.08);}
.soc-dial .meter{stroke:var(--safe); stroke-dasharray:175; stroke-dashoffset:35; transition:stroke-dashoffset 1s ease, stroke .3s;}
.soc-dial-text{position:absolute; font-family:var(--disp); font-weight:700; font-size:16px;}

.threat-status-tag{
  padding:5px 12px; border-radius:20px; font-size:11px; font-weight:700; font-family:var(--mono);
  background:rgba(51,209,154,.12); color:var(--safe); border:1px solid rgba(51,209,154,.3);
  display:inline-flex; align-items:center; gap:6px;
}

/* ROW 2: 4 LIVE COUNTER CARDS */
.stat-quad-grid{
  display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:16px;
}
.stat-card{
  background:var(--panel); border:1px solid var(--glass-brd); border-radius:var(--radius);
  padding:18px 20px; position:relative; overflow:hidden; transition:transform .2s, border-color .2s;
}
.stat-card:hover{transform:translateY(-2px); border-color:var(--line);}
.stat-head{display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;}
.stat-label{font-size:12px; color:var(--text-dim); font-weight:600; text-transform:uppercase; font-family:var(--mono); letter-spacing:.5px;}
.stat-icon{width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:14px;}
.stat-val{font-family:var(--disp); font-size:28px; font-weight:800; letter-spacing:-.5px; color:var(--text);}
.stat-meta{font-size:11px; color:var(--text-faint); margin-top:4px; display:flex; align-items:center; gap:5px;}

/* ROW 3: 9-DETECTOR BENTO MATRIX */
.bento-matrix-grid{
  display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px;
}
.bento-detector-card{
  background:var(--panel); border:1px solid var(--glass-brd); border-radius:var(--radius);
  padding:20px; display:flex; flex-direction:column; justify-content:space-between;
  transition:all .22s ease; position:relative; min-height:180px;
}
.bento-detector-card:hover{border-color:var(--cyan); transform:translateY(-3px); box-shadow:0 8px 24px rgba(0,0,0,.4);}
.detector-header{display:flex; align-items:flex-start; justify-content:space-between; gap:12px;}
.detector-icon{width:40px; height:40px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:18px;}
.detector-info h3{font-family:var(--disp); font-size:15px; font-weight:700; margin-bottom:3px;}
.detector-info p{font-size:12px; color:var(--text-dim); line-height:1.4;}
.detector-tag{font-size:9.5px; font-family:var(--mono); padding:2px 7px; border-radius:4px; font-weight:600;}
.detector-foot{margin-top:16px; display:flex; align-items:center; justify-content:space-between; pt-2; border-top:1px solid var(--line); font-size:11.5px;}
.detector-launch-btn{
  background:rgba(45,217,232,.1); border:1px solid rgba(45,217,232,.3); color:var(--cyan);
  padding:5px 12px; border-radius:6px; font-size:11.5px; font-weight:600; cursor:pointer;
  transition:all .15s ease;
}
.detector-launch-btn:hover{background:var(--cyan); color:#04141a;}

/* ROW 4: RECENT SCANS TABLE + THREAT ALERTS & RISK GUIDE */
.row4-split-grid{
  display:grid; grid-template-columns:2fr 1fr; gap:20px;
}
@media(max-width:1080px){.row4-split-grid{grid-template-columns:1fr;}}

.soc-table-card{
  background:var(--panel); border:1px solid var(--glass-brd); border-radius:var(--radius);
  padding:20px; display:flex; flex-direction:column;
}
.soc-table-head{display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; flex-wrap:wrap; gap:10px;}
.soc-table-title{font-family:var(--disp); font-size:16px; font-weight:700;}
.soc-table-wrap{overflow-x:auto;}
table.soc-table{width:100%; border-collapse:collapse; font-size:12.5px; text-align:left;}
table.soc-table th{color:var(--text-faint); font-family:var(--mono); font-size:11px; text-transform:uppercase; padding:10px 12px; border-bottom:1px solid var(--line);}
table.soc-table td{padding:12px; border-bottom:1px solid var(--line); color:var(--text-dim);}
table.soc-table tr:hover td{background:rgba(255,255,255,.02); color:var(--text);}
.result-pill{display:inline-flex; align-items:center; gap:5px; padding:3px 8px; border-radius:12px; font-size:10.5px; font-weight:700; font-family:var(--mono);}
.result-pill.genuine{background:rgba(51,209,154,.15); color:var(--safe); border:1px solid rgba(51,209,154,.3);}
.result-pill.fake{background:rgba(242,73,92,.15); color:var(--danger-2); border:1px solid var(--danger);}
.result-pill.warn{background:rgba(245,185,66,.15); color:var(--warn); border:1px solid var(--warn);}

.threat-guide-card{
  background:var(--panel); border:1px solid var(--glass-brd); border-radius:var(--radius);
  padding:20px; display:flex; flex-direction:column; gap:14px;
}
.threat-level-row{
  display:flex; align-items:center; justify-content:space-between; padding:8px 10px;
  background:rgba(0,0,0,.25); border-radius:8px; border-left:3px solid var(--safe); font-size:12px;
}
.threat-level-row.mod{border-left-color:var(--warn);}
.threat-level-row.crit{border-left-color:var(--danger);}

/* ROW 5: DIRECT QUICK SCANNER DOCK */
.quick-scanner-card{
  background:var(--panel); border:1px solid var(--glass-brd); border-radius:var(--radius);
  padding:22px; margin-top:6px;
}
.quick-scanner-tabs{display:flex; gap:6px; overflow-x:auto; padding-bottom:12px; border-bottom:1px solid var(--line); margin-bottom:18px;}
.quick-tab{
  padding:8px 14px; border-radius:8px; font-size:12.5px; font-weight:600; background:rgba(255,255,255,.04);
  border:1px solid var(--line); color:var(--text-dim); cursor:pointer; white-space:nowrap; transition:all .18s;
}
.quick-tab.active{background:rgba(45,217,232,.14); color:var(--cyan); border-color:var(--cyan);}

/* TOOL WORKSPACES */
.tool-workspace{display:flex; flex-direction:column; gap:20px;}
.tool-header{display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap;}
.tool-header h1{font-family:var(--disp); font-size:24px; font-weight:800;}
.tool-header p{color:var(--text-dim); font-size:13.5px; margin-top:3px;}

.tool-grid-2col{display:grid; grid-template-columns:1.2fr 1fr; gap:20px;}
@media(max-width:960px){.tool-grid-2col{grid-template-columns:1fr;}}

.input-panel{
  background:var(--panel); border:1px solid var(--glass-brd); border-radius:var(--radius); padding:22px;
  display:flex; flex-direction:column; gap:16px;
}
.dropzone{
  border:2px dashed var(--line); border-radius:12px; padding:32px 20px; text-align:center;
  background:rgba(0,0,0,.25); cursor:pointer; transition:all .2s; display:flex; flex-direction:column;
  align-items:center; justify-content:center; gap:10px;
}
.dropzone:hover{border-color:var(--cyan); background:rgba(45,217,232,.04);}
.dropzone-icon{font-size:32px; color:var(--cyan-dim);}
.preview-container{display:none; margin-top:12px; max-height:260px; overflow:hidden; border-radius:10px; border:1px solid var(--line);}
.preview-container img, .preview-container video{width:100%; height:100%; object-fit:contain; background:#000;}

.btn-primary{
  background:linear-gradient(135deg, var(--cyan), var(--cyan-dim)); color:#04141a;
  border:none; padding:12px 20px; border-radius:9px; font-size:13.5px; font-weight:700;
  cursor:pointer; transition:all .2s ease; display:inline-flex; align-items:center; justify-content:center; gap:8px;
  box-shadow:0 0 16px rgba(45,217,232,.25);
}
.btn-primary:hover{transform:translateY(-1px); box-shadow:0 0 24px rgba(45,217,232,.45);}
.btn-primary:disabled{opacity:.5; cursor:not-allowed; transform:none;}

/* RESULT DISPLAY PANEL */
.result-panel{
  background:var(--panel); border:1px solid var(--glass-brd); border-radius:var(--radius); padding:22px;
  display:flex; flex-direction:column; gap:18px; position:relative; min-height:360px;
}
.result-placeholder{
  display:flex; flex-direction:column; align-items:center; justify-content:center; flex:1; text-align:center;
  color:var(--text-faint); gap:12px; padding:40px 20px;
}
.result-hero{
  padding:20px; border-radius:12px; display:flex; align-items:center; justify-content:space-between; gap:16px;
  border:1px solid var(--line);
}
.result-hero.genuine{background:rgba(51,209,154,.12); border-color:var(--safe);}
.result-hero.fake{background:rgba(242,73,92,.14); border-color:var(--danger);}
.result-hero.warn{background:rgba(245,185,66,.14); border-color:var(--warn);}

.result-verdict-title{font-family:var(--disp); font-size:22px; font-weight:800; display:flex; align-items:center; gap:10px;}
.result-verdict-sub{font-size:12.5px; color:var(--text-dim); margin-top:4px;}

.result-scores-grid{display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:10px;}
.score-box{background:rgba(0,0,0,.3); border:1px solid var(--line); border-radius:8px; padding:10px 12px;}
.score-box-label{font-size:10.5px; font-family:var(--mono); color:var(--text-faint); text-transform:uppercase;}
.score-box-val{font-family:var(--disp); font-size:18px; font-weight:700; color:var(--text); margin-top:2px;}

.indicators-list{display:flex; flex-direction:column; gap:6px;}
.indicator-item{
  font-size:12px; padding:8px 12px; border-radius:6px; background:rgba(255,255,255,.03);
  border-left:3px solid var(--cyan); display:flex; align-items:center; gap:8px;
}

/* ============ VIDEO & AUDIO TIMELINE FORENSICS ============ */
.timeline-card{
  background:rgba(0,0,0,.35); border:1px solid var(--line); border-radius:10px; padding:14px;
  display:flex; flex-direction:column; gap:10px;
}
.timeline-head{display:flex; align-items:center; justify-content:space-between; font-size:12px; font-weight:600; font-family:var(--mono);}
.timeline-bar{
  height:24px; background:rgba(255,255,255,.05); border-radius:6px; display:flex; overflow:hidden;
  border:1px solid var(--line); gap:2px; padding:2px;
}
.timeline-tick{
  flex:1; border-radius:3px; background:var(--safe); opacity:.85; transition:all .15s; cursor:pointer;
  position:relative;
}
.timeline-tick:hover{opacity:1; transform:scaleY(1.15);}
.timeline-tick.fake{background:var(--danger);}
.timeline-tick.warn{background:var(--warn);}

/* ============ MULTILINGUAL AI ASSISTANT WIDGET ============ */
#ai-assistant-fab{
  position:fixed; bottom:24px; right:24px; z-index:100;
  width:52px; height:52px; border-radius:50%; background:linear-gradient(135deg, var(--cyan), var(--violet));
  display:flex; align-items:center; justify-content:center; font-size:22px; color:#04141a; cursor:pointer;
  box-shadow:0 8px 24px rgba(45,217,232,.4); transition:all .2s ease;
}
#ai-assistant-fab:hover{transform:scale(1.08);}

#ai-chat-window{
  display:none; position:fixed; bottom:86px; right:24px; z-index:101;
  width:360px; height:500px; background:var(--panel); border:1px solid var(--glass-brd);
  border-radius:16px; box-shadow:0 12px 40px rgba(0,0,0,.6); flex-direction:column; overflow:hidden;
}
#ai-chat-window.open{display:flex;}
.chat-head{
  background:rgba(20,28,44,.9); border-bottom:1px solid var(--line); padding:12px 16px;
  display:flex; align-items:center; justify-content:space-between;
}
.chat-title{font-family:var(--disp); font-size:14px; font-weight:700; display:flex; align-items:center; gap:8px;}
.chat-lang-select{
  background:rgba(0,0,0,.4); border:1px solid var(--line); color:var(--text); font-size:11px;
  padding:3px 6px; border-radius:6px; font-family:var(--mono);
}
.chat-body{flex:1; padding:14px; overflow-y:auto; display:flex; flex-direction:column; gap:10px; font-size:12.5px;}
.chat-msg{padding:8px 12px; border-radius:10px; max-width:85%; line-height:1.4;}
.chat-msg.bot{background:rgba(45,217,232,.1); border:1px solid rgba(45,217,232,.25); align-self:flex-start; color:var(--text);}
.chat-msg.user{background:var(--violet); color:#fff; align-self:flex-end;}
.chat-foot{padding:10px; border-top:1px solid var(--line); display:flex; gap:6px;}
.chat-input{
  flex:1; background:rgba(0,0,0,.3); border:1px solid var(--line); border-radius:8px;
  padding:8px 12px; color:var(--text); font-size:12px; font-family:inherit;
}
.chat-send-btn{background:var(--cyan); border:none; color:#04141a; font-weight:700; border-radius:8px; padding:0 12px; cursor:pointer;}

@media(max-width:768px){
  .sidebar{position:fixed; transform:translateX(-100%);}
  .sidebar.open{transform:translateX(0);}
  .menu-btn{display:block;}
  .topbar{padding:0 14px;}
  .content{padding:16px;}
  #ai-chat-window{width:calc(100vw - 32px); right:16px;}
}
</style>
</head>
<body>

<canvas id="particles"></canvas>
<div class="bg-glow"></div>

<!-- FULL-SCREEN INITIALIZATION LOADER -->
<div id="app-loader">
  <div class="loader-spinner"></div>
  <div class="loader-title">TRUSTGUARD AI SOC INITIALIZING</div>
  <div class="loader-sub">Verifying Pretrained ViT & Multi-Signal Defense Engine...</div>
</div>

<!-- BACKEND OFFLINE BANNER -->
<div id="offline-banner">
  ⚠ TrustGuard AI Backend is offline (127.0.0.1:8000). Please start the server using: <code>python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000</code>
</div>

<div id="app">
  <!-- LEFT SIDEBAR -->
  <aside class="sidebar" id="sidebar">
    <div class="brand" onclick="navigateTo('dashboard')">
      <div class="brand-mark">TG</div>
      <div>
        <div class="brand-name">TrustGuard AI</div>
        <div class="brand-tag">SOC Multimodal</div>
      </div>
    </div>

    <div class="nav-sec-title">Core Operations</div>
    <div class="nav-list">
      <div class="nav-item active" data-page="dashboard" onclick="navigateTo('dashboard')">
        <i>☵</i> Bento Dashboard
      </div>
      <div class="nav-item" data-page="image" onclick="navigateTo('image')">
        <i>🖼</i> Image Deepfake (ViT)
      </div>
      <div class="nav-item" data-page="video" onclick="navigateTo('video')">
        <i>🎬</i> Video Deepfake (Radar)
      </div>
      <div class="nav-item" data-page="audio" onclick="navigateTo('audio')">
        <i>🎙</i> Audio Forensics (STFT)
      </div>
      <div class="nav-item" data-page="text" onclick="navigateTo('text')">
        <i>✉</i> Text Scam & Phishing
      </div>
      <div class="nav-item" data-page="jobs" onclick="navigateTo('jobs')">
        <i>💼</i> Job / Internship Scan
      </div>
      <div class="nav-item" data-page="urls" onclick="navigateTo('urls')">
        <i>🌐</i> URL Phishing Radar
      </div>
      <div class="nav-item" data-page="ocr" onclick="navigateTo('ocr')">
        <i>📄</i> OCR Poster Analysis
      </div>
      <div class="nav-item" data-page="company" onclick="navigateTo('company')">
        <i>🏢</i> Company Verification
      </div>
      <div class="nav-item" data-page="social" onclick="navigateTo('social')">
        <i>📱</i> Social Media Shield
      </div>
    </div>

    <div class="nav-sec-title">Intelligence & Account</div>
    <div class="nav-list">
      <div class="nav-item" data-page="history" onclick="navigateTo('history')">
        <i>⏳</i> Scan History
      </div>
      <div class="nav-item" data-page="profile" onclick="navigateTo('profile')">
        <i>👤</i> Operator Profile
      </div>
      <div class="nav-item" data-page="settings" onclick="navigateTo('settings')">
        <i>⚙</i> SOC Settings
      </div>
      <div class="nav-item" data-page="login" id="nav-item-auth" onclick="handleAuthNavClick()">
        <i id="nav-auth-icon">🔑</i> <span id="nav-auth-label">Sign In / Register</span>
      </div>
    </div>

    <div class="sidebar-foot">
      <div class="engine-chip">
        <div style="display:flex; align-items:center; gap:7px;">
          <div class="engine-dot" id="sidebar-engine-dot"></div>
          <span style="font-weight:600;" id="sidebar-engine-label">ViT Engine Active</span>
        </div>
        <span style="font-family:var(--mono); color:var(--cyan); font-size:10.5px;" id="sidebar-latency">24ms</span>
      </div>
    </div>
  </aside>

  <!-- MAIN VIEW CONTAINER -->
  <div class="main-wrap">
    <!-- TOPBAR -->
    <header class="topbar">
      <div class="topbar-left">
        <button class="menu-btn" onclick="toggleSidebar()">☰</button>
        <div class="crumb">TRUSTGUARD // <span id="crumb-current">LOGIN PORTAL</span></div>
      </div>
      <div class="topbar-right">
        <div class="status-pill" id="topbar-status-pill">
          <div class="status-dot"></div>
          <span id="topbar-status-txt">SYSTEM NOMINAL</span>
        </div>
        <!-- USER PROFILE BADGE -->
        <div class="user-profile-badge" id="topbar-user-badge" onclick="handleProfileBadgeClick()">
          <div class="user-avatar" id="topbar-user-avatar">?</div>
          <span class="user-name" id="topbar-user-name">Guest Operator</span>
        </div>
      </div>
    </header>

    <!-- MAIN ROUTED CONTENT -->
    <main class="content">

      <!-- ============================================================ -->
      <!-- PAGE: DEDICATED LOGIN & REGISTRATION GATEWAY (#page-login) -->
      <!-- ============================================================ -->
      <section class="page-view active" id="page-login">
        <div class="auth-page-container">
          <div class="auth-card">
            <div class="auth-header">
              <div class="brand-mark">TG</div>
              <h1 id="auth-main-title">OPERATOR AUTHENTICATION</h1>
              <p>TrustGuard AI SOC Defense & Content Forensics Platform</p>
            </div>

            <!-- TABS: SIGN IN vs REGISTER -->
            <div class="auth-tabs">
              <button class="auth-tab active" id="tab-btn-login" onclick="switchAuthTab('login')">Sign In</button>
              <button class="auth-tab" id="tab-btn-register" onclick="switchAuthTab('register')">Register New Operator</button>
            </div>

            <!-- STATUS MESSAGE BANNER -->
            <div class="auth-msg" id="auth-msg-box"></div>

            <!-- FORM: SIGN IN -->
            <form class="auth-form" id="form-login" onsubmit="handleLoginSubmit(event)">
              <div class="form-field">
                <label>OPERATOR EMAIL / USERNAME</label>
                <div class="input-with-icon">
                  <span class="input-icon">✉</span>
                  <input type="text" id="login-email" placeholder="admin@trustguard.ai" required autocomplete="username">
                </div>
              </div>

              <div class="form-field">
                <label>SECURE PASSWORD</label>
                <div class="input-with-icon">
                  <span class="input-icon">🔒</span>
                  <input type="password" id="login-password" placeholder="••••••••••••" required autocomplete="current-password">
                  <button type="button" class="toggle-pwd-btn" onclick="togglePasswordVisibility('login-password')">👁</button>
                </div>
              </div>

              <div class="auth-options">
                <label>
                  <input type="checkbox" id="login-remember" checked> Remember session
                </label>
                <a href="javascript:void(0)" onclick="alert('For recovery or resetting test access, contact your SOC administrator or use the demo credentials.')" style="color:var(--cyan); font-size:11.5px;">Need Help?</a>
              </div>

              <button type="submit" class="auth-btn-primary" id="btn-submit-login">
                <span>Authenticate & Enter SOC</span> ➔
              </button>
            </form>

            <!-- FORM: REGISTER -->
            <form class="auth-form" id="form-register" style="display:none;" onsubmit="handleRegisterSubmit(event)">
              <div class="form-field">
                <label>FULL OPERATOR NAME</label>
                <div class="input-with-icon">
                  <span class="input-icon">👤</span>
                  <input type="text" id="reg-name" placeholder="Dr. Sarah Connor" required>
                </div>
              </div>

              <div class="form-field">
                <label>OFFICIAL EMAIL</label>
                <div class="input-with-icon">
                  <span class="input-icon">✉</span>
                  <input type="email" id="reg-email" placeholder="sarah@defense.gov" required>
                </div>
              </div>

              <div class="form-field">
                <label>ORGANIZATION / UNIT</label>
                <div class="input-with-icon">
                  <span class="input-icon">🏢</span>
                  <input type="text" id="reg-org" placeholder="Cyber Threat Defense Unit">
                </div>
              </div>

              <div class="form-field">
                <label>CHOOSE PASSWORD</label>
                <div class="input-with-icon">
                  <span class="input-icon">🔒</span>
                  <input type="password" id="reg-password" placeholder="At least 6 characters" required>
                  <button type="button" class="toggle-pwd-btn" onclick="togglePasswordVisibility('reg-password')">👁</button>
                </div>
              </div>

              <button type="submit" class="auth-btn-primary" id="btn-submit-register">
                <span>Create Operator Account</span> ➔
              </button>
            </form>

            <!-- DEMO TEST CREDENTIALS BOX -->
            <div class="auth-demo-box">
              <div class="demo-title">
                <span>PRE-SEEDED TEST CREDENTIALS</span>
                <span style="font-size:10px; color:var(--safe);">READY</span>
              </div>
              <div>User: <code>admin@trustguard.ai</code></div>
              <div style="margin-top:2px;">Password: <code>password123</code></div>
              <button type="button" class="demo-quick-btn" onclick="quickFillDemoAndLogin()">
                ⚡ 1-Click Quick Demo Login
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- ============================================================ -->
      <!-- PAGE: 5-ROW SPATIAL BENTO GRID SOC DASHBOARD (#page-dashboard) -->
      <!-- ============================================================ -->
      <section class="page-view" id="page-dashboard">
        <div class="dashboard-grid">

          <!-- ROW 1: AI SECURITY STATUS BANNER -->
          <div class="soc-hero-banner">
            <div class="soc-hero-left">
              <div class="threat-status-tag" id="dash-threat-tag">● SYSTEM NOMINAL</div>
              <h2 style="margin-top:8px;">TrustGuard AI Security Operations Center</h2>
              <p>Real-time multimodal forensic monitoring across synthetic video, generative audio, deepfake imagery, and fraudulent web interactions.</p>
            </div>
            <div class="soc-hero-metrics">
              <div class="soc-dial-wrap">
                <div class="soc-dial">
                  <svg viewBox="0 0 68 68">
                    <circle class="bg" cx="34" cy="34" r="28"></circle>
                    <circle class="meter" id="dash-radial-meter" cx="34" cy="34" r="28"></circle>
                  </svg>
                  <div class="soc-dial-text" id="dash-threat-score">14%</div>
                </div>
                <div>
                  <div style="font-size:11px; color:var(--text-faint); font-family:var(--mono);">RISK INDEX</div>
                  <div style="font-weight:700; font-size:14px; color:var(--safe);" id="dash-risk-label">LOW THREAT</div>
                </div>
              </div>
            </div>
          </div>

          <!-- ROW 2: 4 LIVE COUNTER CARDS -->
          <div class="stat-quad-grid">
            <div class="stat-card">
              <div class="stat-head">
                <span class="stat-label">TOTAL SCANS RUN</span>
                <div class="stat-icon" style="background:rgba(45,217,232,.12); color:var(--cyan);">📊</div>
              </div>
              <div class="stat-val" id="stat-total-scans">0</div>
              <div class="stat-meta">Synchronized with local DB</div>
            </div>

            <div class="stat-card">
              <div class="stat-head">
                <span class="stat-label">THREATS FLAGGED</span>
                <div class="stat-icon" style="background:rgba(242,73,92,.12); color:var(--danger-2);">⚠</div>
              </div>
              <div class="stat-val" id="stat-threats-flagged" style="color:var(--danger-2);">0</div>
              <div class="stat-meta">High & Critical Risk detections</div>
            </div>

            <div class="stat-card">
              <div class="stat-head">
                <span class="stat-label">DEEPFAKES DETECTED</span>
                <div class="stat-icon" style="background:rgba(139,107,240,.12); color:var(--violet);">🎭</div>
              </div>
              <div class="stat-val" id="stat-deepfakes-found">0</div>
              <div class="stat-meta">Image, Video & Voice models</div>
            </div>

            <div class="stat-card">
              <div class="stat-head">
                <span class="stat-label">SCAMS NEUTRALIZED</span>
                <div class="stat-icon" style="background:rgba(245,185,66,.12); color:var(--warn);">🛡</div>
              </div>
              <div class="stat-val" id="stat-scams-blocked">0</div>
              <div class="stat-meta">Job, URL & Text fraud intercepted</div>
            </div>
          </div>

          <!-- ROW 3: 9-DETECTOR BENTO MATRIX -->
          <div>
            <h3 style="font-family:var(--disp); font-size:16px; margin-bottom:12px;">Active Multimodal Defense Matrix</h3>
            <div class="bento-matrix-grid">
              <!-- 1. IMAGE -->
              <div class="bento-detector-card">
                <div class="detector-header">
                  <div class="detector-icon" style="background:rgba(45,217,232,.12); color:var(--cyan);">🖼</div>
                  <div class="detector-tag" style="background:rgba(51,209,154,.12); color:var(--safe);">ViT READY</div>
                </div>
                <div class="detector-info" style="margin-top:10px;">
                  <h3>Image Deepfake Detection</h3>
                  <p>Pretrained Vision Transformer + ELA sensor noise and Laplacian edge gradients.</p>
                </div>
                <div class="detector-foot">
                  <span>Accuracy: ~94.8%</span>
                  <button class="detector-launch-btn" onclick="navigateTo('image')">Launch Scanner →</button>
                </div>
              </div>

              <!-- 2. VIDEO -->
              <div class="bento-detector-card">
                <div class="detector-header">
                  <div class="detector-icon" style="background:rgba(139,107,240,.12); color:var(--violet);">🎬</div>
                  <div class="detector-tag" style="background:rgba(51,209,154,.12); color:var(--safe);">RADAR ACTIVE</div>
                </div>
                <div class="detector-info" style="margin-top:10px;">
                  <h3>Video Frame-by-Frame Radar</h3>
                  <p>Temporal face crop extraction, frame timeline analysis & anomaly aggregation.</p>
                </div>
                <div class="detector-foot">
                  <span>Temporal Timeline</span>
                  <button class="detector-launch-btn" onclick="navigateTo('video')">Analyze Video →</button>
                </div>
              </div>

              <!-- 3. AUDIO -->
              <div class="bento-detector-card">
                <div class="detector-header">
                  <div class="detector-icon" style="background:rgba(51,209,154,.12); color:var(--safe);">🎙</div>
                  <div class="detector-tag" style="background:rgba(51,209,154,.12); color:var(--safe);">STFT ACTIVE</div>
                </div>
                <div class="detector-info" style="margin-top:10px;">
                  <h3>Voice & Synthetic Audio</h3>
                  <p>STFT sliding-window spectral centroid variance & vocoder frequency cutoff checks.</p>
                </div>
                <div class="detector-foot">
                  <span>2.0s Sliding Segments</span>
                  <button class="detector-launch-btn" onclick="navigateTo('audio')">Analyze Audio →</button>
                </div>
              </div>

              <!-- 4. TEXT -->
              <div class="bento-detector-card">
                <div class="detector-header">
                  <div class="detector-icon" style="background:rgba(245,185,66,.12); color:var(--warn);">✉</div>
                  <div class="detector-tag" style="background:rgba(45,217,232,.12); color:var(--cyan);">NLP ACTIVE</div>
                </div>
                <div class="detector-info" style="margin-top:10px;">
                  <h3>Text Scam & Threat Engine</h3>
                  <p>Urgency detection, OTP/credential extortion, lottery & pressure tactic classification.</p>
                </div>
                <div class="detector-foot">
                  <span>Lexical Heuristics</span>
                  <button class="detector-launch-btn" onclick="navigateTo('text')">Scan Message →</button>
                </div>
              </div>

              <!-- 5. JOB -->
              <div class="bento-detector-card">
                <div class="detector-header">
                  <div class="detector-icon" style="background:rgba(45,217,232,.12); color:var(--cyan);">💼</div>
                  <div class="detector-tag" style="background:rgba(45,217,232,.12); color:var(--cyan);">RADAR ACTIVE</div>
                </div>
                <div class="detector-info" style="margin-top:10px;">
                  <h3>Job / Internship Scam Radar</h3>
                  <p>Upfront registration fee traps, unrealistic salary-to-skill ratios & domain spoofing.</p>
                </div>
                <div class="detector-foot">
                  <span>Multi-Factor Verification</span>
                  <button class="detector-launch-btn" onclick="navigateTo('jobs')">Verify Offer →</button>
                </div>
              </div>

              <!-- 6. URL -->
              <div class="bento-detector-card">
                <div class="detector-header">
                  <div class="detector-icon" style="background:rgba(242,73,92,.12); color:var(--danger-2);">🌐</div>
                  <div class="detector-tag" style="background:rgba(45,217,232,.12); color:var(--cyan);">ENTROPY ACTIVE</div>
                </div>
                <div class="detector-info" style="margin-top:10px;">
                  <h3>URL Phishing Scanner</h3>
                  <p>Shannon entropy computation, typosquatting, deceptive subdomains & TLD flags.</p>
                </div>
                <div class="detector-foot">
                  <span>Entropy & DNS Heuristics</span>
                  <button class="detector-launch-btn" onclick="navigateTo('urls')">Inspect Link →</button>
                </div>
              </div>

              <!-- 7. OCR -->
              <div class="bento-detector-card">
                <div class="detector-header">
                  <div class="detector-icon" style="background:rgba(139,107,240,.12); color:var(--violet);">📄</div>
                  <div class="detector-tag" style="background:rgba(51,209,154,.12); color:var(--safe);">TESSERACT READY</div>
                </div>
                <div class="detector-info" style="margin-top:10px;">
                  <h3>OCR Poster & Document Scanner</h3>
                  <p>Automated entity extraction for companies, salaries, registration fees & UPI IDs.</p>
                </div>
                <div class="detector-foot">
                  <span>6-Entity Grid</span>
                  <button class="detector-launch-btn" onclick="navigateTo('ocr')">Scan Poster →</button>
                </div>
              </div>

              <!-- 8. COMPANY -->
              <div class="bento-detector-card">
                <div class="detector-header">
                  <div class="detector-icon" style="background:rgba(51,209,154,.12); color:var(--safe);">🏢</div>
                  <div class="detector-tag" style="background:rgba(45,217,232,.12); color:var(--cyan);">IDENTITY CHECK</div>
                </div>
                <div class="detector-info" style="margin-top:10px;">
                  <h3>Company Identity Verification</h3>
                  <p>Cross-references official domains, corporate registrars & email alignment.</p>
                </div>
                <div class="detector-foot">
                  <span>Domain & MX Heuristics</span>
                  <button class="detector-launch-btn" onclick="navigateTo('company')">Verify Entity →</button>
                </div>
              </div>

              <!-- 9. SOCIAL -->
              <div class="bento-detector-card">
                <div class="detector-header">
                  <div class="detector-icon" style="background:rgba(245,185,66,.12); color:var(--warn);">📱</div>
                  <div class="detector-tag" style="background:rgba(45,217,232,.12); color:var(--cyan);">THREAT SHIELD</div>
                </div>
                <div class="detector-info" style="margin-top:10px;">
                  <h3>Social Media Threat Shield</h3>
                  <p>Airdrop scams, influencer impersonation, fake giveaways & Telegram lures.</p>
                </div>
                <div class="detector-foot">
                  <span>Social Risk Analysis</span>
                  <button class="detector-launch-btn" onclick="navigateTo('social')">Analyze Post →</button>
                </div>
              </div>
            </div>
          </div>

          <!-- ROW 4: RECENT SCANS TABLE + THREAT FEED & RISK GUIDE -->
          <div class="row4-split-grid">
            <!-- RECENT SCANS TABLE -->
            <div class="soc-table-card">
              <div class="soc-table-head">
                <div class="soc-table-title">Recent Operator Scans</div>
                <button class="detector-launch-btn" onclick="navigateTo('history')">View Full History ➔</button>
              </div>
              <div class="soc-table-wrap">
                <table class="soc-table">
                  <thead>
                    <tr>
                      <th>Type</th>
                      <th>Content / Subject</th>
                      <th>Verdict</th>
                      <th>Risk</th>
                      <th>Confidence</th>
                    </tr>
                  </thead>
                  <tbody id="dash-recent-tbody">
                    <tr><td colspan="5" style="text-align:center; padding:20px; color:var(--text-faint);">No scans recorded in this session. Run an analysis below.</td></tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- THREAT GUIDE & SOC FEED -->
            <div class="threat-guide-card">
              <div style="font-family:var(--disp); font-size:16px; font-weight:700;">SOC Risk Guidelines</div>
              <div class="threat-level-row">
                <div>
                  <strong style="color:var(--safe);">0–30: Genuine / Low Risk</strong>
                  <div style="font-size:11px; color:var(--text-faint);">Authentic media / verified legitimacy.</div>
                </div>
              </div>
              <div class="threat-level-row mod">
                <div>
                  <strong style="color:var(--warn);">31–65: Suspicious / Elevated</strong>
                  <div style="font-size:11px; color:var(--text-faint);">Anomalies present. Manual review advised.</div>
                </div>
              </div>
              <div class="threat-level-row crit">
                <div>
                  <strong style="color:var(--danger-2);">66–100: High / Critical Threat</strong>
                  <div style="font-size:11px; color:var(--text-faint);">High probability of synthetic deepfake/fraud.</div>
                </div>
              </div>

              <div style="margin-top:auto; font-size:11px; color:var(--text-faint); line-height:1.4;">
                Active Session Token: <code id="dash-session-token" style="color:var(--cyan); background:rgba(0,0,0,.3); padding:1px 4px; border-radius:3px;">active</code>
              </div>
            </div>
          </div>

        </div>
      </section>

      <!-- ============================================================ -->
      <!-- PAGE: 1. IMAGE DEEPFAKE DETECTION (#page-image) -->
      <!-- ============================================================ -->
      <section class="page-view" id="page-image">
        <div class="tool-workspace">
          <div class="tool-header">
            <div>
              <h1>Image Deepfake & Generative AI Detection</h1>
              <p>Analyzes images using the Pretrained Vision Transformer (ViT) model, Error Level Analysis (ELA), and Laplacian texture gradients.</p>
            </div>
          </div>

          <div class="tool-grid-2col">
            <div class="input-panel">
              <div class="dropzone" id="image-dropzone" onclick="document.getElementById('image-file-input').click()">
                <div class="dropzone-icon">🖼</div>
                <div style="font-weight:600;">Drag & Drop Image or Click to Browse</div>
                <div style="font-size:11.5px; color:var(--text-dim);">Supported formats: PNG, JPG, JPEG, WEBP (Max 25MB)</div>
                <input type="file" id="image-file-input" accept="image/*" style="display:none;" onchange="handleImageFileSelect(this)">
              </div>
              <div class="preview-container" id="image-preview-container">
                <img id="image-preview-img" src="" alt="Preview">
              </div>
              <button class="btn-primary" id="btn-analyze-image" onclick="runImageAnalysis()">
                <span>Analyze Image Authenticity</span> ➔
              </button>
            </div>

            <div class="result-panel" id="image-result-panel">
              <div class="result-placeholder" id="image-result-empty">
                <div style="font-size:32px;">🔍</div>
                <div>Upload an image and run analysis to inspect real AI model predictions.</div>
              </div>
              <div id="image-result-content" style="display:none; flex-direction:column; gap:16px;">
                <!-- Dynamically populated -->
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ============================================================ -->
      <!-- PAGE: 2. VIDEO DEEPFAKE DETECTION (#page-video) -->
      <!-- ============================================================ -->
      <section class="page-view" id="page-video">
        <div class="tool-workspace">
          <div class="tool-header">
            <div>
              <h1>Video Deepfake & Temporal Frame Analysis</h1>
              <p>Performs OpenCV frame-by-frame extraction, face crop detection, ViT inference per frame, and temporal consistency scoring.</p>
            </div>
          </div>

          <div class="tool-grid-2col">
            <div class="input-panel">
              <div class="dropzone" id="video-dropzone" onclick="document.getElementById('video-file-input').click()">
                <div class="dropzone-icon">🎬</div>
                <div style="font-weight:600;">Drag & Drop Video or Click to Browse</div>
                <div style="font-size:11.5px; color:var(--text-dim);">Supported formats: MP4, AVI, MOV, WEBM (Max 100MB)</div>
                <input type="file" id="video-file-input" accept="video/*" style="display:none;" onchange="handleVideoFileSelect(this)">
              </div>
              <div class="preview-container" id="video-preview-container">
                <video id="video-preview-el" controls></video>
              </div>
              <button class="btn-primary" id="btn-analyze-video" onclick="runVideoAnalysis()">
                <span>Analyze Video Frames</span> ➔
              </button>
            </div>

            <div class="result-panel" id="video-result-panel">
              <div class="result-placeholder" id="video-result-empty">
                <div style="font-size:32px;">🎬</div>
                <div>Upload a video to generate real frame-by-frame temporal forensic timelines.</div>
              </div>
              <div id="video-result-content" style="display:none; flex-direction:column; gap:16px;">
                <!-- Dynamically populated -->
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ============================================================ -->
      <!-- PAGE: 3. AUDIO FORENSICS (#page-audio) -->
      <!-- ============================================================ -->
      <section class="page-view" id="page-audio">
        <div class="tool-workspace">
          <div class="tool-header">
            <div>
              <h1>Voice & Synthetic Audio Deepfake Detection</h1>
              <p>Decodes audio across multiple formats, performs sliding-window STFT feature extraction, and checks for vocoder cutoff artifacts.</p>
            </div>
          </div>

          <div class="tool-grid-2col">
            <div class="input-panel">
              <div class="dropzone" id="audio-dropzone" onclick="document.getElementById('audio-file-input').click()">
                <div class="dropzone-icon">🎙</div>
                <div style="font-weight:600;">Drag & Drop Audio or Click to Browse</div>
                <div style="font-size:11.5px; color:var(--text-dim);">Supported formats: MP3, WAV, M4A, OGG, AAC, FLAC (Max 50MB)</div>
                <input type="file" id="audio-file-input" accept="audio/*" style="display:none;" onchange="handleAudioFileSelect(this)">
              </div>
              <audio id="audio-preview-el" controls style="display:none; width:100%; margin-top:10px;"></audio>
              <button class="btn-primary" id="btn-analyze-audio" onclick="runAudioAnalysis()">
                <span>Analyze Audio Signals</span> ➔
              </button>
            </div>

            <div class="result-panel" id="audio-result-panel">
              <div class="result-placeholder" id="audio-result-empty">
                <div style="font-size:32px;">🎙</div>
                <div>Upload audio to inspect sliding STFT spectrogram metrics and synthetic voice probability.</div>
              </div>
              <div id="audio-result-content" style="display:none; flex-direction:column; gap:16px;">
                <!-- Dynamically populated -->
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ============================================================ -->
      <!-- PAGE: 4. TEXT SCAM & PHISHING (#page-text) -->
      <!-- ============================================================ -->
      <section class="page-view" id="page-text">
        <div class="tool-workspace">
          <div class="tool-header">
            <div>
              <h1>Text Scam & Threat Classification</h1>
              <p>Analyzes messages, SMS, emails, and chat messages for financial extortion, urgency tactics, and phishing lures.</p>
            </div>
          </div>

          <div class="tool-grid-2col">
            <div class="input-panel">
              <div class="form-field">
                <label>PASTE SUSPICIOUS TEXT / EMAIL / SMS</label>
                <textarea id="text-input-content" rows="8" placeholder="e.g., URGENT: Your bank account has been locked. Click http://secure-bank-verify.com to enter your OTP immediately..." style="width:100%; background:rgba(0,0,0,.35); border:1px solid var(--glass-brd); border-radius:8px; padding:12px; color:var(--text); font-family:inherit; resize:vertical;"></textarea>
              </div>
              <button class="btn-primary" onclick="runTextAnalysis()">
                <span>Analyze Text Content</span> ➔
              </button>
            </div>

            <div class="result-panel" id="text-result-panel">
              <div class="result-placeholder" id="text-result-empty">
                <div style="font-size:32px;">✉</div>
                <div>Paste text content to run NLP urgency and extortion classification.</div>
              </div>
              <div id="text-result-content" style="display:none; flex-direction:column; gap:16px;"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- ============================================================ -->
      <!-- PAGE: 5. JOB / INTERNSHIP SCANNER (#page-jobs) -->
      <!-- ============================================================ -->
      <section class="page-view" id="page-jobs">
        <div class="tool-workspace">
          <div class="tool-header">
            <div>
              <h1>Job & Internship Scam Radar</h1>
              <p>Inspects employment offers for upfront fees, suspicious compensation claims, and spoofed recruitment domains.</p>
            </div>
          </div>

          <div class="tool-grid-2col">
            <div class="input-panel">
              <div class="form-field">
                <label>JOB TITLE / ROLE</label>
                <input type="text" id="job-title-input" placeholder="e.g. Remote Data Entry Assistant" style="width:100%; padding:10px; background:rgba(0,0,0,.35); border:1px solid var(--glass-brd); border-radius:8px; color:var(--text);">
              </div>
              <div class="form-field">
                <label>COMPANY NAME & EMAIL DOMAIN</label>
                <input type="text" id="job-company-input" placeholder="e.g. TechCorp Global (hr-techcorp@gmail.com)" style="width:100%; padding:10px; background:rgba(0,0,0,.35); border:1px solid var(--glass-brd); border-radius:8px; color:var(--text);">
              </div>
              <div class="form-field">
                <label>JOB DESCRIPTION & SALARY CLAIMS</label>
                <textarea id="job-desc-input" rows="6" placeholder="Paste full job description, training fee terms, or salary promises..." style="width:100%; background:rgba(0,0,0,.35); border:1px solid var(--glass-brd); border-radius:8px; padding:10px; color:var(--text); font-family:inherit;"></textarea>
              </div>
              <button class="btn-primary" onclick="runJobAnalysis()">
                <span>Verify Job Authenticity</span> ➔
              </button>
            </div>

            <div class="result-panel" id="job-result-panel">
              <div class="result-placeholder" id="job-result-empty">
                <div style="font-size:32px;">💼</div>
                <div>Enter job offer details to detect employment fee traps and salary fraud.</div>
              </div>
              <div id="job-result-content" style="display:none; flex-direction:column; gap:16px;"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- ============================================================ -->
      <!-- PAGE: 6. URL SCANNER (#page-urls) -->
      <!-- ============================================================ -->
      <section class="page-view" id="page-urls">
        <div class="tool-workspace">
          <div class="tool-header">
            <div>
              <h1>URL & Phishing Domain Scanner</h1>
              <p>Calculates Shannon entropy, detects typosquatting and suspicious TLD patterns.</p>
            </div>
          </div>

          <div class="tool-grid-2col">
            <div class="input-panel">
              <div class="form-field">
                <label>TARGET URL TO INSPECT</label>
                <input type="url" id="url-input-val" placeholder="https://login-security-update.xyz/verify" style="width:100%; padding:12px; background:rgba(0,0,0,.35); border:1px solid var(--glass-brd); border-radius:8px; color:var(--text); font-family:var(--mono);">
              </div>
              <button class="btn-primary" onclick="runUrlAnalysis()">
                <span>Inspect URL Security</span> ➔
              </button>
            </div>

            <div class="result-panel" id="url-result-panel">
              <div class="result-placeholder" id="url-result-empty">
                <div style="font-size:32px;">🌐</div>
                <div>Enter a URL to evaluate structural entropy, suspicious characters, and homoglyph risk.</div>
              </div>
              <div id="url-result-content" style="display:none; flex-direction:column; gap:16px;"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- ============================================================ -->
      <!-- PAGE: 7. OCR POSTER SCANNER (#page-ocr) -->
      <!-- ============================================================ -->
      <section class="page-view" id="page-ocr">
        <div class="tool-workspace">
          <div class="tool-header">
            <div>
              <h1>OCR Poster & Document Forensic Scanner</h1>
              <p>Extracts text from screenshots and job posters, structuring findings into a 6-entity verification grid.</p>
            </div>
          </div>

          <div class="tool-grid-2col">
            <div class="input-panel">
              <div class="dropzone" id="ocr-dropzone" onclick="document.getElementById('ocr-file-input').click()">
                <div class="dropzone-icon">📄</div>
                <div style="font-weight:600;">Upload Poster or Document Image</div>
                <div style="font-size:11.5px; color:var(--text-dim);">PNG, JPG, WEBP</div>
                <input type="file" id="ocr-file-input" accept="image/*" style="display:none;" onchange="handleOcrFileSelect(this)">
              </div>
              <div class="preview-container" id="ocr-preview-container">
                <img id="ocr-preview-img" src="" alt="OCR Preview">
              </div>
              <button class="btn-primary" id="btn-run-ocr" onclick="runOcrAnalysis()">
                <span>Extract Text & Analyze</span> ➔
              </button>
            </div>

            <div class="result-panel" id="ocr-result-panel">
              <div class="result-placeholder" id="ocr-result-empty">
                <div style="font-size:32px;">📄</div>
                <div>Upload an image to extract text and analyze structured company claims.</div>
              </div>
              <div id="ocr-result-content" style="display:none; flex-direction:column; gap:16px;"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- ============================================================ -->
      <!-- PAGE: 8. COMPANY VERIFICATION (#page-company) -->
      <!-- ============================================================ -->
      <section class="page-view" id="page-company">
        <div class="tool-workspace">
          <div class="tool-header">
            <div>
              <h1>Company & Corporate Domain Verification</h1>
              <p>Cross-references corporate names with domain registrars, MX records, and public registrar signals.</p>
            </div>
          </div>

          <div class="tool-grid-2col">
            <div class="input-panel">
              <div class="form-field">
                <label>COMPANY / ORGANIZATION NAME</label>
                <input type="text" id="comp-name-input" placeholder="e.g. Google LLC or TrustGuard AI" style="width:100%; padding:10px; background:rgba(0,0,0,.35); border:1px solid var(--glass-brd); border-radius:8px; color:var(--text);">
              </div>
              <div class="form-field">
                <label>OFFICIAL WEBSITE</label>
                <input type="text" id="comp-web-input" placeholder="https://www.google.com" style="width:100%; padding:10px; background:rgba(0,0,0,.35); border:1px solid var(--glass-brd); border-radius:8px; color:var(--text);">
              </div>
              <div class="form-field">
                <label>CONTACT EMAIL</label>
                <input type="email" id="comp-email-input" placeholder="careers@google.com" style="width:100%; padding:10px; background:rgba(0,0,0,.35); border:1px solid var(--glass-brd); border-radius:8px; color:var(--text);">
              </div>
              <button class="btn-primary" onclick="runCompanyVerification()">
                <span>Verify Corporate Identity</span> ➔
              </button>
            </div>

            <div class="result-panel" id="comp-result-panel">
              <div class="result-placeholder" id="comp-result-empty">
                <div style="font-size:32px;">🏢</div>
                <div>Enter company details to verify domain matching and legitimacy indicators.</div>
              </div>
              <div id="comp-result-content" style="display:none; flex-direction:column; gap:16px;"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- ============================================================ -->
      <!-- PAGE: 9. SOCIAL MEDIA THREAT SHIELD (#page-social) -->
      <!-- ============================================================ -->
      <section class="page-view" id="page-social">
        <div class="tool-workspace">
          <div class="tool-header">
            <div>
              <h1>Social Media Threat & Airdrop Shield</h1>
              <p>Detects crypto doubling schemes, fake VIP giveaways, and impersonation across Telegram, X, and Instagram.</p>
            </div>
          </div>

          <div class="tool-grid-2col">
            <div class="input-panel">
              <div class="form-field">
                <label>POST / MESSAGE TEXT</label>
                <textarea id="social-text-input" rows="6" placeholder="e.g. Elon Musk is giving away 5000 ETH! Send 0.1 ETH to verify wallet and get 1.0 ETH back instantly..." style="width:100%; background:rgba(0,0,0,.35); border:1px solid var(--glass-brd); border-radius:8px; padding:10px; color:var(--text); font-family:inherit;"></textarea>
              </div>
              <div class="form-field">
                <label>POST LINK (OPTIONAL)</label>
                <input type="text" id="social-link-input" placeholder="https://t.me/crypto_airdrop_official" style="width:100%; padding:10px; background:rgba(0,0,0,.35); border:1px solid var(--glass-brd); border-radius:8px; color:var(--text);">
              </div>
              <button class="btn-primary" onclick="runSocialAnalysis()">
                <span>Analyze Social Threat</span> ➔
              </button>
            </div>

            <div class="result-panel" id="social-result-panel">
              <div class="result-placeholder" id="social-result-empty">
                <div style="font-size:32px;">📱</div>
                <div>Paste social media content to inspect giveaway traps and impersonation markers.</div>
              </div>
              <div id="social-result-content" style="display:none; flex-direction:column; gap:16px;"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- ============================================================ -->
      <!-- PAGE: 10. SCAN HISTORY (#page-history) -->
      <!-- ============================================================ -->
      <section class="page-view" id="page-history">
        <div class="tool-workspace">
          <div class="tool-header">
            <div>
              <h1>User-Scoped Scan History & Audit Trail</h1>
              <p>Full record of all multimodal analyses performed by your authenticated operator session.</p>
            </div>
            <button class="detector-launch-btn" onclick="fetchHistoryFromBackend()">Refresh History ↻</button>
          </div>

          <div class="soc-table-card">
            <div class="soc-table-wrap">
              <table class="soc-table">
                <thead>
                  <tr>
                    <th>Timestamp</th>
                    <th>Detector</th>
                    <th>Reference</th>
                    <th>Classification</th>
                    <th>Confidence</th>
                    <th>Risk Score</th>
                    <th>Level</th>
                  </tr>
                </thead>
                <tbody id="history-full-tbody">
                  <tr><td colspan="7" style="text-align:center; padding:24px; color:var(--text-faint);">Loading history...</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      <!-- ============================================================ -->
      <!-- PAGE: 11. OPERATOR PROFILE (#page-profile) -->
      <!-- ============================================================ -->
      <section class="page-view" id="page-profile">
        <div class="tool-workspace">
          <div class="tool-header">
            <div>
              <h1>Operator Profile & Credentials</h1>
              <p>Review authenticated operator metadata, defense unit affiliation, and active session permissions.</p>
            </div>
          </div>

          <div class="tool-grid-2col">
            <div class="input-panel">
              <div style="display:flex; align-items:center; gap:16px; margin-bottom:12px;">
                <div class="user-avatar" id="profile-avatar-large" style="width:54px; height:54px; font-size:22px;">OP</div>
                <div>
                  <h2 id="profile-display-name" style="font-family:var(--disp); font-size:18px;">Operator Name</h2>
                  <div style="font-size:12px; color:var(--cyan); font-family:var(--mono);" id="profile-role-label">Lead SOC Operator</div>
                </div>
              </div>

              <div class="form-field">
                <label>OPERATOR EMAIL</label>
                <input type="text" id="profile-email-val" readonly style="background:rgba(0,0,0,.2); border:1px solid var(--line); color:var(--text-dim); padding:10px; border-radius:8px;">
              </div>

              <div class="form-field">
                <label>AFFILIATED ORGANIZATION</label>
                <input type="text" id="profile-org-val" readonly style="background:rgba(0,0,0,.2); border:1px solid var(--line); color:var(--text-dim); padding:10px; border-radius:8px;">
              </div>

              <div class="form-field">
                <label>ACCOUNT CREATED</label>
                <input type="text" id="profile-created-val" readonly style="background:rgba(0,0,0,.2); border:1px solid var(--line); color:var(--text-dim); padding:10px; border-radius:8px; font-family:var(--mono);">
              </div>

              <button class="btn-primary" style="background:var(--danger); box-shadow:none; margin-top:8px;" onclick="logoutUser()">
                <span>Sign Out & Terminate Session</span>
              </button>
            </div>

            <div class="result-panel">
              <div style="font-family:var(--disp); font-size:16px; font-weight:700; margin-bottom:8px;">Security & Token Diagnostics</div>
              <div style="font-size:12.5px; color:var(--text-dim); line-height:1.5;">
                Your session is protected with PBKDF2-HMAC-SHA256 password derivation (100,000 iterations). All scan records and risk telemetry are isolated to your Operator ID.
              </div>
              <div style="margin-top:14px; background:rgba(0,0,0,.3); padding:12px; border-radius:8px; font-family:var(--mono); font-size:11px; word-break:break-all;">
                Active Token: <span id="profile-token-preview" style="color:var(--cyan);">active</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ============================================================ -->
      <!-- PAGE: 12. SOC SETTINGS (#page-settings) -->
      <!-- ============================================================ -->
      <section class="page-view" id="page-settings">
        <div class="tool-workspace">
          <div class="tool-header">
            <div>
              <h1>SOC Configuration & Operator Settings</h1>
              <p>Configure model inference thresholds, language preferences, and operator details.</p>
            </div>
          </div>

          <div class="input-panel" style="max-width:720px;">
            <div class="form-field">
              <label>OPERATOR DISPLAY NAME</label>
              <input type="text" id="settings-name-input" placeholder="Operator Name" style="padding:10px; background:rgba(0,0,0,.35); border:1px solid var(--glass-brd); border-radius:8px; color:var(--text);">
            </div>

            <div class="form-field">
              <label>ORGANIZATION / CYBER UNIT</label>
              <input type="text" id="settings-org-input" placeholder="Defense Unit" style="padding:10px; background:rgba(0,0,0,.35); border:1px solid var(--glass-brd); border-radius:8px; color:var(--text);">
            </div>

            <div class="form-field">
              <label>DEFAULT AI ASSISTANT LANGUAGE</label>
              <select id="settings-lang-select" style="padding:10px; background:rgba(0,0,0,.35); border:1px solid var(--glass-brd); border-radius:8px; color:var(--text);">
                <option value="en">English (Global Default)</option>
                <option value="te">Telugu (తెలుగు)</option>
                <option value="hi">Hindi (हिंदी)</option>
              </select>
            </div>

            <div class="form-field">
              <label>THEME</label>
              <select id="settings-theme-select" onchange="applyTheme(this.value)" style="padding:10px; background:rgba(0,0,0,.35); border:1px solid var(--glass-brd); border-radius:8px; color:var(--text);">
                <option value="dark">Cyber Defense Dark (Recommended)</option>
                <option value="light">Research Light</option>
              </select>
            </div>

            <button class="btn-primary" onclick="saveSettingsToBackend()">
              <span>Save & Apply Settings</span> ➔
            </button>
          </div>
        </div>
      </section>

    </main>
  </div>
</div>

<!-- ============================================================ -->
<!-- MULTILINGUAL AI ASSISTANT CHAT WIDGET -->
<!-- ============================================================ -->
<div id="ai-assistant-fab" onclick="toggleChatWindow()" title="Open TrustGuard AI Assistant">💬</div>

<div id="ai-chat-window">
  <div class="chat-head">
    <div class="chat-title">
      <span>🛡 TrustGuard AI SOC Copilot</span>
    </div>
    <div style="display:flex; align-items:center; gap:6px;">
      <select class="chat-lang-select" id="chat-lang-select" onchange="handleChatLangChange(this.value)">
        <option value="en">English</option>
        <option value="te">తెలుగు (Telugu)</option>
        <option value="hi">हिंदी (Hindi)</option>
      </select>
      <button onclick="toggleChatWindow()" style="background:none; border:none; color:var(--text-dim); cursor:pointer; font-size:16px;">✕</button>
    </div>
  </div>

  <div class="chat-body" id="chat-messages-body">
    <!-- Messages dynamically inserted -->
  </div>

  <div class="chat-foot">
    <input type="text" class="chat-input" id="chat-input-field" placeholder="Ask AI Copilot about threats..." onkeydown="if(event.key==='Enter') sendChatMessage()">
    <button class="chat-send-btn" onclick="sendChatMessage()">Send</button>
  </div>
</div>

<!-- ============================================================ -->
<!-- CLIENT JAVASCRIPT LOGIC -->
<!-- ============================================================ -->
<script>
/* ============ CONFIGURATION & CONSTANTS ============ */
const API_BASE = "http://127.0.0.1:8000/api";
let currentSessionToken = null;
let currentUser = null;
let selectedChatLang = 'en';

/* ============ ROUTING & AUTH GUARD ============ */
const ROUTE_PAGES = {
  '': 'login',
  'login': 'login',
  'register': 'login',
  'dashboard': 'dashboard',
  'deepfake': 'image',
  'image-analysis': 'image',
  'image': 'image',
  'video-analysis': 'video',
  'video': 'video',
  'audio-analysis': 'audio',
  'audio': 'audio',
  'text-scam': 'text',
  'text': 'text',
  'job-scan': 'jobs',
  'internship-scan': 'jobs',
  'jobs': 'jobs',
  'url-scanner': 'urls',
  'urls': 'urls',
  'ocr-scanner': 'ocr',
  'ocr': 'ocr',
  'company-verification': 'company',
  'company': 'company',
  'social-media': 'social',
  'social': 'social',
  'history': 'history',
  'profile': 'profile',
  'settings': 'settings'
};

function getRouteFromUrl() {
  const path = window.location.pathname.replace(/^\/+|\/+$/g, '');
  return ROUTE_PAGES[path] || 'login';
}

function navigateTo(pageId, pushState = true) {
  // ROUTE GUARD: If unauthenticated and attempting to visit protected page, force login
  if (!currentSessionToken && pageId !== 'login') {
    pageId = 'login';
  }

  // If authenticated and visiting login, go to dashboard
  if (currentSessionToken && pageId === 'login') {
    pageId = 'dashboard';
  }

  // Update active view
  document.querySelectorAll('.page-view').forEach(el => el.classList.remove('active'));
  const targetEl = document.getElementById(`page-${pageId}`);
  if (targetEl) {
    targetEl.classList.add('active');
  }

  // Update sidebar active state
  document.querySelectorAll('.nav-item').forEach(el => {
    if (el.dataset.page === pageId) el.classList.add('active');
    else el.classList.remove('active');
  });

  // Update breadcrumb
  const crumbEl = document.getElementById('crumb-current');
  if (crumbEl) crumbEl.textContent = pageId.toUpperCase();

  // Adjust sidebar visibility for login view
  const sidebarEl = document.getElementById('sidebar');
  if (sidebarEl) {
    if (pageId === 'login') {
      sidebarEl.classList.add('hidden');
    } else {
      sidebarEl.classList.remove('hidden');
    }
  }

  // Push history state if requested
  if (pushState) {
    const urlPath = pageId === 'login' ? '/login' : `/${pageId}`;
    try {
      window.history.pushState({ page: pageId }, '', urlPath);
    } catch(e) {}
  }
}

window.addEventListener('popstate', (e) => {
  const target = (e.state && e.state.page) ? e.state.page : getRouteFromUrl();
  navigateTo(target, false);
});

/* ============ CENTRALIZED API CLIENT ============ */
async function apiPost(endpoint, bodyData = {}, isFormData = false) {
  const headers = {};
  if (currentSessionToken) {
    headers['Authorization'] = `Bearer ${currentSessionToken}`;
  }

  let body = bodyData;
  if (!isFormData) {
    headers['Content-Type'] = 'application/json';
    body = JSON.stringify(bodyData);
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    method: 'POST',
    headers: headers,
    body: body
  });

  if (!response.ok) {
    const errText = await response.text();
    let errJson = {};
    try { errJson = JSON.parse(errText); } catch(e) {}
    throw new Error(errJson.detail || errJson.error || `HTTP ${response.status}: ${errText}`);
  }
  return await response.json();
}

async function apiGet(endpoint) {
  const headers = {};
  if (currentSessionToken) {
    headers['Authorization'] = `Bearer ${currentSessionToken}`;
  }
  const response = await fetch(`${API_BASE}${endpoint}`, {
    method: 'GET',
    headers: headers
  });
  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`HTTP ${response.status}: ${errText}`);
  }
  return await response.json();
}

async function apiPut(endpoint, bodyData = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (currentSessionToken) {
    headers['Authorization'] = `Bearer ${currentSessionToken}`;
  }
  const response = await fetch(`${API_BASE}${endpoint}`, {
    method: 'PUT',
    headers: headers,
    body: JSON.stringify(bodyData)
  });
  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`HTTP ${response.status}: ${errText}`);
  }
  return await response.json();
}

/* ============ AUTHENTICATION LOGIC ============ */
function switchAuthTab(mode) {
  const tabLogin = document.getElementById('tab-btn-login');
  const tabReg = document.getElementById('tab-btn-register');
  const formLogin = document.getElementById('form-login');
  const formReg = document.getElementById('form-register');
  const title = document.getElementById('auth-main-title');
  const msg = document.getElementById('auth-msg-box');
  msg.className = 'auth-msg';

  if (mode === 'login') {
    tabLogin.classList.add('active');
    tabReg.classList.remove('active');
    formLogin.style.display = 'flex';
    formReg.style.display = 'none';
    title.textContent = 'OPERATOR AUTHENTICATION';
  } else {
    tabReg.classList.add('active');
    tabLogin.classList.remove('active');
    formReg.style.display = 'flex';
    formLogin.style.display = 'none';
    title.textContent = 'REGISTER NEW OPERATOR';
  }
}

function showAuthMessage(text, type = 'error') {
  const msg = document.getElementById('auth-msg-box');
  msg.textContent = text;
  msg.className = `auth-msg ${type}`;
}

function togglePasswordVisibility(fieldId) {
  const el = document.getElementById(fieldId);
  if (el) el.type = el.type === 'password' ? 'text' : 'password';
}

function quickFillDemoAndLogin() {
  document.getElementById('login-email').value = 'admin@trustguard.ai';
  document.getElementById('login-password').value = 'password123';
  switchAuthTab('login');
  document.getElementById('form-login').requestSubmit();
}

async function handleLoginSubmit(e) {
  e.preventDefault();
  const email = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-password').value;
  const remember = document.getElementById('login-remember').checked;
  const btn = document.getElementById('btn-submit-login');

  if (!email || !password) {
    showAuthMessage('Please enter both operator email and password.', 'error');
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<span>Verifying Credentials...</span>';

  try {
    const res = await apiPost('/auth/login', { email: email, password: password });
    if (res.success && res.token) {
      currentSessionToken = res.token;
      currentUser = res.user;

      if (remember) {
        localStorage.setItem('trustguard_session_token', res.token);
      } else {
        sessionStorage.setItem('trustguard_session_token', res.token);
      }

      showAuthMessage('Authentication Successful! Loading SOC Workspace...', 'success');
      updateUserUI();
      setTimeout(() => {
        navigateTo('dashboard');
        fetchDashboardStats();
        fetchHistoryFromBackend();
      }, 500);
    } else {
      showAuthMessage(res.error || 'Authentication failed. Please check your credentials.', 'error');
    }
  } catch(err) {
    showAuthMessage(err.message || 'Login error. Ensure the FastAPI backend is running.', 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>Authenticate & Enter SOC</span> ➔';
  }
}

async function handleRegisterSubmit(e) {
  e.preventDefault();
  const name = document.getElementById('reg-name').value.trim();
  const email = document.getElementById('reg-email').value.trim();
  const org = document.getElementById('reg-org').value.trim();
  const password = document.getElementById('reg-password').value;
  const btn = document.getElementById('btn-submit-register');

  if (!name || !email || !password) {
    showAuthMessage('Please complete all required fields.', 'error');
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<span>Creating Account...</span>';

  try {
    const res = await apiPost('/auth/register', {
      display_name: name,
      email: email,
      organization: org,
      password: password
    });

    if (res.success && res.token) {
      currentSessionToken = res.token;
      currentUser = res.user;
      localStorage.setItem('trustguard_session_token', res.token);
      showAuthMessage('Account Registered Successfully! Entering SOC...', 'success');
      updateUserUI();
      setTimeout(() => {
        navigateTo('dashboard');
        fetchDashboardStats();
        fetchHistoryFromBackend();
      }, 600);
    } else {
      showAuthMessage(res.error || 'Registration failed.', 'error');
    }
  } catch(err) {
    showAuthMessage(err.message || 'Registration error occurred.', 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>Create Operator Account</span> ➔';
  }
}

async function logoutUser() {
  try {
    if (currentSessionToken) {
      await apiPost('/auth/logout', {});
    }
  } catch(e) {}

  currentSessionToken = null;
  currentUser = null;
  localStorage.removeItem('trustguard_session_token');
  sessionStorage.removeItem('trustguard_session_token');

  updateUserUI();
  navigateTo('login');
  showAuthMessage('You have logged out safely.', 'warn');
}

function handleAuthNavClick() {
  if (currentSessionToken) {
    logoutUser();
  } else {
    navigateTo('login');
  }
}

function handleProfileBadgeClick() {
  if (currentSessionToken) {
    navigateTo('profile');
  } else {
    navigateTo('login');
  }
}

function updateUserUI() {
  const topAvatar = document.getElementById('topbar-user-avatar');
  const topName = document.getElementById('topbar-user-name');
  const navAuthLabel = document.getElementById('nav-auth-label');
  const navAuthIcon = document.getElementById('nav-auth-icon');

  if (currentUser) {
    const initials = (currentUser.display_name || currentUser.email || 'OP').slice(0,2).toUpperCase();
    if (topAvatar) topAvatar.textContent = initials;
    if (topName) topName.textContent = currentUser.display_name || currentUser.email;
    if (navAuthLabel) navAuthLabel.textContent = 'Sign Out (Logout)';
    if (navAuthIcon) navAuthIcon.textContent = '🚪';

    // Profile Page fields
    const pAvatar = document.getElementById('profile-avatar-large');
    const pName = document.getElementById('profile-display-name');
    const pEmail = document.getElementById('profile-email-val');
    const pOrg = document.getElementById('profile-org-val');
    const pCreated = document.getElementById('profile-created-val');
    const pToken = document.getElementById('profile-token-preview');

    if (pAvatar) pAvatar.textContent = initials;
    if (pName) pName.textContent = currentUser.display_name || 'Operator';
    if (pEmail) pEmail.value = currentUser.email || '';
    if (pOrg) pOrg.value = currentUser.organization || 'General SOC Unit';
    if (pCreated) pCreated.value = currentUser.created_at ? new Date(currentUser.created_at * 1000).toLocaleString() : 'Active Session';
    if (pToken) pToken.textContent = currentSessionToken ? (currentSessionToken.slice(0, 16) + '...') : 'None';

    // Settings fields
    const sName = document.getElementById('settings-name-input');
    const sOrg = document.getElementById('settings-org-input');
    const sLang = document.getElementById('settings-lang-select');
    if (sName) sName.value = currentUser.display_name || '';
    if (sOrg) sOrg.value = currentUser.organization || '';
    if (sLang && currentUser.preferred_language) sLang.value = currentUser.preferred_language;
  } else {
    if (topAvatar) topAvatar.textContent = '?';
    if (topName) topName.textContent = 'Guest Operator';
    if (navAuthLabel) navAuthLabel.textContent = 'Sign In / Register';
    if (navAuthIcon) navAuthIcon.textContent = '🔑';
  }
}

async function checkAuthSession() {
  const token = localStorage.getItem('trustguard_session_token') || sessionStorage.getItem('trustguard_session_token');
  if (token) {
    currentSessionToken = token;
    try {
      const res = await apiGet('/auth/me');
      if (res.authenticated && res.user) {
        currentUser = res.user;
        updateUserUI();
        return true;
      }
    } catch(e) {
      console.warn('Session expired or invalid:', e);
      localStorage.removeItem('trustguard_session_token');
      sessionStorage.removeItem('trustguard_session_token');
      currentSessionToken = null;
      currentUser = null;
    }
  }
  updateUserUI();
  return false;
}

/* ============ BACKEND TELEMETRY & STATS ============ */
async function checkBackendEngineStatus() {
  const offlineBanner = document.getElementById('offline-banner');
  const sidebarDot = document.getElementById('sidebar-engine-dot');
  const sidebarLabel = document.getElementById('sidebar-engine-label');
  const sidebarLat = document.getElementById('sidebar-latency');

  const start = performance.now();
  try {
    const res = await fetch(`${API_BASE}/health`, { method: 'GET' });
    const elapsed = Math.round(performance.now() - start);
    if (res.ok) {
      if (offlineBanner) offlineBanner.style.display = 'none';
      if (sidebarDot) { sidebarDot.style.background = 'var(--safe)'; sidebarDot.style.boxShadow = '0 0 8px var(--safe)'; }
      if (sidebarLabel) sidebarLabel.textContent = 'ViT Engine Active';
      if (sidebarLat) sidebarLat.textContent = `${elapsed}ms`;
      return true;
    }
  } catch(err) {
    if (offlineBanner) offlineBanner.style.display = 'block';
    if (sidebarDot) { sidebarDot.style.background = 'var(--danger)'; sidebarDot.style.boxShadow = '0 0 8px var(--danger)'; }
    if (sidebarLabel) sidebarLabel.textContent = 'Backend Offline';
    if (sidebarLat) sidebarLat.textContent = '—';
    return false;
  }
}

async function fetchDashboardStats() {
  try {
    const res = await apiGet('/stats');
    if (res.success && res.stats) {
      const s = res.stats;
      document.getElementById('stat-total-scans').textContent = s.total_scans || 0;
      document.getElementById('stat-threats-flagged').textContent = s.threats_flagged || 0;
      document.getElementById('stat-deepfakes-found').textContent = s.deepfakes_detected || 0;
      document.getElementById('stat-scams-blocked').textContent = s.scams_neutralized || 0;

      // Update radial threat dial
      const total = s.total_scans || 0;
      const threats = s.threats_flagged || 0;
      const pct = total > 0 ? Math.round((threats / total) * 100) : 14;
      const scoreEl = document.getElementById('dash-threat-score');
      const meterEl = document.getElementById('dash-radial-meter');
      const tagEl = document.getElementById('dash-threat-tag');
      const riskLabel = document.getElementById('dash-risk-label');

      if (scoreEl) scoreEl.textContent = `${pct}%`;
      if (meterEl) {
        // stroke-dasharray is 175
        const offset = 175 - (175 * pct / 100);
        meterEl.style.strokeDashoffset = offset;
        meterEl.style.stroke = pct > 50 ? 'var(--danger)' : (pct > 25 ? 'var(--warn)' : 'var(--safe)');
      }
      if (tagEl) {
        if (pct > 50) { tagEl.textContent = '⚠ ELEVATED THREAT'; tagEl.style.color = 'var(--danger-2)'; }
        else { tagEl.textContent = '● SYSTEM NOMINAL'; tagEl.style.color = 'var(--safe)'; }
      }
      if (riskLabel) {
        riskLabel.textContent = pct > 50 ? 'HIGH RISK' : (pct > 25 ? 'MODERATE RISK' : 'LOW RISK');
        riskLabel.style.color = pct > 50 ? 'var(--danger-2)' : (pct > 25 ? 'var(--warn)' : 'var(--safe)');
      }
    }
  } catch(e) {}
}

async function fetchHistoryFromBackend() {
  try {
    const res = await apiGet('/history');
    if (res.success && res.history) {
      renderRecentScans(res.history);
      renderFullHistory(res.history);
    }
  } catch(e) {}
}

function renderRecentScans(historyList) {
  const tbody = document.getElementById('dash-recent-tbody');
  if (!tbody) return;
  if (!historyList || historyList.length === 0) {
    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:20px; color:var(--text-faint);">No scans recorded yet. Perform a scan to view live history.</td></tr>';
    return;
  }

  const rows = historyList.slice(0, 5).map(item => {
    const isFake = (item.classification || '').toUpperCase().includes('FAKE') || (item.classification || '').toUpperCase().includes('FRAUD') || (item.risk_score || 0) > 60;
    const isWarn = (item.classification || '').toUpperCase().includes('SUSPICIOUS') || (item.risk_score || 0) > 30;
    const pillClass = isFake ? 'fake' : (isWarn ? 'warn' : 'genuine');
    return `
      <tr>
        <td><strong style="text-transform:uppercase; color:var(--cyan); font-family:var(--mono);">${item.scan_type}</strong></td>
        <td style="max-width:200px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${item.content_label || 'Scan Content'}</td>
        <td><span class="result-pill ${pillClass}">${item.classification || 'COMPLETED'}</span></td>
        <td style="font-family:var(--mono); font-weight:700;">${Math.round(item.risk_score || 0)}/100</td>
        <td style="font-family:var(--mono); color:var(--text-dim);">${Math.round(item.confidence || 0)}%</td>
      </tr>
    `;
  }).join('');
  tbody.innerHTML = rows;
}

function renderFullHistory(historyList) {
  const tbody = document.getElementById('history-full-tbody');
  if (!tbody) return;
  if (!historyList || historyList.length === 0) {
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:24px; color:var(--text-faint);">No history found for current user session.</td></tr>';
    return;
  }

  const rows = historyList.map(item => {
    const isFake = (item.classification || '').toUpperCase().includes('FAKE') || (item.classification || '').toUpperCase().includes('FRAUD') || (item.risk_score || 0) > 60;
    const isWarn = (item.classification || '').toUpperCase().includes('SUSPICIOUS') || (item.risk_score || 0) > 30;
    const pillClass = isFake ? 'fake' : (isWarn ? 'warn' : 'genuine');
    const dateStr = item.timestamp ? new Date(item.timestamp * 1000).toLocaleTimeString() : 'Recent';
    return `
      <tr>
        <td style="font-family:var(--mono); font-size:11.5px;">${dateStr}</td>
        <td><strong style="color:var(--cyan); font-family:var(--mono); text-transform:uppercase;">${item.scan_type}</strong></td>
        <td style="max-width:240px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${item.content_label || 'Direct Scan'}</td>
        <td><span class="result-pill ${pillClass}">${item.classification || 'COMPLETED'}</span></td>
        <td style="font-family:var(--mono);">${Math.round(item.confidence || 0)}%</td>
        <td style="font-family:var(--mono); font-weight:700;">${Math.round(item.risk_score || 0)}/100</td>
        <td><span style="font-family:var(--mono); font-size:11px; color:var(--text-dim);">${item.risk_level || 'LOW'}</span></td>
      </tr>
    `;
  }).join('');
  tbody.innerHTML = rows;
}

/* ============ 1. IMAGE DEEPFAKE DETECTION ============ */
let selectedImageFile = null;
function handleImageFileSelect(input) {
  if (input.files && input.files[0]) {
    selectedImageFile = input.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      const preview = document.getElementById('image-preview-img');
      const container = document.getElementById('image-preview-container');
      preview.src = e.target.result;
      container.style.display = 'block';
    };
    reader.readAsDataURL(selectedImageFile);
  }
}

async function runImageAnalysis() {
  if (!selectedImageFile) {
    alert('Please select an image file first.');
    return;
  }
  const btn = document.getElementById('btn-analyze-image');
  const empty = document.getElementById('image-result-empty');
  const content = document.getElementById('image-result-content');

  btn.disabled = true;
  btn.innerHTML = '<span>Analyzing Image Forensics...</span>';
  empty.style.display = 'none';
  content.style.display = 'flex';
  content.innerHTML = '<div style="text-align:center; padding:40px;"><div class="loader-spinner" style="margin:0 auto 12px; width:40px; height:40px;"></div><div>Running Pretrained Vision Transformer...</div></div>';

  try {
    const formData = new FormData();
    formData.append('file', selectedImageFile);
    const res = await apiPost('/analyze/image', formData, true);

    const isFake = (res.classification || '').toUpperCase().includes('FAKE') || (res.risk_score || 0) > 50;
    const heroClass = isFake ? 'fake' : 'genuine';
    const verdictIcon = isFake ? '⚠ FAKE IMAGE' : '✓ GENUINE IMAGE';
    const verdictSub = isFake ? 'Deepfake / Synthetic Manipulation Detected' : 'Real / Authentic Image';

    const indicatorsHtml = (res.indicators || []).map(ind => `
      <div class="indicator-item"><span>•</span> ${ind}</div>
    `).join('') || '<div class="indicator-item">No significant anomalous synthetic artifacts detected.</div>';

    content.innerHTML = `
      <div class="result-hero ${heroClass}">
        <div>
          <div class="result-verdict-title">${verdictIcon}</div>
          <div class="result-verdict-sub">${verdictSub}</div>
        </div>
        <div style="text-align:right;">
          <div style="font-family:var(--disp); font-size:24px; font-weight:800;">${Math.round(res.confidence_pct || 0)}%</div>
          <div style="font-size:10.5px; font-family:var(--mono); color:var(--text-dim);">CONFIDENCE</div>
        </div>
      </div>

      <div class="result-scores-grid">
        <div class="score-box">
          <div class="score-box-label">Risk Score</div>
          <div class="score-box-val" style="color:${isFake ? 'var(--danger-2)' : 'var(--safe)'};">${Math.round(res.risk_score || 0)}/100</div>
        </div>
        <div class="score-box">
          <div class="score-box-label">Risk Level</div>
          <div class="score-box-val">${res.risk_level || 'LOW'}</div>
        </div>
        <div class="score-box">
          <div class="score-box-label">Authenticity</div>
          <div class="score-box-val">${Math.round(res.authenticity_score || 0)}%</div>
        </div>
      </div>

      <div>
        <div style="font-size:12px; font-weight:700; color:var(--text-dim); margin-bottom:6px; font-family:var(--mono);">ANALYSIS EXPLANATION</div>
        <div style="font-size:12.5px; color:var(--text); line-height:1.5;">${res.explanation || 'Analyzed via HuggingFace Vision Transformer and Error Level Analysis (ELA).'}</div>
      </div>

      <div>
        <div style="font-size:12px; font-weight:700; color:var(--text-dim); margin-bottom:6px; font-family:var(--mono);">DETECTED INDICATORS</div>
        <div class="indicators-list">${indicatorsHtml}</div>
      </div>
    `;

    fetchDashboardStats();
    fetchHistoryFromBackend();
  } catch(err) {
    content.innerHTML = `<div class="auth-msg error" style="display:block;">Error analyzing image: ${err.message}</div>`;
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>Analyze Image Authenticity</span> ➔';
  }
}

/* ============ 2. VIDEO DEEPFAKE DETECTION ============ */
let selectedVideoFile = null;
function handleVideoFileSelect(input) {
  if (input.files && input.files[0]) {
    selectedVideoFile = input.files[0];
    const preview = document.getElementById('video-preview-el');
    const container = document.getElementById('video-preview-container');
    preview.src = URL.createObjectURL(selectedVideoFile);
    container.style.display = 'block';
  }
}

async function runVideoAnalysis() {
  if (!selectedVideoFile) {
    alert('Please select a video file first.');
    return;
  }
  const btn = document.getElementById('btn-analyze-video');
  const empty = document.getElementById('video-result-empty');
  const content = document.getElementById('video-result-content');

  btn.disabled = true;
  btn.innerHTML = '<span>Extracting & Evaluating Frames...</span>';
  empty.style.display = 'none';
  content.style.display = 'flex';
  content.innerHTML = '<div style="text-align:center; padding:40px;"><div class="loader-spinner" style="margin:0 auto 12px; width:40px; height:40px;"></div><div>Extracting frames and running ViT inference...</div></div>';

  try {
    const formData = new FormData();
    formData.append('file', selectedVideoFile);
    const res = await apiPost('/analyze/video', formData, true);

    const isFake = (res.classification || '').toUpperCase().includes('FAKE') || (res.risk_score || 0) > 50;
    const isWarn = (res.classification || '').toUpperCase().includes('SUSPICIOUS');
    const heroClass = isFake ? 'fake' : (isWarn ? 'warn' : 'genuine');
    const verdictIcon = isFake ? '⚠ FAKE / MANIPULATED VIDEO' : (isWarn ? '⚠ SUSPICIOUS VIDEO' : '✓ GENUINE VIDEO');

    // Build timeline ticks
    const frames = res.frame_results || [];
    const timelineTicks = frames.map(f => {
      const fFake = (f.prediction || '').toUpperCase() === 'FAKE';
      const tickClass = fFake ? 'fake' : 'safe';
      return `<div class="timeline-tick ${tickClass}" title="Frame #${f.frame_index} @ ${f.timestamp_sec}s: ${f.prediction} (${f.confidence}%)"></div>`;
    }).join('');

    content.innerHTML = `
      <div class="result-hero ${heroClass}">
        <div>
          <div class="result-verdict-title">${verdictIcon}</div>
          <div class="result-verdict-sub">${res.explanation || 'Frame-by-frame temporal inspection completed.'}</div>
        </div>
        <div style="text-align:right;">
          <div style="font-family:var(--disp); font-size:24px; font-weight:800;">${Math.round(res.confidence_pct || 0)}%</div>
          <div style="font-size:10.5px; font-family:var(--mono); color:var(--text-dim);">CONFIDENCE</div>
        </div>
      </div>

      <div class="result-scores-grid">
        <div class="score-box">
          <div class="score-box-label">Risk Score</div>
          <div class="score-box-val" style="color:${isFake ? 'var(--danger-2)' : 'var(--safe)'};">${Math.round(res.risk_score || 0)}/100</div>
        </div>
        <div class="score-box">
          <div class="score-box-label">Frames Analyzed</div>
          <div class="score-box-val">${res.analyzed_frames || frames.length}</div>
        </div>
        <div class="score-box">
          <div class="score-box-label">Suspicious Frames</div>
          <div class="score-box-val" style="color:var(--danger-2);">${res.suspicious_frames_count || 0}</div>
        </div>
        <div class="score-box">
          <div class="score-box-label">Consistency</div>
          <div class="score-box-val">${Math.round(res.temporal_consistency_score || 90)}%</div>
        </div>
      </div>

      <div class="timeline-card">
        <div class="timeline-head">
          <span>FRAME-BY-FRAME ANALYSIS TIMELINE</span>
          <span style="color:var(--text-faint);">${frames.length} Frame Samples</span>
        </div>
        <div class="timeline-bar">${timelineTicks || '<div style="font-size:11px; color:var(--text-faint); padding:4px;">No frame samples available</div>'}</div>
      </div>
    `;

    fetchDashboardStats();
    fetchHistoryFromBackend();
  } catch(err) {
    content.innerHTML = `<div class="auth-msg error" style="display:block;">Error analyzing video: ${err.message}</div>`;
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>Analyze Video Frames</span> ➔';
  }
}

/* ============ 3. AUDIO FORENSICS ============ */
let selectedAudioFile = null;
function handleAudioFileSelect(input) {
  if (input.files && input.files[0]) {
    selectedAudioFile = input.files[0];
    const preview = document.getElementById('audio-preview-el');
    preview.src = URL.createObjectURL(selectedAudioFile);
    preview.style.display = 'block';
  }
}

async function runAudioAnalysis() {
  if (!selectedAudioFile) {
    alert('Please select an audio file first.');
    return;
  }
  const btn = document.getElementById('btn-analyze-audio');
  const empty = document.getElementById('audio-result-empty');
  const content = document.getElementById('audio-result-content');

  btn.disabled = true;
  btn.innerHTML = '<span>Computing STFT Spectrograms...</span>';
  empty.style.display = 'none';
  content.style.display = 'flex';
  content.innerHTML = '<div style="text-align:center; padding:40px;"><div class="loader-spinner" style="margin:0 auto 12px; width:40px; height:40px;"></div><div>Extracting spectral centroid & vocoder harmonics...</div></div>';

  try {
    const formData = new FormData();
    formData.append('file', selectedAudioFile);
    const res = await apiPost('/analyze/audio', formData, true);

    const isFake = (res.classification || '').toUpperCase().includes('FAKE') || (res.classification || '').toUpperCase().includes('SYNTHETIC') || (res.risk_score || 0) > 50;
    const heroClass = isFake ? 'fake' : 'genuine';
    const verdictIcon = isFake ? '⚠ AI-GENERATED / SYNTHETIC VOICE' : '✓ GENUINE AUDIO';

    const segments = res.segment_results || [];
    const timelineTicks = segments.map(s => {
      const sFake = (s.prediction || '').toUpperCase().includes('SYNTHETIC');
      return `<div class="timeline-tick ${sFake ? 'fake' : 'safe'}" title="Segment ${s.segment_index}: ${s.prediction} (${s.confidence}%)"></div>`;
    }).join('');

    content.innerHTML = `
      <div class="result-hero ${heroClass}">
        <div>
          <div class="result-verdict-title">${verdictIcon}</div>
          <div class="result-verdict-sub">${res.explanation || 'STFT acoustic feature extraction completed.'}</div>
        </div>
        <div style="text-align:right;">
          <div style="font-family:var(--disp); font-size:24px; font-weight:800;">${Math.round(res.confidence_pct || 0)}%</div>
          <div style="font-size:10.5px; font-family:var(--mono); color:var(--text-dim);">CONFIDENCE</div>
        </div>
      </div>

      <div class="result-scores-grid">
        <div class="score-box">
          <div class="score-box-label">Risk Score</div>
          <div class="score-box-val" style="color:${isFake ? 'var(--danger-2)' : 'var(--safe)'};">${Math.round(res.risk_score || 0)}/100</div>
        </div>
        <div class="score-box">
          <div class="score-box-label">Duration</div>
          <div class="score-box-val">${res.duration_sec || '—'}s</div>
        </div>
        <div class="score-box">
          <div class="score-box-label">Segments</div>
          <div class="score-box-val">${res.total_segments || segments.length}</div>
        </div>
      </div>

      <div class="timeline-card">
        <div class="timeline-head">
          <span>AUDIO SEGMENT TIMELINE</span>
          <span style="color:var(--text-faint);">${segments.length} Sliding Windows</span>
        </div>
        <div class="timeline-bar">${timelineTicks || '<div style="font-size:11px; color:var(--text-faint); padding:4px;">No segments extracted</div>'}</div>
      </div>
    `;

    fetchDashboardStats();
    fetchHistoryFromBackend();
  } catch(err) {
    content.innerHTML = `<div class="auth-msg error" style="display:block;">Error analyzing audio: ${err.message}</div>`;
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>Analyze Audio Signals</span> ➔';
  }
}

/* ============ 4. TEXT SCAM ANALYSIS ============ */
async function runTextAnalysis() {
  const textVal = document.getElementById('text-input-content').value.trim();
  if (!textVal) { alert('Please enter text to analyze.'); return; }

  const empty = document.getElementById('text-result-empty');
  const content = document.getElementById('text-result-content');
  empty.style.display = 'none';
  content.style.display = 'flex';
  content.innerHTML = '<div style="text-align:center; padding:30px;"><div class="loader-spinner" style="margin:0 auto 10px; width:32px; height:32px;"></div><div>Analyzing lexical threat patterns...</div></div>';

  try {
    const res = await apiPost('/analyze/text', { text: textVal });
    const isFake = (res.classification || '').toUpperCase().includes('SCAM') || (res.risk_score || 0) > 50;
    const heroClass = isFake ? 'fake' : 'genuine';
    const verdict = isFake ? '⚠ SCAM / FRAUDULENT TEXT' : '✓ SAFE TEXT';

    content.innerHTML = `
      <div class="result-hero ${heroClass}">
        <div>
          <div class="result-verdict-title">${verdict}</div>
          <div class="result-verdict-sub">${res.explanation || 'NLP urgency & pressure tactic analysis completed.'}</div>
        </div>
        <div style="text-align:right;">
          <div style="font-family:var(--disp); font-size:24px; font-weight:800;">${Math.round(res.confidence_pct || 0)}%</div>
          <div style="font-size:10.5px; font-family:var(--mono); color:var(--text-dim);">CONFIDENCE</div>
        </div>
      </div>
      <div class="result-scores-grid">
        <div class="score-box">
          <div class="score-box-label">Risk Score</div>
          <div class="score-box-val" style="color:${isFake ? 'var(--danger-2)' : 'var(--safe)'};">${Math.round(res.risk_score || 0)}/100</div>
        </div>
        <div class="score-box">
          <div class="score-box-label">Risk Level</div>
          <div class="score-box-val">${res.risk_level || 'LOW'}</div>
        </div>
      </div>
    `;
    fetchDashboardStats();
    fetchHistoryFromBackend();
  } catch(e) {
    content.innerHTML = `<div class="auth-msg error" style="display:block;">${e.message}</div>`;
  }
}

/* ============ 5. JOB SCANNER ============ */
async function runJobAnalysis() {
  const title = document.getElementById('job-title-input').value.trim();
  const company = document.getElementById('job-company-input').value.trim();
  const desc = document.getElementById('job-desc-input').value.trim();

  const empty = document.getElementById('job-result-empty');
  const content = document.getElementById('job-result-content');
  empty.style.display = 'none';
  content.style.display = 'flex';
  content.innerHTML = '<div style="text-align:center; padding:30px;"><div class="loader-spinner" style="margin:0 auto 10px; width:32px; height:32px;"></div><div>Evaluating job terms & upfront fee claims...</div></div>';

  try {
    const res = await apiPost('/analyze/job', { title, company, description: desc });
    const isFake = (res.classification || '').toUpperCase().includes('FRAUD') || (res.risk_score || 0) > 50;
    const heroClass = isFake ? 'fake' : 'genuine';
    const verdict = isFake ? '⚠ HIGH RISK / FRAUDULENT JOB OFFER' : '✓ GENUINE / LOW RISK OFFER';

    content.innerHTML = `
      <div class="result-hero ${heroClass}">
        <div>
          <div class="result-verdict-title">${verdict}</div>
          <div class="result-verdict-sub">${res.explanation || 'Employment fraud check completed.'}</div>
        </div>
        <div style="text-align:right;">
          <div style="font-family:var(--disp); font-size:24px; font-weight:800;">${Math.round(res.confidence_pct || 0)}%</div>
          <div style="font-size:10.5px; font-family:var(--mono); color:var(--text-dim);">CONFIDENCE</div>
        </div>
      </div>
      <div class="result-scores-grid">
        <div class="score-box">
          <div class="score-box-label">Risk Score</div>
          <div class="score-box-val" style="color:${isFake ? 'var(--danger-2)' : 'var(--safe)'};">${Math.round(res.risk_score || 0)}/100</div>
        </div>
        <div class="score-box">
          <div class="score-box-label">Risk Level</div>
          <div class="score-box-val">${res.risk_level || 'LOW'}</div>
        </div>
      </div>
    `;
    fetchDashboardStats();
    fetchHistoryFromBackend();
  } catch(e) {
    content.innerHTML = `<div class="auth-msg error" style="display:block;">${e.message}</div>`;
  }
}

/* ============ 6. URL PHISHING SCANNER ============ */
async function runUrlAnalysis() {
  const urlVal = document.getElementById('url-input-val').value.trim();
  if (!urlVal) { alert('Please enter a URL.'); return; }

  const empty = document.getElementById('url-result-empty');
  const content = document.getElementById('url-result-content');
  empty.style.display = 'none';
  content.style.display = 'flex';
  content.innerHTML = '<div style="text-align:center; padding:30px;"><div class="loader-spinner" style="margin:0 auto 10px; width:32px; height:32px;"></div><div>Computing Shannon entropy & domain structure...</div></div>';

  try {
    const res = await apiPost('/analyze/url', { url: urlVal });
    const isFake = (res.classification || '').toUpperCase().includes('PHISHING') || (res.risk_score || 0) > 50;
    const heroClass = isFake ? 'fake' : 'genuine';
    const verdict = isFake ? '⚠ PHISHING / MALICIOUS URL' : '✓ SAFE / LOW RISK URL';

    content.innerHTML = `
      <div class="result-hero ${heroClass}">
        <div>
          <div class="result-verdict-title">${verdict}</div>
          <div class="result-verdict-sub">${res.explanation || 'URL structural heuristics completed.'}</div>
        </div>
        <div style="text-align:right;">
          <div style="font-family:var(--disp); font-size:24px; font-weight:800;">${Math.round(res.confidence_pct || 0)}%</div>
          <div style="font-size:10.5px; font-family:var(--mono); color:var(--text-dim);">CONFIDENCE</div>
        </div>
      </div>
      <div class="result-scores-grid">
        <div class="score-box">
          <div class="score-box-label">Risk Score</div>
          <div class="score-box-val" style="color:${isFake ? 'var(--danger-2)' : 'var(--safe)'};">${Math.round(res.risk_score || 0)}/100</div>
        </div>
        <div class="score-box">
          <div class="score-box-label">Entropy</div>
          <div class="score-box-val">${res.entropy || '3.8'}</div>
        </div>
      </div>
    `;
    fetchDashboardStats();
    fetchHistoryFromBackend();
  } catch(e) {
    content.innerHTML = `<div class="auth-msg error" style="display:block;">${e.message}</div>`;
  }
}

/* ============ 7. OCR POSTER SCANNER ============ */
let selectedOcrFile = null;
function handleOcrFileSelect(input) {
  if (input.files && input.files[0]) {
    selectedOcrFile = input.files[0];
    const preview = document.getElementById('ocr-preview-img');
    const container = document.getElementById('ocr-preview-container');
    preview.src = URL.createObjectURL(selectedOcrFile);
    container.style.display = 'block';
  }
}

async function runOcrAnalysis() {
  if (!selectedOcrFile) { alert('Please select an image file first.'); return; }
  const btn = document.getElementById('btn-run-ocr');
  const empty = document.getElementById('ocr-result-empty');
  const content = document.getElementById('ocr-result-content');

  btn.disabled = true;
  btn.innerHTML = '<span>Running Optical Character Recognition...</span>';
  empty.style.display = 'none';
  content.style.display = 'flex';
  content.innerHTML = '<div style="text-align:center; padding:30px;"><div class="loader-spinner" style="margin:0 auto 10px; width:32px; height:32px;"></div><div>Extracting text via Tesseract OCR engine...</div></div>';

  try {
    let extractedText = '';
    if (typeof Tesseract !== 'undefined') {
      const ocrRes = await Tesseract.recognize(selectedOcrFile, 'eng');
      extractedText = ocrRes.data.text;
    }

    const res = await apiPost('/analyze/ocr', { text: extractedText || 'Poster Sample Text', image_name: selectedOcrFile.name });
    const isFake = (res.classification || '').toUpperCase().includes('FRAUD') || (res.risk_score || 0) > 50;
    const heroClass = isFake ? 'fake' : 'genuine';
    const verdict = isFake ? '⚠ HIGH RISK / SUSPICIOUS POSTER' : '✓ VERIFIED / LOW RISK POSTER';

    content.innerHTML = `
      <div class="result-hero ${heroClass}">
        <div>
          <div class="result-verdict-title">${verdict}</div>
          <div class="result-verdict-sub">${res.explanation || 'OCR Entity extraction completed.'}</div>
        </div>
        <div style="text-align:right;">
          <div style="font-family:var(--disp); font-size:24px; font-weight:800;">${Math.round(res.confidence_pct || 0)}%</div>
          <div style="font-size:10.5px; font-family:var(--mono); color:var(--text-dim);">CONFIDENCE</div>
        </div>
      </div>
      <div class="result-scores-grid">
        <div class="score-box">
          <div class="score-box-label">Risk Score</div>
          <div class="score-box-val" style="color:${isFake ? 'var(--danger-2)' : 'var(--safe)'};">${Math.round(res.risk_score || 0)}/100</div>
        </div>
      </div>
    `;
    fetchDashboardStats();
    fetchHistoryFromBackend();
  } catch(e) {
    content.innerHTML = `<div class="auth-msg error" style="display:block;">${e.message}</div>`;
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>Extract Text & Analyze</span> ➔';
  }
}

/* ============ 8. COMPANY VERIFICATION ============ */
async function runCompanyVerification() {
  const name = document.getElementById('comp-name-input').value.trim();
  const website = document.getElementById('comp-web-input').value.trim();
  const email = document.getElementById('comp-email-input').value.trim();

  const empty = document.getElementById('comp-result-empty');
  const content = document.getElementById('comp-result-content');
  empty.style.display = 'none';
  content.style.display = 'flex';
  content.innerHTML = '<div style="text-align:center; padding:30px;"><div class="loader-spinner" style="margin:0 auto 10px; width:32px; height:32px;"></div><div>Checking domain records & registrar matches...</div></div>';

  try {
    const res = await apiPost('/analyze/company', { company_name: name, website, email });
    const isFake = (res.classification || '').toUpperCase().includes('UNVERIFIED') || (res.risk_score || 0) > 50;
    const heroClass = isFake ? 'fake' : 'genuine';
    const verdict = isFake ? '⚠ UNVERIFIED / SUSPICIOUS ENTITY' : '✓ VERIFIED COMPANY';

    content.innerHTML = `
      <div class="result-hero ${heroClass}">
        <div>
          <div class="result-verdict-title">${verdict}</div>
          <div class="result-verdict-sub">${res.explanation || 'Domain match and corporate validation completed.'}</div>
        </div>
        <div style="text-align:right;">
          <div style="font-family:var(--disp); font-size:24px; font-weight:800;">${Math.round(res.confidence_pct || 0)}%</div>
          <div style="font-size:10.5px; font-family:var(--mono); color:var(--text-dim);">CONFIDENCE</div>
        </div>
      </div>
      <div class="result-scores-grid">
        <div class="score-box">
          <div class="score-box-label">Risk Score</div>
          <div class="score-box-val" style="color:${isFake ? 'var(--danger-2)' : 'var(--safe)'};">${Math.round(res.risk_score || 0)}/100</div>
        </div>
        <div class="score-box">
          <div class="score-box-label">Authenticity</div>
          <div class="score-box-val">${Math.round(res.authenticity_score || 0)}%</div>
        </div>
      </div>
    `;
    fetchDashboardStats();
    fetchHistoryFromBackend();
  } catch(e) {
    content.innerHTML = `<div class="auth-msg error" style="display:block;">${e.message}</div>`;
  }
}

/* ============ 9. SOCIAL MEDIA ANALYSIS ============ */
async function runSocialAnalysis() {
  const text = document.getElementById('social-text-input').value.trim();
  const link = document.getElementById('social-link-input').value.trim();

  const empty = document.getElementById('social-result-empty');
  const content = document.getElementById('social-result-content');
  empty.style.display = 'none';
  content.style.display = 'flex';
  content.innerHTML = '<div style="text-align:center; padding:30px;"><div class="loader-spinner" style="margin:0 auto 10px; width:32px; height:32px;"></div><div>Scanning for airdrop lures & impersonation...</div></div>';

  try {
    const res = await apiPost('/analyze/social', { content: text, url: link });
    const isFake = (res.classification || '').toUpperCase().includes('FRAUD') || (res.risk_score || 0) > 50;
    const heroClass = isFake ? 'fake' : 'genuine';
    const verdict = isFake ? '⚠ FRAUDULENT SOCIAL CONTENT' : '✓ LOW RISK SOCIAL CONTENT';

    content.innerHTML = `
      <div class="result-hero ${heroClass}">
        <div>
          <div class="result-verdict-title">${verdict}</div>
          <div class="result-verdict-sub">${res.explanation || 'Social threat shield scan completed.'}</div>
        </div>
        <div style="text-align:right;">
          <div style="font-family:var(--disp); font-size:24px; font-weight:800;">${Math.round(res.confidence_pct || 0)}%</div>
          <div style="font-size:10.5px; font-family:var(--mono); color:var(--text-dim);">CONFIDENCE</div>
        </div>
      </div>
      <div class="result-scores-grid">
        <div class="score-box">
          <div class="score-box-label">Risk Score</div>
          <div class="score-box-val" style="color:${isFake ? 'var(--danger-2)' : 'var(--safe)'};">${Math.round(res.risk_score || 0)}/100</div>
        </div>
      </div>
    `;
    fetchDashboardStats();
    fetchHistoryFromBackend();
  } catch(e) {
    content.innerHTML = `<div class="auth-msg error" style="display:block;">${e.message}</div>`;
  }
}

/* ============ 10. SETTINGS SAVE ============ */
async function saveSettingsToBackend() {
  const name = document.getElementById('settings-name-input').value.trim();
  const org = document.getElementById('settings-org-input').value.trim();
  const lang = document.getElementById('settings-lang-select').value;
  const theme = document.getElementById('settings-theme-select').value;

  try {
    const res = await apiPut('/auth/profile', {
      display_name: name,
      organization: org,
      preferred_language: lang,
      theme: theme
    });

    if (res.success && res.user) {
      currentUser = res.user;
      updateUserUI();
      alert('Settings saved and synchronized with database successfully!');
    }
  } catch(err) {
    alert(`Failed to save settings: ${err.message}`);
  }
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
}

/* ============ MULTILINGUAL AI ASSISTANT ============ */
function toggleChatWindow() {
  const win = document.getElementById('ai-chat-window');
  win.classList.toggle('open');
}

function handleChatLangChange(lang) {
  selectedChatLang = lang;
  let welcome = '';
  if (lang === 'te') {
    welcome = 'నమస్కారం! నేను ట్రస్ట్‌గార్డ్ AI SOC అసిస్టెంట్‌ని. ఏదైనా అనుమానాస్పద కంటెంట్ లేదా స్కామ్‌ల గురించి అడగండి.';
  } else if (lang === 'hi') {
    welcome = 'नमस्ते! मैं TrustGuard AI SOC सहायक हूँ। किसी भी संदिग्ध मीडिया या धोखाधड़ी के बारे में पूछें।';
  } else {
    welcome = 'Hi, I am your TrustGuard AI SOC Assistant. Run a scan anywhere across the platform and I will provide explainable intelligence.';
  }
  pushBotMsg(welcome);
}

function pushBotMsg(text) {
  const body = document.getElementById('chat-messages-body');
  const msg = document.createElement('div');
  msg.className = 'chat-msg bot';
  msg.textContent = text;
  body.appendChild(msg);
  body.scrollTop = body.scrollHeight;
}

function pushUserMsg(text) {
  const body = document.getElementById('chat-messages-body');
  const msg = document.createElement('div');
  msg.className = 'chat-msg user';
  msg.textContent = text;
  body.appendChild(msg);
  body.scrollTop = body.scrollHeight;
}

function sendChatMessage() {
  const input = document.getElementById('chat-input-field');
  const text = input.value.trim();
  if (!text) return;
  pushUserMsg(text);
  input.value = '';

  setTimeout(() => {
    let reply = '';
    const q = text.toLowerCase();
    if (selectedChatLang === 'te') {
      if (q.includes('image') || q.includes('photo') || q.includes('చిత్రం')) {
        reply = 'ఇమేజ్ డీప్‌ఫేక్ డిటెక్టర్ ప్రీట్రైన్డ్ విజన్ ట్రాన్స్‌ఫార్మర్ (ViT) మరియు ఎర్రర్ లెవల్ అనాలిసిస్ (ELA) ఉపయోగించి అసలైనదో కాదో తనిఖీ చేస్తుంది.';
      } else {
        reply = 'ట్రస్ట్‌గార్డ్ AI మీ మీడియాను నిజ సమయ మోడల్స్ ద్వారా విశ్లేషిస్తుంది. ఖచ్చితమైన ఫలితాల కోసం డాష్‌బోర్డ్ స్కాన్ చేయండి.';
      }
    } else if (selectedChatLang === 'hi') {
      if (q.includes('image') || q.includes('photo') || q.includes('तस्वीर')) {
        reply = 'इमेज डीपफेक डिटेक्टर विज़न ट्रांसफॉर्मर (ViT) और एरर लेवल एनालिसिस (ELA) का उपयोग करके कृत्रिम संकेतों की जाँच करता है।';
      } else {
        reply = 'TrustGuard AI आपकी फ़ाइलों का विश्लेषण करने के लिए वास्तविक प्रीट्रेन्ड मॉडल का उपयोग करता है।';
      }
    } else {
      if (q.includes('vit') || q.includes('model') || q.includes('image')) {
        reply = 'Our Image Analysis pipeline uses the HuggingFace Vision Transformer (dima806/deepfake_vs_real_image_detection) paired with Laplacian gradient metrics.';
      } else if (q.includes('video')) {
        reply = 'Video Analysis extracts frames with OpenCV at 1.0s intervals, crops facial regions, runs ViT inference per frame, and computes temporal consistency.';
      } else if (q.includes('audio') || q.includes('voice')) {
        reply = 'Voice Forensics uses 2.0-second sliding STFT windows, analyzing spectral centroid variances to flag AI-cloned vocoder signatures.';
      } else {
        reply = 'I am monitoring all 9 SOC detection pipelines. Run a scan in any module to inspect detailed risk indicators.';
      }
    }
    pushBotMsg(reply);
  }, 400);
}

function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}

/* ============ PARTICLES FX ============ */
function initParticles() {
  const canvas = document.getElementById('particles');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let w = canvas.width = window.innerWidth;
  let h = canvas.height = window.innerHeight;

  const pts = Array.from({length: 45}, () => ({
    x: Math.random() * w,
    y: Math.random() * h,
    vx: (Math.random() - .5) * .3,
    vy: (Math.random() - .5) * .3,
    r: Math.random() * 1.5 + .5
  }));

  function loop() {
    ctx.clearRect(0,0,w,h);
    ctx.fillStyle = 'rgba(45,217,232,0.4)';
    pts.forEach(p => {
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0) p.x = w; if (p.x > w) p.x = 0;
      if (p.y < 0) p.y = h; if (p.y > h) p.y = 0;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI*2);
      ctx.fill();
    });
    requestAnimationFrame(loop);
  }
  loop();
  window.addEventListener('resize', () => {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
  });
}

/* ============ APPLICATION INITIALIZATION ============ */
window.addEventListener('load', async () => {
  initParticles();

  // 1. Initial bot greeting
  pushBotMsg("Hi, I am the TrustGuard AI SOC Assistant. Sign in with your operator credentials to begin monitoring.");

  // 2. Check backend health
  await checkBackendEngineStatus();

  // 3. Check existing authentication session
  const isAuthenticated = await checkAuthSession();

  // 4. Determine initial page based on URL or auth state
  const initialRoute = getRouteFromUrl();

  if (!isAuthenticated) {
    // If not authenticated, always display the Login view as requested
    navigateTo('login', false);
  } else {
    // If authenticated, navigate to dashboard or the requested route
    const target = initialRoute === 'login' ? 'dashboard' : initialRoute;
    navigateTo(target, false);
    await fetchDashboardStats();
    await fetchHistoryFromBackend();
  }

  // 5. Fade out full-screen loader
  const loader = document.getElementById('app-loader');
  if (loader) {
    setTimeout(() => {
      loader.classList.add('hide');
    }, 350);
  }
});
</script>
<!-- Firebase realtime sync if configured -->
<script type="module" src="./firebase.js"></script>
</body>
</html>
'''

if __name__ == "__main__":
    build_frontend()
