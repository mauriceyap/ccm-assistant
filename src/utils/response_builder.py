import re


def convert_http_mp3_to_https_m3u(http_mp3_url):
    return ("https://0elu033c2a.execute-api.eu-west-1.amazonaws.com/"
            "prod/m3uGenerator?url={}").format(http_mp3_url)


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


def build_audio_player_response(output_speech, reprompt_text, audio_stream_url,
                                should_end_session, card_title=None,
                                card_content=None):
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
                    "token": "MAGIC_STRING_TOKEN",
                    # playBehaviour ENQUEUE is never used so token is arbitrary
                    "url": audio_stream_url,
                    "offsetInMilliseconds": 0
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


def build_response(session_attributes, response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": response

    }
