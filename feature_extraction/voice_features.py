import librosa
import numpy as np

def extract_mfcc(y, sr=16000, n_mfcc=13):
    """
    Extracts MFCC features from preprocessed audio signal.
    Returns the mean MFCC across time.
    """
    if y is None:
        return None
    
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    # Use mean of MFCCs as a fixed-length feature vector
    mfccs_scaled = np.mean(mfccs.T, axis=0)
    return mfccs_scaled

def compute_euclidean_distance(feat1, feat2):
    """
    Computes Euclidean distance between two feature vectors.
    """
    if feat1 is None or feat2 is None:
        return float('inf')
    return np.linalg.norm(feat1 - feat2)

def compute_correlation(feat1, feat2):
    """
    Computes correlation-based similarity score.
    """
    if feat1 is None or feat2 is None:
        return 0.0
    return np.corrcoef(feat1, feat2)[0, 1]
