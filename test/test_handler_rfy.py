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


    @patch('flock.handler.rfxcom.rfy.Roster')
    def test_pair_many(self, mock_roster):
        roster = MagicMock()
        roster.get_device = MagicMock()
        roster.get_device.side_effect = [ None, {}, None, {}, {}, None ]
        mock_roster.instantiate = MagicMock(return_value=roster)

        d = defer.Deferred()
        handler = RfyHandler(reactor)
        handler.send_packet = MagicMock(return_value = d)

        message = FlockMessage()
        message.namespace = 'controller:rts'
        message.type = FlockMessage.Type.pair

        handler.invoke(message)
        handler.invoke(message)
        handler.invoke(message)

        self.assertEqual(3, handler.send_packet.call_count)
        args_list = handler.send_packet.call_args_list
        i=0
        while i < 3:
            args, kwargs = args_list[i]
            actual_id = ord(args[0][6])
            self.assertEqual(i+1, actual_id)
            i += 1

    @patch.object(reactor, 'callLater')
    @patch('flock.handler.rfxcom.rfy.Roster')
    def test_pair_too_many(self, mock_roster, mock_call_later):
        roster = MagicMock()
        roster.get_device = MagicMock()
        roster.get_device.side_effect = [ {}, {}, {}, {}, {}, {}, {}, {},{}, {},
         {}, {}, {}, {}, {}, {}, {}, {},{}, {},
         {}, {}, {}, {}, {}, {}, {}, {},{}, {}]
        mock_roster.instantiate = MagicMock(return_value=roster)

        handler = RfyHandler(reactor)
        handler.send_packet = MagicMock()

        message = FlockMessage()
        message.namespace = 'controller:rts'
        message.type = FlockMessage.Type.pair
        d = handler.invoke(message)

        self.assertEqual(0, handler.send_packet.call_count)
        mock_call_later.assert_called_once_with(0, d.errback, -1)

