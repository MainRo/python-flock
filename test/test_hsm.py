from unittest import TestCase
from mock import patch, call
from flock.hsm import Hsm, HsmState


class TestHsm(Hsm):
    class BaseState(HsmState):
        def on_data(self, hsm, data):
            return self

    class State1(BaseState):
        def on_data(self, hsm, data):
            hsm.data = "State1" + data
            return hsm.state1_1

    class State1_1(BaseState):
        def on_data(self, hsm, data):
            hsm.data = "State1_1" + data
            return self

    def __init__(self):
        super(TestHsm, self).__init__()
        self.state1 = TestHsm.State1()
        self.state1_1 = TestHsm.State1_1()
        self.data = None
        self.transition(self.state1)

    def on_data(self, data):
        return self.dispatch(self.current_state.on_data, data)


class HsmTestCase(TestCase):
    def test_init(self):
        test_hsm = TestHsm()
        self.assertIs(test_hsm.state1, test_hsm.current_state)

    def test_dispatch_one(self):
        test_hsm = TestHsm()
        test_hsm.on_data("one")
        self.assertEqual("State1one", test_hsm.data)
        self.assertIs(test_hsm.state1_1, test_hsm.current_state)

    def test_dispatch_two(self):
        test_hsm = TestHsm()
        test_hsm.on_data("one")
        test_hsm.on_data("two")
        self.assertEqual("State1_1two", test_hsm.data)
        self.assertIs(test_hsm.state1_1, test_hsm.current_state)

