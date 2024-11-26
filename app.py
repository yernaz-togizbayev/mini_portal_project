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
DEADLINE = datetime(2024, 12, 10, 23, 59)

FILE_ID = os.getenv("FILE_ID")

if not FILE_ID:
    raise ValueError("FILE_ID is missing! Ensure it is set in the .env file.")

app = Flask(__name__)

@app.route("/")
def index():
    # client_ip = request.remote_addr
    # if not is_ip_allowed(client_ip):
    #     return "Access Denied", 403

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
    # client_ip = request.remote_addr
    # if not is_ip_allowed(client_ip):
    #     return "Access Denied", 403

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
    app.run(host="0.0.0.0", port=80, debug=False)
