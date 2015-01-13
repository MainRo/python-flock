from unittest import TestCase
from flock.message import FlockMessage

class FlockMessageTestCase(TestCase):
    def test_init(self):
        msg = FlockMessage()
        self.assertEqual(False, msg.is_valid())

    def test_copy(self):
        msg1 = FlockMessage()
        msg1.type = FlockMessage.MSG_TYPE_REPORT
        msg1.device_id = 'foo_id'
        msg1.protocol = 'bar'
        msg1.private_data = 'foobar'
        msg1.set_valid(True)
        msg1.attributes[FlockMessage.MSG_ATTRIBUTE_TEMPERATURE] = '23.5'
        msg1.attributes[FlockMessage.MSG_ATTRIBUTE_HUMIDITY] = '76'
        msg2 = FlockMessage(msg1)

        self.assertEqual(msg1.type, msg2.type)
        self.assertEqual(msg1.device_id, msg2.device_id)
        self.assertEqual(msg1.protocol, msg2.protocol)
        self.assertEqual(msg1.private_data, msg2.private_data)
        self.assertTrue(msg2.is_valid())
        self.assertEqual(msg1.attributes, msg2.attributes)

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

