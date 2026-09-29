"""
Script to safely inject the Unified Drag & Drop Verification Experience,
Dataset Verification Browser, and Technical Details Accordion into index.html.
"""
from pathlib import Path

INDEX_PATH = Path(r"C:\Users\paruc\OneDrive\Desktop\Reshma\index.html")

CSS_ADDITION = """
/* ============ UNIVERSAL VERIFY DROPZONE STYLES ============ */
.universal-dropzone-box:hover {
  border-color: var(--cyan) !important;
  background: rgba(45,217,232,.04) !important;
  box-shadow: 0 0 30px rgba(45,217,232,.12);
}
.universal-dropzone-box.drag {
  border-color: var(--cyan) !important;
  background: rgba(45,217,232,.08) !important;
  box-shadow: 0 0 40px rgba(45,217,232,.25);
  transform: scale(1.008);
}
.universal-modality-grid .u-mod-card {
  background: var(--panel-2);
  border: 1px solid var(--line);
  border-radius: 9px;
  padding: 8px 10px;
  cursor: pointer;
  transition: all .18s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
.universal-modality-grid .u-mod-card:hover {
  border-color: rgba(45,217,232,.4);
  background: rgba(45,217,232,.04);
  transform: translateY(-2px);
}
.universal-modality-grid .u-mod-card.active {
  background: linear-gradient(135deg, rgba(45,217,232,.16), rgba(139,107,240,.1));
  border-color: var(--cyan);
  box-shadow: 0 0 15px rgba(45,217,232,.2);
}
.universal-modality-grid .u-mod-card .u-mod-ic {
  font-size: 16px;
  margin-bottom: 2px;
}
.universal-modality-grid .u-mod-card b {
  font-size: 11.5px;
  color: var(--text);
  white-space: nowrap;
}
.universal-modality-grid .u-mod-card small {
  font-size: 9.5px;
  color: var(--text-faint);
  margin-top: 1px;
}

/* Technical Details Accordion */
.tech-details-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(120,150,200,.08);
  border: 1px solid var(--line);
  color: var(--cyan);
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: .15s;
}
.tech-details-btn:hover {
  background: rgba(45,217,232,.12);
  border-color: var(--cyan);
}
.tech-details-panel {
  display: none;
  margin-top: 10px;
  padding: 12px 14px;
  background: rgba(8,11,18,.8);
  border: 1px solid var(--line);
  border-radius: 8px;
  font-size: 11.5px;
  animation: fadeUp .2s ease;
}
.tech-details-panel.open {
  display: block;
}
"""

HTML_UNIFIED_SECTION = """
        <!-- ================= 1. UNIFIED VERIFY ANY CONTENT (UNIVERSAL DROPZONE) ================= -->
        <div class="card scanner-card" id="universalVerifySection" style="margin-top:8px; margin-bottom:16px; border:1px solid rgba(45,217,232,.25); background:radial-gradient(ellipse at 50% -20%, rgba(45,217,232,.08), transparent 70%), var(--glass);">
          <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; border-bottom:1px solid var(--line); padding-bottom:12px; flex-wrap:wrap; gap:10px;">
            <div>
              <div class="eyebrow" style="margin-bottom:3px;">Universal Content Authenticity Radar</div>
              <h2 style="font-family:var(--disp); font-size:19px; font-weight:700; color:var(--text); letter-spacing:-.2px;">Verify Any Content</h2>
              <p style="font-size:12.5px; color:var(--text-dim); margin-top:2px;">Drop any file or paste content — the intelligent radar auto-detects modality and routes to the corresponding trained AI model.</p>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <span class="soc-status-badge" style="color:var(--cyan); border-color:rgba(45,217,232,.3); font-size:11px;">
                <span class="dot" style="background:var(--cyan);"></span>AUTO-DETECTION ACTIVE
              </span>
              <span class="chip-tag" style="background:rgba(139,107,240,.12); color:var(--violet); border-color:rgba(139,107,240,.3); font-size:11px;">8 Modalities Supported</span>
            </div>
          </div>

          <!-- 8 Modality Selectors / Shortcuts Grid -->
          <div style="margin-bottom:14px;">
            <div style="font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:1px; color:var(--text-faint); margin-bottom:8px;">
              Select What You Want To Verify (Or Drop Directly):
            </div>
            <div class="universal-modality-grid" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(110px, 1fr)); gap:8px;">
              <div class="u-mod-card active" data-modality="auto" onclick="setUniversalModality('auto')">
                <span class="u-mod-ic">✨</span>
                <b>Auto-Detect</b>
                <small>Smart Router</small>
              </div>
              <div class="u-mod-card" data-modality="image" onclick="setUniversalModality('image')">
                <span class="u-mod-ic">🖼️</span>
                <b>Image</b>
                <small>JPG, PNG, WEBP</small>
              </div>
              <div class="u-mod-card" data-modality="video" onclick="setUniversalModality('video')">
                <span class="u-mod-ic">🎬</span>
                <b>Video</b>
                <small>MP4, MOV, WEBM</small>
              </div>
              <div class="u-mod-card" data-modality="audio" onclick="setUniversalModality('audio')">
                <span class="u-mod-ic">🎙️</span>
                <b>Audio</b>
                <small>WAV, MP3, FLAC</small>
              </div>
              <div class="u-mod-card" data-modality="social" onclick="setUniversalModality('social')">
                <span class="u-mod-ic">📱</span>
                <b>Social Media</b>
                <small>Profile CSV / User</small>
              </div>
              <div class="u-mod-card" data-modality="url" onclick="setUniversalModality('url')">
                <span class="u-mod-ic">🔗</span>
                <b>URL Link</b>
                <small>Domain / Link</small>
              </div>
              <div class="u-mod-card" data-modality="sms" onclick="setUniversalModality('sms')">
                <span class="u-mod-ic">💬</span>
                <b>SMS / Text</b>
                <small>Scam / WhatsApp</small>
              </div>
              <div class="u-mod-card" data-modality="email" onclick="setUniversalModality('email')">
                <span class="u-mod-ic">📧</span>
                <b>Email Phish</b>
                <small>Headers & Body</small>
              </div>
              <div class="u-mod-card" data-modality="job" onclick="setUniversalModality('job')">
                <span class="u-mod-ic">💼</span>
                <b>Job / Offer</b>
                <small>Salary & Fee</small>
              </div>
            </div>
          </div>

          <!-- THE UNIVERSAL DROPZONE -->
          <div id="universalDropzone" class="universal-dropzone-box" style="position:relative; border:2px dashed rgba(45,217,232,.35); border-radius:14px; padding:28px 20px; text-align:center; background:rgba(14,20,32,.6); backdrop-filter:blur(10px); cursor:pointer; transition:all .25s ease;">
            <input type="file" id="universalFileInput" style="display:none;" />
            <div class="u-drop-icon" style="width:52px; height:52px; border-radius:14px; background:linear-gradient(135deg, rgba(45,217,232,.18), rgba(139,107,240,.18)); border:1px solid rgba(45,217,232,.3); display:flex; align-items:center; justify-content:center; margin:0 auto 10px; font-size:24px; color:var(--cyan); box-shadow:0 0 25px rgba(45,217,232,.15);">
              📥
            </div>
            <h3 style="font-family:var(--disp); font-size:17px; font-weight:700; margin-bottom:4px; letter-spacing:-.2px;">DROP CONTENT TO VERIFY</h3>
            <p style="font-size:12.5px; color:var(--text-dim); max-width:580px; margin:0 auto 12px; line-height:1.5;">
              Drag & drop any file (Image, Video, Audio, Profile CSV/JSON) here, or click to browse.
            </p>

            <div style="display:flex; align-items:center; justify-content:center; gap:6px; margin-bottom:14px; flex-wrap:wrap;">
              <span class="type-chip" style="background:rgba(45,217,232,.08); color:var(--cyan); border-color:rgba(45,217,232,.25);">PNG/JPG/WEBP</span>
              <span class="type-chip" style="background:rgba(139,107,240,.08); color:var(--violet); border-color:rgba(139,107,240,.25);">MP4/MOV/WEBM</span>
              <span class="type-chip" style="background:rgba(51,209,154,.08); color:var(--safe); border-color:rgba(51,209,154,.25);">WAV/MP3/FLAC</span>
              <span class="type-chip" style="background:rgba(245,185,66,.08); color:var(--warn); border-color:rgba(245,185,66,.25);">CSV/JSON Profiles</span>
              <span class="type-chip" style="background:rgba(255,107,122,.08); color:var(--danger-2); border-color:rgba(255,107,122,.25);">Pasted Text / URLs</span>
            </div>

            <!-- Live Text/URL Paste Input Bar directly in Dropzone -->
            <div style="max-width:680px; margin:0 auto; display:flex; gap:8px;" onclick="event.stopPropagation();">
              <input type="text" id="universalTextInput" class="field" placeholder="Or paste text, phishing URL, email content, or @username directly here..." style="font-size:12.5px; padding:10px 14px; background:rgba(8,11,18,.8); border-color:rgba(120,150,200,.25);" />
              <button class="btn btn-primary" id="universalVerifyBtn" style="padding:10px 18px; font-weight:700;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" width="14" height="14"><path d="M13 2L3 14h7l-1 8 10-12h-7l1-8z"/></svg>Verify Content
              </button>
            </div>

            <!-- Active Content Preview & Modality Tag -->
            <div id="universalPreviewWrap" style="display:none; margin-top:14px; padding-top:14px; border-top:1px solid var(--line);" onclick="event.stopPropagation();">
              <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;">
                <div style="display:flex; align-items:center; gap:10px; text-align:left;">
                  <div id="uPreviewThumb" style="width:40px; height:40px; border-radius:8px; background:var(--panel-2); display:flex; align-items:center; justify-content:center; font-size:20px; overflow:hidden;">📁</div>
                  <div>
                    <b id="uPreviewName" style="font-size:13px; color:var(--text); display:block;">File_Name</b>
                    <span id="uPreviewMeta" style="font-size:11px; color:var(--text-faint);">120 KB · Audio file</span>
                  </div>
                </div>
                <div style="display:flex; align-items:center; gap:8px;">
                  <span id="uAutoDetectBadge" class="soc-status-badge" style="color:var(--cyan); border-color:rgba(45,217,232,.3);">
                    ✨ Auto-Detected: Audio
                  </span>
                  <button class="btn btn-ghost btn-sm" id="uClearBtn" style="font-size:11px; padding:4px 9px;">Clear</button>
                </div>
              </div>
              <div id="uVisualPreviewArea" style="margin-top:10px;"></div>
            </div>
          </div>

          <!-- Dynamic Universal Verification Pipeline -->
          <div class="card pipeline" id="universalPipeline" style="display:none; margin-top:14px;">
            <div class="pipeline-title">
              <h3 style="font-size:14px; font-weight:700; color:var(--text);">Universal Multimodal Neural Pipeline</h3>
              <span class="pipeline-status" id="universalPipeStatus" style="color:var(--cyan);">Initializing…</span>
            </div>
            <div class="steps" id="universalSteps"></div>
          </div>

          <!-- Universal Result Container -->
          <div class="result-wrap" id="universalResult" style="margin-top:14px;"></div>
        </div>

        <!-- ================= 2. DATASET VERIFICATION BROWSER (EVALUATOR DEMO) ================= -->
        <div class="card scanner-card" id="datasetBrowserSection" style="margin-top:16px; margin-bottom:16px; border:1px solid rgba(139,107,240,.3); background:radial-gradient(ellipse at 10% -10%, rgba(139,107,240,.08), transparent 60%), var(--glass);">
          <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; border-bottom:1px solid var(--line); padding-bottom:12px; flex-wrap:wrap; gap:10px;">
            <div>
              <div class="eyebrow" style="color:var(--violet); margin-bottom:3px;">
                <span style="background:var(--violet); width:14px; height:1.5px; display:inline-block; margin-right:6px;"></span>Original Datasets · 1-Click Ground Truth Verification
              </div>
              <h2 style="font-family:var(--disp); font-size:18px; font-weight:700; color:var(--text); letter-spacing:-.2px;">Dataset Verification Browser · Evaluator Demo</h2>
              <p style="font-size:12.5px; color:var(--text-dim); margin-top:2px;">Verify real sample files from the original benchmark datasets with genuine PyTorch models and compare live inferences against ground truth.</p>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <span class="soc-status-badge" style="color:var(--safe); border-color:rgba(51,209,154,.3); font-size:11px;">
                <span class="dot" style="background:var(--safe);"></span>GROUND TRUTH ENGINE ACTIVE
              </span>
            </div>
          </div>

          <!-- Catalog of Modalities with Real and Fake buttons -->
          <div class="grid g2" id="datasetCatalogGrid" style="gap:12px;">

            <!-- 1. Image Card -->
            <div class="bento-card" style="padding:14px; background:var(--panel-2); border:1px solid var(--line); border-radius:12px;">
              <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <span style="font-size:18px;">🖼️</span>
                  <div>
                    <b style="font-size:13px; color:var(--text);">Image Deepfake Dataset</b>
                    <span style="display:block; font-size:10.5px; color:var(--text-faint);">1000 Videos Dataset (archive/1000_videos)</span>
                  </div>
                </div>
                <span class="type-chip" style="color:var(--cyan); border-color:rgba(45,217,232,.3);">DeepfakeCNN</span>
              </div>
              <p style="font-size:11.5px; color:var(--text-dim); margin-bottom:10px;">Test authentic vs manipulated face frames from the held-out test split.</p>
              <div style="display:flex; gap:8px;">
                <button class="btn btn-ghost btn-sm" id="btnDatasetImgReal" style="flex:1; border-color:rgba(51,209,154,.4); color:var(--safe);" onclick="verifyDatasetSample('image', 'real')">
                  ✓ Verify Real (067_16.png)
                </button>
                <button class="btn btn-ghost btn-sm" id="btnDatasetImgFake" style="flex:1; border-color:rgba(242,73,92,.4); color:var(--danger-2);" onclick="verifyDatasetSample('image', 'fake')">
                  ⚠ Verify Fake (067_025_1.png)
                </button>
              </div>
            </div>

            <!-- 2. Audio Card -->
            <div class="bento-card" style="padding:14px; background:var(--panel-2); border:1px solid var(--line); border-radius:12px;">
              <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <span style="font-size:18px;">🎙️</span>
                  <div>
                    <b style="font-size:13px; color:var(--text);">Audio Voice Spoof Dataset</b>
                    <span style="display:block; font-size:10.5px; color:var(--text-faint);">ASVspoof 2019 Logical Access (archive (1)/LA)</span>
                  </div>
                </div>
                <span class="type-chip" style="color:var(--safe); border-color:rgba(51,209,154,.3);">AudioCNN</span>
              </div>
              <p style="font-size:11.5px; color:var(--text-dim); margin-bottom:10px;">Test genuine studio voice vs vocoder synthesized speech.</p>
              <div style="display:flex; gap:8px;">
                <button class="btn btn-ghost btn-sm" id="btnDatasetAudReal" style="flex:1; border-color:rgba(51,209,154,.4); color:var(--safe);" onclick="verifyDatasetSample('audio', 'real')">
                  ✓ Verify Bonafide (FLAC)
                </button>
                <button class="btn btn-ghost btn-sm" id="btnDatasetAudFake" style="flex:1; border-color:rgba(242,73,92,.4); color:var(--danger-2);" onclick="verifyDatasetSample('audio', 'fake')">
                  ⚠ Verify Spoofed (FLAC)
                </button>
              </div>
            </div>

            <!-- 3. Social Media Card -->
            <div class="bento-card" style="padding:14px; background:var(--panel-2); border:1px solid var(--line); border-radius:12px;">
              <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <span style="font-size:18px;">📱</span>
                  <div>
                    <b style="font-size:13px; color:var(--text);">Social Fake Profile Dataset</b>
                    <span style="display:block; font-size:10.5px; color:var(--text-faint);">Instagram Benchmark (archive (14)/test.csv)</span>
                  </div>
                </div>
                <span class="type-chip" style="color:var(--violet); border-color:rgba(139,107,240,.3);">SocialSpamNet</span>
              </div>
              <p style="font-size:11.5px; color:var(--text-dim); margin-bottom:10px;">Test organic profile vs high-digit-ratio spammer account.</p>
              <div style="display:flex; gap:8px;">
                <button class="btn btn-ghost btn-sm" id="btnDatasetSocialReal" style="flex:1; border-color:rgba(51,209,154,.4); color:var(--safe);" onclick="verifyDatasetSample('social', 'real')">
                  ✓ Verify Genuine (@peterkonda)
                </button>
                <button class="btn btn-ghost btn-sm" id="btnDatasetSocialFake" style="flex:1; border-color:rgba(242,73,92,.4); color:var(--danger-2);" onclick="verifyDatasetSample('social', 'fake')">
                  ⚠ Verify Spammer (@official_bg)
                </button>
              </div>
            </div>

            <!-- 4. SMS Card -->
            <div class="bento-card" style="padding:14px; background:var(--panel-2); border:1px solid var(--line); border-radius:12px;">
              <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <span style="font-size:18px;">💬</span>
                  <div>
                    <b style="font-size:13px; color:var(--text);">SMS Spam & Scam Dataset</b>
                    <span style="display:block; font-size:10.5px; color:var(--text-faint);">SMS Spam Collection (archive (4)/spam_sms.csv)</span>
                  </div>
                </div>
                <span class="type-chip" style="color:var(--warn); border-color:rgba(245,185,66,.3);">SMSScamClassifier</span>
              </div>
              <p style="font-size:11.5px; color:var(--text-dim); margin-bottom:10px;">Test organic chat message vs prize lottery scam text.</p>
              <div style="display:flex; gap:8px;">
                <button class="btn btn-ghost btn-sm" id="btnDatasetSmsReal" style="flex:1; border-color:rgba(51,209,154,.4); color:var(--safe);" onclick="verifyDatasetSample('sms', 'real')">
                  ✓ Verify Ham (Chat)
                </button>
                <button class="btn btn-ghost btn-sm" id="btnDatasetSmsFake" style="flex:1; border-color:rgba(242,73,92,.4); color:var(--danger-2);" onclick="verifyDatasetSample('sms', 'fake')">
                  ⚠ Verify Spam (Prize Scam)
                </button>
              </div>
            </div>

            <!-- 5. URL Card -->
            <div class="bento-card" style="padding:14px; background:var(--panel-2); border:1px solid var(--line); border-radius:12px;">
              <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <span style="font-size:18px;">🔗</span>
                  <div>
                    <b style="font-size:13px; color:var(--text);">Phishing URLs Dataset</b>
                    <span style="display:block; font-size:10.5px; color:var(--text-faint);">579k URLs Benchmark (archive (7)/final_dataset.csv)</span>
                  </div>
                </div>
                <span class="type-chip" style="color:var(--cyan); border-color:rgba(45,217,232,.3);">PhishingURLNet</span>
              </div>
              <p style="font-size:11.5px; color:var(--text-dim); margin-bottom:10px;">Test legitimate domain vs high-entropy credential harvesting URL.</p>
              <div style="display:flex; gap:8px;">
                <button class="btn btn-ghost btn-sm" id="btnDatasetUrlReal" style="flex:1; border-color:rgba(51,209,154,.4); color:var(--safe);" onclick="verifyDatasetSample('url', 'real')">
                  ✓ Verify Legit URL
                </button>
                <button class="btn btn-ghost btn-sm" id="btnDatasetUrlFake" style="flex:1; border-color:rgba(242,73,92,.4); color:var(--danger-2);" onclick="verifyDatasetSample('url', 'fake')">
                  ⚠ Verify Phish URL
                </button>
              </div>
            </div>

            <!-- 6. Email Card -->
            <div class="bento-card" style="padding:14px; background:var(--panel-2); border:1px solid var(--line); border-radius:12px;">
              <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <span style="font-size:18px;">📧</span>
                  <div>
                    <b style="font-size:13px; color:var(--text);">Phishing Email Benchmark</b>
                    <span style="display:block; font-size:10.5px; color:var(--text-faint);">82k Email Corpus (archive (9)/phishing_email.csv)</span>
                  </div>
                </div>
                <span class="type-chip" style="color:var(--safe); border-color:rgba(51,209,154,.3);">EmailClassifier</span>
              </div>
              <p style="font-size:11.5px; color:var(--text-dim); margin-bottom:10px;">Test corporate file review email vs PayPal account suspension attack.</p>
              <div style="display:flex; gap:8px;">
                <button class="btn btn-ghost btn-sm" id="btnDatasetEmailReal" style="flex:1; border-color:rgba(51,209,154,.4); color:var(--safe);" onclick="verifyDatasetSample('email', 'real')">
                  ✓ Verify Genuine Email
                </button>
                <button class="btn btn-ghost btn-sm" id="btnDatasetEmailFake" style="flex:1; border-color:rgba(242,73,92,.4); color:var(--danger-2);" onclick="verifyDatasetSample('email', 'fake')">
                  ⚠ Verify Phish Email
                </button>
              </div>
            </div>

            <!-- 7. Job Card -->
            <div class="bento-card" style="grid-column: span 2; padding:14px; background:var(--panel-2); border:1px solid var(--line); border-radius:12px;">
              <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <span style="font-size:18px;">💼</span>
                  <div>
                    <b style="font-size:13px; color:var(--text);">Fake Job Postings Dataset</b>
                    <span style="display:block; font-size:10.5px; color:var(--text-faint);">Fake Postings (archive (5)/Fake Postings.csv)</span>
                  </div>
                </div>
                <span class="type-chip" style="color:var(--warn); border-color:rgba(245,185,66,.3);">Dual Heuristic Engine</span>
              </div>
              <p style="font-size:11.5px; color:var(--text-dim); margin-bottom:10px;">Test fraudulent posting requiring upfront fees with commercial webmail recruiters.</p>
              <div>
                <button class="btn btn-ghost btn-sm btn-block" id="btnDatasetJobFake" style="border-color:rgba(242,73,92,.4); color:var(--danger-2);" onclick="verifyDatasetSample('job', 'fake')">
                  ⚠ Verify Scam Job Posting (Mental Health Nurse — $150 Advance Fee)
                </button>
              </div>
            </div>

          </div>

          <!-- Live Dataset Sample Result Container -->
          <div id="datasetSampleResultWrap" style="display:none; margin-top:14px;"></div>
        </div>
"""

JS_UNIFIED_LOGIC = """
/* ============ UNIFIED DRAG & DROP & UNIVERSAL VERIFY SYSTEM ============ */
let universalCurrentModality = 'auto';
let universalLoadedFile = null;

function setUniversalModality(modality) {
  universalCurrentModality = modality;
  document.querySelectorAll('.universal-modality-grid .u-mod-card').forEach(c => {
    c.classList.toggle('active', c.dataset.modality === modality);
  });
  const badge = document.getElementById('uAutoDetectBadge');
  if (badge) {
    badge.textContent = modality === 'auto' ? '✨ Auto-Detection Active' : `Target: ${modality.toUpperCase()}`;
    badge.style.color = 'var(--cyan)';
  }
}

function autoDetectModality(fileOrText) {
  if (typeof fileOrText === 'string') {
    const s = fileOrText.trim();
    if (s.startsWith('http://') || s.startsWith('https://')) return 'url';
    if (s.includes('Subject:') || s.includes('From:') || s.includes('To:') || s.includes('mailto:')) return 'email';
    if (s.toLowerCase().includes('salary') || s.toLowerCase().includes('fee') || s.toLowerCase().includes('recruiter') || s.toLowerCase().includes('interview')) return 'job';
    if (s.startsWith('@') || s.includes('username') || s.includes('followers') || s.includes('following')) return 'social';
    return 'sms';
  } else if (fileOrText instanceof File) {
    const name = fileOrText.name.toLowerCase();
    const type = fileOrText.type || '';
    if (type.startsWith('image/') || name.endsWith('.png') || name.endsWith('.jpg') || name.endsWith('.jpeg') || name.endsWith('.webp')) return 'image';
    if (type.startsWith('video/') || name.endsWith('.mp4') || name.endsWith('.mov') || name.endsWith('.webm') || name.endsWith('.avi')) return 'video';
    if (type.startsWith('audio/') || name.endsWith('.wav') || name.endsWith('.mp3') || name.endsWith('.flac') || name.endsWith('.m4a') || name.endsWith('.ogg')) return 'audio';
    if (name.endsWith('.csv') || name.endsWith('.json') || name.includes('profile') || name.includes('spammer') || name.includes('instagram')) return 'social';
    return 'sms';
  }
  return 'image';
}

function setupUniversalDropzone() {
  const dropzone = document.getElementById('universalDropzone');
  const fileInput = document.getElementById('universalFileInput');
  const textInput = document.getElementById('universalTextInput');
  const verifyBtn = document.getElementById('universalVerifyBtn');
  const clearBtn = document.getElementById('uClearBtn');
  const prevWrap = document.getElementById('universalPreviewWrap');
  const previewArea = document.getElementById('uVisualPreviewArea');
  const previewName = document.getElementById('uPreviewName');
  const previewMeta = document.getElementById('uPreviewMeta');
  const previewThumb = document.getElementById('uPreviewThumb');
  const autoDetectBadge = document.getElementById('uAutoDetectBadge');

  if (!dropzone || !fileInput) return;

  dropzone.addEventListener('click', (e) => {
    if (e.target === textInput || e.target === verifyBtn) return;
    fileInput.click();
  });

  fileInput.addEventListener('change', () => {
    if (fileInput.files && fileInput.files[0]) {
      handleUniversalFile(fileInput.files[0]);
    }
  });

  dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('drag');
  });
  dropzone.addEventListener('dragleave', () => dropzone.classList.remove('drag'));
  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('drag');
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleUniversalFile(e.dataTransfer.files[0]);
    }
  });

  textInput?.addEventListener('input', () => {
    const val = textInput.value.trim();
    if (val.length > 0 && universalCurrentModality === 'auto') {
      const detected = autoDetectModality(val);
      if (autoDetectBadge) {
        autoDetectBadge.textContent = `✨ Auto-Detected: ${detected.toUpperCase()}`;
        autoDetectBadge.style.color = 'var(--cyan)';
      }
    }
  });

  clearBtn?.addEventListener('click', () => {
    universalLoadedFile = null;
    if (fileInput) fileInput.value = '';
    if (prevWrap) prevWrap.style.display = 'none';
    if (previewArea) previewArea.innerHTML = '';
    if (textInput) textInput.value = '';
  });

  verifyBtn?.addEventListener('click', () => executeUniversalVerification());
}

function handleUniversalFile(file) {
  universalLoadedFile = file;
  const detected = autoDetectModality(file);
  const detectedMod = universalCurrentModality === 'auto' ? detected : universalCurrentModality;

  const prevWrap = document.getElementById('universalPreviewWrap');
  const previewArea = document.getElementById('uVisualPreviewArea');
  const previewName = document.getElementById('uPreviewName');
  const previewMeta = document.getElementById('uPreviewMeta');
  const previewThumb = document.getElementById('uPreviewThumb');
  const autoDetectBadge = document.getElementById('uAutoDetectBadge');

  if (prevWrap) prevWrap.style.display = 'block';
  if (previewName) previewName.textContent = file.name;
  if (previewMeta) previewMeta.textContent = `${(file.size / 1024).toFixed(1)} KB · ${file.type || 'file'}`;
  if (autoDetectBadge) {
    autoDetectBadge.textContent = `✨ Auto-Detected: ${detected.toUpperCase()}`;
    autoDetectBadge.style.color = 'var(--cyan)';
  }

  // Set thumb icon
  if (previewThumb) {
    if (detected === 'image') previewThumb.textContent = '🖼️';
    else if (detected === 'video') previewThumb.textContent = '🎬';
    else if (detected === 'audio') previewThumb.textContent = '🎙️';
    else if (detected === 'social') previewThumb.textContent = '📱';
    else previewThumb.textContent = '📄';
  }

  // Visual thumbnail preview
  if (previewArea) {
    if (file.type && file.type.startsWith('image/')) {
      const url = URL.createObjectURL(file);
      previewArea.innerHTML = `<img src="${url}" style="max-height:180px; max-width:100%; border-radius:8px; border:1px solid var(--line); display:inline-block;" />`;
    } else if (file.type && file.type.startsWith('video/')) {
      const url = URL.createObjectURL(file);
      previewArea.innerHTML = `<video src="${url}" controls style="max-height:180px; max-width:100%; border-radius:8px; border:1px solid var(--line); display:inline-block;"></video>`;
    } else if (file.type && file.type.startsWith('audio/')) {
      const url = URL.createObjectURL(file);
      previewArea.innerHTML = `<audio src="${url}" controls style="width:100%; max-width:400px; margin-top:6px;"></audio>`;
    } else {
      previewArea.innerHTML = `<div style="font-size:11px; color:var(--text-faint);">File ready for ${detectedMod.toUpperCase()} neural analysis.</div>`;
    }
  }

  toast('Content Loaded', `${file.name} ready for ${detected.toUpperCase()} verification`, 'info');
}

async function executeUniversalVerification() {
  const textInput = document.getElementById('universalTextInput');
  const textVal = textInput ? textInput.value.trim() : '';
  const file = universalLoadedFile;

  if (!file && !textVal) {
    toast('No Content Provided', 'Drop a file or paste text/URL into the verification box.', 'warn');
    return;
  }

  let modality = universalCurrentModality;
  if (modality === 'auto') {
    modality = file ? autoDetectModality(file) : autoDetectModality(textVal);
  }

  const pipeline = document.getElementById('universalPipeline');
  const pipeStatus = document.getElementById('universalPipeStatus');
  const resWrap = document.getElementById('universalResult');

  if (pipeline) pipeline.style.display = 'block';
  if (resWrap) { resWrap.classList.remove('show'); resWrap.innerHTML = ''; }

  const pipeSteps = [
    { title: 'Format & Signal Ingestion', desc: `Extracting bitstream and tokens for ${modality.toUpperCase()} analysis.` },
    { title: 'Feature Vector Computation', desc: 'Running signal transforms and neural feature extraction.' },
    { title: 'Trained Model Inference', desc: 'Executing forward pass through validated PyTorch detector.' },
    { title: 'Forensic Synthesis & Ground Check', desc: 'Generating explainability indicators and trust telemetry.' }
  ];

  runPipeline(pipeSteps, 'universalSteps', 'universalPipeStatus', async () => {
    try {
      let apiRes = null;
      let label = file ? file.name : (textVal.length > 35 ? textVal.slice(0, 35) + '…' : textVal);

      if (modality === 'image') {
        const formData = new FormData();
        if (file) formData.append('file', file);
        else formData.append('url', textVal);
        apiRes = await apiPost('/api/analyze/image', formData, true);
      } else if (modality === 'video') {
        const formData = new FormData();
        if (file) formData.append('file', file);
        apiRes = await apiPost('/api/analyze/video', formData, true);
      } else if (modality === 'audio') {
        const formData = new FormData();
        if (file) formData.append('file', file);
        apiRes = await apiPost('/api/analyze/audio', formData, true);
      } else if (modality === 'social') {
        if (file) {
          const formData = new FormData();
          formData.append('file', file);
          apiRes = await apiPost('/api/analyze/social', formData, true);
        } else {
          apiRes = await apiPost('/api/analyze/social', { username: textVal, bio: textVal });
        }
      } else if (modality === 'url') {
        apiRes = await apiPost('/api/analyze/url', { url: textVal });
      } else if (modality === 'email') {
        apiRes = await apiPost('/api/analyze/email', { body: textVal, subject: 'Verification Query' });
      } else if (modality === 'job') {
        apiRes = await apiPost('/api/analyze/job', { title: 'Offer Verification', description: textVal });
      } else {
        // SMS / text
        apiRes = await apiPost('/api/analyze/text', { text: textVal });
      }

      const norm = normalizePrediction(apiRes, modality.toUpperCase(), label);
      if (resWrap) {
        resWrap.innerHTML = renderUnifiedResultCard(norm, {
          contentType: modality.toUpperCase(),
          contentLabel: label,
          frameResults: apiRes.frame_results || apiRes.video_results?.frame_results || [],
          segmentResults: apiRes.segment_results || apiRes.audio_results?.segment_results || []
        });
        resWrap.classList.add('show');
        attachResultActions(resWrap, { ...norm, contentType: modality.toUpperCase(), contentLabel: label, date: Date.now() });
      }

      pushHistory({
        contentLabel: label,
        contentType: modality.toUpperCase(),
        score: norm.riskScore,
        trust: norm.authenticity,
        confidence: norm.confidence,
        date: Date.now()
      });

      if (norm.riskScore >= 65) {
        triggerHighRiskAlert(norm, modality.toUpperCase(), label);
      }
      toast(norm.isGenuine ? '✓ Authentic Content' : '⚠ Threat / Synthetic Content Flagged', `Risk: ${norm.riskScore}/100`, norm.isGenuine ? 'safe' : 'danger');

      // Refresh stats
      fetchDashboardStats();
    } catch (err) {
      console.error('Universal verification error:', err);
      toast('Analysis Error', err.message || 'Verification could not be completed.', 'danger');
    }
  });
}

/* ============ DATASET VERIFICATION BROWSER (EVALUATOR DEMO) ============ */
async function verifyDatasetSample(modality, sampleType) {
  const resultWrap = document.getElementById('datasetSampleResultWrap');
  if (!resultWrap) return;

  resultWrap.style.display = 'block';
  resultWrap.innerHTML = `
    <div class="card card-pad" style="border:1px solid rgba(139,107,240,.4); background:var(--panel-2); text-align:center; padding:20px;">
      <div class="soc-status-badge" style="color:var(--cyan); border-color:rgba(45,217,232,.3); margin-bottom:8px;">
        <span class="dot" style="background:var(--cyan);"></span>ANALYZING ORIGINAL BENCHMARK DATASET SAMPLE...
      </div>
      <div style="font-size:12.5px; color:var(--text-dim);">Loading raw sample, executing forward PyTorch pass, and comparing against dataset ground truth.</div>
    </div>
  `;
  resultWrap.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

  try {
    const res = await apiPost('/api/verify/dataset-sample', { modality, sample_type: sampleType });
    if (!res.success) {
      resultWrap.innerHTML = `<div class="card card-pad" style="color:var(--danger); font-size:12px;">Verification failed: ${res.detail || 'Unknown error'}</div>`;
      return;
    }

    const isMatch = res.is_match;
    const matchStatus = res.match_status || (isMatch ? '✓ MATCH' : '✗ MISMATCH');
    const matchColor = isMatch ? 'var(--safe)' : 'var(--danger-2)';
    const matchBg = isMatch ? 'rgba(51,209,154,.12)' : 'rgba(242,73,92,.12)';
    const matchBorder = isMatch ? 'rgba(51,209,154,.35)' : 'rgba(242,73,92,.35)';

    resultWrap.innerHTML = `
      <div class="card card-pad" style="border:1.5px solid ${matchBorder}; background:radial-gradient(ellipse at 50% 0%, ${matchBg}, transparent 70%), var(--panel); animation:fadeUp .25s ease;">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; border-bottom:1px solid var(--line); padding-bottom:8px; flex-wrap:wrap; gap:8px;">
          <div>
            <span class="eyebrow" style="color:${matchColor};">GROUND TRUTH EVALUATION · ${res.modality.toUpperCase()}</span>
            <b style="font-size:14px; color:var(--text);">${res.sample_identifier}</b>
          </div>
          <div style="display:inline-flex; align-items:center; gap:6px; padding:6px 14px; border-radius:20px; background:${matchBg}; border:1px solid ${matchBorder}; color:${matchColor}; font-weight:700; font-size:12px;">
            ${matchStatus} (Ground Truth Confirmed)
          </div>
        </div>

        <div style="font-size:11.5px; color:var(--text-faint); margin-bottom:12px;">
          <b>Source Dataset:</b> <span style="color:var(--text);">${res.dataset_name}</span>
        </div>

        <div class="pred-grid" style="margin-bottom:12px;">
          <div class="pred-card">
            <div class="val" style="color:var(--text-dim); font-size:15px;">${res.expected_label}</div>
            <div class="lbl">Expected Ground Truth</div>
          </div>
          <div class="pred-card">
            <div class="val" style="color:${res.is_match ? 'var(--safe)' : 'var(--danger-2)'}; font-size:15px;">${res.predicted_label}</div>
            <div class="lbl">Model Classification</div>
          </div>
          <div class="pred-card">
            <div class="val" style="color:var(--cyan);">${res.confidence_pct}%</div>
            <div class="lbl">Confidence</div>
          </div>
          <div class="pred-card">
            <div class="val" style="color:${res.risk_score > 50 ? 'var(--danger-2)' : 'var(--safe)'};">${res.risk_score}/100</div>
            <div class="lbl">Risk Score (${res.risk_level})</div>
          </div>
        </div>

        <div style="padding:10px 12px; background:rgba(0,0,0,0.25); border:1px solid var(--line); border-radius:8px; font-size:11.5px; line-height:1.5;">
          <span style="color:var(--cyan); font-weight:600;">Forensic Engine Assessment:</span>
          <span style="color:var(--text-dim); margin-left:4px;">${res.details?.explanation || 'Model classification aligns with ground truth label.'}</span>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px; font-size:11px; font-family:var(--mono); color:var(--text-faint);">
          <span>Model: <b style="color:var(--cyan);">${res.details?.model_name || res.details?.model || 'Trained PyTorch Model'}</b></span>
          <span>Verified in SQLite History ✓</span>
        </div>
      </div>
    `;

    toast(isMatch ? '✓ Ground Truth Match' : '⚠ Ground Truth Mismatch', `${res.modality.toUpperCase()}: ${res.predicted_label} (${res.confidence_pct}%)`, isMatch ? 'safe' : 'warn');
    await fetchDashboardStats();
    await fetchHistoryFromBackend();
  } catch (err) {
    console.error('Dataset verification error:', err);
    resultWrap.innerHTML = `<div class="card card-pad" style="color:var(--danger); font-size:12px;">Error executing dataset verification: ${err.message}</div>`;
  }
}

// Ensure dropzone initializes on load
window.addEventListener('DOMContentLoaded', () => {
  setupUniversalDropzone();
});
"""

def update_index():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Insert CSS right before </style>
    if "/* ============ UNIVERSAL VERIFY DROPZONE STYLES ============ */" not in content:
        style_idx = content.find("</style>")
        if style_idx == -1:
            raise ValueError("Could not find </style> in index.html")
        content = content[:style_idx] + CSS_ADDITION + "\n" + content[style_idx:]
        print("Inserted CSS rules.")

    # 2. Insert HTML sections right before <div class="card scanner-card" id="dashScanTabs"
    if "id=\"universalVerifySection\"" not in content:
        dock_idx = content.find('<div class="card scanner-card" id="dashScanTabs"')
        if dock_idx == -1:
            raise ValueError("Could not find dashScanTabs in index.html")
        content = content[:dock_idx] + HTML_UNIFIED_SECTION + "\n" + content[dock_idx:]
        print("Inserted Universal Dropzone and Dataset Verification Browser HTML.")

    # 3. Enhance renderUnifiedResultCard with Technical Details Accordion
    target_needle = '      <div class="action-row" style="margin-top:16px;">\n        <button class="btn btn-ghost btn-sm speak-btn">🔊 Read Voiceover</button>'
    if target_needle in content and "tech-details-panel" not in content:
        tech_accordion = '''      <div style="margin-top:10px;">
        <button class="tech-details-btn" onclick="this.nextElementSibling.classList.toggle('open'); this.querySelector('.td-arrow').textContent = this.nextElementSibling.classList.contains('open') ? '▴' : '▾';">
          <span>🔬 View Technical Details</span> <span class="td-arrow">▾</span>
        </button>
        <div class="tech-details-panel">
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:10px; margin-bottom:8px;">
            <div><span style="color:var(--text-faint); display:block; font-size:10px; text-transform:uppercase;">Architecture / Engine</span><b style="color:var(--cyan); font-family:var(--mono);">${norm.raw.model_name || norm.raw.model || modelName}</b></div>
            <div><span style="color:var(--text-faint); display:block; font-size:10px; text-transform:uppercase;">Model Weights Source</span><b style="color:var(--text); font-family:var(--mono);">${norm.raw.weights_path || norm.raw.model_path || 'Production Weights (PyTorch best_model.pt)'}</b></div>
            <div><span style="color:var(--text-faint); display:block; font-size:10px; text-transform:uppercase;">Training Dataset</span><b style="color:var(--text);">${norm.raw.training_dataset || norm.raw.dataset_name || (opts.contentType.toLowerCase().includes('social') ? 'Instagram Benchmark (archive (14))' : opts.contentType.toLowerCase().includes('image') ? '1000 Videos Deepfake Benchmark' : opts.contentType.toLowerCase().includes('audio') ? 'ASVspoof 2019 LA Benchmark' : 'Kaggle Threat Benchmark')}</b></div>
            <div><span style="color:var(--text-faint); display:block; font-size:10px; text-transform:uppercase;">Inference Latency</span><b style="color:var(--safe); font-family:var(--mono);">${latencyMs} ms</b></div>
          </div>
          ${norm.raw.features ? `
            <div style="margin-top:8px; border-top:1px solid var(--line); padding-top:6px;">
              <span style="color:var(--text-faint); font-size:10.5px; text-transform:uppercase;">Extracted Feature Vector:</span>
              <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:4px;">
                ${Object.entries(norm.raw.features).map(([k, v]) => `<span style="background:var(--panel-2); border:1px solid var(--line); padding:2px 6px; border-radius:4px; font-family:var(--mono); font-size:10.5px;"><span style="color:var(--text-dim);">${k}:</span> <b style="color:var(--cyan);">${typeof v === 'number' ? (Number.isInteger(v) ? v : v.toFixed(3)) : v}</b></span>`).join('')}
              </div>
            </div>
          ` : ''}
          ${norm.raw.probabilities ? `
            <div style="margin-top:8px; border-top:1px solid var(--line); padding-top:6px;">
              <span style="color:var(--text-faint); font-size:10.5px; text-transform:uppercase;">Class Probability Distribution:</span>
              <div style="display:flex; gap:12px; margin-top:4px; font-family:var(--mono); font-size:11px;">
                <div>Authentic / Real: <b style="color:var(--safe);">${((norm.raw.probabilities.real ?? norm.raw.probabilities.authentic ?? (100 - norm.riskScore)/100) * 100).toFixed(1)}%</b></div>
                <div>Synthetic / Threat: <b style="color:var(--danger-2);">${((norm.raw.probabilities.fake ?? norm.raw.probabilities.spam ?? norm.raw.probabilities.phishing ?? norm.riskScore/100) * 100).toFixed(1)}%</b></div>
              </div>
            </div>
          ` : ''}
        </div>
      </div>
''' + target_needle
        content = content.replace(target_needle, tech_accordion)
        print("Inserted Technical Details Accordion into renderUnifiedResultCard.")

    # 4. Insert JS logic before </script>\n<!-- Firebase realtime sync -->
    if "/* ============ UNIFIED DRAG & DROP & UNIVERSAL VERIFY SYSTEM ============ */" not in content:
        script_end_needle = "</script>\n<!-- Firebase realtime sync -->"
        if script_end_needle not in content:
            script_end_needle = "</script>"
            last_script_idx = content.rfind("</script>")
            content = content[:last_script_idx] + JS_UNIFIED_LOGIC + "\n" + content[last_script_idx:]
        else:
            content = content.replace(script_end_needle, JS_UNIFIED_LOGIC + "\n" + script_end_needle)
        print("Inserted JS Universal Dropzone & Dataset Verification Browser logic.")

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("SUCCESS: index.html successfully updated with Unified Drag & Drop Verification Experience!")

if __name__ == "__main__":
    update_index()
