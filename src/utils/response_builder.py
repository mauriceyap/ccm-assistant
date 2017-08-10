def build_speechlet_response(output, reprompt_text, should_end_session,
                             directives=None, card_title=None,
                             card_content=None):
    speechlet_response = {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }
    if directives:
        speechlet_response["directives"] = directives
    if card_title and card_content:
        card = {
            "type": "Simple",
            "title": card_title,
            "content": card_content
        }
        speechlet_response["card"] = card
    return speechlet_response


def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response

    }
