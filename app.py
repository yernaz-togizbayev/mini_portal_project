# from flask import Flask, render_template, redirect, request
# from datetime import datetime, timedelta
# import hashlib
# import hmac

# app = Flask(__name__)

# # Configuration
# DEADLINE = datetime(2024, 12, 31, 23, 59)  # Expiration date and time
# ALLOWED_IPS = {"127.0.0.1", "192.168.0.1"}  # Allowed IPs
# FILE_ID = "1mbeqwieCrXfQtGbJJpjjk_tYSX4SR42g"  # Google Drive file ID
# SECRET_KEY = "fa70854ac585838966cf4253c281d505"  # Secret key for token generation

# # Generate a temporary token
# def generate_token():
    # now = datetime.now()
    # # Round the current time down to the nearest 5-minute interval
    # minutes = (now.minute // 5) * 5
    # rounded_time = now.replace(minute=minutes, second=0, microsecond=0)
    # payload = f"{rounded_time}:{FILE_ID}"
    # token = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    # return token

# # Calculate remaining time
# def time_left(deadline):
    # now = datetime.now()
    # delta = deadline - now
    # if delta.total_seconds() > 0:
        # days, seconds = delta.days, delta.seconds
        # hours = seconds // 3600
        # minutes = (seconds % 3600) // 60
        # return f"{days}d {hours}h {minutes}m"
    # return "Expired"

# # Check status based on remaining time
# def get_status(deadline):
    # now = datetime.now()
    # delta = (deadline - now).days
    # if delta > 7:
        # return "green"
    # elif 0 <= delta <= 7:
        # return "yellow"
    # elif delta < 0:
        # return "red"

# @app.route("/")
# def index():
    # client_ip = request.remote_addr
    # if client_ip not in ALLOWED_IPS:
        # return "Access Denied", 403

    # status = get_status(DEADLINE)
    # remaining_time = time_left(DEADLINE)
    # if status == "red":
        # return render_template("index.html", status=status, remaining_time="Expired", link=None)

    # token = generate_token()
    # return render_template(
        # "index.html",
        # status=status,
        # deadline=int(DEADLINE.timestamp() * 1000),  # Convert to milliseconds for JavaScript
        # link=f"/download?token={token}"
    # )

# @app.route("/download")
# def download():
    # client_ip = request.remote_addr
    # if client_ip not in ALLOWED_IPS:
        # return "Access Denied", 403

    # if get_status(DEADLINE) == "red":
        # return "Access expired", 403

    # # Validate token
    # token = request.args.get("token")
    # valid_token = generate_token()
    # if token != valid_token:
        # return "Invalid or expired token", 403

    # # Redirect to Google Drive
    # drive_url = f"https://drive.usercontent.google.com/download?id=1mbeqwieCrXfQtGbJJpjjk_tYSX4SR42g&export=download&authuser=0&confirm=t&uuid=22d8810c-0d56-408f-91f9-0307916e7df7&at=AENtkXadFPYt3LSLaXpyc6_XmqV2%3A1732400226178"
    # return redirect(drive_url)

# if __name__ == "__main__":
    # app.run(debug=True)

from flask import Flask, render_template, redirect, request
from datetime import datetime
from utils.token_utils import generate_token, validate_token
from utils.time_utils import time_left, get_status
from utils.ip_utils import is_ip_allowed
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuration
DEADLINE = datetime(2024, 12, 31, 23, 59)

FILE_ID = os.getenv("FILE_ID")

if not FILE_ID:
    raise ValueError("FILE_ID is missing! Ensure it is set in the .env file.")

app = Flask(__name__)

@app.route("/")
def index():
    client_ip = request.remote_addr
    if not is_ip_allowed(client_ip):
        return "Access Denied", 403

    status = get_status(DEADLINE)
    remaining_time = time_left(DEADLINE)
    if status == "red":
        return render_template("index.html", status=status, remaining_time="Expired", link=None)

    token = generate_token(FILE_ID)
    return render_template(
        "index.html",
        status=status,
        deadline=int(DEADLINE.timestamp() * 1000),
        link=f"/download?token={token}"
    )

@app.route("/download")
def download():
    client_ip = request.remote_addr
    if not is_ip_allowed(client_ip):
        return "Access Denied", 403

    if get_status(DEADLINE) == "red":
        return "Access expired", 403

    # Validate token
    token = request.args.get("token")
    if not validate_token(token, FILE_ID):
        return "Invalid or expired token", 403

    # Redirect to Google Drive
    drive_url = f"https://drive.google.com/uc?export=download&id={FILE_ID}"
    return redirect(drive_url)

if __name__ == "__main__":
    app.run(debug=True)

