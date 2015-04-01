from twisted.internet import defer
from flock.controller.enocean.packet import Packet
from flock.controller.enocean.protocol import EnoceanProtocol
from flock.router import Router
from flock.roster import Roster, Device
from flock.message import FlockMessage

class EnoceanHandler(EnoceanProtocol):
    """ Enocean handler
    """
    def __init__(self, reactor):
        EnoceanProtocol.__init__(self)
        self.roster = Roster.instantiate()
        self.router = Router.instantiate()
        self.reactor = reactor

    def invoke(self, device, message):
        return None

    def publish_packet(self, packet):
        self.router.publish(self._packet_to_message(packet))
        return

    def _packet_to_message(self, packet):
        """ Converts an enocean packet to a message
        """
        device = self.roster.get_device(packet.id, 'encoean')
        if device == None:
            device = Device(protocol='enocean', protocol_id=packet.id)
            if hasattr(packet, 'attr_temperature'):
                device.set_features('temperature')
            self.roster.add_device(device)

        message = FlockMessage()
        if hasattr(packet, 'attr_temperature'):
            message.attributes[FlockMessage.MSG_ATTRIBUTE_TEMPERATURE] = packet.attr_temperature
        message.uid = device.uid
        message.namespace = 'controller'

        return message
