from unittest import TestCase
from mock import patch, call
from flock.protocol import FlockProtocol
from flock.message import FlockMessage


class FlockProtocolTestCase(TestCase):
    def setUp(self):
        return

    """
    def test_message(self):
        msg1 = FlockMessage()
        msg2 = FlockMessage()
        protocol = FlockProtocol()
        protocol.push_message(msg1)
        protocol.push_message(msg2)

        self.assertIs(msg1, protocol.pop_message())
        self.assertIs(msg2, protocol.pop_message())
        return

    def test_pop_message_empty(self):
        protocol = FlockProtocol()
        self.assertIsNone(protocol.pop_message())
    """

    @patch.object(FlockProtocol, 'byte_received')
    def test_process_one_byte(self, test_byte_received):
        protocol = FlockProtocol()
        protocol.dataReceived([1])
        test_byte_received.assert_called_with(1)

    @patch.object(FlockProtocol, 'byte_received')
    def test_process_some_bytes(self, test_byte_received):
        protocol = FlockProtocol()
        protocol.dataReceived('\x01\x02\x03\x04')
        expected = [call('\x01'), call('\x02'), call('\x03'), call('\x04')]
        self.assertEqual(expected, test_byte_received.call_args_list)

