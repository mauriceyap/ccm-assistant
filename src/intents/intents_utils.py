import utils


def ensure_date_and_service_slots_filled(intent):
    if ("value" not in intent["slots"]["Date"]) \
            or ("value" not in intent["slots"]["Service"]):
        speechlet_response = {
            "shouldEndSession": False,
            "directives": [{"type": "Dialog.Delegate"}]
        }
        return utils.build_response({}, speechlet_response)

    return None


def ensure_date_is_a_sunday(intent, session_attributes):
    try:
        date = utils.sunday_from(intent["slots"]["Date"]["value"])
    except RuntimeError as e:
        speech_output = e.message
        get_date_directives = [{"type": "Dialog.ElicitSlot",
                                "slotToElicit": "ReadPassage"}]
        speechlet_response = utils.build_speechlet_response(
            output=speech_output, reprompt_text=None,
            should_end_session=False,
            directives=get_date_directives)
        return None, utils.build_response(session_attributes,
                                          speechlet_response)
    return date, None


def ensure_service_valid(intent, session_attributes):
    try:
        service = intent["slots"]["Service"]["resolutions"][
            "resolutionsPerAuthority"][0]["values"][0]["value"]["id"].lower()
    except KeyError:
        speech_output = "Sorry, I didn't get which sevice you wanted. " \
                        "Please could you repeat that? "
        speechlet_response = utils.build_speechlet_response(
            output=speech_output, reprompt_text=None,
            should_end_session=False,
            directives=[{"type": "Dialog.ElicitSlot",
                         "slotToElicit": "ReadPassage"}])
        return None, utils.build_response(session_attributes,
                                          speechlet_response)
    return service, None