import unittest
from mock import patch

import alexa_main


TEST_APPLICATION_ID = "aPpLiCaTiOnId12345"
TEST_REQUEST_ID = "rEqUeStId123"


class TestAlexaMain(unittest.TestCase):
    def setUp(self):
        alexa_main.config.APPLICATION_ID = TEST_APPLICATION_ID

    @patch("alexa_main.events.on_session_started")
    @patch("alexa_main.events.on_launch")
    def test_lambda_handler_throws_error_with_invalid_session_id(self, on_launch,
                                                                 on_session_started):
        test_invalid_application_id = "iAmAnInvalidId00000"
        test_session_event_with_invalid_id = {
            'session': {
                'application': {
                    'applicationId': test_invalid_application_id
                },
                'new': False
            },
            'request': {
                'requestId': TEST_REQUEST_ID,
                'type': 'LaunchRequest'
            },
            'context': {}
        }
        test_context_only_event_with_invalid_id = {
            'request': {},
            'context': {
                'System': {
                    'application': {
                        'applicationId': test_invalid_application_id
                    }
                }
            }
        }

        with self.assertRaises(ValueError) as cm_session_event:
            alexa_main.lambda_handler(test_session_event_with_invalid_id, None)
        with self.assertRaises(ValueError) as cm_conext_event:
            alexa_main.lambda_handler(test_context_only_event_with_invalid_id, None)
        self.assertEqual(cm_session_event.exception.message, "Invalid Application ID")
        self.assertEqual(cm_conext_event.exception.message, "Invalid Application ID")
        on_session_started.assert_not_called()
        on_launch.assert_not_called()

    @patch("alexa_main.events.on_session_started")
    @patch("alexa_main.events.on_launch")
    def test_lambda_handler_on_session_started_launch_request(self, on_launch, on_session_started):
        test_session_obj = {
            'application': {
                'applicationId': TEST_APPLICATION_ID},
            'new': True
        }

        test_event = {
            'session': test_session_obj,
            'request': {
                'requestId': TEST_REQUEST_ID,
                'type': 'LaunchRequest'
            },
            'context': {}
        }

        alexa_main.lambda_handler(test_event, None)
        on_session_started.assert_called_once_with({
            'requestId': TEST_REQUEST_ID,
        }, test_session_obj)
        on_launch.assert_called_once()

    @patch("alexa_main.events.on_intent")
    def test_lambda_handler_intent_request(self, on_intent):
        test_request_obj = {
            'requestId': TEST_REQUEST_ID,
            'type': 'IntentRequest'
        }
        test_session_obj = {
            'application': {
                'applicationId': TEST_APPLICATION_ID,
            },
            'new': True
        }
        test_context_obj = {
            "System": {},
            "AudioPlayer": {}
        }

        test_event = {
            'session': test_session_obj,
            'request': test_request_obj,
            'context': test_context_obj
        }

        alexa_main.lambda_handler(test_event, None)
        on_intent.assert_called_once_with(test_request_obj, test_session_obj, test_context_obj)

    @patch("alexa_main.events.on_session_ended")
    def test_lambda_handler_session_ended_request(self, on_session_ended):
        test_request_obj = {
            'requestId': TEST_REQUEST_ID,
            'type': 'SessionEndedRequest'
        }
        test_session_obj = {
            'application': {
                'applicationId': TEST_APPLICATION_ID,
            },
            'new': False
        }
        test_context_obj = {
            "System": {},
            "AudioPlayer": {}
        }

        test_event = {
            'session': test_session_obj,
            'request': test_request_obj,
            'context': test_context_obj
        }

        alexa_main.lambda_handler(test_event, None)
        on_session_ended.assert_called_once_with(test_request_obj, test_session_obj)
