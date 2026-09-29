import os
import sys
import json
import csv
from pathlib import Path
from collections import Counter

ALL_PATHS = [
    ("celeb-df-v2-metadata", r"C:\Users\paruc\Downloads\celeb-df-v2-metadata"),
    ("archive", r"C:\Users\paruc\Downloads\archive"),
    ("archive (1)", r"C:\Users\paruc\Downloads\archive (1)"),
    ("archive (3)", r"C:\Users\paruc\Downloads\archive (3)"),
    ("archive (4)", r"C:\Users\paruc\Downloads\archive (4)"),
    ("archive (5)", r"C:\Users\paruc\Downloads\archive (5)"),
    ("archive (6)", r"C:\Users\paruc\Downloads\archive (6)"),
    ("archive (7)", r"C:\Users\paruc\Downloads\archive (7)"),
    ("archive (8)", r"C:\Users\paruc\Downloads\archive (8)"),
    ("archive (9)", r"C:\Users\paruc\Downloads\archive (9)"),
    ("archive (10)", r"C:\Users\paruc\Downloads\archive (10)"),
    ("archive (11)", r"C:\Users\paruc\Downloads\archive (11)"),
    ("archive (12)", r"C:\Users\paruc\Downloads\archive (12)"),
    ("archive (13)", r"C:\Users\paruc\Downloads\archive (13)"),
    ("archive (14)", r"C:\Users\paruc\Downloads\archive (14)"),
    ("archive (15)", r"C:\Users\paruc\Downloads\archive (15)"),
    ("archive (16)", r"C:\Users\paruc\Downloads\archive (16)"),
    ("archive (17)", r"C:\Users\paruc\Downloads\archive (17)")
]

report = {}

for name, p_str in ALL_PATHS:
    p = Path(p_str)
    entry = {
        "name": name,
        "path": p_str,
        "exists": p.exists(),
        "files": [],
        "file_count": 0,
        "total_size_bytes": 0,
        "ext_counts": {},
        "tabular_files": [],
        "media_samples": [],
        "subdirs": []
    }
    
    if not p.exists():
        report[name] = entry
        continue
        
    ext_cnt = Counter()
    total_size = 0
    file_list = []
    
    try:
        subdirs = [d.name for d in p.iterdir() if d.is_dir()]
        entry["subdirs"] = subdirs[:15]
    except Exception as e:
        entry["subdirs_error"] = str(e)

    for root, dirs, files in os.walk(p):
        for f in files:
            fp = Path(root) / f
            try:
                sz = fp.stat().st_size
            except Exception:
                sz = 0
            total_size += sz
            ext = fp.suffix.lower()
            ext_cnt[ext] += 1
            rel = str(fp.relative_to(p))
            file_list.append((rel, sz, ext))
            
    entry["file_count"] = len(file_list)
    entry["total_size_bytes"] = total_size
    entry["total_size_mb"] = round(total_size / (1024 * 1024), 2)
    entry["ext_counts"] = dict(ext_cnt.most_common(10))
    
    # Analyze tabular or json files
    for rel, sz, ext in file_list:
        full_p = p / rel
        if ext in ['.csv', '.tsv', '.json', '.txt'] and sz < 250 * 1024 * 1024:
            tab_info = {"rel_path": rel, "size_bytes": sz, "ext": ext}
            if ext in ['.csv', '.tsv']:
                delimiter = '\t' if ext == '.tsv' else ','
                try:
                    with open(full_p, 'r', encoding='utf-8', errors='ignore') as f:
                        reader = csv.reader(f, delimiter=delimiter)
                        header = next(reader, None)
                        tab_info["columns"] = header
                        row_count = 0
                        sample_rows = []
                        label_candidates = {}
                        for r in reader:
                            row_count += 1
                            if row_count <= 3:
                                sample_rows.append(r[:10])
                            # check potential label columns
                            if header:
                                for col_idx, col_name in enumerate(header):
                                    col_lower = col_name.lower().strip()
                                    if any(k in col_lower for k in ['label', 'target', 'class', 'fraud', 'fake', 'spam', 'type', 'result', 'status', 'is_']):
                                        if col_name not in label_candidates:
                                            label_candidates[col_name] = Counter()
                                        val = r[col_idx] if col_idx < len(r) else ""
                                        label_candidates[col_name][val] += 1
                        tab_info["row_count"] = row_count
                        tab_info["sample_rows"] = sample_rows
                        tab_info["label_candidates"] = {k: dict(v.most_common(10)) for k, v in label_candidates.items()}
                except Exception as e:
                    tab_info["read_error"] = str(e)
            elif ext == '.json' and sz < 5 * 1024 * 1024:
                try:
                    with open(full_p, 'r', encoding='utf-8', errors='ignore') as f:
                        jdata = json.load(f)
                        if isinstance(jdata, list):
                            tab_info["json_type"] = "list"
                            tab_info["json_len"] = len(jdata)
                            if len(jdata) > 0 and isinstance(jdata[0], dict):
                                tab_info["json_keys"] = list(jdata[0].keys())
                        elif isinstance(jdata, dict):
                            tab_info["json_type"] = "dict"
                            tab_info["json_keys"] = list(jdata.keys())[:20]
                except Exception as e:
                    tab_info["json_error"] = str(e)
            entry["tabular_files"].append(tab_info)
        elif ext in ['.mp4', '.avi', '.mov', '.png', '.jpg', '.jpeg', '.flac', '.wav', '.mp3']:
            if len(entry["media_samples"]) < 10:
                entry["media_samples"].append(rel)
                
    report[name] = entry
    print(f"[{name}] Files: {entry['file_count']}, Size: {entry['total_size_mb']} MB, Exts: {entry['ext_counts']}")
    if entry["tabular_files"]:
        print(f"  Tabular: {[t['rel_path'] for t in entry['tabular_files'][:5]]}")
        for t in entry["tabular_files"][:3]:
            if "columns" in t:
                print(f"    {t['rel_path']}: {len(t.get('columns', []))} cols, {t.get('row_count')} rows. Label candidates: {t.get('label_candidates')}")
    if entry["media_samples"]:
        print(f"  Media samples ({len(entry['media_samples'])}): {entry['media_samples'][:3]}")

# Save full report
out_p = Path("data") / "all_18_datasets_raw_inspection.json"
out_p.parent.mkdir(parents=True, exist_ok=True)
with open(out_p, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print(f"\nInspection saved to {out_p}")
