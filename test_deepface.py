print("Testing DeepFace import...")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TF logs

try:
    from deepface import DeepFace
    print("DeepFace imported successfully.")
except Exception as e:
    print(f"DeepFace import failed: {e}")
