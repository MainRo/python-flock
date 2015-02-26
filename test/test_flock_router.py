from unittest import TestCase
from mock import MagicMock, patch, call
from flock.router import Controller, Router
from flock.message import FlockMessage
from twisted.internet.protocol import Protocol

class TestFrontend(Protocol):
    def report_received(self):
        return

class RouterTestCase(TestCase):
    def setUp(self):
        Router.router_instance = None

    def test_instantiate(self):
        router1 = Router.instantiate()
        router2 = Router.instantiate()
        self.assertIs(router1, router2)


    def test_attach_controller(self):
        router = Router.instantiate()
        controller = Controller('foo', 'bar', 'prot')
        self.assertEqual(0, router.attach_controller(controller))

    def test_detach_controller(self):
        router = Router.instantiate()
        controller = Controller('foo', 'bar', 'prot')
        router.attach_controller(controller)
        self.assertEqual(0, router.detach_controller(controller))


    def test_attach_frontend(self):
        router = Router.instantiate()
        frontend = Protocol()
        self.assertEqual(0, router.attach_frontend(frontend))

    def test_detach_frontend(self):
        router = Router.instantiate()
        frontend = Protocol()
        router.attach_frontend(frontend)
        self.assertEqual(0, router.detach_frontend(frontend))

    def test_send_report(self):
        router = Router.instantiate()
        frontend1 = MagicMock()
        frontend2 = MagicMock()
        router.attach_frontend(frontend1)
        router.attach_frontend(frontend2)
        message = FlockMessage()
        router.send_report(message)
        frontend1.report_received.assert_called_once_with(message)
        frontend2.report_received.assert_called_once_with(message)

    @patch('twisted.internet.protocol')
    def test_send_message(self, mock_protocol):
        router = Router.instantiate()
        controller = Controller('foo', 'bar', mock_protocol)
        router.attach_controller(controller)

        message = FlockMessage()
        message.protocol = 'bar'
        router.send_message(message)
        mock_protocol.send_message.assert_called_once_with(message)

    @patch('twisted.internet.protocol')
    @patch('twisted.internet.protocol')
    def test_send_message_on_one_controller(self, mock_protocol1, mock_protocol2):
        router = Router.instantiate()
        controller1 = Controller('foo', 'bar', mock_protocol1)
        controller2 = Controller('foo', 'bar1', mock_protocol2)
        router.attach_controller(controller1)
        router.attach_controller(controller2)

        message = FlockMessage()
        message.protocol = 'bar'
        router.send_message(message)
        mock_protocol1.send_message.assert_called_once_with(message)
        self.assertEqual(0, mock_protocol2.send_message.call_count)

    """
    @patch.object(FlockController, 'start')
    def test_start(self, test_start):
        router = Router.instantiate()
        controller = FlockController()
        router.attach(controller)
        self.assertEqual(0, router.start())
        test_start.assert_called_with('foo')
    """


