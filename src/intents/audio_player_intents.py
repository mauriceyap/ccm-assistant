import utils


def handle_irrelevant_audio_intent():
    speech_output = "I can't do that for a sermon. "
    return utils.build_response({}, utils.build_speechlet_response(
        output=speech_output,
        reprompt_text=None,
        should_end_session=True
        )
    )


def handle_pause(intent, session, context):
    user_id = session["user"]["userId"]
    offset = context["AudioPlayer"]["offsetInMilliseconds"]
    # TODO: store in db

    return utils.build_response({}, utils.build_audio_player_stop_response())


def handle_resume(intent, session):
    user_id = session["user"]["userId"]
    audio_url = ''
    offset = ''
    # TODO: fetch above from database
    # TODO: implement this handler
    return utils.build_response({}, utils.build_audio_player_play_response(
        user_id=user_id, audio_stream_url=audio_url, should_end_session=True,
        offset=offset))
