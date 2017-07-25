def build_speechlet_response(card_title, card_content, output, reprompt_text,
                             should_end_session, directives=None):
    speechlet_response = {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': card_title,
            'content': card_content
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
    if directives: speechlet_response['directives'] = directives
    return speechlet_response

# TODO remove this function by combining it with the one above
def build_speechlet_response_no_card(output, reprompt_text,
                                     should_end_session, directives=None):
    speechlet_response = {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
    if directives: speechlet_response['directives'] = directives
    return speechlet_response


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response

    }
