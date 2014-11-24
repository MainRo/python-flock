import logging
import json
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols import amp
from twisted.internet.endpoints import TCP4ServerEndpoint

# server API

# client API
class MessageReceived(amp.Command):
    arguments = [('message', amp.String())]
    response = [('status', amp.Boolean())]

class FlockClient(amp.AMP):
    @MessageReceived.responder
    def message_received(self, message):
        return

class FlockServer(amp.AMP):
    """
    def makeConnection(self, transport):
        logging.debug("connected")

    def connectionLost(self, reason):
        logging.debug("disconnected")
    """

    def message_received(self, message):
        """ Sends the received message to the endpoint serialized as javascript.
        """
        json_message = json.dumps(message, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        self.callRemote(MessageReceived, message=json_message)
        return

class FlockServerFactory(Factory):
    def __init__(self, frontend):
        self.frontend = frontend

    def buildProtocol(self, addr):
        server = FlockServer()
        self.frontend.set_server(server)
        return server


class Frontend(object):
    def __init__(self, port, reactor):
        self.server = None
        endpoint = TCP4ServerEndpoint(reactor, port, interface='localhost')
        endpoint.listen(FlockServerFactory(self))

    def set_server(self, server):
        self.server = server

    def message_received(self, message):
        if self.server != None:
            self.server.message_received(message)
        return
