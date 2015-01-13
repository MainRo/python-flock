from unittest import TestCase
from mock import MagicMock, patch, call
from flock.roster import Controller, FlockRoster
from flock.message import FlockMessage
from twisted.internet.protocol import Protocol

class TestFrontend(Protocol):
    def report_received(self):
        return

class FlockRosterTestCase(TestCase):
    def setUp(self):
        FlockRoster.roster_instance = None

    def test_instantiate(self):
        roster1 = FlockRoster.instantiate()
        roster2 = FlockRoster.instantiate()
        self.assertIs(roster1, roster2)


    def test_attach_controller(self):
        roster = FlockRoster.instantiate()
        controller = Controller('foo', 'bar', 'prot')
        self.assertEqual(0, roster.attach_controller(controller))

    def test_detach_controller(self):
        roster = FlockRoster.instantiate()
        controller = Controller('foo', 'bar', 'prot')
        roster.attach_controller(controller)
        self.assertEqual(0, roster.detach_controller(controller))


    def test_attach_frontend(self):
        roster = FlockRoster.instantiate()
        frontend = Protocol()
        self.assertEqual(0, roster.attach_frontend(frontend))

    def test_detach_frontend(self):
        roster = FlockRoster.instantiate()
        frontend = Protocol()
        roster.attach_frontend(frontend)
        self.assertEqual(0, roster.detach_frontend(frontend))

    def test_send_report(self):
        roster = FlockRoster.instantiate()
        frontend1 = MagicMock()
        frontend2 = MagicMock()
        roster.attach_frontend(frontend1)
        roster.attach_frontend(frontend2)
        message = FlockMessage()
        roster.send_report(message)
        frontend1.report_received.assert_called_once_with(message)
        frontend2.report_received.assert_called_once_with(message)

    @patch('twisted.internet.protocol')
    def test_send_message(self, mock_protocol):
        roster = FlockRoster.instantiate()
        controller = Controller('foo', 'bar', mock_protocol)
        roster.attach_controller(controller)

        message = FlockMessage()
        message.protocol = 'bar'
        roster.send_message(message)
        mock_protocol.send_message.assert_called_once_with(message)

    @patch('twisted.internet.protocol')
    @patch('twisted.internet.protocol')
    def test_send_message_on_one_controller(self, mock_protocol1, mock_protocol2):
        roster = FlockRoster.instantiate()
        controller1 = Controller('foo', 'bar', mock_protocol1)
        controller2 = Controller('foo', 'bar1', mock_protocol2)
        roster.attach_controller(controller1)
        roster.attach_controller(controller2)

        message = FlockMessage()
        message.protocol = 'bar'
        roster.send_message(message)
        mock_protocol1.send_message.assert_called_once_with(message)
        self.assertEqual(0, mock_protocol2.send_message.call_count)

    """
    @patch.object(FlockController, 'start')
    def test_start(self, test_start):
        roster = FlockRoster.instantiate()
        controller = FlockController()
        roster.attach(controller)
        self.assertEqual(0, roster.start())
        test_start.assert_called_with('foo')
    """


