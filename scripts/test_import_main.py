import sys
import traceback
sys.path.insert(0, r"C:\Users\paruc\OneDrive\Desktop\Reshma")

try:
    import backend.main
    print("Backend main imported successfully!", flush=True)
except Exception as e:
    print("Import error:", e, flush=True)
    traceback.print_exc()
