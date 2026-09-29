"""
TrustGuard AI — Windows User Startup Shortcut Installer
Places a background launcher into the current user's Windows Startup folder.
This ensures TrustGuard AI starts automatically on every Windows boot/logon without needing admin privileges.
"""
import os
import sys

def install_startup_shortcut():
    appdata = os.environ.get("APPDATA")
    if not appdata:
        print("[ERROR] APPDATA environment variable not found.")
        return False

    startup_dir = os.path.join(appdata, "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    if not os.path.exists(startup_dir):
        os.makedirs(startup_dir, exist_ok=True)

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    vbs_target = os.path.join(project_root, "start_trustguard_background.vbs")

    shortcut_file = os.path.join(startup_dir, "TrustGuardAI-AutoStart.vbs")
    
    # Write launcher script into Startup folder
    content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "{project_root}"
WshShell.Run "wscript.exe """ & "{vbs_target}" & """", 0, False
Set WshShell = Nothing
'''
    try:
        with open(shortcut_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[SUCCESS] Startup launcher successfully written to:\n  {shortcut_file}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to write startup launcher: {e}")
        return False

if __name__ == "__main__":
    install_startup_shortcut()
