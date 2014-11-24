from unittest import TestCase
from flock.controller.enocean.message import EnoceanMessage
from flock.message import FlockMessage

class EnoceanMessageTestCase(TestCase):
    def test_init(self):
        message = EnoceanMessage()
        self.assertEqual(False, message.is_valid())

    def test_load_unknown_type(self):
        message = EnoceanMessage()
        data = '\xA5\x00\x00\x84\x00'
        optional_data = ''
        message.load(0, data, optional_data)
        self.assertEqual(False, message.is_valid())

    def test_load_data_incomplete(self):
        message = EnoceanMessage()
        data = ''
        optional_data = ''
        message.load(EnoceanMessage.PACKET_TYPE_RADIO, data, optional_data)
        self.assertEqual(False, message.is_valid())

    def test_temperature_default(self):
        """ Test reception of a temperature message from un-configured (dev)
            sensor, i.e. function and types are set to 0.
        """
        data = '\xA5\x00\x00\x84\x00'
        optional_data = ''
        message = EnoceanMessage()
        message.load(EnoceanMessage.PACKET_TYPE_RADIO, data, optional_data)
        self.assertEqual(True, message.is_valid())
        self.assertEqual('enocean', message.protocol)
        self.assertEqual('', message.device_id)
        self.assertEqual(19.3,
                message.attributes[FlockMessage.MSG_ATTRIBUTE_TEMPERATURE])


    def test_temperature_message(self):
        data = '\xA5\x02\x05\x84\x00'
        optional_data = ''
        message = EnoceanMessage()
        message.load(EnoceanMessage.PACKET_TYPE_RADIO, data, optional_data)
        self.assertEqual(True, message.is_valid())
        self.assertEqual('enocean', message.protocol)
        self.assertEqual('', message.device_id)
        self.assertEqual(19.3,
                message.attributes[FlockMessage.MSG_ATTRIBUTE_TEMPERATURE])


