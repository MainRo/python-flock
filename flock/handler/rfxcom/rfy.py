from flock.controller.rfxcom.packet import Packet
from twisted.internet import defer

class RfyHandler(object):
    """ Rfy handler is the rfxcom somfy rts handler. It contains the specific
        pairing code for this protocol.
    """
    def __init__(self, reactor, controller, roster):
        self.controller = controller
        self.roster = roster
        self.reactor = reactor

    def invoke(self, device, message):
        return

    def pair(self):
        """ Generates a new unit id and send a rts pairing command. Returns a deferred.
        """
        d = None
        unit_id = self._generate_unit_id()
        if unit_id != None:
            packet = Packet()
            packet.id = unit_id
            packet.type = Packet.Type.rfy
            packet.command = Packet.Command.pair
            d = self.controller.send_packet(packet.dump())
            d.addCallback(self._packet_to_message)
        else:
            d = defer.Deferred()
            self.reactor.callLater(0, d.errback, -1)

        return d

    def _generate_unit_id(self):
        unit_id = 1
        retry_count = 30 # rfxcom supports up to 30 remotes
        while retry_count > 0:
            if self.roster.get_device(unit_id, 'rfxcom:rfy') == None:
                return unit_id
            retry_count-=1
        return None

    def _packet_to_message(self, packet):
        return 0
