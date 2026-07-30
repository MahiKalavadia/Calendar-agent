import json, os
from log_file.logs import logger

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
    except json.JSONDecodeError as e:
        logger.error(f"JSON Decode error while loading events: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Exception occurred while loading events: {str(e)}")
        return []