from unittest import TestCase
from mock import MagicMock
from twisted.internet import reactor, defer
from flock.controller.enocean.packet import Packet
from flock.handler.enocean import EnoceanHandler
from flock.roster import Roster, Device
from flock.message import FlockMessage

class TestController(object):
    def __init__(self, d):
        self.d = d

    def send_packet(self, packet):
        return self.d

class EnoceanHandlerTestCase(TestCase):
    def test_invoke(self):
        handler = EnoceanHandler(reactor)
        self.assertIs(None, handler.invoke(Device(protocol='enocean', protocol_id='42'), FlockMessage()))


    def test_publish_packet(self):
        handler = EnoceanHandler(reactor)
        device = Device(protocol='enocean', protocol_id='42')
        device.uid = 'DKEJUFKD'
        handler.roster.get_device = MagicMock(return_value=device)
        handler.router.publish = MagicMock()

        packet = Packet()
        packet.id = '42'
        packet.attr_temperature = 20.4
        handler.publish_packet(packet)

        expected_message = FlockMessage()
        expected_message.uid = device.uid
        expected_message.namespace = 'controller'
        expected_message.attributes[FlockMessage.MSG_ATTRIBUTE_TEMPERATURE] = packet.attr_temperature
        expected_message.type = FlockMessage.Type.report

        handler.router.publish.assert_called_once_with(expected_message)

