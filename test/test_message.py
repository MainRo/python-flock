from unittest import TestCase
from flock.message import FlockMessage

class FlockMessageTestCase(TestCase):
    def test_init(self):
        msg = FlockMessage()
        self.assertEqual(False, msg.is_valid())

    def test_valid(self):
        msg = FlockMessage()
        msg.set_valid(True)
        self.assertEqual(True, msg.is_valid())
        msg.set_valid(False)
        self.assertEqual(False, msg.is_valid())

    def test_reset(self):
        msg = FlockMessage()
        msg.set_valid(True)
        msg.reset()
        self.assertEqual(False, msg.is_valid())

