from twisted.internet import defer
from flock.controller.rfxcom.packet import Packet
from flock.controller.rfxcom.protocol import RfxcomProtocol
from flock.router import Router
from flock.roster import Roster, Device
from flock.message import FlockMessage

class RfxcomHandler(RfxcomProtocol):
    """ Rfy handler is the rfxcom somfy rts handler. It contains the specific
        pairing code for this protocol.
    """
    def __init__(self, reactor):
        RfxcomProtocol.__init__(self)
        self.roster = Roster.instantiate()
        self.router = Router.instantiate()
        self.reactor = reactor

    def invoke(self, device, message):
        if message.namespace == 'controller' and device.protocol == 'rfxcom':
            if message.type == FlockMessage.Type.set:
                return self.__set(device, message)
        return None

    def __set(self, device, message):
        packet = self._message_to_packet(device, message)
        d = self.send_packet(packet.dump())
        d.addCallback(self._packet_to_message)
        return d

    def publish_packet(self, packet):
        self.router.publish(self._packet_to_message(packet))
        return

    def _packet_to_message(self, packet):
        """ Converts an rfxcom packet to a message
        """
        if packet == None:
            return None

        device = self.roster.get_device(packet.id, 'rfxcom')
        if device == None:
            device = Device(protocol='rfxcom', protocol_id=packet.id)
            device.set_private({'type': packet.type, 'unit_code': packet.unit_code})
            if hasattr(packet, 'attr_temperature'):
                device.set_features('temperature')
            self.roster.add_device(device)

        message = FlockMessage()
        if hasattr(packet, 'attr_temperature'):
            message.attributes[FlockMessage.MSG_ATTRIBUTE_TEMPERATURE] = packet.attr_temperature
        message.uid = device.uid
        message.namespace = 'controller'
        message.type = FlockMessage.Type.report
        return message

    def _message_to_packet(self, device, message):
        packet = Packet()
        packet.type = device.private['type']
        packet.unit_code = device.private['unit_code']
        packet.id = device.protocol_id
        packet.command = Packet.Command.set
        return packet

