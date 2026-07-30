from langchain_core.tools import tool
from dotenv import load_dotenv
from services.load_event import load_events
from services.save_event import save_events
from log_file.logs import logger
from datetime import datetime

load_dotenv()

today = datetime.now()


@tool
def cancel_event(date: str| None, time: str | None) -> str:
    """
    Cancel an existing calendar event specified by user.

    Args:
    - date: The date of the event in format YYYY-MM-DD
    - time: The time in 24-hour HH:MM format.

    Returns:
    - returns a message indicating event is cancelled or a message indicating that no matching event found!.

    """
    try:
        logger.info(f"Cancel event tool called!")
        events = load_events()
        logger.info(f"Events: {events}")
        for event in events:
            if event["date"] == date and event["start_time"] == time:
                logger.info(f"Removing event.. {event}")
                events.remove(event)
                logger.info(f"Saving...")
                save_events(events)
                return "Event cancelled successfully."
        return "No event found for the given date and time."
    except Exception as e:
        logger.error(f"Exception occurred while cancelling event {str(e)}")
        return "Error while cancelling event!!"