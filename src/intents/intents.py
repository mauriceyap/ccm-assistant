import utils.response_builder as response_builder


def handle_welcome():

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Christ Church Mayfair Assistant at your service."
    should_end_session = True
    reprompt_text = None
    return response_builder.build_response(
        session_attributes, response_builder.build_speechlet_response(
            card_title, speech_output, reprompt_text, should_end_session
        )
    )


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thanks for using the Christ Church Mayfair Assistant. "
    should_end_session = True
    return response_builder.build_response({}, response_builder.build_speechlet_response(
        title=card_title, output=speech_output, reprompt_text=None, should_end_session=should_end_session))


def create_favorite_color_attributes(favorite_color):
    # TODO: safely get rid of this method
    return {"favoriteColor": favorite_color}


def handle_get_sermon_passage(intent, session):
    # TODO: implement this method

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return response_builder.build_response(session_attributes, response_builder.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_get_next_event(intent, session):
    # TODO: implement this method

    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return response_builder.build_response(session_attributes, response_builder.build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
