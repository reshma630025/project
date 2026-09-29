import zipfile
from pathlib import Path

zip_dirs = [
    ("archive (3)", r"C:\Users\paruc\Downloads\archive (3)"),
    ("archive (8)", r"C:\Users\paruc\Downloads\archive (8)"),
    ("archive (10)", r"C:\Users\paruc\Downloads\archive (10)"),
    ("archive (11)", r"C:\Users\paruc\Downloads\archive (11)"),
    ("archive (12)", r"C:\Users\paruc\Downloads\archive (12)"),
    ("archive (13)", r"C:\Users\paruc\Downloads\archive (13)")
]

for label, p_str in zip_dirs:
    p = Path(p_str)
    print(f"\n==========================================")
    print(f"Checking zip files in {label}")
    zips = list(p.glob("*.zip"))
    for z in zips:
        print(f"  Zip file: {z.name} ({z.stat().st_size / (1024*1024):.2f} MB)")
        try:
            with zipfile.ZipFile(z, 'r') as zf:
                namelist = zf.namelist()
                print(f"  Total items in zip: {len(namelist)}")
                print(f"  First 10 items:")
                for item in namelist[:10]:
                    print(f"    - {item}")
        except Exception as e:
            print(f"  Error reading zip: {e}")
