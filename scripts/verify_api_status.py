import urllib.request
import json

try:
    with urllib.request.urlopen("http://127.0.0.1:8000/api/status", timeout=5) as resp:
        data = json.loads(resp.read().decode())
    print("API STATUS RESPONSE:")
    print(json.dumps(data, indent=2))
except Exception as e:
    print("Error fetching status:", e)
