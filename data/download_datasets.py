import kagglehub
import os

def download_face_dataset():
    print("Downloading Face Recognition Dataset...")
    return kagglehub.dataset_download(
        "vasukipatel/face-recognition-dataset"
    )

def download_voice_dataset():
    print("Downloading Speaker Recognition Dataset...")
    return kagglehub.dataset_download(
        "kongaevans/speaker-recognition-dataset"
    )

def download_iris_dataset():
    print("Downloading Multimodal Biometric Dataset (Iris/Backup)...")
    return kagglehub.dataset_download(
        "olankadhim/multimodal-biometric-dataset-mulb"
    )

if __name__ == "__main__":
    print("\n--- IDentix Dataset Downloader ---\n")
    
    face_path = download_face_dataset()
    voice_path = download_voice_dataset()
    iris_path = download_iris_dataset()
    
    print("\n--- DATASET PATHS (Copy these to config/paths_config.py) ---\n")
    print(f"FACE_DATASET_PATH = \"{face_path}\"")
    print(f"VOICE_DATASET_PATH = \"{voice_path}\"")
    print(f"IRIS_DATASET_PATH = \"{iris_path}\"")
    print("\n----------------------------------------------------------\n")
