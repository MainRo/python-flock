from unittest import TestCase
from mock import patch, call, ANY
import tempfile
import os
import json
from flock.roster import Roster, Device
from twisted.internet import reactor

class RosterTestCase(TestCase):
    def test_instantiate(self):
        roster = Roster()
        self.assertEqual('~/.flock_roster', roster._file)

        roster = Roster('foo')
        self.assertEqual('foo', roster._file)

    def test_add_device(self):
        fd,file = tempfile.mkstemp()
        os.close(fd)
        roster = Roster(file)
        device = Device(protocol_id='4242', protocol='test')
        self.assertIsNotNone(roster.add_device(device))

        list = roster.get_device_list()
        self.assertEqual(1, len(list))
        self.assertEqual(device, list[0])


        os.remove(file)

    @patch.object(reactor, 'callLater')
    def test_add_devices(self, mock_called_later):
        fd,file = tempfile.mkstemp()
        os.close(fd)
        roster = Roster(file)
        device1 = Device(protocol_id='4242', protocol='test')
        device2 = Device(protocol_id='4242', protocol='test')
        device3 = Device(protocol_id='4242', protocol='test')
        d1 = roster.add_device(device1)
        self.assertIsNotNone(d1)
        mock_called_later.assert_called_with(0, d1.callback, 0)

        d2 = roster.add_device(device2)
        self.assertIsNotNone(d2)
        mock_called_later.assert_called_with(0, d2.callback, 0)

        d3 = roster.add_device(device3)
        self.assertIsNotNone(d3)
        mock_called_later.assert_called_with(0, d3.callback, 0)

        list = roster.get_device_list()
        self.assertEqual(3, len(list))

        os.remove(file)

    def test_del_devices(self):
        fd,file = tempfile.mkstemp()
        os.close(fd)
        roster = Roster(file)
        device1 = Device(protocol_id='1', protocol='test')
        device2 = Device(protocol_id='2', protocol='test')
        roster.add_device(device1)
        roster.add_device(device2)
        roster.del_device(device1.uid)

        list = roster.get_device_list()
        self.assertEqual(1, len(list))
        self.assertEqual(device2, list[0])

        os.remove(file)


    def test_load_file(self):
        json = '[ {"uid":"u1", "protocol":"p1", "protocol_id":"i1", "features":["f1"], "private":{"p1": 1}}, \
                {"uid":"u2", "protocol":"p2", "protocol_id":"i2", "features":["f1", "f2"], "private":{}} \
                ]'
        fd,file = tempfile.mkstemp()
        os.write(fd, json)
        os.close(fd)
        roster = Roster(file)
        list = roster.get_device_list()
        self.assertEqual(2, len(list))

        # find matching devices from the list (order is not garanted)
        device1 = list[0]
        device2 = list[1]
        if device1.uid == 'u2':
            device2 = list[0]
            device1 = list[1]

        self.assertEqual('p1', device1.protocol)
        self.assertEqual('p2', device2.protocol)
        self.assertEqual('i1', device1.protocol_id)
        self.assertEqual('i2', device2.protocol_id)
        self.assertEqual(['f1'], device1.features)
        self.assertEqual(['f1', 'f2'], device2.features)
        self.assertEqual({'p1': 1}, device1.private)
        self.assertEqual({}, device2.private)

        os.remove(file)

    def test_save_file(self):
        fd,file = tempfile.mkstemp()
        os.close(fd)
        roster = Roster(file)
        device1 = Device(protocol_id='i1', protocol='p1')
        device2 = Device(protocol_id='i2', protocol='p2')
        device1.set_features('f1').set_private({'p1': 1})
        device2.set_features('f1', 'f2').set_private({'p2': 2})
        roster.add_device(device1)
        roster.add_device(device2)

        fd = open(file, 'r')
        json_list = fd.read()
        fd.close()
        list = json.loads(json_list)


        self.assertEqual(2, len(list))

        # find matching devices from the list (order is not garanted)
        device1 = list[0]
        device2 = list[1]
        if device1['protocol'] == 'p2':
            device2 = list[0]
            device1 = list[1]

        self.assertEqual('p1', device1['protocol'])
        self.assertEqual('p2', device2['protocol'])
        self.assertEqual('i1', device1['protocol_id'])
        self.assertEqual('i2', device2['protocol_id'])
        self.assertEqual(['f1'], device1['features'])
        self.assertEqual(['f1', 'f2'], device2['features'])
        self.assertEqual({'p1':1}, device1['private'])
        self.assertEqual({'p2':2}, device2['private'])

        os.remove(file)

    def test_get_device_from_uid(self):
        fd,file = tempfile.mkstemp()
        os.close(fd)
        roster = Roster(file)
        device = Device(protocol_id='4242', protocol='test')
        roster.add_device(device)

        device_get = roster.get_device(device.uid)
        self.assertEqual(device, device_get)
        os.remove(file)

    def test_get_device_from_uid_not_found(self):
        fd,file = tempfile.mkstemp()
        os.close(fd)
        roster = Roster(file)

        self.assertIsNone(roster.get_device('foo'))
        os.remove(file)

    def test_get_device_from_protocol(self):
        fd,file = tempfile.mkstemp()
        os.close(fd)
        roster = Roster(file)
        device = Device(protocol_id='4242', protocol='test')
        roster.add_device(device)

        device_get = roster.get_device('4242', 'test')
        self.assertEqual(device, device_get)
        os.remove(file)

    def test_get_device_from_protocol_not_found(self):
        fd,file = tempfile.mkstemp()
        os.close(fd)
        roster = Roster(file)

        self.assertEqual(None, roster.get_device('4242', 'test'))
        os.remove(file)


