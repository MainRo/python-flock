import logging

RFXCOM_TYPE = 1
RFXCOM_SUBTYPE = 2
RFXCOM_ID1 = 4
RFXCOM_ID2 = 5

class Packet(object):
    """ Rfxcom packet parsing """

    class Command(object):
        """ Generic enum for usual commands
        """
        pair = 0
        set  = 0


    class Type(object):
        lighting2 = 0x11
        rfy = 0x1A
        temperature = 0x50
        temperature_humidity = 0x52

    def __init__(self):
        self.type = None
        self.command = None
        self.id = None
        self.unit_code = None
        self.is_valid = False
        return

    def load_id_ac(self, packet):
        id1 = (ord(packet[4]) >> 6) & 0x3
        id2 = ord(packet[5])
        id3 = ord(packet[6])
        id4 = ord(packet[7])
        self.id = id1 << 24
        self.id += id2 << 16
        self.id += id3 << 8
        self.id += id4

    def dump_id_ac(self, packet):
        id = self.id
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
        self.unit_code = ord(packet[8])
        self.attr_state = state
        self.is_valid = True
        return

    def temperature_loader(self, packet):
        self.id = ord(packet[RFXCOM_ID1]) << 8
        self.id += ord(packet[RFXCOM_ID2])
        sign = (ord(packet[6]) & 0x80) >> 7
        if sign == 1:
            sign = -1
        else:
            sign = 1
        temperature = (ord(packet[6]) & 0x7f) << 8
        temperature += ord(packet[7])
        temperature = float(temperature) / 10
        temperature *= sign
        self.attr_temperature = temperature
        self.is_valid = True
        return

    def temperature_humidity_loader(self, packet):
        self.temperature_loader(packet)
        humidity = ord(packet[8])
        self.attr_humidity = humidity
        self.is_valid = True
        return

    def lighting2_dumper(self, packet):
        state = 0x00
        if self.attr_state == True:
            state = 0x01
        packet += chr(11) # length
        packet += chr(0x11) # type
        packet += chr(0x00) # subtype
        packet += chr(0x00) # sequence number
        packet = self.dump_id_ac(packet)
        packet += chr(self.unit_code) # unit code
        packet += chr(state) # cmd
        if self.attr_state == True: # level
            packet += chr(0x0F)
        else:
            packet += chr(0x00)
        packet += chr(0x00) # filler + rssi
        return packet

    def rfy_dumper(self, packet):
        packet += chr(12) # length
        packet += chr(Packet.Type.rfy) # type
        packet += chr(0x00) # subtype
        packet += chr(0x00) # sequence number
        packet += chr(self.id >> 16 & 0xF) # id1
        packet += chr(self.id >> 8 & 0xFF) # id2
        packet += chr(self.id & 0xFF) # id3
        packet += chr(0x01) # unit code
        if self.command == self.Command.pair:
            packet += chr(0x07)
        else:
            return None
        packet += chr(0x00) # rfu1
        packet += chr(0x00) # rfu2
        packet += chr(0x00) # rfu3
        packet += chr(0x00) # filler + rssi
        return packet

    loaders = {
        0x11 : lighting2_loader,
        0x50 : temperature_loader,
        0x52 : temperature_humidity_loader
    }

    dumpers = {
        Type.lighting2  : lighting2_dumper,
        Type.rfy        : rfy_dumper
    }

    def load(self, packet):
        """ Loads and parses the packet to initialize the message.
        """
        self.type = ord(packet[RFXCOM_TYPE])
        if self.type in Packet.loaders.keys():
            Packet.loaders[self.type](self, packet)

    def dump(self):
        packet = ''
        if self.type in Packet.dumpers.keys():
            return Packet.dumpers[self.type](self, packet)

        return None


