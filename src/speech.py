from datetime import datetime


IRRELEVANT_AUDIO_INTENT = "I can't do that for a sermon. "
PLEASE_REPEAT_GENERAL = "Sorry, I didn't get that. Please could you repeat that? "
PLEASE_REPEAT_SERVICE = ("Sorry, I didn't get which service you wanted. "
                         "Please could you repeat that? ")
SERVICE_IS_IN_THE_FUTURE = "That service hasn't happened yet! "
DATE_IS_NOT_A_SUNDAY = "That day isn't a Sunday. What's the date of the service you're after? "

# Welcome
WELCOME = ("Welcome to Christ Church Mayfair Assistant! "
           "I can read you the Bible passage for a service or play you a past sermon. "
           "What would you like? ")

# End session
END_SESSION = "Thanks for using Christ Church Mayfair Assistant. See you later! "

# Get passage
NO_BIBLE_PASSAGE = "There isn't a Bible passage for that date "
BIBLE_PASSAGE_RESPONSE = ("It's {bible_passage}. I've sent this bible passage to your Alexa app. "
                          "Would you like me to read it out? ")
READ_RESPONSE = "{passage_text}"
DO_NOT_READ_RESPONSE = "Okay "

# Get next event


def time_to_speech(event_datetime):
    is_evening = event_datetime.hour >= 17
    return "{hour}:{minute}{option_in_evening}".format(
        hour=(event_datetime.hour % 12),
        minute=event_datetime.minute,
        option_in_evening=(" in the evening" if is_evening else ""))


def get_next_event(event_name, event_datetime):
    date_string = datetime.strftime(event_datetime, "%A %d %B")
    time_string = time_to_speech(event_datetime)
    return "The next event is {event_name} on {date_string} at {time_string}. ".format(
        event_name=event_name, date_string=date_string, time_string=time_string)


NO_EVENTS_FOUND = "There aren't any upcoming events. "

# Get sermon
SERMON_NOT_AVAILABLE = "I'm afraid that sermon isn't available. "
SERMON_PREAMBLE = "Here's the sermon, {sermon_title}, by {speaker} "
