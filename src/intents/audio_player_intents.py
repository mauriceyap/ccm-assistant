import utils
import speech


def handle_irrelevant_audio_intent():
    speech_output = speech.IRRELEVANT_AUDIO_INTENT
    return utils.build_response(utils.build_speechlet_response(output=speech_output,
                                                               reprompt_text=None,
                                                               should_end_session=True))


def handle_pause():
    return utils.build_response(utils.build_audio_player_stop_response())


def handle_resume(context):
    audio_url = context["AudioPlayer"]["token"]
    offset = context["AudioPlayer"]["offsetInMilliseconds"]
    return utils.build_response(utils.build_audio_player_play_response(audio_stream_url=audio_url,
                                                                       should_end_session=True,
                                                                       offset=offset))
