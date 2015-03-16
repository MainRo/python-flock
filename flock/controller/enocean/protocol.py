import logging
from flock.hsm import Hsm, HsmState
from flock.protocol import FlockProtocol
from flock.controller.enocean.packet import Packet


class EnoceanPacketHsm(Hsm):
    class BaseState(HsmState):
        def on_data(self, hsm, data):
            return self

    class SyncState(BaseState):
        def on_data(self, hsm, data):
            if ord(data) == 0x55:
                hsm.data = ''
                hsm.optional_data = ''
                hsm.packet_type = None
                return hsm.state_header
            return self

    class HeaderState(BaseState):
        def on_entry(self, hsm, old_state):
            self.size_left = 4
            self.data = ''

        def on_data(self, hsm, data):
            self.data += data
            self.size_left = self.size_left -1
            if self.size_left == 0:
                hsm.data_length = (ord(self.data[0]) << 8) + ord(self.data[1])
                hsm.optional_data_length = ord(self.data[2])
                hsm.packet_type = ord(self.data[3])
                return hsm.state_crc_header
            return self

    class CrcHeaderState(BaseState):
        def on_data(self, hsm, data):
            if hsm.data_length != 0:
                return hsm.state_data
            elif hsm.optional_data_length != 0:
                return hsm.state_optional_data
            return hsm.state_crc_data

    class DataState(BaseState):
        def on_entry(self, hsm, old_state):
            self.size_left = hsm.data_length

        def on_data(self, hsm, data):
            hsm.data += data
            self.size_left = self.size_left -1
            if self.size_left == 0:
                if hsm.optional_data_length != 0:
                    return hsm.state_optional_data
                else:
                    return hsm.state_crc_data
            return self

    class OptionalDataState(BaseState):
        def on_entry(self, hsm, old_state):
            self.size_left = hsm.optional_data_length

        def on_data(self, hsm, data):
            hsm.optional_data += data
            self.size_left = self.size_left -1
            if self.size_left == 0:
                return hsm.state_crc_data
            return self

    class CrcDataState(BaseState):
        def on_data(self, hsm, data):
            hsm.packet = { 'data':hsm.data,
                'optional_data':hsm.optional_data,
                'type': hsm.packet_type}
            return hsm.state_sync

    def __init__(self):
        super(EnoceanPacketHsm, self).__init__()
        self.packet = None
        self.packet_type = None
        self.data = None
        self.optional_data = None
        self.data_length = 0
        self.optional_data_length = 0

        self.state_sync = EnoceanPacketHsm.SyncState()
        self.state_header = EnoceanPacketHsm.HeaderState()
        self.state_crc_header = EnoceanPacketHsm.CrcHeaderState()
        self.state_data = EnoceanPacketHsm.DataState()
        self.state_optional_data = EnoceanPacketHsm.OptionalDataState()
        self.state_crc_data = EnoceanPacketHsm.CrcDataState()
        self.transition(self.state_sync)

    def get_packet(self):
        """ Pops the current complete packet if available, None otherwise.
        """
        packet = self.packet
        self.packet = None
        return packet

    def on_data(self, data):
        """ New data is received data is a single byte provided as a character
        """
        return self.dispatch(self.current_state.on_data, data)

class EnoceanReceiver(FlockProtocol):
    def __init__(self):
        FlockProtocol.__init__(self)
        self.__hsm = None

    def connectionMade(self):
        """ Resets the controller.
        """
        if self.__hsm != None:
            self.__hsm = None
        self.__hsm = EnoceanPacketHsm()

    def byte_received(self, data):
        if self.__hsm == None:
            return

        self.__hsm.on_data(data)
        packet = self.__hsm.get_packet()
        if packet != None:
            message = self.packet_received(packet['type'], packet['data'], packet['optional_data'])
            if message != None:
                return message
        return None

    def packet_received(self, type, data, optional_data):
        """ Processes a packet received from the controller.
            This method must be overriden by inherited classes to process the
            packet.
        """
        return

class EnoceanProtocol(EnoceanReceiver):
    def __init__(self):
        EnoceanReceiver.__init__(self)

    def packet_received(self, type, data, optional_data):
        packet = Packet()
        packet.load(type, data, optional_data)
        logging.info(packet)
        if packet.is_valid == True:
            self.publish_packet(packet)
        else:
            logging.warning('received invalid packet. type: ' + str(type) +
                    'data: ' + data + 'optional_data: ' + optional_data)



