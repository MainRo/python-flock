import logging
import json
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols import amp
from twisted.internet.endpoints import TCP4ServerEndpoint
from flock.roster import FlockRoster
from flock.message import FlockMessage


# client API
class MessageReceived(amp.Command):
    arguments = [('message', amp.String())]
    response = [('status', amp.Boolean())]

class SetState(amp.Command):
    arguments = [('message', amp.String())]
    response = [('status', amp.Boolean())]


class FlockServer(amp.AMP):
    def connectionMade(self):
        roster = FlockRoster.instantiate()
        roster.attach_frontend(self)
        logging.debug("connected")

    def connectionLost(self, reason):
        roster = FlockRoster.instantiate()
        roster.detach_frontend(self)
        logging.debug("disconnected")

    @SetState.responder
    def set_state(self, message):
        logging.debug("set_state" + message)
        message = json.loads(message)
        action = FlockMessage()
        action.device_id = message['id']
        action.protocol = message['protocol']
        action.private_data = message['private_data']
        action.attributes[FlockMessage.MSG_ATTRIBUTE_SWITCH_BISTATE] = message['state']
        roster = FlockRoster.instantiate()
        roster.send_message(action)
        return {'status': True}

    def report_received(self, message):
        """
            Sends the received message to the endpoint serialized as javascript.
            @todo flatten message as AMP fields.
        """
        json_message = json.dumps(message, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        self.callRemote(MessageReceived, message=json_message)
        return

class FlockServerFactory(Factory):
    def buildProtocol(self, addr):
        return FlockServer()

class Frontend(object):
    def __init__(self, port, reactor):
        endpoint = TCP4ServerEndpoint(reactor, port, interface='localhost')
        endpoint.listen(FlockServerFactory())

