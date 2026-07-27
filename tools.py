from langchain_core.tools import tool
from dotenv import load_dotenv
import logging
from services import load_events, save_events
from logger import logger
from datetime import timedelta

load_dotenv()

@tool
def create_event(title: str, date: str, start_time: str, duration:str = "1 hour") -> str:
    """
    Create a new calendar event.
    """
    try:
        logger.info("Create event tool called!")
        events = load_events()
        logger.info(f"Events loaded {events}")
        for event in events:
            if event["date"] == date and event["start_time"] == start_time:
                return f"You already have an event at {start_time} on {date}."
        event = {
            "title": title,
            "date": date,
            "start_time": start_time,
            "duration":duration
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
def get_events(date: str) -> str:
    """
    Get all events for a particular date.
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
def check_availability(date: str, time: str) -> str:
    """
    Check whether a time slot is available.
    """
    try:
        logger.info(f"Check availability tool called!")
        events = load_events()
        logger.info(f"Events: {events}")
        for event in events:
            if event["date"] == date and event["start_time"] == time:
                logger.info(f"You are busy with another event {event["title"]}")
                return f"You are busy with '{event['title']}' from {time}."
        return f"You are available on {date} at {time}."
    except Exception as e:
            logger.error(f"Exception occurred while checking availability {str(e)}")
            return "Error while checking availability!!"
 
 
@tool
def cancel_event(date: str, time: str) -> str:
    """
    Cancel an event using date and time.
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
 
 