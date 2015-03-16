from unittest import TestCase
from mock import MagicMock
from flock.controller.enocean.protocol import EnoceanProtocol
from flock.controller.enocean.message import EnoceanMessage
from flock.message import FlockMessage


class EnoceanProtocolTestCase(TestCase):
    def test_init(self):
        protocol = EnoceanProtocol()

    def test_valid_packet(self):
        protocol = EnoceanProtocol()
        protocol.publish_packet = MagicMock()
        data = '\xA5\x02\x05\xFF\x00'
        protocol.packet_received(EnoceanMessage.PACKET_TYPE_RADIO, data, '')
        """
        message = protocol.pop_message()
        self.assertEqual(True, message.is_valid())
        self.assertEqual(0.0,
                message.attributes[FlockMessage.MSG_ATTRIBUTE_TEMPERATURE])
        """

    def test_invalid_packet(self):
        """ Receive a packet with invalid data
        """
        protocol = EnoceanProtocol()
        data = '\x00\x02\x05\xFF\x00'
        protocol.packet_received(EnoceanMessage.PACKET_TYPE_RADIO, data, '')
#        self.assertIs(None, protocol.pop_message())

    def test_send_message(self):
        protocol = EnoceanProtocol()
        message = FlockMessage()
        protocol.send_message(message)

