from langchain_core.tools import tool
from dotenv import load_dotenv
from services.load_event import load_events
from log_file.logs import logger
from datetime import datetime, timedelta

load_dotenv()

today = datetime.now()

@tool
def check_availability(time: str = "", date: str | None =  today) -> str:
    """
    Checks the availability for the available time slots for the specified date. If date not provided set today's date as default.

    Args:
    - date: The date should be in format YYYY-MM-DD.
    - time: The time in 24-hour HH:MM format. If time not provided check every time for today.

    Returns:
    - Returns all the available slots for the specified date and time and if not available return you are occupied. 
    """
    try:
        logger.info(f"Check availability tool called!")
        events = load_events()
        logger.info(f"Events: {events}")

        try:
            req_time = datetime.strptime(time, "%H:%M")
        except ValueError:
            req_time = None

        for event in events:
            if event["date"] == date:
                if req_time:
                    try:
                        clean_duration = int(event["duration"].split()[0])
                        ev_start = datetime.strptime(event["start_time"], "%H:%M")
                        ev_end = ev_start + timedelta(hours=clean_duration)
                        if ev_start <= req_time < ev_end:
                            logger.info(f"You are busy with another event {event['title']}")
                            return f"You are busy with '{event['title']}' from {event['start_time']} to {ev_end.strftime('%H:%M')}."
                    except ValueError:
                        pass
                if event["start_time"] == time:
                    logger.info(f"You are busy with another event {event['title']}")
                    return f"You are busy with '{event['title']}' from {time}."

        return f"You are available on {date} at {time}."
    except Exception as e:
        logger.error(f"Exception occurred while checking availability {str(e)}")
        return "Error while checking availability!!"