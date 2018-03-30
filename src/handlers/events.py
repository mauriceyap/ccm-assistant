import intents


def on_session_started(session_started_request, session):
    pass


def on_launch(launch_request, session):

    return intents.handle_welcome()


def on_intent(intent_request, session, context):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    # Dispatch to intent handlers
    if intent_name == "GetSermonPassage":
        return intents.handle_get_sermon_passage(intent, session)
    elif intent_name == "PlaySermon":
        return intents.handle_play_sermon(intent, session)
    elif intent_name == "GetNextEvent":
        return intents.handle_get_next_event(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return intents.handle_welcome()
    elif intent_name == "AMAZON.CancelIntent" \
            or intent_name == "AMAZON.StopIntent":
        return intents.handle_session_end_request()
    # Audio player intents
    elif intent_name in ["AMAZON.LoopOffIntent",
                         "AMAZON.LoopOnIntent",
                         "AMAZON.RepeatIntent",
                         "AMAZON.ShuffleOffIntent",
                         "AMAZON.ShuffleOnIntent",
                         "AMAZON.StartOverIntent",
                         "AMAZON.PreviousIntent",
                         "AMAZON.NextIntent"]:
        return intents.handle_irrelevant_audio_intent()
    elif intent_name == "AMAZON.PauseIntent":
        return intents.handle_pause(intent, session, context)
    elif intent_name == "AMAZON.ResumeIntent":
        return intents.handle_resume(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    pass
