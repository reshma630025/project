# -*- coding: utf-8 -*-
"""
Injects the Fake Image Alert System, Alert Center, Live Microphone WAV recorder,
Live Camera snapshot workflow, and api.js integration into index.html.
"""

from pathlib import Path

def inject_features():
    html_path = Path("index.html")
    content = html_path.read_text(encoding="utf-8")

    # 1. Add api.js script tag in <head>
    if '<script src="/api.js"></script>' not in content:
        content = content.replace(
            '<script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>',
            '<script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>\n<script src="/api.js"></script>'
        )
        print("Injected /api.js script tag")

    # 2. Add High-Risk Alert Banner right above <main class="content">
    alert_banner_html = """
    <!-- ============ HIGH RISK / FAKE CONTENT ALERT BANNER ============ -->
    <div id="highRiskAlertBanner" style="display:none; margin:16px 28px 0; background:linear-gradient(90deg, rgba(242,73,92,.18), rgba(255,107,122,.08)); border:1px solid rgba(242,73,92,.45); border-radius:12px; padding:14px 18px; display:none; align-items:center; justify-content:space-between; gap:12px; box-shadow:0 8px 24px rgba(242,73,92,.25); animation:pulseGlow 2s infinite ease-in-out;">
      <div style="display:flex; align-items:center; gap:12px;">
        <div style="width:36px; height:36px; border-radius:10px; background:rgba(242,73,92,.25); color:var(--danger-2); display:flex; align-items:center; justify-content:center; font-size:18px; font-weight:bold; flex-shrink:0;">⚠️</div>
        <div>
          <strong id="alertBannerTitle" style="font-family:var(--disp); font-size:13.5px; color:var(--danger-2); display:block; letter-spacing:.3px;">ALERT: HIGH-RISK SYNTHETIC / FRAUD CONTENT DETECTED</strong>
          <span id="alertBannerDesc" style="font-size:11.5px; color:var(--text-dim); line-height:1.4;">The neural detector identified high synthetic anomalies or fraudulent coercion indicators. Exercise extreme caution.</span>
        </div>
      </div>
      <div style="display:flex; align-items:center; gap:8px; flex-shrink:0;">
        <button class="btn btn-outline btn-sm" id="muteAlertSoundBtn" style="font-size:11px; padding:4px 9px;">🔊 Sound: ON</button>
        <button class="btn btn-ghost btn-sm" onclick="document.getElementById('highRiskAlertBanner').style.display='none';" style="font-size:11px; padding:4px 9px;">Dismiss</button>
      </div>
    </div>
"""
    if '<main class="content">' in content and 'id="highRiskAlertBanner"' not in content:
        content = content.replace('<main class="content">', alert_banner_html + '\n    <main class="content">')
        print("Injected High-Risk Alert Banner")

    # 3. Enhance Alert Center (#notifPanel) in header
    old_notif_panel = """          <div class="dropdown-panel" id="notifPanel">
            <div style="padding:8px 10px 10px; font-weight:700; font-size:12.5px; border-bottom:1px solid var(--line); margin-bottom:6px;">Threat Alerts & Notifications</div>
            <div class="notif-item"><div class="notif-dot" style="background:var(--danger)"></div><div class="notif-text"><b>Deepfake Artifacts Flagged</b><span>Temporal frame anomaly identified</span></div></div>
            <div class="notif-item"><div class="notif-dot" style="background:var(--warn)"></div><div class="notif-text"><b>Suspicious Domain Intercepted</b><span>Shortener entropy > 4.2 bits</span></div></div>
            <div class="notif-item"><div class="notif-dot" style="background:var(--safe)"></div><div class="notif-text"><b>AI Engine Online</b><span>Vision ViT & STFT ready</span></div></div>
          </div>"""

    new_notif_panel = """          <div class="dropdown-panel" id="notifPanel" style="width:320px;">
            <div style="display:flex; align-items:center; justify-content:space-between; padding:8px 10px 10px; border-bottom:1px solid var(--line); margin-bottom:6px;">
              <b style="font-size:12.5px;">Alert Center</b>
              <div style="display:flex; gap:6px;">
                <button id="clearAlertsBtn" style="background:transparent; border:none; color:var(--text-faint); font-size:10.5px; cursor:pointer;">Clear All</button>
              </div>
            </div>
            <div id="alertCenterList" style="max-height:240px; overflow-y:auto; display:flex; flex-direction:column; gap:4px;">
              <div class="notif-item"><div class="notif-dot" style="background:var(--safe)"></div><div class="notif-text"><b>AI Telemetry Online</b><span>Vision ViT, STFT and heuristic engines ready.</span></div></div>
            </div>
          </div>"""

    if old_notif_panel in content:
        content = content.replace(old_notif_panel, new_notif_panel)
        print("Enhanced Alert Center dropdown in header")

    # 4. Enhance Live Camera markup to include snapshot preview and separate analyze button
    old_cam_section = """          <div class="action-row">
            <button class="btn btn-primary" id="camStartBtn">Start Camera</button>
            <button class="btn btn-ghost" id="camCaptureBtn" disabled>Capture Snapshot & Analyze</button>
            <button class="btn btn-outline" id="camStopBtn" disabled>Stop Camera</button>
          </div>
          <div class="result-wrap" id="camResult"></div>"""

    new_cam_section = """          <div id="camSnapshotPrevWrap" style="display:none; margin-top:14px; padding:12px; background:var(--panel-2); border:1px solid var(--line); border-radius:10px;">
            <div style="font-size:11px; font-weight:700; color:var(--cyan); text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">Captured Frame Preview</div>
            <img id="camSnapshotImg" style="max-height:220px; border-radius:8px; border:1px solid var(--line); display:block; margin:0 auto;" />
          </div>
          <div class="action-row">
            <button class="btn btn-primary" id="camStartBtn">Start Camera</button>
            <button class="btn btn-outline" id="camCaptureBtn" disabled>Capture Frame</button>
            <button class="btn btn-primary" id="camAnalyzeCaptureBtn" disabled>Analyze Frame</button>
            <button class="btn btn-outline" id="camStopBtn" disabled>Stop Camera</button>
          </div>
          <div class="result-wrap" id="camResult"></div>"""

    if old_cam_section in content:
        content = content.replace(old_cam_section, new_cam_section)
        print("Enhanced Live Camera controls and snapshot preview")

    # 5. Enhance Live Microphone markup to include status badge and live result container
    old_mic_section = """        <div class="card card-pad">
          <canvas id="liveMicCanvas" style="width:100%; height:120px; border-radius:10px; background:var(--panel-2); border:1px solid var(--line);"></canvas>
          <div style="margin-top:10px; font-size:12px; font-family:var(--mono);" id="liveMicStatus">Microphone Status: IDLE</div>
          <div class="action-row">
            <button class="btn btn-primary" id="liveMicStart">Start Listening</button>
            <button class="btn btn-outline" id="liveMicStop" disabled>Stop</button>
          </div>
        </div>"""

    new_mic_section = """        <div class="card card-pad">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <span style="font-size:11px; font-family:var(--mono); color:var(--text-faint); text-transform:uppercase;">Live Acoustic Waveform</span>
            <span class="chip-tag" id="liveMicStateBadge" style="font-size:10px; color:var(--text-faint);">STATE: READY</span>
          </div>
          <canvas id="liveMicCanvas" style="width:100%; height:120px; border-radius:10px; background:var(--panel-2); border:1px solid var(--line);"></canvas>
          <div style="margin-top:10px; font-size:12px; font-family:var(--mono); color:var(--text-dim);" id="liveMicStatus">Microphone Status: READY (Click Start Listening)</div>
          <div class="action-row">
            <button class="btn btn-primary" id="liveMicStart">Start Listening</button>
            <button class="btn btn-outline" id="liveMicStop" disabled>Stop & Analyze</button>
          </div>
          <div class="result-wrap" id="liveMicResult"></div>
        </div>"""

    if old_mic_section in content:
        content = content.replace(old_mic_section, new_mic_section)
        print("Enhanced Live Microphone controls and result wrapper")

    # 6. Add Alert Center, Sound Alert, Live Camera, and Live Microphone JavaScript functions
    features_js = """
/* ============ SOUND & ALERT CENTER SYSTEM ============ */
let alertSoundActive = true;
let alertHistoryList = [];

function playRiskAlertSound() {
  if (!alertSoundActive) return;
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) return;
    const ctx = new AudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(880, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(440, ctx.currentTime + 0.35);
    gain.gain.setValueAtTime(0.25, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.35);
    osc.start();
    osc.stop(ctx.currentTime + 0.35);
  } catch(e) {
    console.warn('Audio alert not available:', e);
  }
}

document.getElementById('muteAlertSoundBtn')?.addEventListener('click', (e) => {
  alertSoundActive = !alertSoundActive;
  e.target.textContent = alertSoundActive ? '🔊 Sound: ON' : '🔇 Sound: OFF';
  toast('Alert Sound', alertSoundActive ? 'Audio alert enabled' : 'Audio alert muted', 'info');
});

function triggerHighRiskAlert(norm, contentType, contentLabel) {
  const isHighRisk = norm.riskScore >= 50 || norm.classification.includes('AI') || norm.classification.includes('FAKE') || norm.classification.includes('SCAM') || norm.classification.includes('PHISHING');
  if (!isHighRisk) return;

  const banner = document.getElementById('highRiskAlertBanner');
  const bTitle = document.getElementById('alertBannerTitle');
  const bDesc = document.getElementById('alertBannerDesc');

  if (banner && bTitle && bDesc) {
    bTitle.textContent = `ALERT: ${norm.classification} DETECTED (${contentType.toUpperCase()})`;
    bDesc.textContent = `${contentLabel}: Evaluated with ${norm.confidence}% confidence and ${norm.riskScore}/100 risk. ${norm.explanation.slice(0, 100)}...`;
    banner.style.display = 'flex';
    banner.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  playRiskAlertSound();

  // Add to Alert Center
  const now = new Date();
  const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  const alertEntry = {
    time: timeStr,
    title: `${contentType} Flagged: ${norm.classification}`,
    detail: `${contentLabel} · Risk: ${norm.riskScore}/100 · Conf: ${norm.confidence}%`
  };
  alertHistoryList.unshift(alertEntry);
  renderAlertCenter();

  // Highlight notification dot
  const badgeDot = document.querySelector('.badge-dot');
  if (badgeDot) badgeDot.style.display = 'block';
}

function renderAlertCenter() {
  const container = document.getElementById('alertCenterList');
  if (!container) return;
  if (alertHistoryList.length === 0) {
    container.innerHTML = '<div style="padding:14px; text-align:center; color:var(--text-faint); font-size:11.5px;">No high-risk alerts recorded yet.</div>';
    return;
  }
  container.innerHTML = alertHistoryList.map(a => `
    <div class="notif-item">
      <div class="notif-dot" style="background:var(--danger)"></div>
      <div class="notif-text">
        <b style="color:var(--danger-2);">${a.title}</b>
        <span>${a.time} — ${a.detail}</span>
      </div>
    </div>
  `).join('');
}

document.getElementById('clearAlertsBtn')?.addEventListener('click', () => {
  alertHistoryList = [];
  renderAlertCenter();
  const badgeDot = document.querySelector('.badge-dot');
  if (badgeDot) badgeDot.style.display = 'none';
  toast('Alerts Cleared', 'Alert center history reset', 'info');
});

/* ============ UPGRADED LIVE CAMERA WORKFLOW ============ */
let capturedCameraBlob = null;

// Replace camera handlers
const origCamStart = document.getElementById('camStartBtn');
const origCamCapture = document.getElementById('camCaptureBtn');
const origCamAnalyze = document.getElementById('camAnalyzeCaptureBtn');
const origCamStop = document.getElementById('camStopBtn');

if (origCamCapture && origCamAnalyze) {
  origCamCapture.onclick = () => {
    const vid = document.getElementById('camVideo');
    if (!vid) return;
    const canvas = document.createElement('canvas');
    canvas.width = vid.videoWidth || 640;
    canvas.height = vid.videoHeight || 480;
    canvas.getContext('2d').drawImage(vid, 0, 0);
    canvas.toBlob(blob => {
      capturedCameraBlob = blob;
      const prevWrap = document.getElementById('camSnapshotPrevWrap');
      const prevImg = document.getElementById('camSnapshotImg');
      if (prevWrap && prevImg) {
        prevImg.src = URL.createObjectURL(blob);
        prevWrap.style.display = 'block';
      }
      origCamAnalyze.disabled = false;
      toast('Frame Captured', 'Ready to analyze frame with Vision Transformer', 'safe');
    }, 'image/jpeg');
  };

  origCamAnalyze.onclick = async () => {
    if (!capturedCameraBlob) {
      toast('No frame', 'Capture a frame first', 'warn');
      return;
    }
    toast('Analyzing Frame…', 'Sending to Vision Transformer detector', 'info');
    origCamAnalyze.disabled = true;
    try {
      const apiRes = await window.tgAPI.analyzeCameraFrame(capturedCameraBlob);
      const norm = normalizePrediction(apiRes, 'Live Camera', 'Webcam Snapshot');
      const wrap = document.getElementById('camResult');
      if (wrap) {
        wrap.innerHTML = renderUnifiedResultCard(norm, { contentType: 'Live Camera', contentLabel: 'Webcam Snapshot' });
        wrap.classList.add('show');
        attachResultActions(wrap, { ...norm, contentType: 'Live Camera', contentLabel: 'Webcam Snapshot', date: Date.now() });
      }
      pushHistory({ contentLabel: 'Webcam Snapshot', contentType: 'Camera', score: norm.riskScore, trust: norm.trustScore, confidence: norm.confidence, date: Date.now() });
      triggerHighRiskAlert(norm, 'Camera', 'Webcam Snapshot');
      toast(norm.isGenuine ? '✓ Genuine Camera Frame' : '⚠ Anomaly Detected', `Risk: ${norm.riskScore}/100`, norm.isGenuine ? 'safe' : 'danger');
    } catch(err) {
      toast('Camera Analysis Failed', err.message, 'danger');
    } finally {
      origCamAnalyze.disabled = false;
    }
  };
}

/* ============ UPGRADED LIVE MICROPHONE RECORDER ============ */
let liveMediaRecorder = null;
let recordedAudioChunks = [];

const liveMicStartBtn = document.getElementById('liveMicStart');
const liveMicStopBtn = document.getElementById('liveMicStop');
const liveMicBadge = document.getElementById('liveMicStateBadge');

if (liveMicStartBtn && liveMicStopBtn) {
  liveMicStartBtn.onclick = async () => {
    try {
      recordedAudioChunks = [];
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      liveMicStream = stream;
      liveMicCtx = new (window.AudioContext || window.webkitAudioContext)();
      const src = liveMicCtx.createMediaStreamSource(stream);
      const analyser = liveMicCtx.createAnalyser();
      analyser.fftSize = 256;
      src.connect(analyser);

      const canvas = document.getElementById('liveMicCanvas');
      const ctx = canvas.getContext('2d');
      const bufferLength = analyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      function drawWave(){
        liveMicRAF = requestAnimationFrame(drawWave);
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
      drawWave();

      // Setup MediaRecorder
      liveMediaRecorder = new MediaRecorder(stream);
      liveMediaRecorder.ondataavailable = e => {
        if (e.data && e.data.size > 0) recordedAudioChunks.push(e.data);
      };
      liveMediaRecorder.start(250);

      liveMicStartBtn.disabled = true;
      liveMicStopBtn.disabled = false;
      if (liveMicBadge) { liveMicBadge.textContent = 'STATE: RECORDING…'; liveMicBadge.style.color = 'var(--danger-2)'; }
      document.getElementById('liveMicStatus').textContent = 'Microphone Status: RECORDING (Acoustic audio buffer capturing)';
      document.getElementById('liveMicStatus').style.color = 'var(--danger-2)';
      toast('Recording Live Audio', 'Speak into microphone for forensic voice analysis', 'safe');
    } catch(err) {
      toast('Microphone Denied', 'Microphone permission was denied or device unavailable.', 'danger');
    }
  };

  liveMicStopBtn.onclick = () => {
    if (liveMicBadge) { liveMicBadge.textContent = 'STATE: ANALYZING…'; liveMicBadge.style.color = 'var(--warn)'; }
    document.getElementById('liveMicStatus').textContent = 'Microphone Status: PROCESSING (Executing STFT spectral forensics)';
    document.getElementById('liveMicStatus').style.color = 'var(--warn)';
    liveMicStopBtn.disabled = true;

    if (liveMediaRecorder && liveMediaRecorder.state !== 'inactive') {
      liveMediaRecorder.onstop = async () => {
        const audioBlob = new Blob(recordedAudioChunks, { type: 'audio/wav' });
        if (liveMicStream) liveMicStream.getTracks().forEach(t => t.stop());
        if (liveMicCtx) liveMicCtx.close();
        cancelAnimationFrame(liveMicRAF);

        toast('Analyzing voice…', 'Executing STFT spectral forensics', 'info');
        try {
          const apiRes = await window.tgAPI.analyzeLiveAudio(audioBlob);
          const norm = normalizePrediction(apiRes, 'Live Voice', 'Microphone Audio');
          const wrap = document.getElementById('liveMicResult');
          if (wrap) {
            wrap.innerHTML = renderUnifiedResultCard(norm, { contentType: 'Live Voice', contentLabel: 'Microphone Stream Sample' });
            wrap.classList.add('show');
            attachResultActions(wrap, { ...norm, contentType: 'Live Voice', contentLabel: 'Microphone Stream Sample', date: Date.now() });
          }
          pushHistory({ contentLabel: 'Microphone Stream Sample', contentType: 'Audio', score: norm.riskScore, trust: norm.trustScore, confidence: norm.confidence, date: Date.now() });
          triggerHighRiskAlert(norm, 'Live Voice', 'Microphone Stream Sample');
          toast(norm.isGenuine ? '✓ Authentic Human Voice' : '⚠ Synthetic Voice Flagged', `Risk: ${norm.riskScore}/100`, norm.isGenuine ? 'safe' : 'danger');
        } catch(err) {
          toast('Voice Analysis Failed', err.message, 'danger');
        } finally {
          liveMicStartBtn.disabled = false;
          if (liveMicBadge) { liveMicBadge.textContent = 'STATE: READY'; liveMicBadge.style.color = 'var(--text-faint)'; }
          document.getElementById('liveMicStatus').textContent = 'Microphone Status: READY';
          document.getElementById('liveMicStatus').style.color = 'var(--text-dim)';
        }
      };
      liveMediaRecorder.stop();
    }
  };
}
"""

    if '/* ============ SOUND & ALERT CENTER SYSTEM ============ */' not in content:
        content = content.replace('/* ============ INITIALIZATION ============ */', features_js + '\n/* ============ INITIALIZATION ============ */')
        print("Injected Sound, Alert Center, Camera and Live Mic JavaScript")

    html_path.write_text(content, encoding="utf-8")
    print(f"Updated index.html successfully ({len(content)} bytes)")

if __name__ == "__main__":
    inject_features()
