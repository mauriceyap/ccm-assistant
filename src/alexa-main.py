"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import handlers.events as events

APPLICATION_ID = "amzn1.ask.skill.dd677950-cade-4805-b1f1-ce2e3a3569f0"


def lambda_handler(event, context):
    # Make sure only this Alexa skill can use this function
    if event['session']['application']['applicationId'] != APPLICATION_ID:
        raise ValueError("Invalid Application ID")

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
