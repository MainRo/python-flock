from flock.message import FlockMessage

RFXCOM_TYPE = 1
RFXCOM_SUBTYPE = 2
RFXCOM_ID1 = 4
RFXCOM_ID2 = 5

class RfxcomMessage(FlockMessage):
    def temperature_loader(self, packet):
        temperature = (ord(packet[6]) & 0xef) << 8
        temperature += ord(packet[7])
        temperature = float(temperature) / 10
        self.attributes[FlockMessage.MSG_ATTRIBUTE_TEMPERATURE] = temperature
        return

    def temperature_humidity_loader(self, packet):
        self.temperature_loader(packet)
        humidity = ord(packet[8])
        self.attributes[FlockMessage.MSG_ATTRIBUTE_HUMIDITY] = humidity
        return

    RFXCOM_TYPE_LOADERS = {
        0x50 : temperature_loader,
        0x52: temperature_humidity_loader
    }


    def load(self, packet):
        """ Loads and parses the packet to initialize the message.
        """
        self.reset()
        self.type = FlockMessage.MSG_TYPE_REPORT
        self.protocol = "rfxcom"
        self.device_id = packet[RFXCOM_ID1].encode('hex') + packet[RFXCOM_ID2].encode('hex')
        packet_type = ord(packet[RFXCOM_TYPE])
        if packet_type in RfxcomMessage.RFXCOM_TYPE_LOADERS.keys():
            RfxcomMessage.RFXCOM_TYPE_LOADERS[packet_type](self, packet)

    def dump(self):
        return

