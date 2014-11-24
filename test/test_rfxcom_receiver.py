from unittest import TestCase
from mock import patch, call
from flock.controller.rfxcom.protocol import RfxcomReceiver

class TestProtocol(RfxcomReceiver):
    def packet_received(self, data):
        return

@patch.object(TestProtocol, 'packet_received')
class RfxcomReceiverTestCase(TestCase):
    def test_receive_without_connection(self, test_packet_received):
        protocol = TestProtocol()
        data = '\x08\x03\x04\x05\x06\x06\x06\x06\x06'
        protocol.dataReceived(data)

    def test_receive_one_packet(self, test_packet_received):
        protocol = TestProtocol()
        protocol.connectionMade()
        data = '\x08\x03\x04\x05\x06\x06\x06\x06\x06'
        protocol.dataReceived(data)
        test_packet_received.assert_called_with(data)

    def test_receive_packet_from_chunks(self, test_packet_received):
        protocol = TestProtocol()
        protocol.connectionMade()
        data = '\x08\x03\x04\x05\x06\x07\x08\x09\x10'
        protocol.dataReceived(data[:3])
        protocol.dataReceived(data[3:6])
        protocol.dataReceived(data[6:])
        test_packet_received.assert_called_with(data)

    def test_receive_several_packets(self, test_packet_received):
        protocol = TestProtocol()
        protocol.connectionMade()
        data = '\x08\x03\x04\x05\x06\x06\x06\x06\x06'
        protocol.dataReceived(data)
        test_packet_received.assert_called_with(data)
        data = '\x08\x03\x04\x05\x06\x06\x06\x07\x08'
        protocol.dataReceived(data)
        test_packet_received.assert_called_with(data)
        data = '\x08\x03\x04\x05\x06\x06\x06\x09\x10'
        protocol.dataReceived(data)
        test_packet_received.assert_called_with(data)

