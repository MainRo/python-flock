from unittest import TestCase
from mock import patch, call, ANY
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from flock.controller.rfxcom.protocol import RfxcomHsm

TEST_RESET_PACKET = '\x0D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
TEST_STATUS_PACKET = '\x0D\x00\x00\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00'
TEST_MODE_PACKET = '\x0D\x00\x00\x01\x03\x53\x00\x00\x0E\x2F\x00\x00\x00\x00'

class TestTransport(object):
    def __init__(self):
        return

class TestProtocol(Protocol):
    def __init__(self):
        self.transport = TestTransport()

    def dataReceived(self, data):
        return

class RfxcomHsmTestCase(TestCase):
    @patch.object(reactor, 'callLater')
    @patch.object(TestTransport, 'write', create=True)
    @patch.object(TestTransport, 'flushInput', create=True)
    def test_reset(self, mock_flushInput, mock_write, test_callLater):
        protocol = TestProtocol()
        hsm = RfxcomHsm(protocol)
        mock_flushInput.assert_called_once_with()
        mock_write.assert_called_with(TEST_RESET_PACKET)
        test_callLater.assert_called()
        hsm.on_timer1()
        mock_write.assert_called_with(TEST_STATUS_PACKET)
        hsm.process_packet("foo")
        mock_write.assert_called_with(TEST_MODE_PACKET)
        self.assertIs(hsm.state_running, hsm.current_state)

    @patch.object(reactor, 'callLater')
    @patch('test.test_rfxcom_hsm.TestTransport', create=True)
    @patch('test.test_rfxcom_hsm.TestProtocol', create=True)
    def test_send_packet(self, mock_protocol, mock_transport, mock_callLater):
        # Initialize HSM
        protocol = mock_protocol
        protocol.transport = mock_transport
        hsm = RfxcomHsm(protocol)
        mock_transport.flushInput.assert_called_once_with()
        mock_transport.write.assert_called_once_with(TEST_RESET_PACKET)
        mock_callLater.assert_called()
        hsm.on_timer1()
        mock_transport.write.assert_called_with(TEST_STATUS_PACKET)
        hsm.process_packet("foo")
        mock_transport.write.assert_called_with(TEST_MODE_PACKET)
        self.assertIs(hsm.state_running, hsm.current_state)

        # send packet
        packet = '\x0b\x11\x00\x06\x00\xc3\x3e\xae\x02\x00\x00\x70'
        hsm.send_packet(packet)
        mock_transport.write.assert_called_with(packet)
        mock_protocol.report_message.assert_called_once_with(ANY)

    @patch.object(reactor, 'callLater')
    @patch('test.test_rfxcom_hsm.TestTransport', create=True)
    def test_send_packet_uninitialized(self, mock_transport, mock_callLater):
        # Partially initialize HSM
        protocol = Protocol()
        protocol.transport = mock_transport
        hsm = RfxcomHsm(protocol)
        mock_transport.flushInput.assert_called_once_with()
        mock_transport.write.assert_called_once_with(TEST_RESET_PACKET)
        mock_callLater.assert_called()

        # send packet
        packet = '\x12\x32'
        hsm.send_packet(packet)

