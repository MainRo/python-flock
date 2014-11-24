from unittest import TestCase
from mock import patch, call
from flock.roster import FlockController, FlockRoster

class FlockRosterTestCase(TestCase):
    def setUp(self):
        FlockRoster.roster_instance = None

    def test_instantiate(self):
        roster1 = FlockRoster.instantiate()
        roster2 = FlockRoster.instantiate()
        self.assertIs(roster1, roster2)

    def test_attach_before_start(self):
        roster = FlockRoster.instantiate()
        controller = FlockController()
        self.assertEqual(0, roster.attach(controller))

    def test_attach_after_start(self):
        roster = FlockRoster.instantiate()
        roster.start()
        controller = FlockController()
        self.assertEqual(-1, roster.attach(controller))

    def test_detach_before_start(self):
        roster = FlockRoster.instantiate()
        controller = FlockController()
        roster.attach(controller)
        self.assertEqual(0, roster.detach(controller))

    def test_detach_after_start(self):
        roster = FlockRoster.instantiate()
        controller = FlockController()
        roster.attach(controller)
        roster.start()
        self.assertEqual(-1, roster.detach(controller))

    def test_detach_after_several_start(self):
        roster = FlockRoster.instantiate()
        controller = FlockController()
        roster.attach(controller)
        roster.start()
        roster.stop()
        roster.start()
        roster.stop()
        roster.start()
        self.assertEqual(-1, roster.detach(controller))


    def test_multiple_start(self):
        roster = FlockRoster.instantiate()
        self.assertEqual(0, roster.start())
        self.assertEqual(-1, roster.start())
        self.assertEqual(-1, roster.start())
        self.assertEqual(-1, roster.start())

    def test_stop_not_started(self):
        roster = FlockRoster.instantiate()
        self.assertEqual(-1, roster.stop())

    """
    @patch.object(FlockController, 'start')
    def test_start(self, test_start):
        roster = FlockRoster.instantiate()
        controller = FlockController()
        roster.attach(controller)
        self.assertEqual(0, roster.start())
        test_start.assert_called_with('foo')
    """


