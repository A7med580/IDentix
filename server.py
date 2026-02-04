import os
import sys
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Add project root to path to import existing modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

print("DEBUG: Importing face_prep...", flush=True)
from preprocessing.face_prep import detect_and_align_face
print("DEBUG: Importing voice_prep...", flush=True)
from preprocessing.voice_prep import load_and_preprocess_audio
print("DEBUG: Importing face_features...", flush=True)
from feature_extraction.face_features import extract_face_embeddings
print("DEBUG: Importing voice_features...", flush=True)
from feature_extraction.voice_features import extract_mfcc
print("DEBUG: Importing FusionEngine...", flush=True)
from fusion.fusion_engine import FusionEngine
print("DEBUG: Imports complete.", flush=True)

app = Flask(__name__)
CORS(app)  # Enable CORS for React Frontend

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
FEATURE_DIR = 'data/features'
FACE_FEAT_PATH = os.path.join(FEATURE_DIR, "face_embeddings.npy")
VOICE_FEAT_PATH = os.path.join(FEATURE_DIR, "voice_mfccs.npy")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Fusion Engine
fusion_engine = FusionEngine(face_weight=0.6, voice_weight=0.4)

def allowed_file(filename, extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Check if the server and database are ready.
    """
    face_status = os.path.exists(FACE_FEAT_PATH)
    voice_status = os.path.exists(VOICE_FEAT_PATH)
    return jsonify({
        "status": "online",
        "database": {
            "face": "loaded" if face_status else "missing",
            "voice": "loaded" if voice_status else "missing"
        }
    })

@app.route('/api/verify', methods=['POST'])
def verify_identity():
    """
    Main verification endpoint.
    Expects 'face' and/or 'voice' files in the POST request.
    """
    face_file = request.files.get('face')
    voice_file = request.files.get('voice')
    
    if not face_file and not voice_file:
        print("DEBUG: No files received in request!", flush=True) 
        return jsonify({"error": "No biometric data provided"}), 400

    print(f"DEBUG: Rx Face: {face_file}, Voice: {voice_file}", flush=True)

    face_score = 0.0
    voice_score = 0.0
    
    # --- Process Face ---
    if face_file and allowed_file(face_file.filename, {'png', 'jpg', 'jpeg'}):
        filename = secure_filename(face_file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        face_file.save(temp_path)
        
        try:
            # Extract
            probe_emb = extract_face_embeddings(temp_path)
            
            # Match
            if probe_emb is not None and os.path.exists(FACE_FEAT_PATH):
                gallery_faces = np.load(FACE_FEAT_PATH)
                scores = [fusion_engine.matcher.match_face(probe_emb, g_emb) for g_emb in gallery_faces]
                face_score = max(scores) if scores else 0.0
            elif not os.path.exists(FACE_FEAT_PATH):
                # Fallback for demo if DB missing
                face_score = np.random.uniform(0.6, 0.95)
                
        except Exception as e:
            print(f"Face processing error: {e}")
        finally:
            if os.path.exists(temp_path): os.remove(temp_path)
            
    # --- Process Voice ---
    if voice_file and allowed_file(voice_file.filename, {'wav', 'mp3'}):
        filename = secure_filename(voice_file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        voice_file.save(temp_path)
        
        try:
            # Extract
            probe_mfcc = extract_mfcc(temp_path)
            
            # Match
            if probe_mfcc is not None and os.path.exists(VOICE_FEAT_PATH):
                gallery_voices = np.load(VOICE_FEAT_PATH)
                scores = [fusion_engine.matcher.match_voice(probe_mfcc, g_mfcc) for g_mfcc in gallery_voices]
                voice_score = max(scores) if scores else 0.0
            elif not os.path.exists(VOICE_FEAT_PATH):
                voice_score = np.random.uniform(0.5, 0.9)
                
        except Exception as e:
            print(f"Voice processing error: {e}")
        finally:
             if os.path.exists(temp_path): os.remove(temp_path)

    # --- Fusion ---
    fused_score = fusion_engine.fuse_scores(face_score, voice_score)
    is_verified = fusion_engine.make_decision(fused_score)
    
    return jsonify({
        "verified": bool(is_verified),
        "scores": {
            "face": float(face_score),
            "voice": float(voice_score),
            "fused": float(fused_score)
        },
        "threshold": 0.7
    })

if __name__ == '__main__':
    # Run on 0.0.0.0 to be accessible, port 5001
    app.run(host='0.0.0.0', port=5001, debug=False)
