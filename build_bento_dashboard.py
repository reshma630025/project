# Python script to build the Spatial Bento Grid + AI Security Operations Center dashboard in index.html

import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. ENHANCED CSS STYLES FOR SPATIAL BENTO GRID & SOC INTERFACE
bento_css = """
/* ============ SPATIAL BENTO GRID & SOC INTERFACE STYLES ============ */
.bento-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
  margin-bottom: 24px;
}
.bento-card {
  background: var(--glass);
  border: 1px solid var(--glass-brd);
  border-radius: var(--radius);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 22px;
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
  background: radial-gradient(circle at 10% 10%, rgba(45,217,232,.05), transparent 70%);
  pointer-events: none;
}
.bento-card:hover {
  transform: translateY(-2px);
  border-color: rgba(45,217,232,.35);
  box-shadow: 0 16px 36px rgba(0,0,0,.45), 0 0 24px rgba(45,217,232,.08);
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
  margin-bottom: 16px;
  border-bottom: 1px solid var(--line);
  padding-bottom: 12px;
}
.bento-head .title-group {
  display: flex;
  align-items: center;
  gap: 10px;
}
.bento-head .icon-chip {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  background: rgba(45,217,232,.1);
  color: var(--cyan);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.bento-head .icon-chip svg { width: 17px; height: 17px; }
.bento-head h3 {
  font-family: var(--disp);
  font-size: 15px;
  font-weight: 700;
  letter-spacing: .2px;
}
.bento-head .tag {
  font-size: 10px;
  font-family: var(--mono);
  text-transform: uppercase;
  letter-spacing: .8px;
  padding: 4px 8px;
  border-radius: 6px;
  background: var(--panel-2);
  border: 1px solid var(--line);
  color: var(--text-dim);
}

/* Radar & Channel rows */
.radar-channel {
  background: var(--panel-2);
  border: 1px solid var(--line);
  border-radius: 11px;
  padding: 13px 15px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
  transition: .18s ease;
  cursor: pointer;
}
.radar-channel:last-child { margin-bottom: 0; }
.radar-channel:hover {
  border-color: rgba(45,217,232,.4);
  background: rgba(45,217,232,.04);
}
.radar-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}
.radar-icon {
  width: 36px;
  height: 36px;
  border-radius: 9px;
  background: rgba(139,107,240,.12);
  color: var(--violet);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.radar-channel:nth-child(1) .radar-icon { background: rgba(45,217,232,.12); color: var(--cyan); }
.radar-channel:nth-child(2) .radar-icon { background: rgba(139,107,240,.12); color: var(--violet); }
.radar-channel:nth-child(3) .radar-icon { background: rgba(51,209,154,.12); color: var(--safe); }
.radar-info b { font-size: 13px; display: block; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.radar-info span { font-size: 11px; color: var(--text-faint); display: block; margin-top: 1px; }

/* Threat Radial meter in Bento */
.threat-meter-box {
  display: flex;
  align-items: center;
  gap: 22px;
  background: var(--panel-2);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 18px 20px;
  margin-bottom: 18px;
}
.threat-dial {
  position: relative;
  width: 110px;
  height: 110px;
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
.threat-dial-num { font-family: var(--mono); font-size: 22px; font-weight: 800; }
.threat-dial-lbl { font-size: 8.5px; color: var(--text-faint); text-transform: uppercase; letter-spacing: .5px; }

.soc-status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .6px;
  padding: 5px 11px;
  border-radius: 20px;
  background: rgba(51,209,154,.14);
  color: var(--safe);
  border: 1px solid rgba(51,209,154,.35);
}
.soc-status-badge.alert {
  background: rgba(242,73,92,.14);
  color: var(--danger-2);
  border-color: rgba(242,73,92,.35);
}
.soc-status-badge .dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  box-shadow: 0 0 8px currentColor;
  animation: pulse 1.6s infinite;
}

/* Bento stat metrics 4-grid */
.bento-stat-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}
.bento-stat-cell {
  background: var(--panel-2);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 12px 14px;
}
.bento-stat-cell .b-lbl {
  font-size: 10.5px;
  color: var(--text-faint);
  text-transform: uppercase;
  letter-spacing: .6px;
  display: block;
  margin-bottom: 4px;
}
.bento-stat-cell .b-val {
  font-family: var(--mono);
  font-size: 20px;
  font-weight: 700;
}

/* Bento Entity Grid for OCR */
.entity-pill-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-bottom: 14px;
}
.entity-pill {
  background: var(--panel-2);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 8px 10px;
}
.entity-pill .k { font-size: 9.5px; color: var(--text-faint); text-transform: uppercase; letter-spacing: .5px; display: block; }
.entity-pill .v { font-size: 12px; font-weight: 600; color: var(--text); margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; display: block; }

/* Bento Telemetry row */
.telemetry-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 7px 0;
  border-bottom: 1px solid var(--line);
  font-size: 12px;
}
.telemetry-row:last-child { border-bottom: none; }
.telemetry-row span:first-child { color: var(--text-faint); }
.telemetry-row span:last-child { font-family: var(--mono); font-weight: 600; color: var(--text); }

@media(max-width:1200px){
  .bento-grid { grid-template-columns: repeat(2, 1fr); }
  .bento-2x2, .bento-3x1, .bento-4x1 { grid-column: span 2; }
}
@media(max-width:768px){
  .bento-grid { grid-template-columns: 1fr; }
  .bento-2x2, .bento-2x1, .bento-3x1, .bento-4x1, .bento-1x1 { grid-column: span 1; grid-row: auto; }
  .threat-meter-box { flex-direction: column; text-align: center; }
  .entity-pill-grid { grid-template-columns: repeat(2, 1fr); }
}
"""

# Insert Bento CSS right before the </style> tag
if '.bento-grid' not in html:
    style_end = html.find('</style>')
    if style_end != -1:
        html = html[:style_end] + bento_css + "\n" + html[style_end:]

# 2. ENHANCED SPATIAL BENTO GRID DASHBOARD SECTION
bento_dashboard_html = """      <!-- ================= SPATIAL BENTO GRID DASHBOARD (AI SECURITY OPERATIONS CENTER) ================= -->
      <section class="page" id="page-dashboard">
        <div class="page-head" style="display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; gap:14px; margin-bottom:24px;">
          <div>
            <div class="eyebrow">Security Operations Center · Real-Time AI Telemetry</div>
            <div class="page-title">AI Content Authenticity & Threat Radar</div>
            <p class="page-sub">Multimodal neural inspection across images, temporal video frames, synthetic voices, scam texts, and phishing domains.</p>
          </div>
          <div style="display:flex; align-items:center; gap:10px;">
            <div class="soc-status-badge" id="socGlobalShield">
              <span class="dot"></span>
              <span id="socGlobalText">PROTECTED · ENGINE ACTIVE</span>
            </div>
          </div>
        </div>

        <!-- SPATIAL BENTO GRID -->
        <div class="bento-grid">

          <!-- 1. LARGE CARD (2x2): THREAT & RISK INTELLIGENCE OVERVIEW -->
          <div class="bento-card bento-2x2">
            <div class="bento-head">
              <div class="title-group">
                <div class="icon-chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
                <div>
                  <h3>Threat & Risk Intelligence</h3>
                  <div style="font-size:11px; color:var(--text-faint);">Live System Threat Evaluation</div>
                </div>
              </div>
              <span class="tag">REAL-TIME TELEMETRY</span>
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
                <div style="font-size:11px; text-transform:uppercase; letter-spacing:1px; color:var(--text-faint); margin-bottom:4px;">Platform Security Status</div>
                <div style="font-family:var(--disp); font-size:18px; font-weight:700; margin-bottom:8px;" id="bentoSecHeadline">System Nominal · Zero Critical Threats</div>
                <p style="font-size:12.5px; color:var(--text-dim); line-height:1.5; margin-bottom:12px;" id="bentoSecDetail">All multi-signal detectors are actively screening media. No unverified anomalies detected.</p>
                <div style="display:flex; gap:8px;">
                  <button class="btn btn-primary btn-sm" onclick="document.querySelector('#scanTabs .tab-btn.active')?.scrollIntoView({behavior:'smooth'}); document.getElementById('dashAnalyzeBtn')?.click();"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>Execute Scan</button>
                  <button class="btn btn-outline btn-sm" data-goto="history">View History Log</button>
                </div>
              </div>
            </div>

            <div class="bento-stat-grid">
              <div class="bento-stat-cell">
                <span class="b-lbl">Total Scans Today</span>
                <span class="b-val" id="dStat1" style="color:var(--cyan);">0</span>
              </div>
              <div class="bento-stat-cell">
                <span class="b-lbl">Threats Flagged</span>
                <span class="b-val" id="dStat2" style="color:var(--danger-2);">0</span>
              </div>
              <div class="bento-stat-cell">
                <span class="b-lbl">Deepfakes Detected</span>
                <span class="b-val" id="dStat3" style="color:var(--warn);">0</span>
              </div>
              <div class="bento-stat-cell">
                <span class="b-lbl">Scams Neutralized</span>
                <span class="b-val" id="dStat4" style="color:var(--safe);">0</span>
              </div>
            </div>
          </div>

          <!-- 2. LARGE CARD (2x2): MULTI-MODAL DEEPFAKE DETECTION CHANNELS -->
          <div class="bento-card bento-2x2">
            <div class="bento-head">
              <div class="title-group">
                <div class="icon-chip" style="background:rgba(139,107,240,.12); color:var(--violet);"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg></div>
                <div>
                  <h3>Deepfake Detection Radar</h3>
                  <div style="font-size:11px; color:var(--text-faint);">Multimodal Synthetic Media Inspection</div>
                </div>
              </div>
              <span class="tag" style="color:var(--cyan); border-color:rgba(45,217,232,.3);">3 CHANNELS ONLINE</span>
            </div>

            <div style="display:flex; flex-direction:column; gap:10px; flex:1; justify-content:space-between;">
              <!-- Image Channel -->
              <div class="radar-channel" data-goto="image">
                <div class="radar-left">
                  <div class="radar-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg></div>
                  <div class="radar-info">
                    <b>Image Deepfake Channel</b>
                    <span>Vision Transformer (ViT) · ELA Frequency Analysis</span>
                  </div>
                </div>
                <button class="btn btn-outline btn-sm" data-goto="image">Scan Image →</button>
              </div>

              <!-- Video Channel -->
              <div class="radar-channel" data-goto="video">
                <div class="radar-left">
                  <div class="radar-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><rect x="2" y="5" width="15" height="14" rx="2"/><path d="M17 10l5-3v10l-5-3"/></svg></div>
                  <div class="radar-info">
                    <b>Video Deepfake Channel</b>
                    <span>Temporal Frame Consistency · Face Swap Radar</span>
                  </div>
                </div>
                <button class="btn btn-outline btn-sm" data-goto="video">Scan Video →</button>
              </div>

              <!-- Audio Channel -->
              <div class="radar-channel" data-goto="audio">
                <div class="radar-left">
                  <div class="radar-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10a7 7 0 0014 0M12 19v3"/></svg></div>
                  <div class="radar-info">
                    <b>Voice & Audio Forensics</b>
                    <span>STFT Spectral Centroid · Vocoder Phase Detection</span>
                  </div>
                </div>
                <button class="btn btn-outline btn-sm" data-goto="audio">Scan Audio →</button>
              </div>
            </div>
          </div>

          <!-- 3. MEDIUM CARD (2x1): SCAM & TEXT FRAUD INTELLIGENCE -->
          <div class="bento-card bento-2x1">
            <div class="bento-head">
              <div class="title-group">
                <div class="icon-chip" style="background:rgba(245,185,66,.12); color:var(--warn);"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16v13H7l-3 3z"/></svg></div>
                <div>
                  <h3>Scam & Text Intelligence</h3>
                  <div style="font-size:11px; color:var(--text-faint);">Urgency, OTP & Fake Job Traps</div>
                </div>
              </div>
              <span class="tag">NLP HEURISTICS</span>
            </div>
            <div class="grid g2" style="gap:10px; margin-bottom:12px;">
              <div style="background:var(--panel-2); border:1px solid var(--line); border-radius:9px; padding:10px 12px;">
                <b style="font-size:12.5px; display:block;">Financial & Phishing Traps</b>
                <span style="font-size:11px; color:var(--text-faint);">Detects OTP demands & crypto wire pressure</span>
              </div>
              <div style="background:var(--panel-2); border:1px solid var(--line); border-radius:9px; padding:10px 12px;">
                <b style="font-size:12.5px; display:block;">Job & Internship Fraud</b>
                <span style="font-size:11px; color:var(--text-faint);">Scans recruiter domains & upfront fees</span>
              </div>
            </div>
            <div style="display:flex; gap:8px; margin-top:auto;">
              <button class="btn btn-ghost btn-sm" data-goto="text">Analyze Text Message</button>
              <button class="btn btn-ghost btn-sm" data-goto="job">Verify Job Offer</button>
            </div>
          </div>

          <!-- 4. MEDIUM CARD (1x1): URL & PHISHING SECURITY -->
          <div class="bento-card bento-1x1">
            <div class="bento-head">
              <div class="title-group">
                <div class="icon-chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg></div>
                <div>
                  <h3 style="font-size:14px;">URL Security</h3>
                </div>
              </div>
              <span class="tag">RADAR</span>
            </div>
            <p style="font-size:12px; color:var(--text-dim); line-height:1.5; margin-bottom:12px;">Scans Shannon entropy, suspicious TLDs, shorteners, and domain typosquatting.</p>
            <div style="margin-top:auto;">
              <button class="btn btn-ghost btn-sm btn-block" data-goto="url">Inspect URL Link →</button>
            </div>
          </div>

          <!-- 5. MEDIUM CARD (1x1): SOCIAL MEDIA PROTECTION -->
          <div class="bento-card bento-1x1">
            <div class="bento-head">
              <div class="title-group">
                <div class="icon-chip" style="background:rgba(45,217,232,.12); color:var(--cyan);"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg></div>
                <div>
                  <h3 style="font-size:14px;">Social Shield</h3>
                </div>
              </div>
              <span class="tag">PROTECT</span>
            </div>
            <p style="font-size:12px; color:var(--text-dim); line-height:1.5; margin-bottom:12px;">Detects crypto airdrop doubling lures, VIP impersonation, and engagement bait.</p>
            <div style="margin-top:auto;">
              <button class="btn btn-ghost btn-sm btn-block" data-goto="social">Scan Social Post →</button>
            </div>
          </div>

          <!-- 6. MEDIUM CARD (2x1): OCR & POSTER FORENSIC VERIFICATION -->
          <div class="bento-card bento-2x1">
            <div class="bento-head">
              <div class="title-group">
                <div class="icon-chip" style="background:rgba(51,209,154,.12); color:var(--safe);"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg></div>
                <div>
                  <h3>OCR & Poster Extraction</h3>
                  <div style="font-size:11px; color:var(--text-faint);">Client-Side Tesseract + Backend Entity Parser</div>
                </div>
              </div>
              <span class="tag">STRUCTURED</span>
            </div>

            <div class="entity-pill-grid">
              <div class="entity-pill"><span class="k">Company</span><span class="v">Identity Verification</span></div>
              <div class="entity-pill"><span class="k">Email Domain</span><span class="v">Corporate vs Personal</span></div>
              <div class="entity-pill"><span class="k">Phone / UPI</span><span class="v">Payment Traps</span></div>
              <div class="entity-pill"><span class="k">Website</span><span class="v">DNS Alignment</span></div>
              <div class="entity-pill"><span class="k">Salary Claims</span><span class="v">Ratio Anomaly</span></div>
              <div class="entity-pill"><span class="k">Reg. Fee</span><span class="v">Upfront Solicitations</span></div>
            </div>

            <div style="display:flex; gap:8px; margin-top:auto;">
              <button class="btn btn-primary btn-sm" data-goto="ocr">Scan Screenshot / Poster →</button>
            </div>
          </div>

          <!-- 7. SMALL CARD (1x1): AI ENGINE STATUS -->
          <div class="bento-card bento-1x1">
            <div class="bento-head">
              <div class="title-group">
                <div class="icon-chip" style="background:rgba(51,209,154,.12); color:var(--safe);"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg></div>
                <div>
                  <h3 style="font-size:14px;">Engine Status</h3>
                </div>
              </div>
              <span class="tag" id="bentoEngineStatusTag" style="color:var(--safe);">ONLINE</span>
            </div>

            <div style="display:flex; flex-direction:column; gap:4px; margin-bottom:10px;">
              <div class="telemetry-row"><span>Status</span><span style="color:var(--safe);" id="bentoStatusTxt">● Online</span></div>
              <div class="telemetry-row"><span>Backend</span><span>127.0.0.1:8000</span></div>
              <div class="telemetry-row"><span>Vision ViT</span><span style="color:var(--cyan);">Ready</span></div>
              <div class="telemetry-row"><span>Audio STFT</span><span style="color:var(--cyan);">Ready</span></div>
              <div class="telemetry-row"><span>Latency</span><span id="bentoLatency">32ms</span></div>
            </div>
          </div>

          <!-- 8. SMALL CARD (1x1): RECENT ACTIVITY FEED -->
          <div class="bento-card bento-1x1">
            <div class="bento-head">
              <div class="title-group">
                <div class="icon-chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>
                <div>
                  <h3 style="font-size:14px;">Recent Feed</h3>
                </div>
              </div>
              <span class="tag" data-goto="history" style="cursor:pointer;">ALL →</span>
            </div>
            <div id="dashRecent" style="flex:1; overflow-y:auto; max-height:160px;">
              <div class="empty-state" style="padding:16px 0;"><p style="font-size:11.5px;">No scans yet — execute an analysis below.</p></div>
            </div>
          </div>

        </div>

        <!-- ================= MULTI-MODAL QUICK SCANNER DOCK ================= -->
        <div class="card scanner-card" style="margin-top:10px;">
          <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:16px; border-bottom:1px solid var(--line); padding-bottom:12px; flex-wrap:wrap; gap:8px;">
            <div>
              <h3 style="font-family:var(--disp); font-size:17px; font-weight:700;">Multi-Modal Direct Content Scanner</h3>
              <p style="font-size:12.5px; color:var(--text-faint);">Upload files, paste strings, or engage live sensors directly into the neural pipeline.</p>
            </div>
            <div class="chip-tag" style="color:var(--cyan); border-color:rgba(45,217,232,.3);">Real Pretrained Models Active</div>
          </div>

          <div class="tab-row" id="scanTabs" role="tablist">
            <button class="tab-btn active" data-tab="up-image"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>Image</button>
            <button class="tab-btn" data-tab="up-video"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="15" height="14" rx="2"/><path d="M17 10l5-3v10l-5-3"/></svg>Video</button>
            <button class="tab-btn" data-tab="up-audio"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10a7 7 0 0014 0M12 19v3"/></svg>Audio</button>
            <button class="tab-btn" data-tab="up-doc"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2h9l5 5v15H6z"/><path d="M14 2v6h6"/></svg>PDF / Screenshot</button>
            <button class="tab-btn" data-tab="up-text"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16v13H7l-3 3z"/></svg>Text</button>
            <button class="tab-btn" data-tab="up-url"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 17H7a5 5 0 010-10h2M15 7h2a5 5 0 010 10h-2M8 12h8"/></svg>URL</button>
            <button class="tab-btn" data-tab="up-live"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg>Live</button>
          </div>

          <div class="tab-panel active" id="tab-up-image">
            <div class="dropzone" data-accept="image/*" data-kind="image">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 16v3a2 2 0 002 2h12a2 2 0 002-2v-3"/></svg>
              <h4>Upload Image for Neural Deepfake Inspection</h4><p>Click to browse or drag & drop · JPG, PNG, WEBP</p>
              <div class="chip-row"><span class="type-chip">Face swaps</span><span class="type-chip">GAN/Diffusion art</span><span class="type-chip">Manipulated photos</span></div>
            </div>
            <div id="prev-up-image"></div>
          </div>
          <div class="tab-panel" id="tab-up-video">
            <div class="dropzone" data-accept="video/*" data-kind="video">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 16v3a2 2 0 002 2h12a2 2 0 002-2v-3"/></svg>
              <h4>Upload Video for Temporal Consistency Check</h4><p>Click to browse or drag & drop · MP4, MOV, WEBM</p>
              <div class="chip-row"><span class="type-chip">Face reenactment</span><span class="type-chip">Lip-sync fraud</span><span class="type-chip">Frame splicing</span></div>
            </div>
            <div id="prev-up-video"></div>
          </div>
          <div class="tab-panel" id="tab-up-audio">
            <div class="dropzone" data-accept="audio/*" data-kind="audio">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 16v3a2 2 0 002 2h12a2 2 0 002-2v-3"/></svg>
              <h4>Upload Audio for Voice Synthesis Analysis</h4><p>Click to browse or drag & drop · MP3, WAV, M4A</p>
              <div class="chip-row"><span class="type-chip">Voice cloning</span><span class="type-chip">Synthetic speech</span><span class="type-chip">Vocoder artifacts</span></div>
            </div>
            <div id="prev-up-audio"></div>
          </div>
          <div class="tab-panel" id="tab-up-doc">
            <div class="dropzone" data-accept="image/*,application/pdf" data-kind="doc">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 16v3a2 2 0 002 2h12a2 2 0 002-2v-3"/></svg>
              <h4>Upload Document / Poster Screenshot</h4><p>Job ads, offer letters, poster screenshots</p>
              <div class="chip-row"><span class="type-chip">OCR extraction + Entity Fraud Engine</span></div>
            </div>
            <div id="prev-up-doc"></div>
          </div>
          <div class="tab-panel" id="tab-up-text">
            <label class="field-label">Paste text message, suspicious job offer, email or social post</label>
            <textarea class="textarea" id="quickText" placeholder="Paste message or offer text here…"></textarea>
          </div>
          <div class="tab-panel" id="tab-up-url">
            <label class="field-label">Paste suspicious link or URL</label>
            <input class="field" id="quickUrl" type="text" placeholder="https://example.com/verify-credentials">
          </div>
          <div class="tab-panel" id="tab-up-live">
            <div class="grid g2">
              <div class="card card-pad" style="text-align:center;">
                <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" style="color:var(--cyan); margin-bottom:8px;"><path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg>
                <h4 style="font-family:var(--disp); margin-bottom:6px;">Live Camera Scanner</h4>
                <p style="font-size:12px; color:var(--text-faint); margin-bottom:14px;">Instant facial authenticity checking</p>
                <button class="btn btn-ghost btn-block" data-goto="camera">Go to Camera Scanner</button>
              </div>
              <div class="card card-pad" style="text-align:center;">
                <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" style="color:var(--cyan); margin-bottom:8px;"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10a7 7 0 0014 0M12 19v3"/></svg>
                <h4 style="font-family:var(--disp); margin-bottom:6px;">Live Microphone Forensics</h4>
                <p style="font-size:12px; color:var(--text-faint); margin-bottom:14px;">Real-time speech synthesis detector</p>
                <button class="btn btn-ghost btn-block" data-goto="mic">Go to Live Microphone</button>
              </div>
            </div>
          </div>

          <div class="action-row">
            <button class="btn btn-primary" id="dashAnalyzeBtn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>Execute Multimodal Analysis</button>
            <button class="btn btn-outline" id="dashResetBtn">Reset Scanner</button>
          </div>

          <div class="pipeline card" id="dashPipeline" style="display:none;">
            <div class="pipeline-title"><h3>Neural Execution Pipeline</h3><span class="chip-tag" id="pipelineStatus">Running…</span></div>
            <div class="steps" id="dashSteps"></div>
          </div>

          <div class="result-wrap" id="dashResult"></div>
        </div>
      </section>
"""

# Replace the existing #page-dashboard section with the new Spatial Bento Grid section
pattern = r'<!-- ================= DASHBOARD ================= -->\s*<section class="page" id="page-dashboard">.*?</section>'
m = re.search(pattern, html, re.DOTALL)
if m:
    html = html[:m.start()] + bento_dashboard_html + html[m.end():]
    print("Replaced #page-dashboard with Spatial Bento Grid!")
else:
    print("Could not locate #page-dashboard via regex. Searching alternative pattern...")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully!")
