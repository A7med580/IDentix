import os

# --- Dataset Paths (Update these after running data/download_datasets.py) ---
FACE_DATASET_PATH = "" 
VOICE_DATASET_PATH = ""
IRIS_DATASET_PATH = ""

# --- Precomputed Feature Paths (For storage-constrained environments) ---
# If you processed data on Colab, point these to your local copies of .npy / .pkl files
PRECOMPUTED_FACE_FEATURES = "data/features/face_embeddings.npy"
PRECOMPUTED_VOICE_FEATURES = "data/features/voice_mfccs.npy"

# --- Output Directories ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
EVAL_DIR = os.path.join(BASE_DIR, "evaluation", "reports")

# Ensure directories exist
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(EVAL_DIR, exist_ok=True)
os.makedirs(os.path.dirname(PRECOMPUTED_FACE_FEATURES), exist_ok=True)
