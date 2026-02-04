import librosa
import numpy as np

def load_and_preprocess_audio(audio_path, sr=16000, duration=3):
    """
    Loads audio, trims silence, and ensures fixed duration.
    """
    try:
        y, _ = librosa.load(audio_path, sr=sr)
        
        # Trim leading/trailing silence
        y_trimmed, _ = librosa.effects.trim(y)
        
        # Ensure fixed duration for consistency
        max_samples = sr * duration
        if len(y_trimmed) > max_samples:
            y_trimmed = y_trimmed[:max_samples]
        else:
            padding = max_samples - len(y_trimmed)
            y_trimmed = np.pad(y_trimmed, (0, padding), 'constant')
            
        return y_trimmed
    except Exception as e:
        print(f"Error processing audio {audio_path}: {e}")
        return None

def normalize_audio(y):
    """
    Normalizes audio amplitude.
    """
    if y is None:
        return None
    return librosa.util.normalize(y)
