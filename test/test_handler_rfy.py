from unittest import TestCase
from twisted.internet import reactor, defer
from flock.handler.rfxcom.rfy import RfyHandler
from flock.roster import Roster

class TestController(object):
    def __init__(self, d):
        self.d = d

    def send_packet(self, packet):
        return self.d

class RfyHandlerTestCase(TestCase):
    def test_pair(self):
        d = defer.Deferred()
        controller = TestController(d)
        roster = Roster()
        handler = RfyHandler(reactor, controller, roster)
        pair_defer = handler.pair()
        self.assertEqual(d, pair_defer)
        return

