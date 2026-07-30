from langchain_core.tools import tool
from dotenv import load_dotenv
from services.load_event import load_events
from services.save_event import save_events
from log_file.logs import logger
from datetime import datetime, timedelta

load_dotenv()

today = datetime.now()

@tool
def create_event(title: str | None, date: str, start_time: str, duration:str = "1 hour") -> str:
    """
    Scheduling a new calender event for the given date and start time.
    
    Args:
    - title: The title of the event inside user's query.
    - date: The date provided by user in format YYYY-MM-DD and if not provided defaults to today.
    - start_time: The start_time of the event in 24-hour HH:MM format.
    - duration: The duration for which the event will occur. Defaults to 1 followed by unit hour.

    Returns:
    - Message indicating that an event has been created successfully or the message indicating that there is already an existing event occurring at that time.
    """
    try:
        logger.info("Create event tool called!")
        events = load_events()
        logger.info(f"Events loaded {events}")

        try:
            new_start = datetime.strptime(start_time, "%H:%M")
            clean_duration = int(duration.split()[0])
            print(clean_duration)
            new_end = new_start + timedelta(hours=clean_duration)
        except ValueError:
            new_start = new_end = None

        for event in events:
            if event["date"] == date:
                if new_start:
                    try:
                        clean_duration = int(event["duration"].split()[0])
                        ev_start = datetime.strptime(event["start_time"], "%H:%M")
                        ev_end = ev_start + timedelta(hours=clean_duration)
                        if max(new_start, ev_start) < min(new_end, ev_end):
                            return f"You already have an event '{event['title']}' from {event['start_time']} to {ev_end.strftime('%H:%M')} on {date}."
                    except ValueError:
                        pass
                if event["start_time"] == start_time:
                    return f"You already have an event at {start_time} on {date}."

        event = {
            "title": title,
            "date": date,
            "start_time": start_time,
            "duration": duration
        }
        logger.info("Events appending....")
        events.append(event)
        logger.info("Events appended....")
        save_events(events)
        logger.info("Saving events!")
        return f"Event '{title}' has been created on {date} at {start_time} for {duration}."
    except Exception as e:
        logger.error(f"Exception occurred while creating event {str(e)}")
        return "Error while creating event!!"
