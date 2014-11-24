from unittest import TestCase
from mock import patch, call
from flock.controller.enocean.protocol import EnoceanReceiver

class TestProtocol(EnoceanReceiver):
    def packet_received(self, data):
        return

@patch.object(TestProtocol, 'packet_received')
class EnoceanReceiverTestCase(TestCase):
    def test_receive_without_connection(self, test_packet_received):
        protocol = TestProtocol()
        data = '\x55\x00\x02\x00\x08\x42\x01\x02\x42'
        protocol.dataReceived(data)

    def test_receive_one_packet(self, test_packet_received):
        protocol = TestProtocol()
        protocol.connectionMade()
        data = '\x55\x00\x02\x00\x08\x42\x01\x02\x42'
        protocol.dataReceived(data)
        test_packet_received.assert_called_with(ord(data[4]), data[6:8], '')

    def test_receive_packet_from_chunks(self, test_packet_received):
        protocol = TestProtocol()
        protocol.connectionMade()
        data = '\x55\x00\x02\x00\x08\x42\x01\x02\x42'
        protocol.dataReceived(data[:3])
        protocol.dataReceived(data[3:6])
        protocol.dataReceived(data[6:])
        test_packet_received.assert_called_with(ord(data[4]), data[6:8], '')

    def test_receive_several_packets(self, test_packet_received):
        protocol = TestProtocol()
        protocol.connectionMade()
        data = '\x55\x00\x02\x00\x08\x42\x01\x02\x42'
        protocol.dataReceived(data)
        test_packet_received.assert_called_with(ord(data[4]), data[6:8], '')
        data = '\x55\x00\x02\x00\x08\x42\x03\x04\x42'
        protocol.dataReceived(data)
        test_packet_received.assert_called_with(ord(data[4]), data[6:8], '')
        data = '\x55\x00\x02\x00\x08\x42\x05\x06\x42'
        protocol.dataReceived(data)
        test_packet_received.assert_called_with(ord(data[4]), data[6:8], '')

