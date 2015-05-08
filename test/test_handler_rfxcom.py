from unittest import TestCase
from mock import MagicMock, patch

from twisted.internet import reactor, defer
from flock.handler.rfxcom.rfy import RfxcomHandler
from flock.controller.rfxcom.packet import Packet
from flock.message import FlockMessage
from flock.roster import Device

class RfxcomHandlerTestCase(TestCase):
    def test_set_bistate_true(self):
        d = defer.Deferred()
        handler = RfxcomHandler(reactor)
        handler.send_packet = MagicMock(return_value = d)

        device = Device(protocol='rfxcom', protocol_id=0x42)
        device.set_private({'type': Packet.Type.lighting2, 'unit_code': 4 })
        message = FlockMessage()
        message.namespace = 'controller'
        message.type = FlockMessage.Type.set
        message.device = device
        message.attributes[FlockMessage.MSG_ATTRIBUTE_SWITCH_BISTATE] = True

        pair_defer = handler.invoke(message)

        expected_packet = '\x0b\x11\x00\x00\x00\x00\x00\x42\x04\x01\x0f\x00'
        self.assertEqual(d, pair_defer)
        handler.send_packet.assert_called_once_with(expected_packet)
        return

    def test_set_bistate_false(self):
        d = defer.Deferred()
        handler = RfxcomHandler(reactor)
        handler.send_packet = MagicMock(return_value = d)

        device = Device(protocol='rfxcom', protocol_id=0x42)
        device.set_private({'type': Packet.Type.lighting2, 'unit_code': 4 })
        message = FlockMessage()
        message.namespace = 'controller'
        message.type = FlockMessage.Type.set
        message.device = device
        message.attributes[FlockMessage.MSG_ATTRIBUTE_SWITCH_BISTATE] = False

        pair_defer = handler.invoke(message)

        expected_packet = '\x0b\x11\x00\x00\x00\x00\x00\x42\x04\x00\x00\x00'
        self.assertEqual(d, pair_defer)
        handler.send_packet.assert_called_once_with(expected_packet)
        return

    def test_set_bistate_rfy_false(self):
        d = defer.Deferred()
        handler = RfxcomHandler(reactor)
        handler.send_packet = MagicMock(return_value = d)

        device = Device(protocol='rfxcom:rfy', protocol_id=1)
        device.set_private({'type': Packet.Type.rfy, 'unit_code': 1 })
        message = FlockMessage()
        message.namespace = 'controller'
        message.type = FlockMessage.Type.set
        message.device = device
        message.attributes[FlockMessage.MSG_ATTRIBUTE_SWITCH_BISTATE] = False

        pair_defer = handler.invoke(message)

        expected_packet = '\x0c\x1a\x00\x00\x00\x00\x01\x01\x03\x00\x00\x00\x00'
        self.assertEqual(d, pair_defer)
        handler.send_packet.assert_called_once_with(expected_packet)
        return

