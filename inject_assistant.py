import re

with open(r"C:\Users\paruc\OneDrive\Desktop\project\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update HTML Header
old_head = """  <div class="assist-head">
    <div class="av"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M12 2a5 5 0 00-5 5v2a5 5 0 0010 0V7a5 5 0 00-5-5z"/><path d="M4 12v1a8 8 0 0016 0v-1M12 21v-4"/></svg></div>
    <div><b>TrustGuard AI Assistant</b><span>● Context-aware online</span></div>
    <button class="assist-close" id="assistClose">✕</button>
  </div>"""

new_head = """  <div class="assist-head" style="align-items:center;">
    <div class="av"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M12 2a5 5 0 00-5 5v2a5 5 0 0010 0V7a5 5 0 00-5-5z"/><path d="M4 12v1a8 8 0 0016 0v-1M12 21v-4"/></svg></div>
    <div style="flex:1;"><b>TrustGuard AI Assistant</b><span style="display:block;">● Context-aware online</span></div>
    <button class="btn btn-ghost btn-sm" id="assistClearBtn" style="font-size:10px; padding:2px 6px; margin-right:4px;">Clear Chat</button>
    <button class="assist-close" id="assistClose">✕</button>
  </div>
  <div id="assistContextBox" style="padding:6px 12px; background:rgba(45,217,232,0.05); border-bottom:1px solid var(--line); font-size:11px; line-height:1.4;">
    <b>CURRENT SCAN</b><br/><span style="color:var(--text-dim)">None</span>
  </div>"""

html = html.replace(old_head, new_head)

# 2. Add global variables
html = html.replace("let currentToken = localStorage.getItem('trustguard_token') || '';", "let currentToken = localStorage.getItem('trustguard_token') || '';\nlet conversationHistory = [];\nlet assistantLastScanId = null;")


# 3. Replace the JS logic
old_js = """function pushBotMsg(text){
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
}
document.getElementById('assistSendBtn')?.addEventListener('click', async ()=>{
  const inp = document.getElementById('assistInput');
  if(!inp || !inp.value.trim()) return;
  const q = inp.value.trim();
  pushUserMsg(q); inp.value='';
  try {
    const res = await apiPost('/api/assistant', { query: q, context: lastScanContext });
    if(res && (res.response || res.answer)) {
      pushBotMsg(res.response || res.answer);
      return;
    } else {
      pushBotMsg("AI Assistant is temporarily unavailable.");
    }
  } catch(e) {
    console.warn("Backend assistant API fallback:", e);
    pushBotMsg("AI Assistant is temporarily unavailable.");
  }
  // setTimeout(()=> pushBotMsg(assistantReply(q)), 300);
});"""

new_js = """function updateAssistantContextUI() {
  const ctxBox = document.getElementById('assistContextBox');
  if (!ctxBox) return;
  if (!lastScanContext) {
      ctxBox.innerHTML = `<b>CURRENT SCAN</b><br/><span style="color:var(--text-dim)">None</span>`;
      return;
  }
  const nm = lastScanContext.contentLabel || lastScanContext.contentType || 'Asset';
  const cl = lastScanContext.classification || 'UNKNOWN';
  const cf = lastScanContext.confidence !== undefined ? lastScanContext.confidence : 90;
  const rk = lastScanContext.score || lastScanContext.risk_score || 0;
  ctxBox.innerHTML = `<b>CURRENT SCAN</b><br/><span style="color:var(--cyan)">${nm}</span><br/><span style="font-size:10px;">${cl} • Conf: ${cf}% • Risk: ${rk}/100</span>`;
}

document.getElementById('assistClearBtn')?.addEventListener('click', ()=>{
  conversationHistory = [];
  const body = document.getElementById('assistBody');
  if(body) body.innerHTML = '';
});

function pushBotMsg(text, save=true){
  const body = document.getElementById('assistBody');
  if(!body) return;
  const div = document.createElement('div'); div.className='msg bot';
  let html = text.replace(/</g, '&lt;').replace(/>/g, '&gt;');
  html = html.replace(/\\*\\*(.*?)\\*\\*/g, '<b>$1</b>');
  html = html.replace(/\\n/g, '<br/>');
  div.innerHTML = html;
  body.appendChild(div); body.scrollTop = body.scrollHeight;
  if(save) conversationHistory.push({ role: 'assistant', content: text });
}

function pushUserMsg(text, save=true){
  const body = document.getElementById('assistBody');
  if(!body) return;
  const div = document.createElement('div'); div.className='msg user'; div.textContent = text;
  body.appendChild(div); body.scrollTop = body.scrollHeight;
  if(save) conversationHistory.push({ role: 'user', content: text });
}

document.getElementById('assistSendBtn')?.addEventListener('click', async ()=>{
  const inp = document.getElementById('assistInput');
  if(!inp || !inp.value.trim()) return;
  const q = inp.value.trim();
  pushUserMsg(q, true); 
  inp.value='';
  
  updateAssistantContextUI();
  
  const body = document.getElementById('assistBody');
  const thinkingId = 'think_' + Date.now();
  const divThink = document.createElement('div'); 
  divThink.className='msg bot'; 
  divThink.id = thinkingId;
  divThink.innerHTML = '<i>Thinking...</i>';
  body.appendChild(divThink); body.scrollTop = body.scrollHeight;

  // Provide only the history up to this question, minus the current question (which is passed as query)
  const historyToSend = conversationHistory.slice(0, -1);

  try {
    const res = await apiPost('/api/assistant', { 
        query: q, 
        current_scan_context: lastScanContext,
        conversation_history: historyToSend
    });
    
    document.getElementById(thinkingId)?.remove();
    
    if(res && (res.response || res.answer || res.reply)) {
      pushBotMsg(res.response || res.answer || res.reply, true);
    } else {
      pushBotMsg("AI Assistant is temporarily unavailable.", false);
    }
  } catch(e) {
    console.warn("Backend assistant API fallback:", e);
    document.getElementById(thinkingId)?.remove();
    pushBotMsg("AI Assistant is temporarily unavailable.", false);
  }
});
"""

# Just checking if old_js matches precisely by using regex or split to be safe
start_idx = html.find("function pushBotMsg(text){")
end_idx = html.find("document.getElementById('assistInput')?.addEventListener('keydown'")

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_js + html[end_idx:]
else:
    print("Could not find exact JS block to replace!")

with open(r"C:\Users\paruc\OneDrive\Desktop\project\index.html", "w", encoding="utf-8") as f:
    f.write(html)
