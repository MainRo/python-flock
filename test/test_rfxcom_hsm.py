from unittest import TestCase
from mock import patch, call
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

@patch.object(reactor, 'callLater')
@patch.object(TestTransport, 'write', create=True)
@patch.object(TestTransport, 'flushInput', create=True)
class RfxcomHsmTestCase(TestCase):
    def test_reset(self, test_flushInput, test_write, test_callLater):
        protocol = TestProtocol()
        hsm = RfxcomHsm(protocol)
        test_flushInput.assert_called_with()
        test_write.assert_called_with(TEST_RESET_PACKET)
        test_callLater.assert_called()
        hsm.on_timer1()
        test_write.assert_called_with(TEST_STATUS_PACKET)
        hsm.process_packet("foo")
        test_write.assert_called_with(TEST_MODE_PACKET)
        self.assertIs(hsm.state_running, hsm.current_state)

