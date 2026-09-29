import os
from pathlib import Path

dl = Path(r"C:\Users\paruc\Downloads")
out_file = Path(r"C:\Users\paruc\OneDrive\Desktop\Reshma\data\downloads_check.txt")

lines = []
for i in range(1, 30):
    for pattern in [f"archive ({i})", f"archive ({i}).zip", f"archive_{i}"]:
        p = dl / pattern
        if p.exists():
            lines.append(f"EXISTS: {p} (dir={p.is_dir()})")

for name in ["instagram", "social", "fake_profiles", "spammer", "twitter", "facebook"]:
    p = dl / name
    if p.exists():
        lines.append(f"EXISTS: {p} (dir={p.is_dir()})")

out_file.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {len(lines)} findings to {out_file}", flush=True)
