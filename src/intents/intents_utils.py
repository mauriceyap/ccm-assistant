import utils
import speech

LARGE_NUMBER_DAYS = 3650


def ensure_date_and_service_slots_filled(intent):
    if ("value" not in intent["slots"]["Date"]) or ("value" not in intent["slots"]["Service"]):
        speechlet_response = {
            "shouldEndSession": False,
            "directives": [{"type": "Dialog.Delegate"}]
        }
        return utils.build_response(speechlet_response)

    return None


def ensure_date_is_a_sunday(intent, future_days_go_back_year_threshold=LARGE_NUMBER_DAYS):
    try:
        date = utils.sunday_from(intent["slots"]["Date"]["value"],
                                 future_days_go_back_year_threshold)
    except RuntimeError as e:
        speech_output = e.message
        get_date_directives = [{"type": "Dialog.ElicitSlot", "slotToElicit": "Date"}]
        speechlet_response = utils.build_speechlet_response(output=speech_output,
                                                            reprompt_text=None,
                                                            should_end_session=False,
                                                            directives=get_date_directives)
        return None, utils.build_response(speechlet_response)
    return date, None


def ensure_service_valid(intent):
    try:
        service = intent["slots"]["Service"]["resolutions"]["resolutionsPerAuthority"][0]["values"][
            0]["value"]["id"].lower()
    except KeyError:
        speech_output = speech.PLEASE_REPEAT_SERVICE
        speechlet_response = utils.build_speechlet_response(output=speech_output,
                                                            reprompt_text=None,
                                                            should_end_session=False,
                                                            directives=[{
                                                                "type": "Dialog.ElicitSlot",
                                                                "slotToElicit": "Service"}])
        return None, utils.build_response(speechlet_response)
    return service, None


def ensure_date_is_not_in_the_future(date):
    if not utils.is_not_in_future(date):
        speech_output = speech.SERVICE_IS_IN_THE_FUTURE
        speechlet_response = utils.build_speechlet_response(output=speech_output,
                                                            reprompt_text=None,
                                                            should_end_session=True)
        return utils.build_response(speechlet_response)
    return None
