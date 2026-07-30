import json, os
from log_file.logs import logger

CALENDAR_DIR = "calendar"
if not os.path.exists(CALENDAR_DIR):
    os.makedirs(CALENDAR_DIR)

calender_filename = "calendar.json"

def save_events(event):
    """Create a new event in calender for the event with its specific datetime and duration"""
    try:
        os.makedirs(CALENDAR_DIR, exist_ok=True)
        with open(os.path.join(CALENDAR_DIR, calender_filename), 'w') as f:
            json.dump(event, f, indent=4)
    except Exception as e:
        logger.error(f"Exception occurred while saving events: {str(e)}")