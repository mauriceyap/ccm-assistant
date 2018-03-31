import utils
import resources.bible as bible
import resources.passages as passages
import resources.sermons as sermons
from .intents_utils import ensure_date_and_service_slots_filled, \
    ensure_date_is_a_sunday, ensure_service_valid, ensure_date_is_not_in_the_future


def handle_welcome():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Christ Church Mayfair Assistant at your service. What " \
                    "would you like? "
    should_end_session = False
    reprompt_text = None
    return utils.build_response(
        session_attributes, utils.build_speechlet_response(
            card_title=card_title, card_content="Hello!", output=speech_output,
            reprompt_text=reprompt_text,
            should_end_session=should_end_session
        )
    )


def handle_session_end_request():
    card_title = "Goodbye"
    speech_output = "Thanks for using Christ Church Mayfair Assistant. "
    should_end_session = True
    return utils.build_response(
        {}, utils.build_speechlet_response(
            card_title=card_title, card_content=speech_output,
            output=speech_output, reprompt_text=None,
            should_end_session=should_end_session
        )
    )


def handle_get_sermon_passage(intent, session):
    session_attributes = {}

    maybe_response = ensure_date_and_service_slots_filled(intent)
    if maybe_response:
        return maybe_response

    date, maybe_response = ensure_date_is_a_sunday(intent, session_attributes)
    if maybe_response:
        return maybe_response

    service, maybe_response = ensure_service_valid(intent, session_attributes)
    if maybe_response:
        return maybe_response

    reading_data = passages.get_passage(date, service)
    if not reading_data:
        speech_output = "There isn't a Bible passage for that date "
        speechlet_response = utils.build_speechlet_response(
            output=speech_output, reprompt_text=None,
            should_end_session=False)
        return utils.build_response(session_attributes, speechlet_response)

    book = reading_data["book"]
    start_chapter = str(reading_data["start"]["chapter"])
    start_verse = str(reading_data["start"]["verse"])
    end_chapter = str(reading_data["end"]["chapter"])
    end_verse = str(reading_data["end"]["verse"])
    passage_text = bible.get_bible_text(book, start_chapter, start_verse,
                                        end_chapter, end_verse)

    get_read_passage_directives = [{"type": "Dialog.ElicitSlot",
                                    "slotToElicit": "ReadPassage"}]

    if "value" not in intent["slots"]["ReadPassage"]:
        should_end_session = False
        if 4 <= date.day <= 20 or 24 <= date.day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][date.day % 10 - 1]
        service_text = "AM" if service == "morning" else "PM"
        card_title = "{}{} {} {} - ".format(
            str(date.day),
            suffix,
            date.strftime("%B %Y"),
            service_text
        )
        card_title += "{} {}:{}-{}:{}".format(
            book,
            start_chapter,
            start_verse,
            end_chapter,
            end_verse
        )

        speech_output = "It's {} chapter {} ".format(book, start_chapter)
        if start_chapter == end_chapter:
            speech_output += "verses {} to {}. ".format(
                start_verse,
                end_verse
            )
        else:
            speech_output += "verse {} to chapter {} verse {}. ".format(
                start_verse,
                end_chapter,
                end_verse
            )
        speech_output += "I've sent this bible passage to your Alexa app. "
        speech_output += "Would you like me to read this out? "

        speechlet_response = utils.build_speechlet_response(
            card_title=card_title, card_content=passage_text,
            output=speech_output, reprompt_text=None,
            should_end_session=should_end_session,
            directives=get_read_passage_directives)

        return utils.build_response(session_attributes, speechlet_response)

    try:
        to_read_passage = intent["slots"]["ReadPassage"]["resolutions"][
                              "resolutionsPerAuthority"][0]["values"][0][
                              "value"]["id"] == "YES"
    except KeyError:
        speech_output = "Sorry, I didn't get that. Please could you repeat " \
                        "that? "
        speechlet_response = utils.build_speechlet_response(
            output=speech_output, reprompt_text=None,
            should_end_session=False,
            directives=get_read_passage_directives)
        return utils.build_response(session_attributes, speechlet_response)

    output = bible.remove_square_bracketed_verse_numbers(passage_text) \
        if to_read_passage else "Okay "

    speechlet_response = utils.build_speechlet_response(
        output=output, reprompt_text=None,
        should_end_session=True)

    return utils.build_response(session_attributes, speechlet_response)


def handle_get_next_event(intent, session):
    # TODO: implement this method
    session_attributes = {}
    reprompt_text = None
    speech_output = "You asked me for the next CCM event, but I can't do it " \
                    "because I've not been programmed to yet. Sorry! "
    should_end_session = True
    return utils.build_response(
        session_attributes, utils.build_speechlet_response(
            output=speech_output, reprompt_text=reprompt_text,
            should_end_session=should_end_session, card_content=None,
            card_title=None
        )
    )


def handle_play_sermon(intent, session):
    session_attributes = {}

    maybe_response = ensure_date_and_service_slots_filled(intent)
    if maybe_response:
        return maybe_response

    date, maybe_response = ensure_date_is_a_sunday(intent, session_attributes)
    if maybe_response:
        return maybe_response

    service, maybe_response = ensure_service_valid(intent, session_attributes)
    if maybe_response:
        return maybe_response

    maybe_response = ensure_date_is_not_in_the_future(intent,
                                                      session_attributes)
    if maybe_response:
        return maybe_response

    sermon = sermons.get_sermon(date, service)

    reprompt_text = None
    speech_output = "Here's the sermon, {}, by {} ".format(sermon["title"],
                                                           sermon["speaker"])
    should_end_session = True
    card_content = "{}\n{}\n{}".format(sermon["passage"], sermon["series_name"],
                                       sermon["speaker"])
    return utils.build_response(
        session_attributes, utils.build_audio_player_play_response(
            output_speech=speech_output, reprompt_text=reprompt_text,
            audio_stream_url=sermon["audio_url"],
            should_end_session=should_end_session,
            user_id=session["user"]["userId"], card_content=card_content,
            card_title=sermon["title"]
        )
    )
