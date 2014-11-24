import logging
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from flock.protocol import FlockProtocol
from flock.hsm import Hsm, HsmState
from flock.controller.rfxcom.message import RfxcomMessage

RESET_PACKET = '\x0D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
STATUS_PACKET = '\x0D\x00\x00\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00'
MODE_PACKET = '\x0D\x00\x00\x01\x03\x53\x00\x00\x0E\x2F\x00\x00\x00\x00'

class RfxcomPacketHsm(Hsm):
    """ This state machine processes incoming data to build full rfxcom packets.
       The structure of a packet is the following:
       length | type | subtype | sequence number | data

       Length is the length of the following fields.
    """
    class BaseState(HsmState):
        def on_data(self, hsm, data):
            return self

    class LengthState(BaseState):
        def on_data(self, hsm, data):
            hsm.data = ''
            hsm.data += data
            hsm.size_left = ord(data)
            if hsm.size_left <= 0: # Error on data, drop packet
                return self
            return hsm.state_type

    class TypeState(BaseState):
        def on_data(self, hsm, data):
            hsm.data += data
            hsm.size_left = hsm.size_left - 1
            if hsm.size_left == 0:
                hsm.packet = hsm.data
                return hsm.state_length
            return hsm.state_subtype

    class SubTypeState(BaseState):
        def on_data(self, hsm, data):
            hsm.data += data
            hsm.size_left = hsm.size_left - 1
            if hsm.size_left == 0:
                hsm.packet = hsm.data
                return hsm.state_length
            return hsm.state_sequence

    class SequenceState(BaseState):
        def on_data(self, hsm, data):
            hsm.data += data
            hsm.size_left = hsm.size_left - 1
            if hsm.size_left == 0:
                hsm.packet = hsm.data
                return hsm.state_length
            return hsm.state_data

    class DataState(BaseState):
        def on_data(self, hsm, data):
            hsm.data += data
            hsm.size_left = hsm.size_left - 1
            if hsm.size_left == 0:
                hsm.packet = hsm.data
                return hsm.state_length
            return self

    def __init__(self):
        super(RfxcomPacketHsm, self).__init__()
        self.packet = None
        self.data = None
        self.size_left = 0

        self.state_length = RfxcomPacketHsm.LengthState()
        self.state_type = RfxcomPacketHsm.TypeState()
        self.state_subtype = RfxcomPacketHsm.SubTypeState()
        self.state_sequence = RfxcomPacketHsm.SequenceState()
        self.state_data = RfxcomPacketHsm.DataState()
        self.transition(self.state_length)

    def get_packet(self):
        packet = self.packet
        self.packet = None
        return packet

    def on_data(self, data):
        """ New data is received data is a single byte provided as a character
        """
        return self.dispatch(self.current_state.on_data, data)

class RfxcomReceiver(FlockProtocol):
    def __init__(self):
        FlockProtocol.__init__(self)
        self.__hsm = None

    def connectionMade(self):
        """ Resets the controller.
        """
        if self.__hsm != None:
            self.__hsm = None
        self.__hsm = RfxcomPacketHsm()

    def byte_received(self, data):
        if self.__hsm == None:
            return

        self.__hsm.on_data(data)
        packet = self.__hsm.get_packet()
        if packet != None:
            message = self.packet_received(packet)
            if message != None:
                return message
        return None

    def packet_received(self, data):
        """ Processes a packet received from the controller.
            This method must be overriden by inherited classes to process the
            packet.
        """
        return


class RfxcomHsm(Hsm):

    @staticmethod
    def make_timer1(self):
        def do_timer1(arg):
            self.timer1()
        return do_timer1


    class BaseState(HsmState):
        def process_packet(self, hsm, packet):
            return self

        def on_timer1(self, hsm):
            return self

    class SendResetState(BaseState):
        def on_entry(self, hsm, old_state):
            hsm.protocol.transport.flushInput()
            hsm.protocol.transport.write(RESET_PACKET)
            reactor.callLater(0.1, RfxcomHsm.make_timer1(hsm.protocol), None)
            return

        def on_timer1(self, hsm):
            hsm.protocol.transport.write(STATUS_PACKET)
            return hsm.state_wait_reset_status

    class WaitResetStatusState(BaseState):
        def process_packet(self, hsm, packet):
            # todo ensure that packet is STATUS ack
            hsm.protocol.transport.write(MODE_PACKET)
            return hsm.state_running

    class RunningState(BaseState):
        def process_packet(self, hsm, packet):
            logging.debug(packet.encode('hex'))
            message = RfxcomMessage()
            message.load(packet)
            logging.info(message)
            hsm.protocol.push_message(message)
            return self

    def __init__(self, protocol):
        super(RfxcomHsm, self).__init__()
        self.protocol = protocol

        self.state_send_reset = RfxcomHsm.SendResetState()
        self.state_wait_reset_status = RfxcomHsm.WaitResetStatusState()
        self.state_running = RfxcomHsm.RunningState()
        self.transition(self.state_send_reset)

    def process_packet(self, packet):
        return self.dispatch(self.current_state.process_packet, packet)

    def on_timer1(self):
        return self.dispatch(self.current_state.on_timer1)


class RfxcomProtocol(RfxcomReceiver):
    def __init__(self):
        RfxcomReceiver.__init__(self)
        self.__hsm = None

    def connectionMade(self):
        """ Resets the controller.
        """
        RfxcomReceiver.connectionMade(self)
        if self.__hsm != None:
            self.__hsm = None
        self.__hsm = RfxcomHsm(self)

    def timer1(self):
        self.__hsm.on_timer1()

    def packet_received(self, data):
        self.__hsm.process_packet(data)

