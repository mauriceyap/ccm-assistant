config = {
    "bible_api_url": ("https://bibles.org/v2/eng-{translation}/passages.js?"
                      "q[]={book}+{start_chapter}:{start_verse}-"
                      "{end_chapter}:{end_verse}"),
    "bible_api_key": "xfrxzZpI8YdyOvTFP2RJkhn0FYQRNnfq3xZgOtrc",
    "bible_translation": "GNBDC",  # Can't use NIV - it's still in copyright
    "http_mp3_to_https_m3u_api_url": ("https://0elu033c2a."
                                      "execute-api.eu-west-1.amazonaws.com/"
                                      "prod/m3uGenerator?url={http_mp3_url}"),
    "application_id": "amzn1.ask.skill.dd677950-cade-4805-b1f1-ce2e3a3569f0"
}


def get(key):
    return config[key]
