from unittest import TestCase
from flock.controller.rfxcom.packet import Packet

class RfxcomMessageTestCase(TestCase):
    def test_temperature_message(self):
        packet_data = '\x08\x50\x02\x01\x91\x01\x00\xf7\x89'
        packet = Packet()
        packet.load(packet_data)
        self.assertEqual(Packet.Type.temperature, packet.type)
        self.assertEqual(0x9101, packet.id)
        self.assertEqual(24.7, packet.attr_temperature)
        self.assertTrue(packet.is_valid == True)

    def test_temperature_on_two_bytes(self):
        packet_data = '\x08\x50\x02\x01\x91\x01\x02\x01\x89'
        packet = Packet()
        packet.load(packet_data)
        self.assertEqual(Packet.Type.temperature, packet.type)
        self.assertEqual(0x9101, packet.id)
        self.assertEqual(51.3, packet.attr_temperature)
        self.assertTrue(packet.is_valid == True)

    def test_negative_temperature_message(self):
        packet_data = '\x08\x50\x01\x10\x00\x01\x80\xBC\x69'
        packet = Packet()
        packet.load(packet_data)
        self.assertEqual(Packet.Type.temperature, packet.type)
        self.assertEqual(0x01, packet.id)
        self.assertEqual(-18.8, packet.attr_temperature)
        self.assertTrue(packet.is_valid)


    def test_temperature_and_humidity(self):
        packet_data = '\x0a\x52\x01\x06\xf9\x01\x00\xcb\x4a\x03\x69'
        packet = Packet()
        packet.load(packet_data)
        self.assertEqual(Packet.Type.temperature_humidity, packet.type)
        self.assertEqual(0xf901, packet.id)
        self.assertEqual(20.3, packet.attr_temperature)
        self.assertEqual(74, packet.attr_humidity)
        self.assertTrue(packet.is_valid)

    def test_lighting2_ac_id_min(self):
        packet_data = '\x0b\x11\x00\x06\x3f\x00\x00\x00\x4a\x01\x69\x00'
        packet = Packet()
        packet.load(packet_data)
        self.assertTrue(packet.is_valid)
        self.assertEqual(Packet.Type.lighting2, packet.type)
        self.assertEqual(0x00, packet.id)

    def test_lighting2_ac_id_max(self):
        packet_data = '\x0b\x11\x00\x06\xff\xff\xff\xff\x4a\x01\x69\x00'
        packet = Packet()
        packet.load(packet_data)
        self.assertTrue(packet.is_valid)
        self.assertEqual(0x03FFFFFF, packet.id)

    def test_lighting2_ac_on(self):
        packet_data = '\x0b\x11\x00\x06\xf9\x01\x00\xcb\x4a\x01\x69\x00'
        packet = Packet()
        packet.load(packet_data)
        self.assertEqual(Packet.Type.lighting2, packet.type)
        self.assertTrue(packet.attr_state)
        self.assertTrue(packet.is_valid)

    def test_lighting2_ac_off(self):
        packet_data = '\x0b\x11\x00\x06\xf9\x01\x00\xcb\x4a\x00\x69\x00'
        packet = Packet()
        packet.load(packet_data)
        self.assertEqual(Packet.Type.lighting2, packet.type)
        self.assertFalse(packet.attr_state)
        self.assertTrue(packet.is_valid)

    def test_dump_lighting2_ac_on(self):
        expected_packet = '\x0b\x11\x00\x00\x40\x23\x45\x67\x03\x01\x0f\x00'
        packet = Packet()
        packet.type = Packet.Type.lighting2
        packet.id = 0x01234567
        packet.unit_code = 0x03
        packet.attr_state = True
        self.assertEqual(expected_packet, packet.dump())

    def test_dump_lighting2_ac_off(self):
        expected_packet = '\x0b\x11\x00\x00\x40\x23\x45\x67\x03\x00\x00\x00'
        packet = Packet()
        packet.type = Packet.Type.lighting2
        packet.id = 0x01234567
        packet.unit_code = 0x03
        packet.attr_state = False
        self.assertEqual(expected_packet, packet.dump())

    def test_lighting2_load_and_dump(self):
        packet_data = '\x0b\x11\x00\x00\x80\x01\x00\xcb\x4a\x01\x0f\x00'
        packet = Packet()
        packet.load(packet_data)
        dump_packet = packet.dump()
        self.assertEqual(packet_data, dump_packet)

    def test_dump_rfy_pair(self):
        expected_packet = '\x0c\x1a\x00\x00\x0f\xff\xff\x01\x07\x00\x00\x00\x00'
        packet = Packet()
        packet.id = 0x0FFFFF
        packet.type = Packet.Type.rfy
        packet.command = Packet.Command.pair
        self.assertEqual(expected_packet, packet.dump())
        return

    def test_dump_rfy_true(self):
        ''' True is mapped on 'up', i.e. shutter open.
        '''
        expected_packet = '\x0c\x1a\x00\x00\x0f\xff\xff\x01\x01\x00\x00\x00\x00'
        packet = Packet()
        packet.id = 0x0FFFFF
        packet.type = Packet.Type.rfy
        packet.attr_state = True
        packet.command = Packet.Command.set
        self.assertEqual(expected_packet, packet.dump())
        return

    def test_dump_rfy_false(self):
        ''' False is mapped on 'down', i.e. shutter closed.
        '''
        expected_packet = '\x0c\x1a\x00\x00\x0f\xff\xff\x01\x01\x00\x00\x00\x00'
        packet = Packet()
        packet.id = 0x0FFFFF
        packet.type = Packet.Type.rfy
        packet.attr_state = True
        packet.command = Packet.Command.set
        self.assertEqual(expected_packet, packet.dump())
        return
