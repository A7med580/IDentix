from deepface import DeepFace
import numpy as np

def extract_face_embeddings(image_path_or_array, model_name='VGG-Face'):
    """
    Extracts face embeddings using DeepFace.
    """
    try:
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

def compute_cosine_similarity(embedding1, embedding2):
    """
    Computes cosine similarity between two embeddings.
    """
    if embedding1 is None or embedding2 is None:
        return 0.0
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    return dot_product / (norm1 * norm2)
