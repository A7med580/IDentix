import json
import os
from datetime import datetime
from typing import Dict, List, Optional

DATABASE_PATH = 'data/database.json'

def load_database() -> Dict:
    """Load the database from JSON file."""
    if not os.path.exists(DATABASE_PATH):
        return initialize_database()
    
    with open(DATABASE_PATH, 'r') as f:
        return json.load(f)

def save_database(data: Dict) -> None:
    """Save the database to JSON file."""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    with open(DATABASE_PATH, 'w') as f:
        json.dump(data, f, indent=2)

def initialize_database() -> Dict:
    """Initialize empty database structure."""
    return {
        "admin": None,
        "persons": [],
        "attendance": [],
        "settings": {
            "late_threshold": "09:00:00",
            "work_start": "08:00:00",
            "work_end": "17:00:00"
        }
    }

# ============ ADMIN OPERATIONS ============

def set_admin(name: str, face_embedding: list) -> Dict:
    """Set admin credentials."""
    db = load_database()
    db['admin'] = {
        "id": "admin_001",
        "name": name,
        "face_embedding": face_embedding,
        "created_at": datetime.now().isoformat()
    }
    save_database(db)
    return db['admin']

def get_admin() -> Optional[Dict]:
    """Get admin data."""
    db = load_database()
    return db.get('admin')

# ============ PERSON OPERATIONS ============

def add_person(person_data: Dict) -> Dict:
    """Add a new person to the database."""
    db = load_database()
    
    # Generate ID
    person_id = f"P{len(db['persons']) + 1:03d}"
    
    person = {
        "id": person_id,
        "name": person_data['name'],
        "employee_id": person_data.get('employee_id', person_id),
        "date_of_birth": person_data.get('date_of_birth'),
        "gender": person_data.get('gender'),
        "department": person_data.get('department', 'General'),
        "email": person_data.get('email'),
        "phone": person_data.get('phone'),
        "face_embedding": person_data.get('face_embedding', []),
        "voice_mfcc": person_data.get('voice_mfcc', []),
        "registered_at": datetime.now().isoformat(),
        "status": "active"
    }
    
    db['persons'].append(person)
    save_database(db)
    return person

def get_person(person_id: str) -> Optional[Dict]:
    """Get person by ID."""
    db = load_database()
    for person in db['persons']:
        if person['id'] == person_id:
            return person
    return None

def get_all_persons(status: Optional[str] = None, department: Optional[str] = None) -> List[Dict]:
    """Get all persons with optional filters."""
    db = load_database()
    persons = db['persons']
    
    if status:
        persons = [p for p in persons if p['status'] == status]
    if department:
        persons = [p for p in persons if p['department'] == department]
    
    return persons

def update_person(person_id: str, updates: Dict) -> Optional[Dict]:
    """Update person information."""
    db = load_database()
    for i, person in enumerate(db['persons']):
        if person['id'] == person_id:
            db['persons'][i].update(updates)
            save_database(db)
            return db['persons'][i]
    return None

def deactivate_person(person_id: str) -> bool:
    """Deactivate a person."""
    return update_person(person_id, {"status": "inactive"}) is not None

# ============ ATTENDANCE OPERATIONS ============

def log_attendance(person_id: str, action: str, verification_method: str = "face_voice") -> Dict:
    """Log attendance (check-in or check-out)."""
    db = load_database()
    
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    
    # Find today's attendance record
    attendance_record = None
    for record in db['attendance']:
        if record['person_id'] == person_id and record['date'] == today:
            attendance_record = record
            break
    
    if action == "checkin":
        if attendance_record:
            # Update existing check-in
            attendance_record['check_in'] = current_time
        else:
            # Create new record
            late_threshold = db['settings']['late_threshold']
            status = "late" if current_time > late_threshold else "on_time"
            
            attendance_id = f"ATT{len(db['attendance']) + 1:05d}"
            attendance_record = {
                "id": attendance_id,
                "person_id": person_id,
                "date": today,
                "check_in": current_time,
                "check_out": None,
                "status": status,
                "verification_method": verification_method
            }
            db['attendance'].append(attendance_record)
    
    elif action == "checkout":
        if attendance_record:
            attendance_record['check_out'] = current_time
        else:
            # No check-in, create record with only check-out
            attendance_id = f"ATT{len(db['attendance']) + 1:05d}"
            attendance_record = {
                "id": attendance_id,
                "person_id": person_id,
                "date": today,
                "check_in": None,
                "check_out": current_time,
                "status": "incomplete",
                "verification_method": verification_method
            }
            db['attendance'].append(attendance_record)
    
    save_database(db)
    return attendance_record

def get_attendance_today() -> List[Dict]:
    """Get today's attendance records."""
    db = load_database()
    today = datetime.now().strftime("%Y-%m-%d")
    return [a for a in db['attendance'] if a['date'] == today]

def get_attendance_history(person_id: Optional[str] = None, 
                          start_date: Optional[str] = None,
                          end_date: Optional[str] = None) -> List[Dict]:
    """Get attendance history with filters."""
    db = load_database()
    records = db['attendance']
    
    if person_id:
        records = [r for r in records if r['person_id'] == person_id]
    if start_date:
        records = [r for r in records if r['date'] >= start_date]
    if end_date:
        records = [r for r in records if r['date'] <= end_date]
    
    return sorted(records, key=lambda x: x['date'], reverse=True)

# ============ ANALYTICS ============

def calculate_attendance_stats(person_id: str, start_date: str, end_date: str) -> Dict:
    """Calculate attendance statistics for a person."""
    records = get_attendance_history(person_id, start_date, end_date)
    
    total_days = len(records)
    on_time = len([r for r in records if r['status'] == 'on_time'])
    late = len([r for r in records if r['status'] == 'late'])
    absent = 0  # Calculate based on expected working days
    
    attendance_percentage = (total_days / (total_days + absent) * 100) if (total_days + absent) > 0 else 0
    
    return {
        "total_days_present": total_days,
        "on_time_count": on_time,
        "late_count": late,
        "absent_count": absent,
        "attendance_percentage": round(attendance_percentage, 2)
    }

def get_dashboard_overview() -> Dict:
    """Get overview statistics for dashboard."""
    db = load_database()
    today_attendance = get_attendance_today()
    
    total_persons = len([p for p in db['persons'] if p['status'] == 'active'])
    present_today = len(today_attendance)
    late_today = len([a for a in today_attendance if a['status'] == 'late'])
    
    return {
        "total_persons": total_persons,
        "present_today": present_today,
        "late_today": late_today,
        "attendance_rate": round((present_today / total_persons * 100) if total_persons > 0 else 0, 2)
    }
