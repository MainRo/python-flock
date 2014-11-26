import logging
import json
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols import amp
from twisted.internet.endpoints import TCP4ServerEndpoint
from flock.roster import FlockRoster


# client API
class MessageReceived(amp.Command):
    arguments = [('message', amp.String())]
    response = [('status', amp.Boolean())]

class FlockClient(amp.AMP):
    @MessageReceived.responder
    def message_received(self, message):
        return

class FlockServer(amp.AMP):
    def connectionMade(self):
        roster = FlockRoster.instantiate()
        roster.attach_frontend(self)
        logging.debug("connected")

    def connectionLost(self, reason):
        roster = FlockRoster.instantiate()
        roster.detach_frontend(self)
        logging.debug("disconnected")

    def report_received(self, message):
        """ Sends the received message to the endpoint serialized as javascript.
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

