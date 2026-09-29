import os
from pathlib import Path

dl = Path(r"C:\Users\paruc\Downloads")
out_file = Path(r"C:\Users\paruc\OneDrive\Desktop\Reshma\data\archive_14_15_contents.txt")

lines = []
for item in ["archive (14)", "archive (15)"]:
    p = dl / item
    if p.exists() and p.is_dir():
        lines.append(f"=== {item} ===")
        for f in os.listdir(p):
            fp = p / f
            lines.append(f"  {f} (dir={fp.is_dir()}, size={fp.stat().st_size if not fp.is_dir() else 0})")

out_file.write_text("\n".join(lines), encoding="utf-8")
print(f"Contents written to {out_file}", flush=True)
