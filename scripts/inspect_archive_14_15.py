import os
import zipfile
from pathlib import Path

dl = Path(r"C:\Users\paruc\Downloads")
out_file = Path(r"C:\Users\paruc\OneDrive\Desktop\Reshma\data\archive_14_15_inspection.txt")

lines = []

for item in ["archive (14)", "archive (15)"]:
    p = dl / item
    if p.exists() and p.is_dir():
        lines.append(f"=== {item} (Directory) ===")
        for root, dirs, files in os.walk(p):
            for f in files:
                fp = Path(root) / f
                lines.append(f"  {fp.relative_to(p)} ({fp.stat().st_size:,} bytes)")

for zname in ["archive (2).zip", "archive (3).zip", "archive (8).zip"]:
    zp = dl / zname
    if zp.exists():
        lines.append(f"=== {zname} (Zip) ===")
        try:
            with zipfile.ZipFile(zp, 'r') as z:
                for zi in z.infolist()[:10]:
                    lines.append(f"  {zi.filename} ({zi.file_size:,} bytes)")
        except Exception as e:
            lines.append(f"  Error reading zip: {e}")

out_file.write_text("\n".join(lines), encoding="utf-8")
print(f"Inspection complete. Written to {out_file}", flush=True)
