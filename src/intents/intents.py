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
    card_title = "Get Sermon Bible Passage"
    session_attributes = {}
    should_end_session = True

    book = 'Matthew'
    chapter = '17'
    start_verse = '1'
    end_verse = '10'  # TODO: change all this using fetched data

    speech_output = book + ' chapter ' + chapter + ' verses ' + start_verse + ' to ' + end_verse

    return response_builder.build_response(session_attributes, response_builder.build_speechlet_response(
        title=card_title, output=speech_output, reprompt_text=None , should_end_session=should_end_session))


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
