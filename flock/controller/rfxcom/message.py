import logging
from flock.message import FlockMessage

RFXCOM_TYPE = 1
RFXCOM_SUBTYPE = 2
RFXCOM_ID1 = 4
RFXCOM_ID2 = 5

class RfxcomMessage(FlockMessage):
    """ Rfxcom message implementation.
        private data : type (1 byte) + unit code (1 byte)
    """

    def load_id_ac(self, packet):
        '''
            id for the ac protocol is composed of 4 bytes, whose value is
            encoded as a string representing their hex value.
            e.g. : '00112233' for an id of [0x00, 0x11, 0x22, 0x33]
        '''
        id1 = (ord(packet[4]) >> 6) & 0x3
        id2 = ord(packet[5])
        id3 = ord(packet[6])
        id4 = ord(packet[7])
        self.device_id = "{:02X}{:02X}{:02X}{:02X}".format(id1, id2, id3, id4)

    def dump_id_ac(self, packet):
        # @todo : how to parse this a better way ?
        id = int(self.device_id, 16)
        id1 = id >> 24 & 0xFF
        id2 = id >> 16 & 0xFF
        id3 = id >> 8 & 0xFF
        id4 = id & 0xFF
        packet += chr((id1 << 6) & 0xC0)
        packet += chr(id2)
        packet += chr(id3)
        packet += chr(id4)
        return packet

    def lighting2_loader(self, packet):
        state = ord(packet[9])
        if state == 0x00:
            state = False
        elif state == 0x01:
            state = True
        else:
            return

        self.load_id_ac(packet)
#        self.private_data += packet[8]
        self.private_data += "{:02X}".format(ord(packet[8]))
        self.attributes[FlockMessage.MSG_ATTRIBUTE_SWITCH_BISTATE] = state
        self.set_valid(True)
        return

    def temperature_loader(self, packet):
        self.device_id = packet[RFXCOM_ID1].encode('hex') + packet[RFXCOM_ID2].encode('hex')
        sign = (ord(packet[6]) & 0x80) >> 7
        if sign == 1:
            sign = -1
        else:
            sign = 1
        temperature = (ord(packet[6]) & 0x7f) << 8
        temperature += ord(packet[7])
        temperature = float(temperature) / 10
        temperature *= sign
        self.attributes[FlockMessage.MSG_ATTRIBUTE_TEMPERATURE] = temperature
        self.set_valid(True)
        return

    def temperature_humidity_loader(self, packet):
        self.temperature_loader(packet)
        humidity = ord(packet[8])
        self.attributes[FlockMessage.MSG_ATTRIBUTE_HUMIDITY] = humidity
        self.set_valid(True)
        return

    def lighting2_dumper(self, packet):
        state = self.attributes[FlockMessage.MSG_ATTRIBUTE_SWITCH_BISTATE]
        if state == True:
            state = 0x01
        else:
            state = 0x00
        packet += chr(11) # length
        packet += chr(0x11) # type
        packet += chr(0x00) # subtype
        packet += chr(0x00) # sequence number
        packet = self.dump_id_ac(packet)
        packet += chr(int(self.private_data[2:4], 16)) # unit code
        packet += chr(state) # cmd
        if state == True: # level
            packet += chr(0x0F)
        else:
            packet += chr(0x00)
        packet += chr(0x00) # filler + rssi
        return packet

    RFXCOM_TYPE_LOADERS = {
        0x11 : lighting2_loader,
        0x50 : temperature_loader,
        0x52 : temperature_humidity_loader
    }

    RFXCOM_TYPE_DUMPERS = {
        0x11 : lighting2_dumper
    }

    def load(self, packet):
        """ Loads and parses the packet to initialize the message.
        """
        self.reset()
        self.type = FlockMessage.MSG_TYPE_REPORT
        self.protocol = "rfxcom"
        self.device_id = ""
        packet_type = ord(packet[RFXCOM_TYPE])
        self.private_data = "{:02X}".format(packet_type)
        if packet_type in RfxcomMessage.RFXCOM_TYPE_LOADERS.keys():
            RfxcomMessage.RFXCOM_TYPE_LOADERS[packet_type](self, packet)

    def dump(self):
        packet_type = int(self.private_data[0:2], 16)
        packet = ''
        if packet_type in RfxcomMessage.RFXCOM_TYPE_DUMPERS.keys():
            return RfxcomMessage.RFXCOM_TYPE_DUMPERS[packet_type](self, packet)

        return None


