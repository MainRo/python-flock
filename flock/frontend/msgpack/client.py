from __future__ import print_function

from twisted.internet import defer, reactor
from txmsgpackrpc.client import connect_UNIX


class FlockMsgClient(object):
    def __init__(self,):
        self._connection = None
        self._actions = []
        d = connect_UNIX('/tmp/rpc-flock-sock', connectTimeout=5)
        d.addCallback(self._connected)
        d.addErrback(self._on_error)

    def monitor(self, state):
        d = defer.Deferred()
        self._actions.append((self._monitor_request, d))
        return d

    def set(self, uid, attribute, value):
        d = defer.Deferred()
        self._actions.append((self._set_request, (d, uid, attribute, value)))
        return d

    def pair(self, protocol):
        d = defer.Deferred()
        self._actions.append((self._pair_request, (d, protocol)))
        return d

    def list_device(self):
        d = defer.Deferred()
        self._actions.append((self._list_device_request, d))
        return d

    def _connected(self, result):
        print("connected")
        self._connection = result
        for action in self._actions:
            params = action[1]
            if isinstance(params, tuple):
                action[0](*params)
            else:
                action[0](params)
        self._actions = []

    def _on_error(self, result):
        print("Error : " + str(result))
        reactor.stop()

    def _on_state_change(self, topic, data):
        print('topic: ' + topic + ' data: ' + str(data))

    def _monitor_request(self, d1):
        d = self._connection.createSubscribe('report', self._on_state_change)
        d.addErrback(self._on_error)
        d.addCallback(d1.callback)

    def _set_request(self, d1, uid, attribute, value):
        d = self._connection.createRequest('set', uid, attribute, value)
        d.addErrback(self._on_error)
        d.addCallback(d1.callback)

    def _pair_request(self, d1, protocol):
        d = self._connection.createRequest('pair', protocol)
        d.addErrback(self._on_error)
        d.addCallback(d1.callback)

    def _list_device_request(self, d1):
        d = self._connection.createRequest('list')
        d.addErrback(self._on_error)
        d.addCallback(d1.callback)
