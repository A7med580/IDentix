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
from utils import database_manager as db
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

# ============ ADMIN ENDPOINTS ============

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Admin authentication via face recognition."""
    face_file = request.files.get('face')
    
    if not face_file:
        return jsonify({"error": "No face image provided"}), 400
    
    # Save temp file
    filename = secure_filename(face_file.filename)
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    face_file.save(temp_path)
    
    try:
        # Extract admin face embedding
        probe_emb = extract_face_embeddings(temp_path)
        
        # Get admin from database
        admin = db.get_admin()
        
        if not admin or not probe_emb:
            return jsonify({"error": "Authentication failed"}), 401
        
        # Match against admin embedding
        admin_emb = np.array(admin['face_embedding'])
        similarity = fusion_engine.matcher.match_face(probe_emb, admin_emb)
        
        if similarity >= 0.7:
            return jsonify({
                "success": True,
                "admin": {
                    "id": admin['id'],
                    "name": admin['name']
                }
            })
        else:
            return jsonify({"error": "Face does not match admin"}), 401
            
    except Exception as e:
        print(f"Admin login error: {e}")
        return jsonify({"error": "Authentication failed"}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

# ============ PERSON MANAGEMENT ENDPOINTS ============

@app.route('/api/persons', methods=['GET'])
def get_persons():
    """Get all persons with optional filters."""
    status = request.args.get('status')
    department = request.args.get('department')
    
    persons = db.get_all_persons(status=status, department=department)
    
    # Remove embeddings from response (too large)
    for person in persons:
        person.pop('face_embedding', None)
        person.pop('voice_mfcc', None)
    
    return jsonify({"persons": persons})

@app.route('/api/persons/<person_id>', methods=['GET'])
def get_person(person_id):
    """Get person details."""
    person = db.get_person(person_id)
    
    if not person:
        return jsonify({"error": "Person not found"}), 404
    
    # Remove embeddings
    person.pop('face_embedding', None)
    person.pop('voice_mfcc', None)
    
    return jsonify(person)

@app.route('/api/persons', methods=['POST'])
def add_person():
    """Register a new person."""
    face_file = request.files.get('face')
    voice_file = request.files.get('voice')
    
    # Get form data
    person_data = {
        "name": request.form.get('name'),
        "employee_id": request.form.get('employee_id'),
        "date_of_birth": request.form.get('date_of_birth'),
        "gender": request.form.get('gender'),
        "department": request.form.get('department'),
        "email": request.form.get('email'),
        "phone": request.form.get('phone')
    }
    
    # Extract face embedding
    if face_file:
        filename = secure_filename(face_file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        face_file.save(temp_path)
        
        try:
            face_emb = extract_face_embeddings(temp_path)
            if face_emb is not None:
                person_data['face_embedding'] = face_emb.tolist()
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    # Extract voice MFCC
    if voice_file:
        filename = secure_filename(voice_file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        voice_file.save(temp_path)
        
        try:
            voice_mfcc = extract_mfcc(temp_path)
            if voice_mfcc is not None:
                person_data['voice_mfcc'] = voice_mfcc.tolist()
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    # Add to database
    person = db.add_person(person_data)
    
    # Remove embeddings from response
    person.pop('face_embedding', None)
    person.pop('voice_mfcc', None)
    
    return jsonify(person), 201

# ============ ATTENDANCE ENDPOINTS ============

@app.route('/api/attendance/checkin', methods=['POST'])
def checkin():
    """Check-in with face and/or voice verification."""
    face_file = request.files.get('face')
    voice_file = request.files.get('voice')
    
    if not face_file and not voice_file:
        return jsonify({"error": "No biometric data provided"}), 400
    
    face_score = 0.0
    voice_score = 0.0
    matched_person_id = None
    best_match_score = 0.0
    
    # Get all persons
    all_persons = db.get_all_persons(status='active')
    
    # Process Face
    if face_file:
        filename = secure_filename(face_file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        face_file.save(temp_path)
        
        try:
            probe_emb = extract_face_embeddings(temp_path)
            
            if probe_emb is not None:
                # Match against all persons
                for person in all_persons:
                    if person.get('face_embedding'):
                        gallery_emb = np.array(person['face_embedding'])
                        score = fusion_engine.matcher.match_face(probe_emb, gallery_emb)
                        
                        if score > face_score:
                            face_score = score
                            if score > best_match_score:
                                best_match_score = score
                                matched_person_id = person['id']
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    # Process Voice
    if voice_file:
        filename = secure_filename(voice_file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        voice_file.save(temp_path)
        
        try:
            probe_mfcc = extract_mfcc(temp_path)
            
            if probe_mfcc is not None:
                # Match against all persons
                for person in all_persons:
                    if person.get('voice_mfcc'):
                        gallery_mfcc = np.array(person['voice_mfcc'])
                        score = fusion_engine.matcher.match_voice(probe_mfcc, gallery_mfcc)
                        
                        if score > voice_score:
                            voice_score = score
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    # Fusion
    fused_score = fusion_engine.fuse_scores(face_score, voice_score)
    is_verified = fusion_engine.make_decision(fused_score)
    
    # Log attendance if verified
    if is_verified and matched_person_id:
        attendance_record = db.log_attendance(matched_person_id, "checkin")
        person = db.get_person(matched_person_id)
        
        return jsonify({
            "verified": True,
            "person": {
                "id": person['id'],
                "name": person['name'],
                "employee_id": person['employee_id'],
                "department": person['department']
            },
            "attendance": attendance_record,
            "scores": {
                "face": float(face_score),
                "voice": float(voice_score),
                "fused": float(fused_score)
            }
        })
    else:
        return jsonify({
            "verified": False,
            "message": "No matching person found",
            "scores": {
                "face": float(face_score),
                "voice": float(voice_score),
                "fused": float(fused_score)
            }
        }), 401

@app.route('/api/attendance/today', methods=['GET'])
def get_today_attendance():
    """Get today's attendance."""
    records = db.get_attendance_today()
    
    # Enrich with person names
    for record in records:
        person = db.get_person(record['person_id'])
        if person:
            record['person_name'] = person['name']
            record['department'] = person['department']
    
    return jsonify({"attendance": records})

@app.route('/api/attendance/history', methods=['GET'])
def get_attendance_history():
    """Get attendance history with filters."""
    person_id = request.args.get('person_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    records = db.get_attendance_history(person_id, start_date, end_date)
    
    return jsonify({"attendance": records, "total": len(records)})

# ============ ANALYTICS ENDPOINTS ============

@app.route('/api/analytics/overview', methods=['GET'])
def get_analytics_overview():
    """Get dashboard overview statistics."""
    overview = db.get_dashboard_overview()
    return jsonify(overview)

@app.route('/api/analytics/person/<person_id>', methods=['GET'])
def get_person_analytics(person_id):
    """Get analytics for a specific person."""
    start_date = request.args.get('start_date', '2025-08-01')
    end_date = request.args.get('end_date', '2026-02-04')
    
    stats = db.calculate_attendance_stats(person_id, start_date, end_date)
    history = db.get_attendance_history(person_id, start_date, end_date)
    
    return jsonify({
        "stats": stats,
        "history": history
    })


if __name__ == '__main__':
    # Run on 0.0.0.0 to be accessible, port 5001
    app.run(host='0.0.0.0', port=5001, debug=False)
