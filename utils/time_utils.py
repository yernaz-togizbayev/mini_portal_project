from datetime import datetime

def time_left(deadline):
    now = datetime.now()
    delta = deadline - now
    if delta.total_seconds() > 0:
        days, seconds = delta.days, delta.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{days}d {hours}h {minutes}m"
    return "Expired"

def get_status(deadline):
    now = datetime.now()
    delta = (deadline - now).days
    if delta > 7:
        return "green"
    elif 0 <= delta <= 7:
        return "yellow"
    elif delta < 0:
        return "red"
