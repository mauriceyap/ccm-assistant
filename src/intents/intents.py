import utils.response_builder as response_builder
import resources.bible as bible
import yaml
import utils.date_utils as date_utils
import os


def handle_welcome():

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Christ Church Mayfair Assistant at your service. What " \
                    "would you like? "
    should_end_session = False
    reprompt_text = None
    return response_builder.build_response(
        session_attributes, response_builder.build_speechlet_response(
            card_title, 'Hello!', speech_output, reprompt_text,
            should_end_session
        )
    )


def handle_session_end_request():
    card_title = 'Goodbye'
    speech_output = 'Thanks for using Christ Church Mayfair Assistant. '
    should_end_session = True
    return response_builder.build_response(
        {}, response_builder.build_speechlet_response(
        card_title=card_title, card_content=speech_output,
        output=speech_output, reprompt_text=None,
        should_end_session=should_end_session
        )
    )


def handle_get_sermon_passage(intent, session):
    if ('value' not in intent['slots']['Date']) \
            or ('value' not in intent['slots']['Service']):
        speechlet_response = {
            'shouldEndSession': False,
            'directives': [{'type': 'Dialog.Delegate'}]
        }
        return response_builder.build_response({}, speechlet_response)

    session_attributes = {}

    try:
        date = date_utils.sunday_from(intent['slots']['Date']['value'])
    except RuntimeError as e:
        speech_output = e.value()
        get_date_directives = [{'type': 'Dialog.ElicitSlot',
                                'slotToElicit': 'ReadPassage'}]
        speechlet_response = response_builder.build_speechlet_response_no_card(
            output=speech_output, reprompt_text=None,
            should_end_session=False,
            directives=get_date_directives)
        return response_builder.build_response(session_attributes,
                                               speechlet_response)

    service = intent['slots']['Service']['resolutions'][
        'resolutionsPerAuthority'][0]['values'][0]['value']['id'].lower()
    data_path = os.environ['LAMBDA_TASK_ROOT'] + '/resources/data/passages.yaml'
    data = open(data_path).read()
    reading_data = yaml.load(data)[date][service]
    book = reading_data['book']
    start_chapter = str(reading_data['start']['chapter'])
    start_verse = str(reading_data['start']['verse'])
    end_chapter = str(reading_data['end']['chapter'])
    end_verse = str(reading_data['end']['verse'])
    passage_text = bible.get_bible_text(book, start_chapter, start_verse,
                                        end_chapter, end_verse)

    get_read_passage_directives = [{'type': 'Dialog.ElicitSlot',
                                    'slotToElicit': 'ReadPassage'}]

    if 'value' not in intent['slots']['ReadPassage']:
        should_end_session = False

        # TODO: Add another case for same chapter
        card_title = book + ' ' + start_chapter + ':' + start_verse + '-' + \
            end_chapter + ':' + end_verse

        speech_output = book + ' chapter ' + start_chapter + ' verse ' + \
            start_verse + ' to  chapter ' + end_chapter + \
            ' verse ' + end_verse + '. '
        speech_output += 'I\'ve sent this bible passage to your Alexa app. '
        speech_output += 'Would you like me to read this out?'

        speechlet_response = response_builder.build_speechlet_response(
            card_title=card_title, card_content=passage_text,
            output=speech_output, reprompt_text=None,
            should_end_session=should_end_session,
            directives=get_read_passage_directives)

        return response_builder.build_response(session_attributes,
                                               speechlet_response)

    try:
        to_read_passage = intent['slots']['ReadPassage']['resolutions'][
            'resolutionsPerAuthority'][0]['values'][0]['value']['id'] == 'YES'
    except KeyError:
        speech_output = 'Sorry, I didn\'t get that. Please could you repeat ' \
                      'that? '
        speechlet_response = response_builder.build_speechlet_response_no_card(
            output=speech_output, reprompt_text=None,
            should_end_session=False,
            directives=get_read_passage_directives)
        return response_builder.build_response(session_attributes,
                                               speechlet_response)


    if to_read_passage:
        output = bible.remove_square_bracketed_verse_numbers(passage_text)

    else:
        output = 'Okay '

    speechlet_response = response_builder.build_speechlet_response_no_card(
        output=output, reprompt_text=None,
        should_end_session=True)

    return response_builder.build_response(session_attributes,
                                           speechlet_response)


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
        intent['name'], None, speech_output, reprompt_text, should_end_session))
