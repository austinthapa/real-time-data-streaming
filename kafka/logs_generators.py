import logging
import random

from datetime import datetime, timedelta
from faker import Faker

# Logging set up
logging.basicConfig(level=logging.INFO)

# Glovbal variables
faker = Faker()
producer = None

# Configuration Files
DEVICES = ["mobile", "desktop", "laptop", "tablet"]
OS = ["iOS", "Android", "Windows", "macOS"]
BROWSERS = ["Chrome", "Safari", "Firefox", "Opera"]
AUTH_EVENTS = ["login_success", "login_failure", "logout", "password_reset", "mfa_success", "account_locked", "device_registered"]
SUCCESS_EVENTS = ["login_success", "password_reset", "mfa_success", "device_registered"]
AUTH_WEIGHTS = [0.5, 0.2, 0.1, 0.1, 0.05, 0.03, 0.02]
EVENT_TYPES = ['login', 'click', 'scroll', 'search', 'logout']

def generate_session_data():
    """
    Generate consistent session data to be used across the logs types
    
    Returns:
        dict: session logs dictionary
    """
    user_id = faker.uuid4()
    session_id = faker.uuid4()
    device = random.choice(DEVICES)
    location = faker.city()
    ip_address = random.choice([faker.ipv4(), faker.ipv6()])
    login_time = datetime.now() - timedelta(minutes=random.randint(2, 181))
    logout_time = datetime.now()
    session_duration = logout_time - login_time
    
    return {
        "user_id": user_id,
        "session_id": session_id,
        "device": device,
        "location": location,
        "ip_address": ip_address,
        "login_time": login_time,
        "logout_time": logout_time,
        "session_duration": session_duration
    }
    
def generate_user_session_log(session):
    """
    Creates a user session log from the session data
    
    Returns:
        dict: user_session_logs dictionary
    """
    return {
        "user_id": session["user_id"],
        "session_id": session["session_id"],
        "login_time": session["login_time"].isoformat(),
        "logout_time": session["logout_time"].isoformat(),
        "duration": session["session_duration"].total_seconds(),
        "device": session["device"],
        "os": random.choice(OS),
        "browser": random.choice(BROWSERS),
        "location": session["location"],
        "ip_address": session["ip_address"]
    }
    
def generate_user_auth_log(session):
    """
    Creates a user authentication logs from the session data
    
    Returns:
        dict: user_auth_logs dictionary
    """
    auth_type = random.choices(AUTH_EVENTS, weights=AUTH_WEIGHTS, k = 1)[0]
    return {
        "user_id": session["user_id"],
        "session_id": session["session_id"] if auth_type in SUCCESS_EVENTS else None,
        "timestamp": datetime.now().isoformat(),
        "ip_address": session["ip_address"],
        "device": session["device"],
        "success": auth_type if auth_type in SUCCESS_EVENTS else None,
        "failure_reason":random.choice(["wrong_password", "mfa_failed", "account_locked", "suspicious_location"]) 
        if auth_type not in SUCCESS_EVENTS else None
    }
    
def generate_user_activity_log(session):
    """
    Creates a list of user activity logs from the session data
    
    Returns:
        dict: user_activity_logs dictionary
    """
    count = None
    if count is None:
        count = random.randint(1, 30)
    
    activity_logs = []
    login_time = session["login_time"]
    session_duration_seconds = session["session_duration"].total_seconds()
    
    for _ in range(count):
        seconds_after_login = random.randint(0, int(session_duration_seconds))
        activity_timestamp = login_time + timedelta(seconds=seconds_after_login)
        
        activity_logs.append({
            "user_id": session["user_id"],
            "session_id": session["session_id"],
            "event_type": random.choice(EVENT_TYPES),
            "timestamp": activity_timestamp.isoformat(),
            "url": faker.uri_path(),
            "device": session["device"],
            "location": session["location"],
            "event_category": random.choice(["navigation", "content", "transaction"]),
            "event_details": {
                "page_id": faker.uuid4(),
                "content_id": faker.uuid4() if random.random() > 0.5 else None,
                "action_taken": random.choice(["view", "click", "scroll", "purchase"])
            }
        })
    return sorted(activity_logs, key=lambda x:x["timestamp"])