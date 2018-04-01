import json
import config
import handlers.events as events


def lambda_handler(event, context):
    # Log input event to CloudWatch
    print("EVENT OBJECT:")
    print(json.dumps(event))

    # Make sure only this Alexa skill can use this function
    application_id = (
        event["session"]["application"]["applicationId"]
        if "session" in event.keys()
        else event["context"]["System"]["application"]["applicationId"]
    )
    if application_id != config.get("application_id"):
        raise ValueError("Invalid Application ID")

    if event["session"]["new"]:
        events.on_session_started({"requestId": event["request"]["requestId"]},
                                  event["session"])

    request_type = event["request"]["type"]

    if request_type == "LaunchRequest":
        return events.on_launch(event["request"], event["session"])
    elif request_type == "IntentRequest":
        return events.on_intent(event["request"], event["session"],
                                event["context"])
    elif request_type == "SessionEndedRequest":
        return events.on_session_ended(event["request"], event["session"])
