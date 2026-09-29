import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. ADD BACKGROUND HTML if not exists
if '<div class="bg-layer" id="appBackground">' not in html:
    bg_html = """
  <!-- Animated Background System -->
  <div class="bg-layer" id="appBackground" style="position:fixed; top:0; left:0; width:100vw; height:100vh; z-index:-10; pointer-events:none; overflow:hidden;">
    <div class="bg-gradient" style="position:absolute; width:200%; height:200%; top:-50%; left:-50%; background:radial-gradient(circle at center, rgba(16,21,34,1) 0%, rgba(10,14,23,1) 100%); animation: slowGradientMove 30s infinite alternate;"></div>
    <div class="bg-grid" style="position:absolute; width:100%; height:100%; background-image: linear-gradient(rgba(45,217,232,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(45,217,232,0.03) 1px, transparent 1px); background-size: 50px 50px; animation: gridDrift 60s linear infinite;"></div>
    <div class="bg-glow" style="position:absolute; width:100%; height:100%; background: radial-gradient(circle at 30% 70%, rgba(139,107,240,0.04) 0%, transparent 50%), radial-gradient(circle at 70% 30%, rgba(45,217,232,0.04) 0%, transparent 50%); animation: pulseAmbient 15s ease-in-out infinite alternate;"></div>
    <canvas id="bgCanvas" style="position:absolute; top:0; left:0; width:100%; height:100%; opacity:0.5;"></canvas>
    <div class="bg-scanline" style="position:absolute; top:0; left:0; width:100%; height:2px; background:linear-gradient(90deg, transparent, rgba(45,217,232,0.3), transparent); animation: horizontalScan 8s linear infinite; opacity:0.4;"></div>
  </div>
"""
    body_idx = html.find('<body data-theme="dark">')
    if body_idx != -1:
        html = html[:body_idx+24] + bg_html + html[body_idx+24:]

# 2. INJECT CSS ANIMATIONS
css_animations = """
    /* --- TRUSTGUARD PROFESSIONAL ANIMATIONS --- */
    
    /* Background Keyframes */
    @keyframes slowGradientMove { 0% { transform: translate(0, 0); } 100% { transform: translate(5%, 5%); } }
    @keyframes gridDrift { 0% { background-position: 0px 0px; } 100% { background-position: -50px -50px; } }
    @keyframes pulseAmbient { 0% { opacity: 0.6; } 100% { opacity: 1; } }
    @keyframes horizontalScan { 0% { top: -10%; } 100% { top: 110%; } }

    /* Page & Card Entrance */
    .page.active { animation: pageFadeIn 0.3s ease-out forwards; }
    @keyframes pageFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    
    .bento-card, .unified-card, .det-tile, .module-card {
        animation: cardEntrance 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) backwards;
    }
    .bento-card:nth-child(1) { animation-delay: 0.05s; }
    .bento-card:nth-child(2) { animation-delay: 0.1s; }
    .bento-card:nth-child(3) { animation-delay: 0.15s; }
    .bento-card:nth-child(4) { animation-delay: 0.2s; }
    @keyframes cardEntrance { from { opacity: 0; transform: translateY(15px) scale(0.98); } to { opacity: 1; transform: translateY(0) scale(1); } }

    /* Button Animations */
    .btn { transition: all 0.2s cubic-bezier(0.25, 1, 0.5, 1) !important; position: relative; overflow: hidden; }
    .btn:active { transform: translateY(1px) scale(0.98) !important; }
    
    .btn.analyzing {
        pointer-events: none;
        opacity: 0.9;
        background: var(--panel) !important;
        color: var(--cyan) !important;
        border: 1px solid var(--cyan) !important;
        box-shadow: 0 0 15px rgba(45,217,232,0.2) !important;
    }
    .btn.analyzing::after {
        content: ''; position: absolute; top:0; left:-100%; width:100%; height:100%;
        background: linear-gradient(90deg, transparent, rgba(45,217,232,0.2), transparent);
        animation: scanningSweep 1.5s infinite linear;
    }
    @keyframes scanningSweep { to { left: 100%; } }

    /* AI Assistant Hover/Pulse */
    .assist-fab { transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important; animation: breathGlow 4s ease-in-out infinite alternate; }
    .assist-fab:hover { transform: scale(1.08) !important; box-shadow: 0 0 25px rgba(139,107,240,0.6) !important; animation: none; }
    @keyframes breathGlow { from { box-shadow: 0 0 10px rgba(139,107,240,0.3); } to { box-shadow: 0 0 25px rgba(139,107,240,0.8); } }

    /* Pipeline Animation */
    .pipe-step { transition: opacity 0.3s, transform 0.3s; }
    .pipe-step.active .step-icon { animation: spinPulse 2s linear infinite; color: var(--cyan); }
    @keyframes spinPulse { 0% { transform: rotate(0deg) scale(1); } 50% { transform: rotate(180deg) scale(1.1); } 100% { transform: rotate(360deg) scale(1); } }

    /* Result Animation */
    .result-card.show { animation: resultPop 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
    @keyframes resultPop { from { opacity: 0; transform: scale(0.95) translateY(10px); } to { opacity: 1; transform: scale(1) translateY(0); } }

    /* Accessibility */
    @media (prefers-reduced-motion: reduce) {
        *, ::before, ::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; scroll-behavior: auto !important; }
    }
    /* --- END ANIMATIONS --- */
"""
style_idx = html.find('</style>')
if style_idx != -1 and '/* --- TRUSTGUARD PROFESSIONAL ANIMATIONS --- */' not in html:
    html = html[:style_idx] + css_animations + html[style_idx:]

# 3. Add JS for Background Canvas Particles & Connections
js_bg = """
  // Background Particles and Network Lines
  const canvas = document.getElementById('bgCanvas');
  if (canvas && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const ctx = canvas.getContext('2d');
    let width, height, nodes = [];
    function resize() { width = canvas.width = window.innerWidth; height = canvas.height = window.innerHeight; }
    window.addEventListener('resize', resize);
    resize();
    for(let i=0; i<40; i++) {
      nodes.push({
        x: Math.random() * width, y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.3, vy: (Math.random() - 0.5) * 0.3,
        r: Math.random() * 1.5 + 0.5
      });
    }
    function draw() {
      ctx.clearRect(0, 0, width, height);
      ctx.fillStyle = 'rgba(45, 217, 232, 0.6)';
      ctx.strokeStyle = 'rgba(45, 217, 232, 0.15)';
      for(let i=0; i<nodes.length; i++) {
        let n = nodes[i];
        n.x += n.vx; n.y += n.vy;
        if(n.x < 0 || n.x > width) n.vx *= -1;
        if(n.y < 0 || n.y > height) n.vy *= -1;
        ctx.beginPath(); ctx.arc(n.x, n.y, n.r, 0, Math.PI*2); ctx.fill();
        for(let j=i+1; j<nodes.length; j++) {
          let n2 = nodes[j];
          let d = Math.hypot(n.x - n2.x, n.y - n2.y);
          if (d < 150) {
            ctx.beginPath(); ctx.moveTo(n.x, n.y); ctx.lineTo(n2.x, n2.y); ctx.stroke();
          }
        }
      }
      requestAnimationFrame(draw);
    }
    draw();
  }
"""
if 'const canvas = document.getElementById(\'bgCanvas\');' not in html:
    html = html.replace('function initParticles(){', js_bg + '\nfunction initParticles(){')

# 4. Enhance Number Count Animation
js_count = """
function animateValue(obj, start, end, duration) {
  if (!obj) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { obj.textContent = end; return; }
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    // easing out
    const ease = 1 - Math.pow(1 - progress, 3);
    obj.textContent = Math.floor(ease * (end - start) + start);
    if (progress < 1) window.requestAnimationFrame(step);
    else obj.textContent = end;
  };
  window.requestAnimationFrame(step);
}
"""
if 'function animateValue' not in html:
    html = html.replace('function updateDashboardStats(){', js_count + '\nfunction updateDashboardStats(){')

# Hook animateValue into updateDashboardStats
html = html.replace("if(el) el.textContent = statCounters.scans;", "if(el) animateValue(el, parseInt(el.textContent)||0, statCounters.scans, 1000);")
html = html.replace("if(el) el.textContent = statCounters.ai_generated ?? statCounters.deepfakes ?? 0;", "if(el) animateValue(el, parseInt(el.textContent)||0, statCounters.ai_generated ?? statCounters.deepfakes ?? 0, 1000);")
html = html.replace("if(el) el.textContent = statCounters.suspicious ?? statCounters.threats ?? 0;", "if(el) animateValue(el, parseInt(el.textContent)||0, statCounters.suspicious ?? statCounters.threats ?? 0, 1000);")
html = html.replace("if(el) el.textContent = statCounters.authentic ?? 0;", "if(el) animateValue(el, parseInt(el.textContent)||0, statCounters.authentic ?? 0, 1000);")
html = html.replace("latestRiskEl.textContent = `${threatScore}%`;", "animateValue(latestRiskEl, parseInt(latestRiskEl.textContent)||0, threatScore, 1000); setTimeout(()=>latestRiskEl.textContent=`${threatScore}%`, 1050);")

# 5. Fix Button analyzing states
# Update all instances of apiPost to change the button state if a button is clicked
# Actually, the best way is to modify the button's class in the event listeners.

def patch_button_analyzing(html_str, btn_id):
    # This will inject button state changes around apiPost calls for specific buttons
    # Example: document.getElementById('imgAnalyzeBtn')?.addEventListener('click', async ()=>{ 
    # we inject btn.classList.add('analyzing'); btn.innerHTML='ANALYZING...';
    pass

# A simpler robust way: patch the `runPipeline` function which wraps around the backend calls for the universal scanner, 
# and for individual pages we can patch the `Analyze` click events.

# Let's do a global replace for the analyze buttons:
btn_pairs = [
    ("document.getElementById('deepfakeAnalyzeBtn')?.addEventListener('click', async ()=>{", "const _btn = document.getElementById('deepfakeAnalyzeBtn'); if(_btn) { _btn.classList.add('analyzing'); _btn.innerHTML = 'ANALYZING...'; } try {"),
    ("document.getElementById('imgAnalyzeBtn')?.addEventListener('click', async ()=>{", "const _btn = document.getElementById('imgAnalyzeBtn'); if(_btn) { _btn.classList.add('analyzing'); _btn.innerHTML = 'ANALYZING...'; } try {"),
    ("document.getElementById('vidAnalyzeBtn')?.addEventListener('click', async ()=>{", "const _btn = document.getElementById('vidAnalyzeBtn'); if(_btn) { _btn.classList.add('analyzing'); _btn.innerHTML = 'ANALYZING...'; } try {"),
    ("document.getElementById('audAnalyzeBtn')?.addEventListener('click', async ()=>{", "const _btn = document.getElementById('audAnalyzeBtn'); if(_btn) { _btn.classList.add('analyzing'); _btn.innerHTML = 'ANALYZING...'; } try {"),
    ("document.getElementById('scamAnalyzeBtn')?.addEventListener('click', async ()=>{", "const _btn = document.getElementById('scamAnalyzeBtn'); if(_btn) { _btn.classList.add('analyzing'); _btn.innerHTML = 'ANALYZING...'; } try {"),
    ("document.getElementById('emailAnalyzeBtn')?.addEventListener('click', async ()=>{", "const _btn = document.getElementById('emailAnalyzeBtn'); if(_btn) { _btn.classList.add('analyzing'); _btn.innerHTML = 'ANALYZING...'; } try {"),
    ("document.getElementById('jobAnalyzeBtn')?.addEventListener('click', async ()=>{", "const _btn = document.getElementById('jobAnalyzeBtn'); if(_btn) { _btn.classList.add('analyzing'); _btn.innerHTML = 'ANALYZING...'; } try {"),
    ("document.getElementById('urlAnalyzeBtn')?.addEventListener('click', async ()=>{", "const _btn = document.getElementById('urlAnalyzeBtn'); if(_btn) { _btn.classList.add('analyzing'); _btn.innerHTML = 'ANALYZING...'; } try {"),
    ("document.getElementById('socialAnalyzeBtn')?.addEventListener('click', async ()=>{", "const _btn = document.getElementById('socialAnalyzeBtn'); if(_btn) { _btn.classList.add('analyzing'); _btn.innerHTML = 'ANALYZING...'; } try {"),
    ("document.getElementById('ocrRunBtn')?.addEventListener('click', async ()=>{", "const _btn = document.getElementById('ocrRunBtn'); if(_btn) { _btn.classList.add('analyzing'); _btn.innerHTML = 'ANALYZING...'; } try {"),
    ("document.getElementById('compVerifyBtn')?.addEventListener('click', async ()=>{", "const _btn = document.getElementById('compVerifyBtn'); if(_btn) { _btn.classList.add('analyzing'); _btn.innerHTML = 'VERIFYING...'; } try {")
]

for old, new_p in btn_pairs:
    html = html.replace(old, old + "\\n" + new_p)

# We need to remove the analyzing class and restore the text in a finally block... but Javascript try{} catch{} finally{} is hard to inject flawlessly with regex.
# Instead, let's inject a global fetch interceptor OR just use the `apiPost` function which wraps all requests!
# In apiPost, we can look at the active element (the button clicked) and animate it!

html = html.replace("async function apiPost(endpoint, body, isFormData = false, timeoutMs = 60000) {", 
"""async function apiPost(endpoint, body, isFormData = false, timeoutMs = 60000) {
  const activeBtn = document.activeElement;
  let originalHtml = '';
  if (activeBtn && activeBtn.tagName === 'BUTTON' && !activeBtn.classList.contains('analyzing')) {
      originalHtml = activeBtn.innerHTML;
      activeBtn.classList.add('analyzing');
      activeBtn.innerHTML = 'ANALYZING...';
  }
""")

html = html.replace("return await parseSafeResponse(response, endpoint);", 
"""
    if (activeBtn && originalHtml) {
        activeBtn.classList.remove('analyzing');
        activeBtn.innerHTML = originalHtml;
    }
    return await parseSafeResponse(response, endpoint);
""")

html = html.replace("throw err;", 
"""
    if (activeBtn && originalHtml) {
        activeBtn.classList.remove('analyzing');
        activeBtn.innerHTML = originalHtml;
    }
    throw err;
""")


# Ensure Risk Graph History uses real data animation
html = html.replace('const chHist = document.getElementById(\'dashChartRiskHistory\');',
"""const chHist = document.getElementById('dashChartRiskHistory');
  if (chHist && window.matchMedia('(prefers-reduced-motion: no-preference)').matches) {
     chHist.style.opacity = '0';
     setTimeout(() => { chHist.style.transition = 'opacity 0.8s ease'; chHist.style.opacity = '1'; }, 100);
  }
""")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Animations added successfully.")
