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
            d.addCallback(self.__on_pair_completed, unit_id)
        else:
            d = defer.Deferred()
            self.reactor.callLater(0, d.errback, -1)

        return d

    def __generate_unit_id(self):
        unit_id = 1
        retry_count = 30 # rfxcom supports up to 30 remotes
        while retry_count > 0:
            if self.roster.get_device(unit_id, 'rfxcom:rfy') == None:
                return unit_id
            retry_count-=1
            unit_id += 1
        return None

    def __add_device(self, unit_id):
        ''' adds a new device to the roster.
        '''
        device = Device(protocol='rfxcom:rfy', protocol_id=unit_id)
        device.set_private({'type': Packet.Type.rfy, 'unit_code': 1})
        if self.roster.add_device(device) == None:
            raise RuntimeError('unable to add device to roster')
        return device

    def __on_pair_completed(self, packet, unit_id):
        device = self.__add_device(unit_id)
        message = FlockMessage()
        message.uid = device.uid
        message.namespace = 'controller:rts'
        message.type = FlockMessage.Type.pair_reply
        return message



