import sqlite3
from pathlib import Path

db_path = Path(r"C:\Users\paruc\OneDrive\Desktop\Reshma\backend\trustguard.db")
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("""
    SELECT id, scan_type, content_label, classification, confidence, risk_score, risk_level, timestamp
    FROM scan_history
    ORDER BY id DESC
    LIMIT 20
""")
rows = cursor.fetchall()
print(f"Total verified scans in database: {len(rows)}\n", flush=True)
print(f"{'ID':<4} | {'Scan Type':<12} | {'Content Label':<35} | {'Classification':<15} | {'Conf':<6} | {'Risk':<6} | {'Risk Level':<10}", flush=True)
print("-" * 100, flush=True)
for r in rows:
    lbl = (r['content_label'][:32] + '...') if len(r['content_label']) > 32 else r['content_label']
    print(f"{r['id']:<4} | {r['scan_type']:<12} | {lbl:<35} | {r['classification']:<15} | {r['confidence']:<6.1f} | {r['risk_score']:<6.1f} | {r['risk_level']:<10}", flush=True)
conn.close()
