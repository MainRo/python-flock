from unittest import TestCase
from flock.message import FlockMessage

class FlockMessageTestCase(TestCase):
    def test_init(self):
        msg = FlockMessage()

    def test_reset(self):
        msg = FlockMessage()
        msg.reset()
        self.assertEqual(None, msg.type)
        self.assertEqual(None, msg.uid)
        self.assertEqual(None, msg.device)
        self.assertEqual(None, msg.namespace)

