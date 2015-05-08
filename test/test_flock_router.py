from unittest import TestCase
from mock import MagicMock, patch, call
from flock.router import Router
from flock.message import FlockMessage
from twisted.internet.protocol import Protocol

class TestFrontend(Protocol):
    def event(self, message):
        return

class RouterTestCase(TestCase):
    def setUp(self):
        Router.router_instance = None

    def test_instantiate(self):
        router1 = Router.instantiate()
        router2 = Router.instantiate()
        self.assertIs(router1, router2)


    def test_attach_handler(self):
        router = Router.instantiate()
        handler = MagicMock()
        self.assertEqual(0, router.attach_handler(handler))

    def test_detach_handler(self):
        router = Router.instantiate()
        handler = MagicMock()
        router.attach_handler(handler)
        self.assertEqual(0, router.detach_handler(handler))


    def test_attach_frontend(self):
        router = Router.instantiate()
        frontend = Protocol()
        self.assertEqual(0, router.attach_frontend(frontend))

    def test_detach_frontend(self):
        router = Router.instantiate()
        frontend = Protocol()
        router.attach_frontend(frontend)
        self.assertEqual(0, router.detach_frontend(frontend))

    def test_publish(self):
        router = Router.instantiate()
        frontend1 = MagicMock()
        frontend2 = MagicMock()
        router.attach_frontend(frontend1)
        router.attach_frontend(frontend2)
        message = FlockMessage()
        message.uid = '42'
        router.publish(message)
        frontend1.event.assert_called_once_with(message)
        frontend2.event.assert_called_once_with(message)

    @patch('flock.router.Roster')
    def test_call(self, mock_roster):
        router = Router.instantiate()
        device = {}
        roster = MagicMock()
        roster.get_device = MagicMock(return_value=device)
        mock_roster.instantiate = MagicMock(return_value=roster)
        handler = MagicMock()
        router.attach_handler(handler)

        message = FlockMessage()
        message.uid = '42'
        router.call(message)

        expected_message = FlockMessage()
        expected_message.uid = '42'
        expected_message.device = device
        handler.invoke.assert_called_once_with(expected_message)

    @patch('flock.router.Roster')
    def test_call_on_one_controller(self, mock_roster):
        router = Router.instantiate()
        device = {}
        roster = MagicMock()
        roster.get_device = MagicMock(return_value=device)
        mock_roster.instantiate = MagicMock(return_value=roster)
        handler1 = MagicMock()
        handler1.invoke = MagicMock(return_value=None)
        handler2 = MagicMock()
        router.attach_handler(handler1)
        router.attach_handler(handler2)

        message = FlockMessage()
        message.uid = '42'
        router.call(message)

        expected_message = FlockMessage()
        expected_message.uid = '42'
        expected_message.device = device
        handler1.invoke.assert_called_once_with(expected_message)
        handler2.invoke.assert_called_once_with(expected_message)

    """
    @patch.object(FlockController, 'start')
    def test_start(self, test_start):
        router = Router.instantiate()
        controller = FlockController()
        router.attach(controller)
        self.assertEqual(0, router.start())
        test_start.assert_called_with('foo')
    """


