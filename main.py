"""
TrustGuard AI - Root Entry Point
Allows starting the server via:
  python main.py
  python -m uvicorn main:app --host 127.0.0.1 --port 8000
  python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
"""
import sys
from pathlib import Path
import uvicorn

# Ensure workspace root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.main import app

import socket
from scripts.detect_lan_ip import get_lan_ip

if __name__ == "__main__":
    lan_ip = get_lan_ip()
    print("=" * 60)
    print("  TrustGuard AI SOC Server Starting on 0.0.0.0:8000")
    print(f"  Local Access: http://127.0.0.1:8000/")
    print(f"  LAN Access:   http://{lan_ip}:8000/")
    print(f"  API Status:   http://{lan_ip}:8000/api/status")
    print("=" * 60)
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
