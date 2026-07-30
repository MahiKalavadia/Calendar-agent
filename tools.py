from langchain_core.tools import tool
from dotenv import load_dotenv
from services import load_events, save_events
from logger import logger
from datetime import datetime, timedelta
import json
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# llm = ChatGroq(model="llama-3.3-70b-versatile")
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash")
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