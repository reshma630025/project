import os
import sys
import json
import csv
from pathlib import Path
from collections import Counter

PATHS_TO_INSPECT = [
    ("archive (4)", r"C:\Users\paruc\Downloads\archive (4)"),
    ("archive (5)", r"C:\Users\paruc\Downloads\archive (5)"),
    ("archive (6)", r"C:\Users\paruc\Downloads\archive (6)"),
    ("archive (7)", r"C:\Users\paruc\Downloads\archive (7)"),
    ("archive (9)", r"C:\Users\paruc\Downloads\archive (9)"),
    ("archive (10)", r"C:\Users\paruc\Downloads\archive (10)"),
    ("archive (11)", r"C:\Users\paruc\Downloads\archive (11)"),
    ("archive (12)", r"C:\Users\paruc\Downloads\archive (12)"),
    ("archive (13)", r"C:\Users\paruc\Downloads\archive (13)"),
    ("celeb-df-v2-metadata", r"C:\Users\paruc\Downloads\celeb-df-v2-metadata"),
    ("archive (1) - Audio (Existing)", r"C:\Users\paruc\Downloads\archive (1)\LA\LA"),
    ("archive - Image/1000_videos (Existing)", r"C:\Users\paruc\Downloads\archive\1000_videos")
]

results = {}

for label, p_str in PATHS_TO_INSPECT:
    p = Path(p_str)
    print(f"\n========================================================")
    print(f"INSPECTING: {label} -> {p_str}")
    print(f"========================================================")
    
    if not p.exists():
        print(f"EXISTS: False")
        results[label] = {"exists": False, "path": p_str}
        continue
        
    total_size = 0
    file_count = 0
    dir_count = 0
    ext_counter = Counter()
    sample_files = []
    metadata_files = []
    
    # Top level dirs/files
    top_entries = []
    try:
        for item in p.iterdir():
            top_entries.append((item.name, "DIR" if item.is_dir() else f"FILE ({item.stat().st_size:,} bytes)"))
    except Exception as e:
        top_entries = [f"Error listing top level: {e}"]
        
    print(f"Top-level entries ({len(top_entries)}):")
    for name, t in top_entries[:15]:
        print(f"  - {name} [{t}]")
    if len(top_entries) > 15:
        print(f"  ... and {len(top_entries) - 15} more entries")
        
    # Walk tree (capped if huge)
    for root, dirs, files in os.walk(p):
        dir_count += len(dirs)
        for f in files:
            file_count += 1
            fp = os.path.join(root, f)
            try:
                sz = os.path.getsize(fp)
                total_size += sz
            except Exception:
                sz = 0
            ext = os.path.splitext(f)[1].lower()
            ext_counter[ext] += 1
            if len(sample_files) < 10:
                sample_files.append(os.path.relpath(fp, p_str))
            if ext in ['.csv', '.json', '.txt', '.tsv', '.xlsx']:
                metadata_files.append((fp, sz))

    print(f"\nSummary:")
    print(f"  Total directories: {dir_count}")
    print(f"  Total files: {file_count}")
    print(f"  Total size: {total_size / (1024*1024):.2f} MB ({total_size:,} bytes)")
    print(f"  Extension distribution: {dict(ext_counter.most_common(10))}")
    
    # Inspect metadata files
    meta_inspections = []
    print(f"\nMetadata / Tabular files found ({len(metadata_files)}):")
    for fp, sz in metadata_files[:10]:
        rel = os.path.relpath(fp, p_str)
        print(f"\n  Analyzing: {rel} ({sz:,} bytes)")
        inspection = {"path": rel, "size": sz}
        ext = os.path.splitext(fp)[1].lower()
        if ext in ['.csv', '.tsv']:
            delimiter = '\t' if ext == '.tsv' else ','
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.reader(f, delimiter=delimiter)
                    header = next(reader, None)
                    inspection["header"] = header
                    print(f"    Header columns: {header}")
                    rows = []
                    for i, r in enumerate(reader):
                        if i < 3:
                            rows.append(r[:8]) # truncate wide rows
                        if i >= 500000: # safety cap
                            break
                    total_rows = i + 1 if 'i' in locals() else 0
                    inspection["sample_rows"] = rows
                    inspection["row_count"] = total_rows
                    print(f"    Row count: ~{total_rows}")
                    if rows:
                        print(f"    Sample row 0: {rows[0]}")
            except Exception as e:
                print(f"    Error reading CSV: {e}")
                inspection["error"] = str(e)
        elif ext == '.json':
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        inspection["type"] = "list"
                        inspection["len"] = len(data)
                        inspection["sample"] = data[:2]
                        print(f"    JSON list length: {len(data)}")
                    elif isinstance(data, dict):
                        inspection["type"] = "dict"
                        inspection["keys"] = list(data.keys())[:15]
                        print(f"    JSON dict keys: {list(data.keys())[:15]}")
            except Exception as e:
                print(f"    Error reading JSON: {e}")
                inspection["error"] = str(e)
        elif ext == '.txt':
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = [f.readline().strip() for _ in range(5)]
                    inspection["sample_lines"] = lines
                    print(f"    Sample lines: {lines[:3]}")
            except Exception as e:
                print(f"    Error reading TXT: {e}")
                inspection["error"] = str(e)
        meta_inspections.append(inspection)
        
    results[label] = {
        "exists": True,
        "path": p_str,
        "dir_count": dir_count,
        "file_count": file_count,
        "total_size_mb": round(total_size / (1024*1024), 2),
        "extensions": dict(ext_counter),
        "sample_files": sample_files,
        "top_entries": top_entries[:20],
        "metadata_inspections": meta_inspections
    }

# Save results to json for detailed analysis
output_json = Path(r"C:\Users\paruc\OneDrive\Desktop\Reshma\data\raw_inspection_results.json")
output_json.parent.mkdir(parents=True, exist_ok=True)
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print(f"\nInspection results saved to {output_json}")
