import logging
import json
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols import amp
from twisted.internet.endpoints import TCP4ServerEndpoint
from flock.router import Router
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
        router = Router.instantiate()
        router.attach_frontend(self)
        logging.debug("connected")

    def connectionLost(self, reason):
        router = Router.instantiate()
        router.detach_frontend(self)
        logging.debug("disconnected")

    @SetState.responder
    def SetState(self, message):
        logging.debug("set_state" + message)
        message = json.loads(message)
        action = FlockMessage()
        action.uid = message['id']
        action.attributes[FlockMessage.MSG_ATTRIBUTE_SWITCH_BISTATE] = message['state']
        action.type = FlockMessage.Type.set
        action.namespace = 'controller'
        router = Router.instantiate()
        router.call(action)
        return {'status': True}

    def event(self, message):
        """
            Sends the received message to the endpoint serialized as javascript.
            @todo flatten message as AMP fields.
        """
        legacy_message = {}
        legacy_message['protocol'] = 'flock'
        legacy_message['device_id'] = message.uid
        legacy_message['private_data'] = ''
        legacy_message['attributes'] = message.attributes
        json_message = json.dumps(legacy_message, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        self.callRemote(MessageReceived, message=json_message)
        return

class FlockServerFactory(Factory):
    def buildProtocol(self, addr):
        return FlockServer()

class Frontend(object):
    def __init__(self, port, reactor):
        endpoint = TCP4ServerEndpoint(reactor, port, interface='localhost')
        endpoint.listen(FlockServerFactory())

