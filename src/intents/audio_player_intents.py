import utils


def handle_irrelevant_audio_intent():
    speech_output = "I can't do that for a sermon. "
    return utils.build_response({}, utils.build_speechlet_response(
        output=speech_output,
        reprompt_text=None,
        should_end_session=True
        )
    )


def handle_pause(intent, session):
    return utils.build_response({}, utils.build_audio_player_stop_response())


def handle_resume(intent, session, context):
    audio_url = context["AudioPlayer"]['token']
    offset = context["AudioPlayer"]['offsetInMilliseconds']
    return utils.build_response({}, utils.build_audio_player_play_response(
        audio_stream_url=audio_url, should_end_session=True, offset=offset))
