from __future__ import print_function

from twisted.internet import defer, reactor
from txmsgpackrpc.client import connect_UNIX


class FlockMsgClient(object):
    def __init__(self, monitor = False):
        self.monitor = monitor
        self.connection = None
        d = connect_UNIX('/tmp/rpc-flock-sock', connectTimeout=5)
        d.addCallback(self._connected)
        d.addErrback(self._on_error)

    def _connected(self, result):
        print("connected")
        self.connection = result
        if self.monitor == True:
            d = self.connection.createSubscribe('report', self._on_state_change)
            d.addErrback(self._on_error)

    def _on_error(self, result):
        print("Error : " + str(result))
        reactor.stop()

    def _on_state_change(self, topic, data):
        print('topic: ' + topic + ' data: ' + str(data))
