from unittest import TestCase
from mock import MagicMock, patch

from twisted.internet import reactor, defer
from flock.handler.rfxcom.rfy import RfyHandler
from flock.message import FlockMessage

class RfyHandlerTestCase(TestCase):
    ''' tests for rfxcom rfy handler (alias somfy rts).
        @todo : test several pairing, add checks on roster device creation.
    '''

    def test_pair(self):
        d = defer.Deferred()
        handler = RfyHandler(reactor)
        handler.send_packet = MagicMock(return_value = d)

        message = FlockMessage()
        message.namespace = 'controller:rts'
        message.type = FlockMessage.Type.pair

        pair_defer = handler.invoke(message)
        self.assertEqual(d, pair_defer)
        return

