from langchain_core.tools import tool
from dotenv import load_dotenv
from services.load_event import load_events
from log_file.logs import logger
from datetime import datetime

load_dotenv()

today = datetime.now()

@tool
def get_events(date: str | None = today):
    """
    Retrieve all the existing events for the specified date.

    Args:
    - date: The date should be in format YYYY-MM-DD. If date not provided default date is today's date.

    Returns:
    - Returns a formatted list of scheduled events or message indicating no events available.
    """
    try:
        logger.info("Get Events tool called!")
        events = load_events()
        logger.info(f"Events: {events}")
        filtered_events = [
            event for event in events
            if event["date"] == date
        ]
        logger.info("Filtered events..")
        if not filtered_events:
            logger.warning(f"No filtered events..")
            return f"No events found for {date}."
        response = []
        for event in filtered_events:
            response.append(
                f"{event['title']} at {event['start_time']}"
            )
        logger.info(f"Events available: {response}")
        return "\n".join(response)
    except Exception as e:
        logger.error(f"Exception occurred while loading events {str(e)}")
        return "Error while loading events!!"