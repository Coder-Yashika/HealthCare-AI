import json
import os
import hashlib
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
SCREENINGS_FILE = os.path.join(DATA_DIR, "screenings.json")

def _hash_password(password: str) -> str:
    """Hashes a password using SHA-256 with a salt."""
    salt = "healthai_secure_salt_2026"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def _ensure_data_files():
    """Initializes data directory and default seeded users if not present."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(USERS_FILE):
        default_users = {
            "dr.alex@healthai.org": {
                "email": "dr.alex@healthai.org",
                "password_hash": _hash_password("admin123"),
                "name": "Dr. Alex Sharma",
                "role": "Doctor",
                "specialty": "Cardiology & Internal Medicine",
                "license_id": "MED-IND-8849",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            },
            "rahul@patient.com": {
                "email": "rahul@patient.com",
                "password_hash": _hash_password("patient123"),
                "name": "Rahul Verma",
                "role": "Patient",
                "age": 38,
                "blood_group": "O+",
                "emergency_contact": "+91 98765 43210",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
        }
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_users, f, indent=4)

    if not os.path.exists(SCREENINGS_FILE):
        default_screenings = [
            {
                "case_id": "HLT-1001",
                "user_email": "rahul@patient.com",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "condition": "Heart Disease",
                "stage": "Stage 1: Early Pre-Condition (Mild)",
                "confidence": 95.2,
                "specialist": "Cardiologist",
                "vitals_summary": "BP: 135/88, Glucose: 105, BMI: 26.2"
            }
        ]
        with open(SCREENINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_screenings, f, indent=4)

def get_all_users():
    _ensure_data_files()
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def register_user(email, password, name, role="Patient", extra_info=None):
    """
    Registers a new user into the JSON database.
    Returns (success: bool, message: str, user_dict: dict or None)
    """
    _ensure_data_files()
    users = get_all_users()
    email_clean = email.strip().lower()

    if not email_clean or "@" not in email_clean:
        return False, "Please enter a valid email address.", None

    if len(password) < 6:
        return False, "Password must be at least 6 characters long.", None

    if email_clean in users:
        return False, "An account with this email address already exists. Please log in.", None

    user_data = {
        "email": email_clean,
        "password_hash": _hash_password(password),
        "name": name.strip(),
        "role": role,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    if extra_info and isinstance(extra_info, dict):
        user_data.update(extra_info)

    users[email_clean] = user_data
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

    # Return clean user profile without password hash
    profile = {k: v for k, v in user_data.items() if k != "password_hash"}
    return True, "Account registered successfully!", profile

def authenticate_user(email, password):
    """
    Validates user credentials.
    Returns (success: bool, message: str, user_dict: dict or None)
    """
    _ensure_data_files()
    users = get_all_users()
    email_clean = email.strip().lower()

    if email_clean not in users:
        return False, "No account found with this email. Please register first.", None

    user_record = users[email_clean]
    expected_hash = _hash_password(password)

    if user_record.get("password_hash") != expected_hash:
        return False, "Incorrect password. Please try again.", None

    profile = {k: v for k, v in user_record.items() if k != "password_hash"}
    return True, f"Welcome back, {profile['name']}!", profile

def save_patient_screening(user_email, condition, stage, confidence, specialist, vitals_summary):
    """Saves a screening record linked to the patient's account."""
    _ensure_data_files()
    try:
        with open(SCREENINGS_FILE, "r", encoding="utf-8") as f:
            records = json.load(f)
    except Exception:
        records = []

    case_id = f"HLT-{1000 + len(records) + 1}"
    new_record = {
        "case_id": case_id,
        "user_email": user_email.strip().lower() if user_email else "guest",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "condition": condition,
        "stage": stage,
        "confidence": confidence,
        "specialist": specialist,
        "vitals_summary": vitals_summary
    }

    records.insert(0, new_record)
    with open(SCREENINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(records[:100], f, indent=4) # keep latest 100

    return case_id

def get_user_screenings(user_email=None):
    """Retrieves screening history for a specific patient or all records for doctors."""
    _ensure_data_files()
    try:
        with open(SCREENINGS_FILE, "r", encoding="utf-8") as f:
            records = json.load(f)
    except Exception:
        return []

    if user_email:
        clean = user_email.strip().lower()
        return [r for r in records if r.get("user_email") == clean]
    return records
