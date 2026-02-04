import numpy as np
import os

def extract_face_embeddings(image_path_or_array, model_name='VGG-Face'):
    """
    Extracts face embeddings using DeepFace.
    """
    try:
        from deepface import DeepFace  # Lazy import to avoid startup hang
        
        # DeepFace.represent returns a list of dictionaries (one per face)
        embeddings = DeepFace.represent(
            img_path=image_path_or_array,
            model_name=model_name,
            enforce_detection=False
        )
        
        if embeddings and len(embeddings) > 0:
            return np.array(embeddings[0]["embedding"])
        return None
    except Exception as e:
        print(f"Error extracting face embeddings: {e}")
        return None
