"""
Verification test suite for TrustGuard AI login flow, SPA routes, and backend endpoints.
"""
import urllib.request
import urllib.error
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_routes():
    print("=" * 60)
    print("  TRUSTGUARD AI ROUTE & AUTHENTICATION VERIFICATION")
    print("=" * 60)

    # 1. Health check
    print("\n[1] Testing GET /api/health...")
    req = urllib.request.Request(f"{BASE_URL}/api/health")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode())
        print("  -> Health Response:", data)
        assert data.get("status") == "ok"

    # 2. Stats check
    print("\n[2] Testing GET /api/stats...")
    req = urllib.request.Request(f"{BASE_URL}/api/stats")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode())
        print("  -> Stats Response:", data)
        assert data.get("success") is True

    # 3. SPA Root & Subroutes returning index.html
    spa_paths = ["/", "/index.html", "/login", "/register", "/dashboard", "/image-analysis", "/video-analysis", "/audio-analysis", "/text-scam", "/job-scan", "/url-scanner", "/ocr-scanner", "/company-verification", "/social-media", "/profile", "/settings", "/history"]
    print("\n[3] Testing SPA Route Handlers (Expecting index.html on direct URL & refresh)...")
    for p in spa_paths:
        req = urllib.request.Request(f"{BASE_URL}{p}")
        with urllib.request.urlopen(req) as resp:
            assert resp.status == 200
            html = resp.read().decode('utf-8')
            assert "TrustGuard AI" in html
            assert "page-login" in html
            print(f"  -> Path {p.ljust(22)}: HTTP {resp.status} (Length: {len(html)} bytes) [OK]")

    # 4. Login with default admin credentials
    print("\n[4] Testing Login with Default Seeded Operator (admin@trustguard.ai / password123)...")
    login_data = json.dumps({"email": "admin@trustguard.ai", "password": "password123"}).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/api/auth/login", data=login_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        auth_res = json.loads(resp.read().decode())
        token = auth_res.get("token")
        user = auth_res.get("user")
        print(f"  -> Login Successful! Token: {token[:16]}... | User: {user.get('display_name')} ({user.get('email')})")
        assert token is not None
        assert user.get("email") == "admin@trustguard.ai"

    # 5. Profile / Session Check with Token
    print("\n[5] Testing GET /api/auth/me with Bearer Token...")
    req = urllib.request.Request(f"{BASE_URL}/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        me_res = json.loads(resp.read().decode())
        print(f"  -> Profile Authenticated: {me_res.get('authenticated')} | User: {me_res.get('user', {}).get('display_name')}")
        assert me_res.get("authenticated") is True

    # 6. Logout test
    print("\n[6] Testing POST /api/auth/logout...")
    req = urllib.request.Request(f"{BASE_URL}/api/auth/logout", data=b"{}", headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        logout_res = json.loads(resp.read().decode())
        print("  -> Logout Response:", logout_res)

    # 7. Verify Revoked Token
    print("\n[7] Verifying Token is Revoked after Logout...")
    req = urllib.request.Request(f"{BASE_URL}/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        me_res2 = json.loads(resp.read().decode())
        print(f"  -> Post-Logout /api/auth/me Response: {me_res2}")
        assert me_res2.get("authenticated") is False

    print("\n" + "=" * 60)
    print("  ALL 7 AUTHENTICATION & SPA ROUTING TESTS PASSED (100%)!")
    print("=" * 60)

if __name__ == "__main__":
    test_routes()
