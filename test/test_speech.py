import unittest
import src.speech as speech
from datetime import datetime


class TestSpeech(unittest.TestCase):
    def test_get_next_event(self):
        test_event_datetime = datetime(2016, 11, 13, 13, 14, 15)
        self.assertEqual(speech.get_next_event("A great event!", test_event_datetime),
                         "The next event is A great event! on Sunday 13 November at 13:14. ")


if __name__ == '__main__':
    unittest.main()
