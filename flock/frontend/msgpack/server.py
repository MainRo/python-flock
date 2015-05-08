from twisted.internet import defer, reactor, task
from txmsgpackrpc.server import MsgpackRPCPubServer
from flock.router import Router
from flock.message import FlockMessage


class FlockRPC(MsgpackRPCPubServer):

    def __init__(self):
        super(FlockRPC, self).__init__()
        router = Router.instantiate()
        router.attach_frontend(self)
        print("FlockRpc initialized")

    def event(self, message):
        if message.type == FlockMessage.Type.report:
            self.Publish('report', (message.type,
                        message.namespace,
                        message.uid,
                        message.attributes))

    @defer.inlineCallbacks
    def remote_echo(self, value, delay=None, msgid=None):
        if delay is not None:
            yield task.deferLater(reactor, delay, lambda: None)
        defer.returnValue(value)

    def remote_set(self, uid, attribute, value):
        router = Router.instantiate()
        message = FlockMessage()
        message.type = FlockMessage.Type.set
        message.uid = uid
        message.namespace = 'controller'
        if attribute == 'switch_bistate':
            message.attributes[FlockMessage.MSG_ATTRIBUTE_SWITCH_BISTATE] = value
        d = router.call(message)
        return d

    def remote_pair(self, protocol):
        router = Router.instantiate()
        message = FlockMessage()
        message.type = FlockMessage.Type.pair
        message.namespace = protocol
        d = router.call(message)
        return d


class FlockMsgServer(object):
    def __init__(self):
        server = FlockRPC()
        reactor.listenUNIX('/tmp/rpc-flock-sock', server.getStreamFactory())

