import logging


def is_valid_response(response):
    if 'version' not in response:
        logging.error('version not in response object')
        return False
    if 'response' not in response:
        return False

    response_obj = response['response']

    if 'outputSpeech' in response_obj:
        output_speech_obj = response_obj['outputSpeech']
        if 'type' not in output_speech_obj:
            return False
        if output_speech_obj['type'] == 'PlainText':
            if 'text' not in output_speech_obj:
                return False
        elif output_speech_obj['type'] == 'SSML':
            if 'ssml' not in output_speech_obj:
                return False
        else:
            return False

    if 'card' in response_obj:
        card_obj = response_obj['card']
        if 'title' not in card_obj:
            return False
        if 'type' not in card_obj:
            return False
        if card_obj['type'] == 'Simple':
            if 'content' not in card_obj:
                return False
        elif card_obj['type'] == 'Standard':
            if 'text' not in card_obj:
                return False
            if 'image' not in card_obj:
                return False
            if 'smallImageUrl' not in card_obj['image']:
                return False
            if 'largeImageUrl' not in card_obj['image']:
                return False
        else:
            return False

    return True


class ValidResponseObjectTester:
    def __init__(self, response):
        self.response = response
        self.response_obj = response['response']

    def get_speech_plain(self):
        if self.response_obj['outputSpeech']['type'] == 'PlainText':
            return self.response_obj['outputSpeech']['text']

    def get_speech_ssml(self):
        if self.response_obj['outputSpeech']['type'] == 'SSML':
            return self.response_obj['outputSpeech']['ssml']

    def get_card_title(self):
        return self.response_obj['card']['title']

    def get_card_text(self):
        return (self.response_obj['card']['content']
                if self.response_obj['card']['type'] == 'Simple'
                else self.response_obj['card']['text'])

    def get_card_small_image_url(self):
        if 'card' in self.response_obj and self.response_obj['card'] == 'Standard':
            return self.response_obj['card']['smallImageUrl']

    def get_card_large_image_url(self):
        if 'card' in self.response_obj and self.response_obj['card'] == 'Standard':
            return self.response_obj['card']['largeImageUrl']

    def get_reprompt_text(self):
        if 'reprompt' in self.response_obj:
            return (self.response_obj['reprompt']['text']
                    if self.response_obj['reprompt']['type'] == 'PlainText'
                    else self.response_obj['reprompt']['ssml'])

    def is_session_ending(self):
        return self.response_obj['shouldEndSession']
