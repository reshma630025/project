import urllib.request
import sys

try:
    resp = urllib.request.urlopen('http://127.0.0.1:8000/api/status', timeout=1)
    if resp.getcode() == 200:
        sys.exit(0)
    else:
        sys.exit(1)
except Exception:
    sys.exit(1)
