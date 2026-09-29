import re

with open(r"C:\Users\paruc\OneDrive\Desktop\project\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Replace the Dashboard HTML
start_html = html.find('<section class="page active" id="page-dashboard">')
end_html = html.find('<!-- ================= 3. IMAGE ANALYSIS ================= -->')

new_dashboard_html = """<section class="page active" id="page-dashboard">
  <!-- TOP HEADER -->
  <div class="page-head" style="display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; gap:12px; margin-bottom:20px;">
    <div>
      <div class="eyebrow">Content Authenticity & Digital Fraud Detection</div>
      <div class="page-title">TrustGuard AI</div>
    </div>
    <div style="display:flex; align-items:center; gap:8px;">
      <div class="soc-status-badge" id="dashboardBackendShield">
        <span class="dot"></span>
        <span id="dashboardBackendText">Checking Status...</span>
      </div>
    </div>
  </div>

  <div class="bento-grid">
    <!-- ROW 1: 4 Simple Summary Cards -->
    <div class="bento-card bento-1x1">
      <span class="b-lbl" style="font-size:10px; color:var(--text-faint); text-transform:uppercase; letter-spacing:.6px;">Total Scans</span>
      <span class="b-val" id="dTotalScans" style="font-family:var(--mono); font-size:24px; font-weight:700; color:var(--cyan); margin-top:4px;">0</span>
    </div>
    <div class="bento-card bento-1x1">
      <span class="b-lbl" style="font-size:10px; color:var(--text-faint); text-transform:uppercase; letter-spacing:.6px;">REAL</span>
      <span class="b-val" id="dTotalReal" style="font-family:var(--mono); font-size:24px; font-weight:700; color:var(--safe); margin-top:4px;">0</span>
    </div>
    <div class="bento-card bento-1x1">
      <span class="b-lbl" style="font-size:10px; color:var(--text-faint); text-transform:uppercase; letter-spacing:.6px;">FAKE</span>
      <span class="b-val" id="dTotalFake" style="font-family:var(--mono); font-size:24px; font-weight:700; color:var(--warn); margin-top:4px;">0</span>
    </div>
    <div class="bento-card bento-1x1">
      <span class="b-lbl" style="font-size:10px; color:var(--text-faint); text-transform:uppercase; letter-spacing:.6px;">High Risk</span>
      <span class="b-val" id="dTotalHighRisk" style="font-family:var(--mono); font-size:24px; font-weight:700; color:var(--danger-2); margin-top:4px;">0</span>
    </div>

    <!-- MAIN HERO CARD & QUICK VERIFY (Row 2) -->
    <div class="bento-card bento-2x1">
      <div class="bento-head">
        <div class="title-group">
          <div class="icon-chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
          <div><h3>SECURITY OVERVIEW</h3></div>
        </div>
      </div>
      <div style="flex:1; display:flex; flex-direction:column; justify-content:center;">
        <div style="font-size:13px; color:var(--text-dim); margin-bottom:12px;">Current Status: <span id="heroCurrentStatus" style="color:var(--cyan); font-weight:bold;">Monitoring</span></div>
        <div style="background:var(--panel-2); padding:15px; border-radius:6px; margin-bottom:15px;">
          <div style="font-size:11px; color:var(--text-dim); margin-bottom:4px;">Latest Scan: <span id="heroLatestFile" style="color:var(--text);">None</span></div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>Result: <strong id="heroLatestResult" style="color:var(--text-faint);">N/A</strong></div>
            <div>Confidence: <strong id="heroLatestConf">0%</strong></div>
            <div>Risk: <strong id="heroLatestRisk">0 / 100</strong></div>
          </div>
        </div>
        <button class="btn btn-primary btn-block" onclick="document.getElementById('dashScanTabs')?.scrollIntoView({behavior:'smooth'}); document.querySelector('.drop-zone')?.click();">QUICK VERIFY</button>
      </div>
    </div>
    
    <div class="bento-card bento-2x1" id="dashScanTabs" style="display:flex; flex-direction:column;">
       <div class="bento-head">
          <div>
            <h3 style="font-size:14px;">VERIFY ANY CONTENT</h3>
            <div style="font-size:11px; color:var(--text-faint);">Upload, drag & drop, or paste content to analyze it.</div>
          </div>
       </div>
       <div style="flex:1; display:flex; gap:6px; flex-wrap:wrap; margin-top:10px;">
          <button class="btn btn-outline btn-sm" data-goto="image">Image</button>
          <button class="btn btn-outline btn-sm" data-goto="video">Video</button>
          <button class="btn btn-outline btn-sm" data-goto="audio">Audio</button>
          <button class="btn btn-outline btn-sm" data-goto="text">Text</button>
          <button class="btn btn-outline btn-sm" data-goto="email">Email</button>
          <button class="btn btn-outline btn-sm" data-goto="url">URL</button>
          <button class="btn btn-outline btn-sm" data-goto="social">Social</button>
          <button class="btn btn-outline btn-sm" data-goto="job">Job</button>
       </div>
       <div class="drop-zone" id="dashDropZone" style="margin-top:10px; border:2px dashed var(--line); border-radius:8px; padding:20px; text-align:center; color:var(--text-dim); cursor:pointer;" onclick="document.getElementById('dashFileInput').click();">
          DROP CONTENT HERE<br/><span style="font-size:11px;">or click to browse file</span>
       </div>
       <input type="file" id="dashFileInput" style="display:none;">
    </div>

    <!-- LARGE RISK ANALYTICS CARD (Row 3, 4x1) -->
    <div class="bento-card bento-4x1" style="min-height:220px; display:flex; flex-direction:column;">
      <div class="bento-head">
        <div class="title-group">
          <div class="icon-chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"/><path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/></svg></div>
          <div>
            <h3>RISK ACTIVITY</h3>
            <div style="font-size:10.5px; color:var(--text-faint);">Risk levels from your actual recent scans</div>
          </div>
        </div>
      </div>
      <div style="display:flex; justify-content:space-between; margin-bottom:10px; padding:0 10px;">
         <div style="font-size:12px;">CURRENT RISK: <strong id="graphCurrentRisk" style="color:var(--cyan);">0 / 100</strong></div>
         <div style="font-size:12px;">AVERAGE RISK: <strong id="graphAvgRisk" style="color:var(--text-dim);">0 / 100</strong></div>
         <div style="font-size:12px;">LATEST RESULT: <strong id="graphLatestResult" style="color:var(--text-dim);">N/A</strong></div>
      </div>
      <div id="dashRiskLargeGraph" style="flex:1; width:100%; position:relative;"></div>
      <div style="display:flex; justify-content:center; gap:15px; font-size:10px; color:var(--text-faint); margin-top:10px; padding-top:10px; border-top:1px solid var(--line);">
         <span>0-20 LOW</span>
         <span>21-40 MODERATE</span>
         <span>41-60 HIGH</span>
         <span>61-80 VERY HIGH</span>
         <span>81-100 CRITICAL</span>
      </div>
    </div>

    <!-- RECENT SCANS & SYSTEM STATUS (Row 4, 2x1 / 2x1) -->
    <div class="bento-card bento-2x1" style="display:flex; flex-direction:column; max-height:250px;">
      <div class="bento-head">
        <h3>RECENT SCANS</h3>
        <button class="btn btn-ghost btn-sm" data-goto="history">VIEW ALL</button>
      </div>
      <div id="dashRecentScansList" style="flex:1; overflow-y:auto; font-size:12px; display:flex; flex-direction:column; gap:4px; padding-right:5px;">
         <!-- Populated via JS -->
      </div>
    </div>

    <div class="bento-card bento-2x1" style="display:flex; flex-direction:column; max-height:250px;">
      <div class="bento-head">
        <h3>SYSTEM STATUS</h3>
        <div style="font-size:10px; color:var(--text-faint);">Security Tools</div>
      </div>
      <div id="dashSystemStatus" style="flex:1; display:flex; flex-direction:column; gap:8px; font-size:12px;">
         <!-- Populated via JS /api/status -->
      </div>
    </div>

  </div>
</section>
"""

if start_html != -1 and end_html != -1:
    html = html[:start_html] + new_dashboard_html + html[end_html:]
else:
    print("Failed to replace dashboard HTML")

# 2. Add dashFileInput change listener inside JS setup
old_init = "window.addEventListener('load', async () => {"
new_init = """window.addEventListener('load', async () => {
  const dashFileInp = document.getElementById('dashFileInput');
  if(dashFileInp) {
    dashFileInp.addEventListener('change', async (e) => {
      const file = e.target.files[0];
      if(!file) return;
      gotoPage('image');
      const gDrop = document.getElementById('globalFileInput');
      if (gDrop) {
          // Transfer file via DataTransfer
          const dt = new DataTransfer();
          dt.items.add(file);
          gDrop.files = dt.files;
          gDrop.dispatchEvent(new Event('change'));
      }
    });
  }
"""
html = html.replace(old_init, new_init)

# 3. Replace updateDashboardStats function
start_js = html.find("function updateDashboardStats(){")
end_js = html.find("/* ============ ENGINE STATUS POLLING ============ */")

new_js = """function updateDashboardStats(){
  const scans = statCounters.scans || 0;
  let realCount = statCounters.authentic || 0;
  let fakeCount = (statCounters.ai_generated || 0) + (statCounters.suspicious || 0);
  let highRiskCount = statCounters.threats || 0;

  ['dTotalScans','landStat1'].forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent = scans; });
  ['dTotalReal','landStat4'].forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent = realCount; });
  ['dTotalFake','landStat2'].forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent = fakeCount; });
  ['dTotalHighRisk','landStat3'].forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent = highRiskCount; });

  if (scanHistory.length > 0) {
      const latest = scanHistory[0];
      const risk = latest.score || 0;
      const conf = latest.confidence || 0;
      const isReal = risk <= 50; 
      const resultTxt = latest.classification || (isReal ? 'REAL' : 'FAKE');
      
      const fileEl = document.getElementById('heroLatestFile');
      if (fileEl) fileEl.textContent = latest.contentLabel || latest.contentType;
      
      const resEl = document.getElementById('heroLatestResult');
      if (resEl) {
          resEl.textContent = resultTxt;
          resEl.style.color = isReal ? 'var(--safe)' : 'var(--warn)';
      }
      
      const confEl = document.getElementById('heroLatestConf');
      if(confEl) confEl.textContent = conf + '%';
      const rEl = document.getElementById('heroLatestRisk');
      if(rEl) rEl.textContent = risk + ' / 100';
      const grEl = document.getElementById('graphLatestResult');
      if(grEl) grEl.textContent = resultTxt;
      const crEl = document.getElementById('graphCurrentRisk');
      if(crEl) crEl.textContent = risk + ' / 100';
  } else {
      ['heroLatestFile','heroLatestResult','heroLatestConf','heroLatestRisk','graphLatestResult','graphCurrentRisk'].forEach(id=>{
         const el = document.getElementById(id); if(el) el.textContent = id.includes('File') ? 'None' : (id.includes('Conf') ? '0%' : (id.includes('Risk') ? '0 / 100' : 'N/A'));
      });
  }

  let avgRisk = 0;
  if (scanHistory.length > 0) {
      const sum = scanHistory.reduce((acc, h) => acc + (Number(h.score) || 0), 0);
      avgRisk = Math.round(sum / scanHistory.length);
  }
  const arEl = document.getElementById('graphAvgRisk');
  if(arEl) arEl.textContent = avgRisk + ' / 100';

  const graphEl = document.getElementById('dashRiskLargeGraph');
  if (graphEl) {
      if (scanHistory.length === 0) {
          graphEl.innerHTML = '<div style="width:100%; height:100%; display:flex; align-items:center; justify-content:center; color:var(--text-faint); font-size:12px;">NO SCAN DATA YET</div>';
      } else {
          const recent = scanHistory.slice(0, 30).reverse();
          const points = recent.map((h, i) => {
              const x = (i / (Math.max(1, recent.length - 1))) * 100;
              return { x, y: 100 - h.score, score: h.score };
          });
          
          let pathD = `M ${points[0].x} ${points[0].y}`;
          for(let i = 1; i < points.length; i++) {
            const prev = points[i-1];
            const curr = points[i];
            const cx = (prev.x + curr.x) / 2;
            pathD += ` C ${cx} ${prev.y} ${cx} ${curr.y} ${curr.x} ${curr.y}`;
          }
          let areaD = pathD + ` L 100 100 L 0 100 Z`;
          const circles = points.map(p => 
            `<circle cx="${p.x}" cy="${p.y}" r="2" fill="var(--panel)" stroke="var(--cyan)" stroke-width="1.5"><title>Risk: ${p.score}</title></circle>`
          ).join('');

          graphEl.innerHTML = `
            <style>
              .dash-line { stroke-dasharray: 1000; stroke-dashoffset: 1000; animation: dashLineDraw 1.5s ease forwards; }
              @keyframes dashLineDraw { to { stroke-dashoffset: 0; } }
              .dash-points { opacity: 0; animation: fadeHist 0.5s ease 1s forwards; }
              .dash-area { opacity: 0; animation: fadeArea 1s ease 0.5s forwards; }
            </style>
            <div style="width:100%; height:100%; position:absolute; top:0; left:0; right:0; bottom:0;">
              <svg width="100%" height="100%" viewBox="0 -5 100 110" preserveAspectRatio="none" style="overflow:visible;">
                <line x1="0" y1="0" x2="100" y2="0" stroke="var(--line)" stroke-dasharray="2,2" stroke-width="0.5"/>
                <line x1="0" y1="25" x2="100" y2="25" stroke="var(--line)" stroke-dasharray="2,2" stroke-width="0.5"/>
                <line x1="0" y1="50" x2="100" y2="50" stroke="var(--line)" stroke-dasharray="2,2" stroke-width="0.5"/>
                <line x1="0" y1="75" x2="100" y2="75" stroke="var(--line)" stroke-dasharray="2,2" stroke-width="0.5"/>
                <line x1="0" y1="100" x2="100" y2="100" stroke="var(--line)" stroke-dasharray="2,2" stroke-width="0.5"/>
                <path d="${areaD}" fill="rgba(45,217,232,0.1)" class="dash-area" />
                <path d="${pathD}" fill="none" stroke="var(--cyan)" stroke-width="2" class="dash-line" style="filter: drop-shadow(0 0 3px var(--cyan));" />
                <g class="dash-points">${circles}</g>
              </svg>
            </div>
          `;
      }
  }

  const rsEl = document.getElementById('dashRecentScansList');
  if (rsEl) {
      if (scanHistory.length === 0) {
          rsEl.innerHTML = '<div style="color:var(--text-faint); padding:10px;">NO SCANS YET</div>';
      } else {
          rsEl.innerHTML = scanHistory.slice(0, 15).map(h => {
              const isReal = h.score <= 50;
              const cl = isReal ? 'var(--safe)' : 'var(--warn)';
              const rt = h.classification || (isReal ? 'REAL' : 'FAKE');
              return `<div style="display:flex; justify-content:space-between; padding:6px; border-bottom:1px solid var(--line);">
                  <div style="flex:2; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="${h.contentLabel || 'File'}">${h.contentLabel || 'File'}</div>
                  <div style="flex:1; color:var(--text-dim);">${h.contentType}</div>
                  <div style="flex:1; font-weight:bold; color:${cl};">${rt}</div>
                  <div style="flex:1; text-align:right;">${h.score}%</div>
              </div>`;
          }).join('');
      }
  }
}
"""

if start_js != -1 and end_js != -1:
    html = html[:start_js] + new_js + "\n" + html[end_js:]
else:
    print("Failed to replace updateDashboardStats logic")


# 4. Replace checkBackendEngineStatus to use /api/status as the single source of truth for dashboard header and top banner.
start_chk = html.find("async function checkBackendEngineStatus() {")
end_chk = html.find("setInterval(checkBackendEngineStatus, 15000);")

new_chk = """async function checkBackendEngineStatus() {
  const offlineBanner = document.getElementById('backendOfflineBanner');
  const dbShield = document.getElementById('dashboardBackendShield');
  const dbTxt = document.getElementById('dashboardBackendText');
  const heroStat = document.getElementById('heroCurrentStatus');
  const sysEl = document.getElementById('dashSystemStatus');
  
  const baseUrl = window.API_BASE_URL || 'http://127.0.0.1:8000';
  try {
    const res = await fetch(baseUrl + '/api/status', { mode: 'cors' });
    if (!res.ok) throw new Error('API not ok');
    const data = await res.json();
    
    // Online
    if(offlineBanner) offlineBanner.style.display = 'none';
    if(dbShield) dbShield.className = 'soc-status-badge';
    if(dbTxt) dbTxt.textContent = 'Local Backend Connected';
    if(heroStat) { heroStat.textContent = 'Protected / Monitoring'; heroStat.style.color = 'var(--safe)'; }
    
    if(sysEl) {
        let sysHtml = '';
        const models = [
            {name: 'Image Model', key: 'vision_transformer', fallback: 'Ready'},
            {name: 'Video Model', key: 'video_analyzer', fallback: 'Ready'},
            {name: 'Audio Model', key: 'audio_dsp', fallback: 'Ready'},
            {name: 'Text Model', key: 'text_nlp', fallback: 'Ready'},
            {name: 'URL Model', key: 'url_scanner', fallback: 'Ready'},
            {name: 'Database', key: 'database', fallback: 'Connected'}
        ];
        models.forEach(m => {
            const s = data[m.key] || m.fallback;
            sysHtml += `<div style="display:flex; justify-content:space-between; padding:4px 0; border-bottom:1px solid var(--line);"><span style="color:var(--text-dim);">${m.name}</span><span style="color:var(--cyan);">${s}</span></div>`;
        });
        sysEl.innerHTML = sysHtml;
    }
  } catch(e) {
    if(offlineBanner) offlineBanner.style.display = 'block';
    if(dbShield) dbShield.className = 'soc-status-badge alert';
    if(dbTxt) dbTxt.textContent = 'Backend Offline';
    if(heroStat) { heroStat.textContent = 'Backend Offline'; heroStat.style.color = 'var(--danger-2)'; }
    if(sysEl) sysEl.innerHTML = '<div style="color:var(--danger-2);">All models unavailable. Start the backend.</div>';
  }
}
"""

if start_chk != -1 and end_chk != -1:
    html = html[:start_chk] + new_chk + "\n" + html[end_chk:]
else:
    print("Failed to replace checkBackendEngineStatus logic")

# Remove flash/neon animations and make them subtle
html = html.replace("animation: pulseGlow 1s infinite alternate;", "animation: pulseGlow 5s ease-in-out infinite alternate;")

with open(r"C:\Users\paruc\OneDrive\Desktop\project\index.html", "w", encoding="utf-8") as f:
    f.write(html)
