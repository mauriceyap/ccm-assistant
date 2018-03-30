import utils
import resources.playback_db as playback_db


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
    playback_db.store_offset_for_user(user_id, offset)
    return utils.build_response({}, utils.build_audio_player_stop_response())


def handle_resume(intent, session):
    user_id = session["user"]["userId"]
    playback_data = playback_db.get_data_for_user(user_id)
    audio_url = playback_data['audio_url']
    offset = playback_data['offset']
    return utils.build_response({}, utils.build_audio_player_play_response(
        user_id=user_id, audio_stream_url=audio_url, should_end_session=True,
        offset=offset))


def handle_finished_playing(session):
    user_id = session["user"]["userId"]
    playback_db.reset_user(user_id)
