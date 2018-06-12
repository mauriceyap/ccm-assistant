import unittest
from datetime import datetime

import speech


class TestSpeech(unittest.TestCase):
    def test_get_next_event(self):
        test_event_datetime = datetime(2016, 11, 13, 13, 14, 15)
        self.assertEqual(speech.get_next_event("A great event!", test_event_datetime),
                         "The next event is A great event! on Sunday 13 November at 13:14. ")
