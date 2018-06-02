import config
import requests
from datetime import datetime


EVENT_NAMES_TO_IGNORE = ["10.15 Service", "6pm Service"]


def get_next_event():
    events = requests.get(config.EVENTS_JSON_URL).json()  # TODO: handle connection failures
    events = [e for e in events if e["name"] not in EVENT_NAMES_TO_IGNORE]

    if not events:
        return None

    # Next event, assuming events only includes future events
    events.sort(key=(lambda e: e['datetime_start']))
    event = events[0]

    event_name = event["name"] if event["name"] else ""
    event_description = event["description"] if event["description"] else ""
    event_datetime = (
        datetime.strptime(event["datetime_start"], "%Y-%m-%d %H:%M:%S")
        if event["datetime_start"]
        else None)
    event_location_name = event["location"]["name"] if event["location"]["name"] else ""
    event_location_address = event["location"]["address"] if event["location"]["address"] else ""
    event_small_image_url = (
        event["images"]["original_500"]
        if (event["images"] and event["images"]["original_500"])
        else None)
    event_large_image_url = (
        event["images"]["original_1000"]
        if (event["images"] and event["images"]["original_1000"])
        else None)

    return {
        "name": event_name,
        "datetime": event_datetime,
        "description": event_description,
        "location_name": event_location_name,
        "location_address": event_location_address,
        "small_image_url": event_small_image_url,
        "large_image_url": event_large_image_url
    }
