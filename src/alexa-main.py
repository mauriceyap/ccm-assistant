import handlers.events as events

APPLICATION_ID = "amzn1.ask.skill.dd677950-cade-4805-b1f1-ce2e3a3569f0"


def lambda_handler(event, context):
    if event['session']['new']:
        events.on_session_started({'requestId': event['request']['requestId']},
                                  event['session'])

    request_type = event['request']['type']

    if request_type == "LaunchRequest":
        return events.on_launch(event['request'], event['session'])
    elif request_type == "IntentRequest":
        return events.on_intent(event['request'], event['session'])
    elif request_type == "SessionEndedRequest":
        return events.on_session_ended(event['request'], event['session'])
