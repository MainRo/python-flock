from unittest import TestCase
from flock.roster import Device

class DeviceTestCase(TestCase):
    def test_instantiate(self):
        device = Device(protocol_id='4242', protocol='test')
        self.assertEqual('4242', device.protocol_id)
        self.assertEqual('test', device.protocol)
        self.assertEqual([], device.features)
        self.assertIsNone(device.uid)
        self.assertEqual({}, device.private)
        self.assertEqual([], device.features)

    def test_non_str_attributes(self):
        device = Device(protocol_id=4242, protocol=27)
        self.assertEqual(4242, device.protocol_id)
        self.assertEqual('27', device.protocol)

    def test_features(self):
        device = Device(protocol_id='4242', protocol='test')
        device.set_features('one', 'two', 'three')
        self.assertEqual('one', device.features[0])
        self.assertEqual('two', device.features[1])
        self.assertEqual('three', device.features[2])

    def test_private(self):
        device = Device(protocol_id='4242', protocol='test')
        private = {'p1' : 'one', 'p2': 18}
        device.set_private(private)
        self.assertEqual(private, device.private)
