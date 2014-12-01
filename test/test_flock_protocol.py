from unittest import TestCase
from mock import Mock, patch, call
from flock.protocol import FlockProtocol

class FlockProtocolTestCase(TestCase):
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

    @patch('flock.protocol.FlockRoster')
    def test_report_message(self, mock_roster):
        mock_roster.instantiate.return_value = mock_roster
        message = Mock()
        protocol = FlockProtocol()
        protocol.report_message(message)
        mock_roster.send_report.assert_called_once_with(message)

