import hashlib
import hmac
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is missing! Ensure it is set in the .env file.")

def generate_token(file_id):
    now = datetime.now()
    # Round the current time down to the nearest 5-minute interval
    minutes = (now.minute // 5) * 5
    rounded_time = now.replace(minute=minutes, second=0, microsecond=0)
    payload = f"{rounded_time}:{file_id}"
    token = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return token

def validate_token(token, file_id):
    valid_token = generate_token(file_id)
    return hmac.compare_digest(token, valid_token)
