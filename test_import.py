print("Starting import test...")
import os
import sys

# Add project root
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from fusion.fusion_engine import FusionEngine
    print("FusionEngine imported successfully.")
except Exception as e:
    print(f"Import failed: {e}")

print("Test complete.")
