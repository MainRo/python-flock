import copy
from twisted.internet import defer
from flock.handler.rfxcom.rfxcom import RfxcomHandler
from flock.controller.rfxcom.packet import Packet
from flock.roster import Roster, Device
from flock.message import FlockMessage

class RfyHandler(RfxcomHandler):
    """ Rfy handler is the rfxcom somfy rts handler. It contains the specific
        pairing code for this protocol.
    """
    def __init__(self, reactor):
        RfxcomHandler.__init__(self, reactor)
        self.roster = Roster.instantiate()
        self.reactor = reactor

    def invoke(self, message):
        if message.namespace == 'controller:rts':
            if message.type == FlockMessage.Type.pair:
                    return self.__pair()

        return RfxcomHandler.invoke(self, message)

    def __pair(self):
        """ Generates a new unit id and send a rts pairing command. Returns a deferred.
        """
        d = None
        unit_id = self.__generate_unit_id()
        if unit_id != None:
            packet = Packet()
            packet.id = unit_id
            packet.type = Packet.Type.rfy
            packet.command = Packet.Command.pair
            d = self.send_packet(packet.dump())
#            d.addCallback(self._packet_to_message)
        else:
            d = defer.Deferred()
            self.reactor.callLater(0, d.errback, -1)

        return d

    def __generate_unit_id(self):
        unit_id = 1
        retry_count = 30 # rfxcom supports up to 30 remotes
        roster = Roster.instantiate()
        while retry_count > 0:
            if roster.get_device(str(unit_id), 'rfxcom:rfy') == None:
                return unit_id
            retry_count-=1
            unit_id += 1
        return None

    def __packet_to_message(self, packet):
        ''' Converts a pairing notification packet to a message.
            If pairing succeeded, then a new device is created. Otherwise an
            error is returned to errback.
        '''
        if packet == None:
            raise RuntimeError('received packet is None')

        device = Device(protocol='rfxcom:rfy', protocol_id=packet.id)
        device.set_private({'type': packet.type, 'unit_code': 1})
        if self.roster.add_device(device) == None:
            raise RuntimeError('unable to add device to roster')

        message = FlockMessage()
        message.uid = device.uid
        message.namespace = 'controller:rts'
        message.type = FlockMessage.Type.pair_reply
        return message

