import json, os
from logger import logger

CALENDAR_DIR = "calendar"
if not os.path.exists(CALENDAR_DIR):
    os.makedirs(CALENDAR_DIR)

calender_filename = "calendar.json"

def load_events():
    """Load all the events for the specific date and time."""
    if not os.path.exists(os.path.join(CALENDAR_DIR, calender_filename)):
        logger.warning("Calendar file does not exist.")
        return []
    try:
        with open(os.path.join(CALENDAR_DIR, calender_filename), "r") as f:
            content = f.read().strip()
        if not content:
            logger.warning(f"No content found!")
            return []
        return json.loads(content)
    except json.JSONDecodeError:
        logger.error("JSON Decode error!")
        return "JSON Decode error occurred while loading events!"

def save_events(event:str) -> str:
    """Create a new event in calender for the event with its specific datetime and duration"""
    with open(os.path.join(CALENDAR_DIR, calender_filename), 'w') as f:
        json.dump(event, f, indent=4)