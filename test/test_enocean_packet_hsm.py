from unittest import TestCase
from flock.controller.enocean.protocol import EnoceanPacketHsm

class EnoceanPacketHsmTestCase(TestCase):
    def test_init(self):
        hsm = EnoceanPacketHsm()
        self.assertEqual(hsm.state_sync, hsm.current_state)
        self.assertIsNone(hsm.get_packet())

    def test_sync(self):
        hsm = EnoceanPacketHsm()
        hsm.on_data('\x55')
        self.assertEqual(hsm.state_header, hsm.current_state)
        self.assertIsNone(hsm.get_packet())

    def test_sync_lock(self):
        hsm = EnoceanPacketHsm()
        # invalid sync packets must be dropped
        hsm.on_data('\x50')
        self.assertEqual(hsm.state_sync, hsm.current_state)
        hsm.on_data('\x51')
        self.assertEqual(hsm.state_sync, hsm.current_state)
        hsm.on_data('\x52')
        self.assertEqual(hsm.state_sync, hsm.current_state)

        # and sync packet must match
        hsm.on_data('\x55')
        self.assertEqual(hsm.state_header, hsm.current_state)
        self.assertIsNone(hsm.get_packet())

    def test_header(self):
        # go to header state
        hsm = EnoceanPacketHsm()
        hsm.on_data('\x55')
        self.assertEqual(hsm.state_header, hsm.current_state)

        hsm.on_data('\x02')
        hsm.on_data('\x05')
        hsm.on_data('\x07')
        hsm.on_data('\x08')
        self.assertEqual(hsm.state_crc_header, hsm.current_state)

    def test_crc_header(self):
        # go to header state
        hsm = EnoceanPacketHsm()
        hsm.on_data('\x55')
        hsm.on_data('\x02')
        hsm.on_data('\x05')
        hsm.on_data('\x07')
        hsm.on_data('\x08')
        self.assertEqual(hsm.state_crc_header, hsm.current_state)

        hsm.on_data('\x42')
        self.assertEqual(hsm.state_data, hsm.current_state)

    def test_crc_header_no_optional(self):
        """ packet with no optional data
        """
        # go to header state
        hsm = EnoceanPacketHsm()
        hsm.on_data('\x55')
        hsm.on_data('\x00') # size MSB
        hsm.on_data('\x02') # size LSB
        hsm.on_data('\x00') # optional size
        hsm.on_data('\x08')
        self.assertEqual(hsm.state_crc_header, hsm.current_state)

        hsm.on_data('\x42')
        self.assertEqual(hsm.state_data, hsm.current_state)


    def test_crc_header_no_data(self):
        """ packet with no data but optional data
        """
        # go to header state
        hsm = EnoceanPacketHsm()
        hsm.on_data('\x55')
        hsm.on_data('\x00') # size MSB
        hsm.on_data('\x00') # size LSB
        hsm.on_data('\x07')
        hsm.on_data('\x08')
        self.assertEqual(hsm.state_crc_header, hsm.current_state)

        hsm.on_data('\x42')
        self.assertEqual(hsm.state_optional_data, hsm.current_state)

    def test_crc_header_no_data_no_optional(self):
        """ packet with no data and no optional data
        """
        # go to header state
        hsm = EnoceanPacketHsm()
        hsm.on_data('\x55')
        hsm.on_data('\x00') # size MSB
        hsm.on_data('\x00') # size LSB
        hsm.on_data('\x00') # optional size
        hsm.on_data('\x08')
        self.assertEqual(hsm.state_crc_header, hsm.current_state)

        hsm.on_data('\x42')
        self.assertEqual(hsm.state_crc_data, hsm.current_state)


    def test_data(self):
        # go to header state
        hsm = EnoceanPacketHsm()
        hsm.on_data('\x55')
        hsm.on_data('\x00') # size MSB
        hsm.on_data('\x02') # size LSB
        hsm.on_data('\x07')
        hsm.on_data('\x08')
        hsm.on_data('\x42')
        self.assertEqual(hsm.state_data, hsm.current_state)

        hsm.on_data('\x01')
        hsm.on_data('\x02')
        self.assertEqual(hsm.state_optional_data, hsm.current_state)

    def test_optional_data(self):
        # initialize
        hsm = EnoceanPacketHsm()
        hsm.on_data('\x55')
        hsm.on_data('\x00') # size MSB
        hsm.on_data('\x02') # size LSB
        hsm.on_data('\x01') # optional size
        hsm.on_data('\x08')
        hsm.on_data('\x42')
        hsm.on_data('\x01')
        hsm.on_data('\x02')
        self.assertEqual(hsm.state_optional_data, hsm.current_state)

        hsm.on_data('\x03')
        self.assertEqual(hsm.state_crc_data, hsm.current_state)

    def test_crc_data(self):
        # initialize
        hsm = EnoceanPacketHsm()
        hsm.on_data('\x55')
        hsm.on_data('\x00') # size MSB
        hsm.on_data('\x02') # size LSB
        hsm.on_data('\x01') # optional size
        hsm.on_data('\x08')
        hsm.on_data('\x42')
        hsm.on_data('\x01')
        hsm.on_data('\x02')
        hsm.on_data('\x03')
        self.assertEqual(hsm.state_crc_data, hsm.current_state)

        hsm.on_data('\x42')
        self.assertEqual(hsm.state_sync, hsm.current_state)

    def test_data_packet(self):
        # initialize
        data = '\x55\x00\x02\x01\x08\x42\x01\x02\x03\x42'
        hsm = EnoceanPacketHsm()
        for byte in data:
            hsm.on_data(byte)
        self.assertEqual(hsm.state_sync, hsm.current_state)
        packet = hsm.get_packet()
        self.assertEqual(ord(data[4]), packet['type'])
        self.assertEqual(data[6:8], packet['data'])
        self.assertEqual(data[8:9], packet['optional_data'])

    def test_packet_no_optional(self):
        # initialize
        data = '\x55\x00\x02\x00\x08\x42\x01\x02\x42'
        hsm = EnoceanPacketHsm()
        for byte in data:
            hsm.on_data(byte)
        self.assertEqual(hsm.state_sync, hsm.current_state)
        packet = hsm.get_packet()
        self.assertEqual(ord(data[4]), packet['type'])
        self.assertEqual(data[6:8], packet['data'])
        self.assertEqual('', packet['optional_data'])


    def test_packet_empty(self):
        """ Packet with no data and no optional data
        """
        data = '\x55\x00\x00\x00\x08\x42\x42'
        hsm = EnoceanPacketHsm()
        for byte in data:
            hsm.on_data(byte)
        self.assertEqual(hsm.state_sync, hsm.current_state)
        packet = hsm.get_packet()
        self.assertEqual(ord(data[4]), packet['type'])
        self.assertEqual('', packet['data'])
        self.assertEqual('', packet['optional_data'])

