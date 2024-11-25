from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

ALLOWED_IPS = set(os.getenv("ALLOWED_IPS", "").split(","))

if not ALLOWED_IPS:
    raise ValueError("ALLOWED_IPS is missing! Ensure it is set in the .env file.")

def is_ip_allowed(client_ip, allowed_ips=ALLOWED_IPS):
    return client_ip in allowed_ips
