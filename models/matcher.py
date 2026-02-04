import numpy as np
from feature_extraction.face_features import compute_cosine_similarity
from feature_extraction.voice_features import compute_euclidean_distance

class BiometricMatcher:
    def __init__(self, face_threshold=0.6, voice_threshold=10.0):
        self.face_threshold = face_threshold
        self.voice_threshold = voice_threshold

    def match_face(self, probe_embedding, gallery_embedding):
        """
        Matches two face embeddings. Higher score is better.
        """
        similarity = compute_cosine_similarity(probe_embedding, gallery_embedding)
        return similarity

    def match_voice(self, probe_mfcc, gallery_mfcc):
        """
        Matches two voice MFCCs. Lower distance is better.
        We convert distance to similarity: 1 / (1 + distance)
        """
        distance = compute_euclidean_distance(probe_mfcc, gallery_mfcc)
        similarity = 1.0 / (1.0 + distance)
        return similarity

    def verify_identity(self, face_score, voice_score, fusion_threshold=0.5):
        """
        Simple decision-level check for individual modalities (optional).
        """
        face_pass = face_score >= self.face_threshold
        voice_pass = voice_score >= (1.0 / (1.0 + self.voice_threshold))
        return face_pass, voice_pass
