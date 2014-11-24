from unittest import TestCase
from flock.controller.rfxcom.message import RfxcomMessage
from flock.message import FlockMessage

class RfxcomMessageTestCase(TestCase):
    def test_temperature_message(self):
        packet = '\x08\x50\x02\x01\x91\x01\x00\xf7\x89'
        message = RfxcomMessage()
        message.load(packet)
        self.assertEqual("rfxcom", message.protocol)
        self.assertEqual("9101", message.device_id)
        self.assertEqual(24.7,
                message.attributes[FlockMessage.MSG_ATTRIBUTE_TEMPERATURE])

    def test_temperature_on_two_bytes(self):
        packet = '\x08\x50\x02\x01\x91\x01\x02\x01\x89'
        message = RfxcomMessage()
        message.load(packet)
        self.assertEqual("rfxcom", message.protocol)
        self.assertEqual("9101", message.device_id)
        self.assertEqual(51.3,
                message.attributes[FlockMessage.MSG_ATTRIBUTE_TEMPERATURE])

    def test_temperature_and_humidyty(self):
        packet = '\x0a\x52\x01\x06\xf9\x01\x00\xcb\x4a\x03\x69'
        message = RfxcomMessage()
        message.load(packet)
        self.assertEqual("rfxcom", message.protocol)
        self.assertEqual("f901", message.device_id)
        self.assertEqual(20.3,
                message.attributes[FlockMessage.MSG_ATTRIBUTE_TEMPERATURE])
        self.assertEqual(74,
                message.attributes[FlockMessage.MSG_ATTRIBUTE_HUMIDITY])

