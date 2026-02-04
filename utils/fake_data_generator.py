"""
Generate fake data for the attendance management system.
Creates 20 people with realistic 6-month attendance history.
"""

import json
import random
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from utils.database_manager import initialize_database, save_database

fake = Faker()

# Departments
DEPARTMENTS = ['Engineering', 'Marketing', 'Sales', 'HR', 'Finance', 'Operations']

# Attendance patterns
PATTERNS = {
    'perfect': {'late_prob': 0.0, 'absent_prob': 0.0},      # 5 people
    'good': {'late_prob': 0.1, 'absent_prob': 0.05},        # 8 people
    'average': {'late_prob': 0.25, 'absent_prob': 0.15},    # 5 people
    'poor': {'late_prob': 0.4, 'absent_prob': 0.3}          # 2 people
}

def generate_fake_embedding(dim=2622):
    """Generate fake face embedding."""
    return np.random.randn(dim).tolist()

def generate_fake_mfcc(n_mfcc=13):
    """Generate fake voice MFCC."""
    return np.random.randn(n_mfcc).tolist()

def generate_check_in_time(is_late=False):
    """Generate realistic check-in time."""
    if is_late:
        # Late: 9:00 AM - 10:30 AM
        hour = random.randint(9, 10)
        minute = random.randint(0, 59) if hour == 9 else random.randint(0, 30)
    else:
        # On time: 7:30 AM - 8:59 AM
        hour = random.randint(7, 8)
        minute = random.randint(30, 59) if hour == 7 else random.randint(0, 59)
    
    return f"{hour:02d}:{minute:02d}:{random.randint(0, 59):02d}"

def generate_check_out_time():
    """Generate realistic check-out time."""
    hour = random.randint(17, 19)
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}:{random.randint(0, 59):02d}"

def generate_person(person_id, pattern_type):
    """Generate a fake person."""
    gender = random.choice(['Male', 'Female'])
    first_name = fake.first_name_male() if gender == 'Male' else fake.first_name_female()
    last_name = fake.last_name()
    
    return {
        "id": f"P{person_id:03d}",
        "name": f"{first_name} {last_name}",
        "employee_id": f"EMP{person_id:03d}",
        "date_of_birth": fake.date_of_birth(minimum_age=22, maximum_age=60).strftime("%Y-%m-%d"),
        "gender": gender,
        "department": random.choice(DEPARTMENTS),
        "email": f"{first_name.lower()}.{last_name.lower()}@company.com",
        "phone": fake.phone_number(),
        "face_embedding": generate_fake_embedding(),
        "voice_mfcc": generate_fake_mfcc(),
        "registered_at": "2025-08-01T10:00:00Z",
        "status": "active",
        "pattern": pattern_type  # For tracking (will be removed before saving)
    }

def generate_attendance_history(person, start_date, end_date):
    """Generate attendance history for a person."""
    pattern = PATTERNS[person['pattern']]
    attendance_records = []
    
    current_date = start_date
    attendance_id = 1
    
    while current_date <= end_date:
        # Skip weekends
        if current_date.weekday() < 5:  # Monday = 0, Friday = 4
            # Determine if absent
            if random.random() > pattern['absent_prob']:
                # Present
                is_late = random.random() < pattern['late_prob']
                
                record = {
                    "id": f"ATT{attendance_id:05d}",
                    "person_id": person['id'],
                    "date": current_date.strftime("%Y-%m-%d"),
                    "check_in": generate_check_in_time(is_late),
                    "check_out": generate_check_out_time(),
                    "status": "late" if is_late else "on_time",
                    "verification_method": "face_voice"
                }
                attendance_records.append(record)
                attendance_id += 1
        
        current_date += timedelta(days=1)
    
    return attendance_records

def generate_fake_data():
    """Generate complete fake database."""
    print("🔧 Generating fake data...")
    
    # Initialize database
    db = initialize_database()
    
    # Set admin
    print("👤 Creating admin...")
    db['admin'] = {
        "id": "admin_001",
        "name": "Admin User",
        "face_embedding": generate_fake_embedding(),
        "created_at": "2025-08-01T09:00:00Z"
    }
    
    # Generate 20 persons
    print("👥 Generating 20 persons...")
    pattern_distribution = (
        ['perfect'] * 5 +
        ['good'] * 8 +
        ['average'] * 5 +
        ['poor'] * 2
    )
    random.shuffle(pattern_distribution)
    
    persons = []
    for i, pattern in enumerate(pattern_distribution, 1):
        person = generate_person(i, pattern)
        persons.append(person)
        print(f"  ✓ {person['name']} ({person['department']}) - {pattern} attendance")
    
    db['persons'] = persons
    
    # Generate 6 months of attendance (Aug 2025 - Feb 2026)
    print("📅 Generating 6 months of attendance history...")
    start_date = datetime(2025, 8, 1)
    end_date = datetime(2026, 2, 4)
    
    all_attendance = []
    for person in persons:
        attendance = generate_attendance_history(person, start_date, end_date)
        all_attendance.extend(attendance)
        print(f"  ✓ {person['name']}: {len(attendance)} records")
        # Remove pattern field before saving
        del person['pattern']
    
    db['attendance'] = all_attendance
    
    # Save to file
    print("💾 Saving to database.json...")
    save_database(db)
    
    # Print summary
    print("\n✅ Fake data generation complete!")
    print(f"   📊 Total Persons: {len(db['persons'])}")
    print(f"   📊 Total Attendance Records: {len(db['attendance'])}")
    print(f"   📊 Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"   📂 Saved to: data/database.json")

if __name__ == "__main__":
    generate_fake_data()
