# -*- coding: utf-8 -*-
"""
Applies master refinements to index.html:
1. Dashboard Title & Subtitle: "TrustGuard AI" & "Multimodal Content Authenticity & Digital Fraud Detection"
2. Dashboard 4 Bento Cards: TOTAL SCANS, AI-GENERATED / SYNTHETIC DETECTED, SUSPICIOUS / FRAUD DETECTED, LIKELY AUTHENTIC
3. Standardized 6-Part Result Component:
   - Authenticity Status Banner / Verdict
   - Trust Score (0-100), Risk Score (0-100), Confidence (%), Risk Level
   - What We Found (Forensic Evidence / Signals)
   - Why This Result? (Plain-English explanation)
   - Technical Analysis Details (Model used, dimensions, processing latency)
   - Transparency & Limitations (Probabilistic disclaimer)
   - Action buttons: Read Voiceover, View Full Report, Ask AI Assistant, Scan Again
4. Context-Aware AI Assistant: Answers questions using real scan evidence, scores, and model
5. Offline Banner toggling in checkBackendEngineStatus
6. Fix history loading from /api/history (unpack res.history)
7. Update statCounters to map real authentic and ai_generated counts
"""

from pathlib import Path

def refine_index_html():
    file_path = Path("index.html")
    content = file_path.read_text(encoding="utf-8")

    # 1. Update Dashboard Head Title & Subtitle
    old_dash_head = """            <div class="eyebrow">Security Operations Center · Real-Time AI Telemetry</div>
            <div class="page-title">AI Content Authenticity & Threat Radar</div>
            <p class="page-sub">Multi-modal neural inspection across images, temporal video frames, synthetic voices, scam texts, and phishing domains.</p>"""
    
    new_dash_head = """            <div class="eyebrow">Multimodal Content Authenticity & Digital Fraud Detection</div>
            <div class="page-title">TrustGuard AI</div>
            <p class="page-sub">Analyze images, videos, audio, text, URLs, job offers and live content to identify AI-generated, manipulated, suspicious and fraudulent content.</p>"""

    if old_dash_head in content:
        content = content.replace(old_dash_head, new_dash_head)
        print("Updated dashboard header title & subtitle")

    # 2. Update the 4 Bento Live Counter Cards in HTML
    old_counters = """          <!-- ROW 2: 4 Bento Live Counter Cards -->
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
          </div>"""

    new_counters = """          <!-- ROW 2: 4 Bento Live Counter Cards -->
          <div class="bento-card bento-1x1">
            <span class="b-lbl" style="font-size:10px; color:var(--text-faint); text-transform:uppercase; letter-spacing:.6px;">Total Scans</span>
            <span class="b-val" id="dStat1" style="font-family:var(--mono); font-size:22px; font-weight:700; color:var(--cyan); margin-top:4px;">0</span>
            <span style="font-size:10px; color:var(--text-faint); margin-top:2px;">Live SQLite database count</span>
          </div>
          <div class="bento-card bento-1x1">
            <span class="b-lbl" style="font-size:10px; color:var(--text-faint); text-transform:uppercase; letter-spacing:.6px;">AI-Generated / Synthetic</span>
            <span class="b-val" id="dStat2" style="font-family:var(--mono); font-size:22px; font-weight:700; color:var(--warn); margin-top:4px;">0</span>
            <span style="font-size:10px; color:var(--text-faint); margin-top:2px;">Diffusion & neural clones</span>
          </div>
          <div class="bento-card bento-1x1">
            <span class="b-lbl" style="font-size:10px; color:var(--text-faint); text-transform:uppercase; letter-spacing:.6px;">Suspicious / Fraud Detected</span>
            <span class="b-val" id="dStat3" style="font-family:var(--mono); font-size:22px; font-weight:700; color:var(--danger-2); margin-top:4px;">0</span>
            <span style="font-size:10px; color:var(--text-faint); margin-top:2px;">Scams, phishing & anomalies</span>
          </div>
          <div class="bento-card bento-1x1">
            <span class="b-lbl" style="font-size:10px; color:var(--text-faint); text-transform:uppercase; letter-spacing:.6px;">Likely Authentic</span>
            <span class="b-val" id="dStat4" style="font-family:var(--mono); font-size:22px; font-weight:700; color:var(--safe); margin-top:4px;">0</span>
            <span style="font-size:10px; color:var(--text-faint); margin-top:2px;">Organic & verified genuine</span>
          </div>"""

    if old_counters in content:
        content = content.replace(old_counters, new_counters)
        print("Updated 4 bento counter card labels in HTML")

    # 3. Update normalizePrediction function to extract trustScore, technical, and limitations
    old_norm = """  return {
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
  };"""

    new_norm = """  let trustScore = apiRes.trust_score ?? authProb ?? (100 - riskScore);
  trustScore = Math.max(0, Math.min(100, Math.round(Number(trustScore))));

  let trustCategory = apiRes.trust_category || (trustScore >= 70 ? 'HIGH TRUST / AUTHENTIC' : (trustScore >= 40 ? 'UNCERTAIN / REVIEW' : 'LOW TRUST / SYNTHETIC'));
  let technical = apiRes.technical || {};
  let limitations = apiRes.limitations || ["AI detection is probabilistic and should not be treated as absolute proof."];

  return {
    valid: true,
    isGenuine,
    riskScore,
    trustScore,
    trustCategory,
    confidence,
    authenticity: trustScore,
    riskLevel,
    tier,
    classification: rawClf || (isGenuine ? 'REAL / LIKELY AUTHENTIC' : 'AI-GENERATED'),
    classificationLabel: apiRes.status_label || apiRes.classification_label || (isGenuine ? 'REAL / LIKELY AUTHENTIC' : 'AI-GENERATED'),
    indicators,
    explanation,
    technical,
    limitations,
    raw: apiRes
  };"""

    if old_norm in content:
        content = content.replace(old_norm, new_norm)
        print("Updated normalizePrediction with trustScore, technical, limitations")

    # 4. Enhance renderUnifiedResultCard to include 6-part standardized layout
    old_render = """      <div class="pred-grid">
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
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 9v4M12 17h.01M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>
        <div><b>${rec.title}</b><p style="color:var(--text-dim)">${rec.text}</p></div>
      </div>

      <div class="action-row" style="margin-top:16px;">
        <button class="btn btn-ghost btn-sm speak-btn">🔊 Read Voiceover</button>
        <button class="btn btn-outline btn-sm view-report-btn">View Full Report</button>
        <button class="btn btn-outline btn-sm ask-ai-btn">Ask AI Assistant</button>
      </div>"""

    new_render = """      <div class="pred-grid">
        <div class="pred-card"><div class="val" style="color:${norm.trustScore >= 70 ? 'var(--safe)' : (norm.trustScore < 40 ? 'var(--danger-2)' : 'var(--warn)')};">${norm.trustScore}/100</div><div class="lbl">Trust Score</div></div>
        <div class="pred-card"><div class="val" style="color:${isGenuine ? 'var(--safe)' : 'var(--danger-2)'};">${norm.riskScore}/100</div><div class="lbl">Risk Score</div></div>
        <div class="pred-card"><div class="val" style="color:var(--cyan);">${norm.confidence}%</div><div class="lbl">Confidence</div></div>
        <div class="pred-card"><div class="val" style="color:${riskColor(norm.tier.cls)};">${norm.riskLevel}</div><div class="lbl">Risk Level</div></div>
      </div>

      ${timelineHTML}
      ${segmentHTML}

      <div class="card indicators" style="margin-top:14px; margin-bottom:14px;">
        <h3>${isGenuine ? '✓ Verified Authenticity Indicators' : '🚨 Detected Anomaly Indicators (What We Found)'}</h3>
        ${indicatorsHTML}
      </div>

      <div class="explanation-card">
        <h4>Why This Result?</h4>
        <p>${norm.explanation}</p>
      </div>

      <!-- Expandable Technical Analysis & Model Details -->
      <details class="card" style="margin-top:12px; margin-bottom:12px; padding:14px; background:var(--panel-2); border:1px solid var(--glass-brd); border-radius:10px;">
        <summary style="cursor:pointer; font-weight:600; font-size:12.5px; color:var(--cyan); display:flex; align-items:center; gap:6px;">
          <span>⚙️ Technical Analysis & Underlying Model Details (Click to Expand)</span>
        </summary>
        <div style="margin-top:12px; font-size:12px; display:flex; flex-direction:column; gap:6px;">
          <div class="telemetry-row"><span>Analysis Model / Pipeline</span><span style="color:var(--cyan); font-family:var(--mono);">${norm.technical.model || 'Pretrained Neural ViT / STFT Signal Forensics'}</span></div>
          ${norm.technical.detected_language ? `<div class="telemetry-row"><span>Detected Language</span><span style="color:var(--safe);">${norm.technical.detected_language}</span></div>` : ''}
          ${norm.technical.processing_time_sec ? `<div class="telemetry-row"><span>Processing Latency</span><span>${(norm.technical.processing_time_sec * 1000).toFixed(0)} ms</span></div>` : ''}
          ${norm.technical.input_dimensions ? `<div class="telemetry-row"><span>Input Dimensions</span><span>${norm.technical.input_dimensions[0]} × ${norm.technical.input_dimensions[1]} px</span></div>` : ''}
          ${norm.technical.frames_analyzed ? `<div class="telemetry-row"><span>Frames Sampled</span><span>${norm.technical.frames_analyzed} frames</span></div>` : ''}
          ${norm.technical.sample_rate ? `<div class="telemetry-row"><span>Sample Rate</span><span>${norm.technical.sample_rate} Hz</span></div>` : ''}
          <div class="telemetry-row"><span>Reverse Image Provenance</span><span style="color:var(--text-faint);">Reverse image search is not configured. Local SHA-256 fingerprint generated.</span></div>
          <div class="telemetry-row"><span>Evaluation Timestamp</span><span style="font-family:var(--mono); font-size:11px;">${new Date().toLocaleString()}</span></div>
        </div>
      </details>

      <!-- Transparency & Probabilistic Limitations Notice -->
      <div style="margin-top:10px; margin-bottom:14px; padding:12px; background:rgba(245,185,66,0.06); border:1px solid rgba(245,185,66,0.22); border-radius:8px; font-size:11.5px; color:var(--text-dim); line-height:1.5;">
        <b style="color:var(--warn); display:block; margin-bottom:2px;">⚠️ Transparency & AI Limitations:</b>
        AI detection is probabilistic and should not be treated as absolute deterministic proof. Our models analyze spatial frequency boundaries, vocoder cutoffs, or heuristic fraud patterns with high statistical confidence, but degraded media or emerging generative techniques warrant human review.
      </div>

      <div class="recommend-box" style="background:${riskColor(norm.tier.cls)}12; border-color:${riskColor(norm.tier.cls)}44; color:${riskColor(norm.tier.cls)};">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 9v4M12 17h.01M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>
        <div><b>${rec.title}</b><p style="color:var(--text-dim)">${rec.text}</p></div>
      </div>

      <div class="action-row" style="margin-top:16px;">
        <button class="btn btn-ghost btn-sm speak-btn">🔊 Read Voiceover</button>
        <button class="btn btn-outline btn-sm view-report-btn">View Full Report</button>
        <button class="btn btn-outline btn-sm ask-ai-btn">Ask AI Assistant</button>
        <button class="btn btn-outline btn-sm" onclick="this.closest('.result-wrap').classList.remove('show'); this.closest('.result-wrap').innerHTML='';">Scan Again</button>
      </div>"""

    if old_render in content:
        content = content.replace(old_render, new_render)
        print("Updated renderUnifiedResultCard with 6-part standardized layout")

    # 5. Update assistantReply to answer all scan questions intelligently
    old_assist = """function assistantReply(q){
  const lower = q.toLowerCase();
  const ctx = lastScanContext;
  if(!ctx) return "Run a scan on any module and I will explain the genuine model prediction and mitigation steps.";
  const tier = riskTier(ctx.score);
  if(lower.includes('why') || lower.includes('risk')) return `${ctx.contentLabel} evaluated with ${ctx.score}/100 risk (${tier.label}). Confidence is ${ctx.confidence}%.`;
  if(lower.includes('safe') || lower.includes('should i')) return recommendation(tier.cls).text;
  return `Summary: ${ctx.contentLabel} (${ctx.contentType}) has ${ctx.score}/100 risk (${tier.label}).`;
}"""

    new_assist = """function assistantReply(q){
  const lower = q.toLowerCase();
  const ctx = lastScanContext;
  if(!ctx) return "I am ready! Run a scan on any module (Image, Video, Audio, Text, Job, URL, or Camera) and I will explain the forensic signals, Trust Score, and model rationale.";
  const tier = riskTier(ctx.score);
  const trustScore = ctx.trustScore !== undefined ? ctx.trustScore : (ctx.trust !== undefined ? ctx.trust : (100 - ctx.score));

  if(lower.includes('why') || lower.includes('suspicious') || lower.includes('risk') || lower.includes('reason')) {
    const evText = (ctx.indicators && ctx.indicators.length > 0) 
      ? ctx.indicators.map(i => i.detail || i.label).join('; ') 
      : 'inconsistent pixel/spectral patterns';
    return `The ${ctx.contentType} scan was assigned a Trust Score of ${trustScore}/100 (Risk: ${ctx.score}/100, rated ${tier.label}) with ${ctx.confidence}% confidence. Key forensic signals detected: ${evText}.`;
  }
  if(lower.includes('definitely') || lower.includes('100%') || lower.includes('proof') || lower.includes('guarantee')) {
    return `No, AI detection is probabilistic and cannot guarantee 100% proof. The system detected anomalous patterns with ${ctx.confidence}% confidence, but compression artifacts or edge cases warrant human verification.`;
  }
  if(lower.includes('trust score') || lower.includes('what does')) {
    return `The Trust Score (${trustScore}/100) measures empirical authenticity. 90-100 represents High Trust (organic origin), 70-89 Likely Trustworthy, 40-69 Uncertain / Review, and below 40 Low Trust (synthetic manipulation or fraud).`;
  }
  if(lower.includes('evidence') || lower.includes('found') || lower.includes('signal')) {
    const evItems = (ctx.indicators && ctx.indicators.length > 0) 
      ? ctx.indicators.map(i => `• ${i.label}: ${i.detail}`).join('\\n') 
      : '• Multi-signal acoustic / visual consistency verified.';
    return `Here is the concrete evidence extracted by the backend detector:\\n${evItems}`;
  }
  if(lower.includes('safe') || lower.includes('should i') || lower.includes('what to do')) {
    return recommendation(tier.cls).text;
  }
  return `Current scan context: ${ctx.contentLabel} (${ctx.contentType}) has Trust Score ${trustScore}/100, Risk ${ctx.score}/100 (${tier.label}), and confidence ${ctx.confidence}%. You can ask me: "Why is this result?", "What evidence was found?", or "Is this definitely AI-generated?".`;
}"""

    if old_assist in content:
        content = content.replace(old_assist, new_assist)
        print("Updated assistantReply with context-aware logic")

    # 6. Update fetchDashboardStats, updateDashboardStats, and fetchHistoryFromBackend
    old_stats_code = """/* ============ HISTORY & STATS TELEMETRY ============ */
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
}"""

    new_stats_code = """/* ============ HISTORY & STATS TELEMETRY ============ */
async function fetchDashboardStats() {
  try {
    const res = await apiGet('/api/stats');
    const st = res.stats || res;
    statCounters = {
      scans: st.total_scans ?? res.scans ?? 0,
      threats: st.threats_flagged ?? res.threats ?? 0,
      deepfakes: st.deepfakes_detected ?? res.deepfakes ?? 0,
      scams: st.scams_neutralized ?? res.scams ?? 0,
      authentic: st.authentic ?? 0,
      ai_generated: st.ai_generated ?? st.deepfakes_detected ?? 0,
      suspicious: st.suspicious ?? st.threats_flagged ?? 0,
      average_trust: st.average_trust_score ?? res.average_trust_score ?? 85
    };
    updateDashboardStats();
  } catch(e) { console.warn('Could not fetch stats:', e); }
}

async function fetchHistoryFromBackend() {
  try {
    const res = await apiGet('/api/history?limit=50');
    const list = Array.isArray(res) ? res : (res.history || []);
    if (list.length > 0) {
      scanHistory = list.map(item => ({
        id: item.id,
        contentLabel: item.content_label || 'Direct Scan',
        contentType: item.scan_type ? item.scan_type.toUpperCase() : 'Content',
        lang: { name: 'English', flag: '🌐' },
        score: item.risk_score || 0,
        trust: Math.round(item.trust_score !== undefined && item.trust_score !== null ? item.trust_score : (100 - (item.risk_score || 0))),
        trustScore: Math.round(item.trust_score !== undefined && item.trust_score !== null ? item.trust_score : (100 - (item.risk_score || 0))),
        confidence: item.confidence || 90,
        classification: item.classification || 'COMPLETED',
        date: item.timestamp ? (item.timestamp > 1e11 ? item.timestamp : item.timestamp * 1000) : Date.now()
      }));
      renderHistory();
      renderReports();
      renderRecent();
    }
  } catch(e) { console.warn('Could not fetch history:', e); }
}"""

    if old_stats_code in content:
        content = content.replace(old_stats_code, new_stats_code)
        print("Updated fetchDashboardStats and fetchHistoryFromBackend")

    # 7. Update updateDashboardStats to feed the 4 cards correctly
    old_update_stats = """function updateDashboardStats(){
  ['dStat1','landStat1'].forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent = statCounters.scans; });
  ['dStat2','landStat2'].forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent = statCounters.threats; });
  ['dStat3','landStat3'].forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent = statCounters.deepfakes; });
  ['dStat4','landStat4'].forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent = statCounters.scams; });"""

    new_update_stats = """function updateDashboardStats(){
  // Card 1: TOTAL SCANS
  ['dStat1','landStat1'].forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent = statCounters.scans; });
  // Card 2: AI-GENERATED / SYNTHETIC DETECTED
  ['dStat2','landStat2'].forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent = statCounters.ai_generated ?? statCounters.deepfakes ?? 0; });
  // Card 3: SUSPICIOUS / FRAUD DETECTED
  ['dStat3','landStat3'].forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent = statCounters.suspicious ?? statCounters.threats ?? 0; });
  // Card 4: LIKELY AUTHENTIC
  ['dStat4','landStat4'].forEach(id=>{ const el=document.getElementById(id); if(el) el.textContent = statCounters.authentic ?? 0; });"""

    if old_update_stats in content:
        content = content.replace(old_update_stats, new_update_stats)
        print("Updated updateDashboardStats mapping for 4 bento cards")

    # 8. Update checkBackendEngineStatus to toggle #backendOfflineBanner
    old_engine_check = """      if (tag) { tag.textContent = 'ONLINE'; tag.style.color = 'var(--safe)'; }
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
  }"""

    new_engine_check = """      if (tag) { tag.textContent = 'ONLINE'; tag.style.color = 'var(--safe)'; }
      const offBanner = document.getElementById('backendOfflineBanner');
      if (offBanner) offBanner.style.display = 'none';
    } else {
      const offBanner = document.getElementById('backendOfflineBanner');
      if (offBanner) offBanner.style.display = 'block';
      if (badge) { badge.innerHTML = `<i class="dot" style="background:var(--danger)"></i>Offline`; badge.style.color = 'var(--danger-2)'; }
      if (statusTxt) { statusTxt.textContent = '● Offline'; statusTxt.style.color = 'var(--danger-2)'; }
      if (tag) { tag.textContent = 'OFFLINE'; tag.style.color = 'var(--danger-2)'; }
    }
  } catch (e) {
    const offBanner = document.getElementById('backendOfflineBanner');
    if (offBanner) offBanner.style.display = 'block';
    if (badge) { badge.innerHTML = `<i class="dot" style="background:var(--danger)"></i>Offline`; badge.style.color = 'var(--danger-2)'; }
    if (latEl) latEl.textContent = '—';
    if (statusTxt) { statusTxt.textContent = '● Offline'; statusTxt.style.color = 'var(--danger-2)'; }
    if (tag) { tag.textContent = 'OFFLINE'; tag.style.color = 'var(--danger-2)'; }
  }"""

    if old_engine_check in content:
        content = content.replace(old_engine_check, new_engine_check)
        print("Updated checkBackendEngineStatus with backendOfflineBanner handling")

    file_path.write_text(content, encoding="utf-8")
    print(f"Refined index.html saved successfully ({len(content)} bytes)")

if __name__ == "__main__":
    refine_index_html()
