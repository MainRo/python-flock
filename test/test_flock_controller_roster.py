from unittest import TestCase
from mock import patch, call
from flock.controller_roster import FlockController, FlockControllerRoster

class FlockControllerRosterTestCase(TestCase):
    def setUp(self):
        FlockControllerRoster.roster_instance = None

    def test_instantiate(self):
        roster1 = FlockControllerRoster.instantiate()
        roster2 = FlockControllerRoster.instantiate()
        self.assertIs(roster1, roster2)

    def test_attach_before_start(self):
        roster = FlockControllerRoster.instantiate()
        controller = FlockController()
        self.assertEqual(0, roster.attach(controller))

    def test_attach_after_start(self):
        roster = FlockControllerRoster.instantiate()
        roster.start()
        controller = FlockController()
        self.assertEqual(-1, roster.attach(controller))

    def test_detach_before_start(self):
        roster = FlockControllerRoster.instantiate()
        controller = FlockController()
        roster.attach(controller)
        self.assertEqual(0, roster.detach(controller))

    def test_detach_after_start(self):
        roster = FlockControllerRoster.instantiate()
        controller = FlockController()
        roster.attach(controller)
        roster.start()
        self.assertEqual(-1, roster.detach(controller))

    def test_detach_after_several_start(self):
        roster = FlockControllerRoster.instantiate()
        controller = FlockController()
        roster.attach(controller)
        roster.start()
        roster.stop()
        roster.start()
        roster.stop()
        roster.start()
        self.assertEqual(-1, roster.detach(controller))


    def test_multiple_start(self):
        roster = FlockControllerRoster.instantiate()
        self.assertEqual(0, roster.start())
        self.assertEqual(-1, roster.start())
        self.assertEqual(-1, roster.start())
        self.assertEqual(-1, roster.start())

    def test_stop_not_started(self):
        roster = FlockControllerRoster.instantiate()
        self.assertEqual(-1, roster.stop())

    """
    @patch.object(FlockController, 'start')
    def test_start(self, test_start):
        roster = FlockControllerRoster.instantiate()
        controller = FlockController()
        roster.attach(controller)
        self.assertEqual(0, roster.start())
        test_start.assert_called_with('foo')
    """


