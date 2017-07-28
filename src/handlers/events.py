import intents.intents as intents


def on_session_started(session_started_request, session):
    """ Called when the session starts """
    pass


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to welcome intent handler
    return intents.handle_welcome()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent """
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to intent handlers
    if intent_name == "GetSermonPassage":
        return intents.handle_get_sermon_passage(intent, session)
    elif intent_name == "PlaySermon":
        return intents.handle_play_sermon(intent, session)
    elif intent_name == "GetNextEvent":
        return intents.handle_get_next_event(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return intents.handle_welcome()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return intents.handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    pass
