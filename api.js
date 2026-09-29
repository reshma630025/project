/**
 * TrustGuard AI — Centralized API Client Layer
 * Handles robust communication with the FastAPI backend.
 * Compatible with local execution (127.0.0.1:8000), LAN devices, and GitHub Pages.
 */

function getTrustGuardApiBase() {
  // 1. Explicit window override (e.g. from config.js)
  let remoteUrl = null;
  if (typeof window !== 'undefined' && window.TRUSTGUARD_CONFIG && window.TRUSTGUARD_CONFIG.remoteBackend) {
    remoteUrl = window.TRUSTGUARD_CONFIG.remoteBackend.trim().replace(/\/+$/, '');
  }

  // 2. LocalStorage override (e.g. set by user for remote LAN testing)
  if (typeof window !== 'undefined' && window.localStorage) {
    try {
      const saved = window.localStorage.getItem('trustguard_backend_url');
      if (saved && typeof saved === 'string' && saved.trim()) {
        return saved.trim().replace(/\/+$/, '');
      }
    } catch (_) {}
  }

  // 3. Current origin detection
  if (typeof window !== 'undefined' && window.location) {
    const origin = window.location.origin || '';
    const protocol = window.location.protocol || '';
    const hostname = window.location.hostname || '';

    // If hosted on GitHub Pages or other static CDNs, point to REMOTE backend if configured, else fallback to local backend for testing
    if (hostname.includes('github.io') || hostname.includes('pages.dev') || hostname.includes('netlify.app') || hostname.includes('vercel.app')) {
      return remoteUrl || 'http://127.0.0.1:8000'; // Fallback to localhost so testing still works if no remote is configured
    }

    // If opened via local file protocol (file://)
    if (protocol === 'file:' || !origin || origin === 'null') {
      return 'http://127.0.0.1:8000';
    }

    // If opened via frontend dev server (Vite :5173, etc.)
    if (origin.includes(':5173') || origin.includes(':3000') || origin.includes(':5500') || origin.includes(':8080')) {
      return 'http://127.0.0.1:8000';
    }

    // If served directly by FastAPI backend on localhost or LAN (e.g. http://127.0.0.1:8000 or http://192.168.x.x:8000)
    if (origin.startsWith('http://') || origin.startsWith('https://')) {
      return origin.replace(/\/+$/, '');
    }
  }

  return 'http://127.0.0.1:8000';
}

window.getTrustGuardApiBase = getTrustGuardApiBase;
window.API_BASE_URL = getTrustGuardApiBase();
var API_BASE_URL = window.API_BASE_URL;

class TrustGuardAPI {
  constructor(baseUrl = null) {
    this.baseUrl = (baseUrl || getTrustGuardApiBase()).replace(/\/+$/, '');
  }

  /**
   * Helper to set a custom backend URL dynamically (e.g. for LAN testing from phone)
   */
  setBackendUrl(url) {
    if (url && typeof url === 'string') {
      this.baseUrl = url.trim().replace(/\/+$/, '');
      window.TRUSTGUARD_BACKEND_URL = this.baseUrl;
      window.API_BASE_URL = this.baseUrl;
      API_BASE_URL = this.baseUrl;
      try {
        localStorage.setItem('trustguard_backend_url', this.baseUrl);
      } catch (_) {}
    }
  }

  /**
   * Safe response parser: Prevents "Unexpected token '<'" SyntaxError when a web server or GitHub Pages returns HTML.
   */
  async parseSafeResponse(response, endpoint) {
    const contentType = response.headers.get('content-type') || '';
    const isJson = contentType.toLowerCase().includes('application/json');

    let rawText = '';
    try {
      rawText = await response.text();
    } catch (_) {
      rawText = '';
    }

    let data = null;
    if (isJson && rawText) {
      try {
        data = JSON.parse(rawText);
      } catch (_) {
        data = null;
      }
    }

    // If the server returned HTML (e.g. GitHub Pages 404, nginx default, etc.)
    if (!isJson || rawText.trim().startsWith('<') || rawText.trim().toLowerCase().startsWith('<!doctype')) {
      const activeUrl = window.API_BASE_URL || 'http://127.0.0.1:8000';
      const isGitHub = window.location.hostname.includes('github.io');
      const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      
      let environment = isGitHub ? "DEPLOYED FRONTEND (GitHub Pages)" : (isLocalhost ? "LOCAL BACKEND" : "LAN BACKEND");
      
      throw new Error(
        `Backend connection failed on ${environment}. ` +
        `Received HTML response instead of JSON API response from ${activeUrl}. ` +
        (isGitHub ? `Live AI backend is currently unavailable.` : `Please ensure your local TrustGuard AI backend is running (run start_trustguard.bat) and configure the correct API URL.`)
      );
    }

    if (!data) {
      throw new Error(`Invalid or empty JSON response received from backend (HTTP ${response.status}).`);
    }

    if (!response.ok) {
      let errMsg = data.error || data.detail || data.message;
      if (typeof errMsg === 'object') errMsg = JSON.stringify(errMsg);
      if (!errMsg) {
        if (response.status === 400) errMsg = 'Bad Request: Missing or invalid parameters sent to detector.';
        else if (response.status === 401) errMsg = 'Authentication error: Session expired or invalid token.';
        else if (response.status === 404) errMsg = `Endpoint not found: ${endpoint}`;
        else if (response.status === 422) errMsg = `Validation Error: ${JSON.stringify(data.detail || data)}`;
        else if (response.status === 500) errMsg = 'Internal Server Error: Forensic model processing error in backend.';
        else errMsg = `Server returned HTTP ${response.status}`;
      }
      throw new Error(errMsg);
    }

    if (data.success === false && data.error) {
      throw new Error(data.error);
    }

    return data;
  }

  /**
   * Generic request handler with timeout, auth tokens, and safe response parsing.
   */
  async request(endpoint, options = {}, timeoutMs = 60000) {
    if (endpoint.includes('/video')) {
      timeoutMs = Math.max(timeoutMs, 120000);
    }

    const url = `${this.baseUrl}${endpoint}`;
    const token = localStorage.getItem('trustguard_token') || localStorage.getItem('tg_token');
    
    const headers = options.headers || {};
    if (token) {
      headers['x-session-token'] = token;
      headers['Authorization'] = `Bearer ${token}`;
    }

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);

    try {
      const response = await fetch(url, {
        ...options,
        headers,
        signal: controller.signal
      });
      clearTimeout(timer);
      return await this.parseSafeResponse(response, endpoint);
    } catch (err) {
      clearTimeout(timer);
      if (err.name === 'AbortError') {
        throw new Error(`Analysis request timed out after ${timeoutMs / 1000}s. Processing took longer than expected.`);
      }
      if (err.message && (err.message.includes('Failed to fetch') || err.message.includes('NetworkError') || err.message.includes('fetch failed'))) {
        const isGitHub = window.location.hostname.includes('github.io');
        if (isGitHub) {
          throw new Error(`Live AI backend is currently unavailable. Please try again later.`);
        } else {
          throw new Error(`TrustGuard AI local backend is not running at ${this.baseUrl}. Start the FastAPI server on port 8000 and try again.`);
        }
      }
      throw err;
    }
  }

  // System & Telemetry Endpoints
  async getHealth() {
    return this.request('/api/health');
  }

  async getStatus() {
    return this.request('/api/status');
  }

  async getStats() {
    return this.request('/api/stats');
  }

  async getHistory(limit = 50) {
    return this.request(`/api/history?limit=${limit}`);
  }

  async getScan(scanId) {
    return this.request(`/api/scan/${scanId}`);
  }

  async clearHistory() {
    return this.request('/api/history/clear', { method: 'POST' });
  }

  // Multimodal Detector Endpoints
  async analyzeImage(file) {
    const formData = new FormData();
    formData.append('image', file);
    formData.append('file', file);
    return this.request('/api/analyze/image', {
      method: 'POST',
      body: formData
    });
  }

  async analyzeVideo(file) {
    const formData = new FormData();
    formData.append('video', file);
    formData.append('file', file);
    return this.request('/api/analyze/video', {
      method: 'POST',
      body: formData
    }, 120000);
  }

  async analyzeAudio(file) {
    const formData = new FormData();
    formData.append('audio', file);
    formData.append('file', file);
    return this.request('/api/analyze/audio', {
      method: 'POST',
      body: formData
    });
  }

  async analyzeText(text) {
    return this.request('/api/analyze/text', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
  }

  async analyzeSMS(text) {
    return this.request('/api/analyze/text', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
  }

  async analyzeEmail(emailData) {
    const payload = typeof emailData === 'string' ? { body: emailData } : emailData;
    return this.request('/api/analyze/email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  }

  async analyzeJob(jobData) {
    return this.request('/api/analyze/job', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(jobData)
    });
  }

  async analyzeInternship(internshipData) {
    return this.request('/api/analyze/internship', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(internshipData)
    });
  }

  async analyzeUrl(url) {
    return this.request('/api/analyze/url', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
  }

  async analyzeOCR(fileOrText, filename = 'document.png') {
    if (typeof fileOrText === 'string') {
      return this.request('/api/analyze/ocr', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: fileOrText, filename })
      });
    } else {
      const formData = new FormData();
      formData.append('file', fileOrText);
      formData.append('image', fileOrText);
      return this.request('/api/analyze/ocr', {
        method: 'POST',
        body: formData
      });
    }
  }

  async analyzeCompany(companyName, website, email) {
    return this.request('/api/analyze/company', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ company_name: companyName, website, email })
    });
  }

  async analyzeSocial(content, url, platform = 'General') {
    return this.request('/api/analyze/social', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content, url, platform })
    });
  }

  async analyzeCameraFrame(blob, filename = 'camera_snapshot.jpg') {
    const formData = new FormData();
    const file = new File([blob], filename, { type: 'image/jpeg' });
    formData.append('image', file);
    formData.append('file', file);
    return this.request('/api/analyze/camera', {
      method: 'POST',
      body: formData
    });
  }

  async analyzeLiveAudio(blob, filename = 'live_recording.wav') {
    const formData = new FormData();
    const file = new File([blob], filename, { type: blob.type || 'audio/wav' });
    formData.append('audio', file);
    formData.append('file', file);
    return this.request('/api/analyze/live-audio', {
      method: 'POST',
      body: formData
    });
  }

  async analyzeMultimodal(formData) {
    return this.request('/api/analyze/multimodal', {
      method: 'POST',
      body: formData
    });
  }

  async askAssistant(query, scanContextOrId = null) {
    let scanId = null;
    let context = null;
    if (typeof scanContextOrId === 'object' && scanContextOrId !== null) {
      context = scanContextOrId;
      scanId = scanContextOrId.scan_id || scanContextOrId.id || null;
    } else if (scanContextOrId) {
      scanId = scanContextOrId;
    }
    return this.request('/api/assistant', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, scan_id: scanId, context })
    });
  }

  async getReports(limit = 50) {
    return this.request(`/api/reports?limit=${limit}`);
  }

  async createReport(reportData) {
    return this.request('/api/reports', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(reportData)
    });
  }

  async getReport(reportId) {
    return this.request(`/api/reports/${reportId}`);
  }
}

// Global instance attached to window
window.TrustGuardAPI = TrustGuardAPI;
window.tgAPI = new TrustGuardAPI();
TrustGuardAPI.askAssistant = (q, ctx) => window.tgAPI.askAssistant(q, ctx);

window.analyzeImage = (f) => window.tgAPI.analyzeImage(f);
window.analyzeVideo = (f) => window.tgAPI.analyzeVideo(f);
window.analyzeAudio = (f) => window.tgAPI.analyzeAudio(f);
window.analyzeText = (t) => window.tgAPI.analyzeText(t);
window.analyzeSMS = (s) => window.tgAPI.analyzeSMS(s);
window.analyzeEmail = (e) => window.tgAPI.analyzeEmail(e);
window.analyzeJob = (j) => window.tgAPI.analyzeJob(j);
window.analyzeUrl = (u) => window.tgAPI.analyzeUrl(u);
window.analyzeOCR = (f, name) => window.tgAPI.analyzeOCR(f, name);
window.analyzeCameraFrame = (b) => window.tgAPI.analyzeCameraFrame(b);
window.analyzeLiveAudio = (b) => window.tgAPI.analyzeLiveAudio(b);
window.analyzeMultimodal = (fd) => window.tgAPI.analyzeMultimodal(fd);
window.askAssistant = (q, ctx) => window.tgAPI.askAssistant(q, ctx);
window.getReports = (lim) => window.tgAPI.getReports(lim);
window.createReport = (rep) => window.tgAPI.createReport(rep);
window.getReport = (id) => window.tgAPI.getReport(id);
window.getStats = () => window.tgAPI.getStats();
window.getHistory = (lim) => window.tgAPI.getHistory(lim);
window.getScan = (id) => window.tgAPI.getScan(id);
