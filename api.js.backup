/**
 * TrustGuard AI — Centralized API Client Layer
 * Handles communication with the FastAPI backend running at /api.
 */

window.API_BASE_URL = window.API_BASE_URL || window.location.origin;

class TrustGuardAPI {
  constructor(baseUrl = window.API_BASE_URL) {
    this.baseUrl = (baseUrl || window.location.origin).replace(/\/+$/, '');
  }

  /**
   * Generic request handler with error normalization.
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const token = localStorage.getItem('tg_token');
    
    const headers = options.headers || {};
    if (token) {
      headers['x-session-token'] = token;
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, { ...options, headers });
      if (!response.ok) {
        let errMessage = `HTTP ${response.status} ${response.statusText}`;
        try {
          const errData = await response.json();
          if (errData.detail) errMessage = typeof errData.detail === 'string' ? errData.detail : JSON.stringify(errData.detail);
          else if (errData.error) errMessage = errData.error;
        } catch (_) {}
        throw new Error(errMessage);
      }
      return await response.json();
    } catch (err) {
      console.error(`[TrustGuard API] Error calling ${endpoint}:`, err);
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
    });
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
