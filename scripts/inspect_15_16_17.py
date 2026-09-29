import pandas as pd
import json
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

p15 = Path(r"C:\Users\paruc\Downloads\archive (15)")
prof = pd.read_csv(p15 / "raw_user_profiles.csv", nrows=10)
print("=== archive (15) raw_user_profiles.csv columns ===")
for col in prof.columns:
    print(f"  {col}: dtype={prof[col].dtype}, sample={prof[col].iloc[0]}")

act = pd.read_csv(p15 / "raw_user_activities.csv", nrows=10)
print("\n=== archive (15) raw_user_activities.csv columns ===")
for col in act.columns:
    print(f"  {col}: dtype={act[col].dtype}, sample={act[col].iloc[0]}")

print("\n=== archive (16) structure ===")
p16 = Path(r"C:\Users\paruc\Downloads\archive (16)")
subdirs16 = [d.name for d in p16.iterdir() if d.is_dir()]
print("Subdirs in archive (16):", subdirs16)
for sd in subdirs16:
    vids = list((p16 / sd).glob("*.mp4"))
    print(f"  {sd}: {len(vids)} mp4 videos")

txt16 = p16 / "List_of_testing_videos.txt"
if txt16.exists():
    with open(txt16, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    print(f"List_of_testing_videos.txt: {len(lines)} lines. First 5: {lines[:5]}")

print("\n=== archive (17) structure ===")
p17 = Path(r"C:\Users\paruc\Downloads\archive (17)")
for root, dirs, files in os.walk(p17):
    mp4s = [f for f in files if f.endswith(".mp4")]
    csvs = [f for f in files if f.endswith(".csv")]
    if mp4s or csvs:
        rel = os.path.relpath(root, p17)
        print(f"  {rel}: {len(mp4s)} mp4s, {len(csvs)} csvs")
