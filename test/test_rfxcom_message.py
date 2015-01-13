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
        self.assertTrue(message.is_valid())

    def test_temperature_on_two_bytes(self):
        packet = '\x08\x50\x02\x01\x91\x01\x02\x01\x89'
        message = RfxcomMessage()
        message.load(packet)
        self.assertEqual("rfxcom", message.protocol)
        self.assertEqual("9101", message.device_id)
        self.assertEqual(51.3,
                message.attributes[FlockMessage.MSG_ATTRIBUTE_TEMPERATURE])

    def test_negative_temperature_message(self):
        packet = '\x08\x50\x01\x10\x00\x01\x80\xBC\x69'
        message = RfxcomMessage()
        message.load(packet)
        self.assertEqual("rfxcom", message.protocol)
        self.assertEqual("0001", message.device_id)
        self.assertEqual(-18.8,
                message.attributes[FlockMessage.MSG_ATTRIBUTE_TEMPERATURE])
        self.assertTrue(message.is_valid())


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
        self.assertTrue(message.is_valid())

    def test_lighting2_ac_id_min(self):
        packet = '\x0b\x11\x00\x06\x3f\x00\x00\x00\x4a\x01\x69\x00'
        message = RfxcomMessage()
        message.load(packet)
        self.assertTrue(message.is_valid())
        self.assertEqual("rfxcom", message.protocol)
        self.assertEqual("00000000", message.device_id)

    def test_lighting2_ac_id_max(self):
        packet = '\x0b\x11\x00\x06\xff\xff\xff\xff\x4a\x01\x69\x00'
        message = RfxcomMessage()
        message.load(packet)
        self.assertTrue(message.is_valid())
        self.assertEqual("rfxcom", message.protocol)
        self.assertEqual("03FFFFFF", message.device_id)

    def test_lighting2_ac_on(self):
        packet = '\x0b\x11\x00\x06\xf9\x01\x00\xcb\x4a\x01\x69\x00'
        message = RfxcomMessage()
        message.load(packet)
        self.assertEqual("rfxcom", message.protocol)
        self.assertTrue(message.attributes[FlockMessage.MSG_ATTRIBUTE_SWITCH_BISTATE])
        self.assertTrue(message.is_valid())

    def test_lighting2_ac_off(self):
        packet = '\x0b\x11\x00\x06\xf9\x01\x00\xcb\x4a\x00\x69\x00'
        message = RfxcomMessage()
        message.load(packet)
        self.assertEqual("rfxcom", message.protocol)
        self.assertFalse(message.attributes[FlockMessage.MSG_ATTRIBUTE_SWITCH_BISTATE])
        self.assertTrue(message.is_valid())

    def test_dump_lighting2_ac_on(self):
        expected_packet = '\x0b\x11\x00\x00\x40\x23\x45\x67\x03\x01\x0f\x00'
        message = RfxcomMessage()
        message.device_id = '01234567'
        message.protocol = 'rfxcom'
        message.private_data = '1103'
        message.attributes[FlockMessage.MSG_ATTRIBUTE_SWITCH_BISTATE] = True
        packet = message.dump()
        self.assertEqual(expected_packet, packet)

    def test_dump_lighting2_ac_off(self):
        expected_packet = '\x0b\x11\x00\x00\x40\x23\x45\x67\x03\x00\x00\x00'
        message = RfxcomMessage()
        message.device_id = '01234567'
        message.protocol = 'rfxcom'
        message.private_data = '1103'
        message.attributes[FlockMessage.MSG_ATTRIBUTE_SWITCH_BISTATE] = False
        packet = message.dump()
        self.assertEqual(expected_packet, packet)

    def test_lighting2_load_and_dump(self):
        packet = '\x0b\x11\x00\x00\x80\x01\x00\xcb\x4a\x01\x0f\x00'
        message = RfxcomMessage()
        message.load(packet)
        dump_packet = message.dump()
        self.assertEqual(packet, dump_packet)

