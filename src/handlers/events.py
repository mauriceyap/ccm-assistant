import handlers.intents as intents


def on_session_started(session_started_request, session):
    """ Called when the session starts """
    pass


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to welcome intent handler
    return intents.get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent """
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to intent handlers
    if intent_name == "MyColorIsIntent":
        return intents.set_color_in_session(intent, session)
    elif intent_name == "WhatsMyColorIntent":
        return intents.get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return intents.get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return intents.handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    pass
