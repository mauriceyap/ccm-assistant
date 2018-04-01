import re
import config


def convert_http_mp3_to_https_m3u(http_mp3_url):
    return config.get("http_mp3_to_https_m3u_api_url").format(
        http_mp3_url=http_mp3_url)


def build_speechlet_response(output, reprompt_text, should_end_session,
                             directives=None, card_title=None,
                             card_content=None):
    speechlet_response = {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }
    if directives:
        speechlet_response["directives"] = directives
    if card_title and card_content:
        card = {
            "type": "Simple",
            "title": card_title,
            "content": card_content
        }
        speechlet_response["card"] = card
    return speechlet_response


def build_audio_player_play_response(audio_stream_url, should_end_session,
                                     output_speech=None, reprompt_text=None,
                                     card_title=None, card_content=None,
                                     offset=0):
    audio_player_response = {
        "outputSpeech": {
            "type": "PlainText",
            "text": output_speech
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

    audio_stream_url = (
        audio_stream_url
        if re.match(r"https://.*", audio_stream_url)
        else convert_http_mp3_to_https_m3u(audio_stream_url))

    directives = [
        {
            "type": "AudioPlayer.Play",
            "playBehavior": "REPLACE_ALL",
            "audioItem": {
                "stream": {
                    "token": audio_stream_url,
                    "url": audio_stream_url,
                    "offsetInMilliseconds": offset
                }
            }
        }
    ]

    audio_player_response["directives"] = directives

    if card_title and card_content:
        card = {
            "type": "Simple",
            "title": card_title,
            "content": card_content
        }
        audio_player_response["card"] = card

    return audio_player_response


def build_audio_player_stop_response():
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": None
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": None
            }
        },
        "shouldEndSession": True,
        "directives": [
            {
                "type": "AudioPlayer.Stop"
            }
        ]
    }


def build_response(session_attributes, response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": response
    }
