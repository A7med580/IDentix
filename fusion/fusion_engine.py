import numpy as np

class FusionEngine:
    def __init__(self, face_weight=0.6, voice_weight=0.4):
        self.face_weight = face_weight
        self.voice_weight = voice_weight

    def normalize_scores(self, scores):
        """
        Simple Min-Max normalization (not always needed if using similarities).
        """
        if len(scores) == 0:
            return scores
        min_val = min(scores)
        max_val = max(scores)
        if max_val == min_val:
            return [1.0 for _ in scores]
        return [(s - min_val) / (max_val - min_val) for s in scores]

    def fuse_scores(self, face_score, voice_score):
        """
        Implements weighted sum fusion.
        """
        if face_score is None: face_score = 0.0
        if voice_score is None: voice_score = 0.0
        
        fused_score = (self.face_weight * face_score) + (self.voice_weight * voice_score)
        return fused_score

    def make_decision(self, fused_score, threshold=0.7):
        """
        Final authentication decision.
        """
        return fused_score >= threshold
