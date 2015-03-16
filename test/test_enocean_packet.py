from unittest import TestCase
from flock.controller.enocean.packet import Packet

class EnoceanPacketTestCase(TestCase):
    def test_init(self):
        packet = Packet()
        self.assertEqual(False, packet.is_valid)

    def test_load_unknown_type(self):
        packet = Packet()
        data = '\xA5\x00\x00\x84\x00'
        optional_data = ''
        packet.load(0, data, optional_data)
        self.assertEqual(False, packet.is_valid)

    def test_load_data_incomplete(self):
        packet = Packet()
        data = ''
        optional_data = ''
        packet.load(Packet.PACKET_TYPE_RADIO, data, optional_data)
        self.assertEqual(False, packet.is_valid)

    def test_temperature_default(self):
        """ Test reception of a temperature message from un-configured (dev)
            sensor, i.e. function and types are set to 0.
        """
        data = '\xA5\x00\x00\x84\x00'
        optional_data = ''
        packet = Packet()
        packet.load(Packet.PACKET_TYPE_RADIO, data, optional_data)
        self.assertEqual(True, packet.is_valid)
        self.assertEqual('', packet.id)
        self.assertEqual(19.3, packet.attr_temperature)

    def test_temperature_message(self):
        data = '\xA5\x02\x05\x84\x00'
        optional_data = ''
        packet = Packet()
        packet.load(Packet.PACKET_TYPE_RADIO, data, optional_data)
        self.assertEqual(True, packet.is_valid)
        self.assertEqual('', packet.id)
        self.assertEqual(19.3, packet.attr_temperature)


