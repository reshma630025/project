import pandas as pd
df = pd.read_csv(r"C:\Users\paruc\Downloads\archive (14)\test.csv")
r60 = df.iloc[60].to_dict()
print("ROW 60 (FAKE):", r60)
r0 = df.iloc[0].to_dict()
print("ROW 0 (REAL):", r0)
