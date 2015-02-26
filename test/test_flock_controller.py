from unittest import TestCase
from flock.router import Controller
from twisted.internet.protocol import Protocol

class FlockControllerTestCase(TestCase):
    def test_init(self):
        protocol = Protocol()
        controller = Controller('/foo', 'foo', protocol)
        self.assertEqual('/foo', controller.path)
        self.assertEqual('foo', controller.protocol_name)
        self.assertEqual(protocol, controller.protocol)


