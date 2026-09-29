import os
import pandas as pd
from pathlib import Path

dl = Path(r"C:\Users\paruc\Downloads")
out_file = Path(r"C:\Users\paruc\OneDrive\Desktop\Reshma\data\social_media_datasets_detailed.txt")

lines = []

def inspect_df(p, name):
    lines.append(f"\n=======================================================")
    lines.append(f"DATASET: {name} ({p})")
    lines.append(f"=======================================================")
    if not p.exists():
        lines.append(f"File not found: {p}")
        return
    try:
        df = pd.read_csv(p)
        lines.append(f"Rows: {len(df):,}")
        lines.append(f"Columns ({len(df.columns)}): {list(df.columns)}")
        lines.append("\nData Types:")
        for col, dt in df.dtypes.items():
            lines.append(f"  - {col}: {dt} (Nulls: {df[col].isnull().sum()})")
        
        # Check potential target columns
        for target in ["fake", "is_fake", "label", "class", "target", "spammer", "is_spammer"]:
            if target in df.columns:
                lines.append(f"\nLabel Distribution for '{target}':")
                lines.append(str(df[target].value_counts(dropna=False)))
                
        lines.append("\nFirst 3 rows:")
        lines.append(df.head(3).to_string())
    except Exception as e:
        lines.append(f"Error inspecting {name}: {e}")

# Inspect archive (14)
inspect_df(dl / "archive (14)" / "train.csv", "archive (14) - train.csv")
inspect_df(dl / "archive (14)" / "test.csv", "archive (14) - test.csv")

# Inspect archive (15)
inspect_df(dl / "archive (15)" / "raw_user_profiles.csv", "archive (15) - raw_user_profiles.csv")
inspect_df(dl / "archive (15)" / "raw_user_activities.csv", "archive (15) - raw_user_activities.csv")

out_file.write_text("\n".join(lines), encoding="utf-8")
print(f"Social media datasets inspection written to {out_file}", flush=True)
