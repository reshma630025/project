import csv
import os
import sys

csv.field_size_limit(10000000)

print("=== 1. Fake Postings.csv (archive 5) ===")
with open(r"C:\Users\paruc\Downloads\archive (5)\Fake Postings.csv", "r", encoding="utf-8", errors="ignore") as f:
    reader = csv.DictReader(f)
    print("Fieldnames:", reader.fieldnames)
    counts = {}
    for i, row in enumerate(reader):
        val = row.get("fraudulent", "")
        counts[val] = counts.get(val, 0) + 1
        if i < 3:
            print(f"Sample {i}: title={row.get('title')}, fraudulent={val}, company={row.get('company_profile')[:30] if row.get('company_profile') else ''}")
    print("Fraudulent label distribution:", counts)

print("\n=== 2. archive (9) Email Datasets ===")
base = r"C:\Users\paruc\Downloads\archive (9)"
for fn in sorted(os.listdir(base)):
    if fn.endswith(".csv"):
        fp = os.path.join(base, fn)
        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            hdr = next(reader)
            label_col = -1
            for idx, col in enumerate(hdr):
                if any(k in col.lower() for k in ["label", "target", "fraud", "class", "spam"]):
                    label_col = idx
            counts = {}
            total = 0
            for r in reader:
                total += 1
                if label_col != -1 and len(r) > label_col:
                    lbl = r[label_col].strip()
                    counts[lbl] = counts.get(lbl, 0) + 1
            print(f"\n{fn} ({os.path.getsize(fp):,} bytes):")
            print(f"   Header: {hdr}")
            print(f"   Total rows: {total}")
            print(f"   Label col ({label_col}: '{hdr[label_col] if label_col != -1 else 'None'}'): {counts}")
