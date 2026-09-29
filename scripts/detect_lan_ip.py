"""
Detects the actual active IPv4 LAN address of the host computer.
"""
import socket
import subprocess
import re
import sys

def get_lan_ip():
    # Method 1: Outbound socket connection check (doesn't send traffic)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and not ip.startswith('127.'):
            return ip
    except Exception:
        pass

    # Method 2: Hostname resolution
    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if not ip.startswith('127.') and not ip.startswith('169.254'):
                return ip
    except Exception:
        pass

    # Method 3: ipconfig parse
    try:
        out = subprocess.check_output('ipconfig', shell=True, text=True, errors='ignore')
        matches = re.findall(r'IPv4 Address[ .:]+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', out)
        for m in matches:
            if not m.startswith('127.') and not m.startswith('169.254'):
                return m
    except Exception:
        pass

    return "127.0.0.1"

if __name__ == "__main__":
    ip = get_lan_ip()
    print(f"ACTUAL_LAN_IP={ip}")
