import logging
from flock.message import FlockMessage

ENOCEAN_TYPE = 1

class Packet(object):
    def __init__(self):
        self.id = '-'
        self.is_valid = False
        return

    def temperature_loader(self, data, optional_data):
        subtype = ord(data[2])
        temperature = ord(data[3])
        valid = False
        if subtype == 5 or subtype == 0 :
            temperature = float(255 - temperature)
            temperature = temperature * 40.0 / 255.0
            valid = True

        if valid == True:
            temperature = round(temperature, 1)
            self.attr_temperature = temperature
            self.is_valid = True

    def four_byte_loader(self, data, optional_data):
        func = ord(data[1]) & 0x3F
        if func in Packet.FUNC_LOADERS.keys():
            Packet.FUNC_LOADERS[func](self, data, optional_data)


    def radio_loader(self, data, optional_data):
        if len(data) < 5: # radio message have rorg + 4 byte data
            return
        rorg = ord(data[0])
        if rorg in Packet.RORG_LOADERS.keys():
            Packet.RORG_LOADERS[rorg](self, data, optional_data)


    PACKET_TYPE_RADIO = 1
    PACKET_TYPE_RESPONSE = 2
    PACKET_TYPE_RADIO_SUB_TEL = 3
    PACKET_TYPE_EVENT = 4
    PACKET_TYPE_COMMON_COMMAND = 5
    PACKET_TYPE_SMART_ACK_COMMAND = 6
    PACKET_TYPE_REMOTE_MAN_COMMAND = 7
    PACKET_TYPE_RADIO_MESSAGE = 9
    PACKET_TYPE_RADIO_ADVANCED = 10
    TYPE_LOADERS = {
        PACKET_TYPE_RADIO : radio_loader
    }

    RORG_4BS = 0xA5
    RORG_LOADERS = {
        RORG_4BS : four_byte_loader
    }

    FUNC_TEMPERATURE_DEFAULT = 0X00
    FUNC_TEMPERATURE_SENSOR = 0X02
    FUNC_LOADERS = {
        FUNC_TEMPERATURE_DEFAULT : temperature_loader,
        FUNC_TEMPERATURE_SENSOR : temperature_loader
    }


    def load(self, type, data, optional_data):
        """ Loads and parses the packet to initialize the message.
        """
        if type in Packet.TYPE_LOADERS.keys():
            Packet.TYPE_LOADERS[type](self, data, optional_data)


