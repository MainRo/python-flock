from unittest import TestCase
from flock.controller.rfxcom.protocol import RfxcomPacketHsm


class RfxcomPacketHsmTestCase(TestCase):
    def test_init(self):
        hsm = RfxcomPacketHsm()
        self.assertEqual(hsm.state_length, hsm.current_state)
        self.assertIsNone(hsm.get_packet())

    def test_size_is_zero(self):
        """ No data at all
        """
        hsm = RfxcomPacketHsm()
        hsm.on_data('\x00')
        self.assertEqual(hsm.state_length, hsm.current_state)
        self.assertIsNone(hsm.get_packet())

    def test_size_is_one(self):
        """ Type only
        """
        hsm = RfxcomPacketHsm()
        hsm.on_data('\x01')
        self.assertEqual(hsm.state_type, hsm.current_state)
        hsm.on_data('\x02')
        self.assertEqual(hsm.state_length, hsm.current_state)
        packet = hsm.get_packet()
        self.assertEqual('\x01\x02', packet)

    def test_size_is_two(self):
        """ Up to subtype
        """
        hsm = RfxcomPacketHsm()
        hsm.on_data('\x02')
        hsm.on_data('\x03')
        self.assertEqual(hsm.state_subtype, hsm.current_state)
        hsm.on_data('\x04')
        self.assertEqual(hsm.state_length, hsm.current_state)
        packet = hsm.get_packet()
        self.assertEqual('\x02\x03\x04', packet)

    def test_size_is_three(self):
        """ Up to sequence number
        """
        hsm = RfxcomPacketHsm()
        hsm.on_data('\x03')
        hsm.on_data('\x04')
        hsm.on_data('\x05')
        self.assertEqual(hsm.state_sequence, hsm.current_state)
        hsm.on_data('\x06')
        self.assertEqual(hsm.state_length, hsm.current_state)
        packet = hsm.get_packet()
        self.assertEqual('\x03\x04\x05\x06', packet)

    def test_complete_packet(self):
        hsm = RfxcomPacketHsm()
        hsm.on_data('\x08')
        hsm.on_data('\x03')
        hsm.on_data('\x04')
        hsm.on_data('\x05')
        self.assertEqual(hsm.state_data, hsm.current_state)
        hsm.on_data('\x06')
        hsm.on_data('\x06')
        hsm.on_data('\x06')
        hsm.on_data('\x06')
        hsm.on_data('\x06')
        self.assertEqual(hsm.state_length, hsm.current_state)
        packet = hsm.get_packet()
        self.assertEqual('\x08\x03\x04\x05\x06\x06\x06\x06\x06', packet)

        packet = hsm.get_packet()
        self.assertIsNone(packet)

    def test_receive_several_packets(self):
        hsm = RfxcomPacketHsm()
        i=0
        while i<5:
            hsm.on_data('\x08')
            hsm.on_data('\x03')
            hsm.on_data('\x04')
            hsm.on_data('\x05')
            hsm.on_data('\x06')
            hsm.on_data('\x06')
            hsm.on_data('\x06')
            hsm.on_data('\x06')
            hsm.on_data('\x06')
            packet = hsm.get_packet()
            self.assertEqual('\x08\x03\x04\x05\x06\x06\x06\x06\x06', packet)
            i+= 1


