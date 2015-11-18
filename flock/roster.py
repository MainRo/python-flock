import random
import string
import json
import os.path

from twisted.internet import reactor, defer

class Device(object):
    def __init__(self, **kwargs):
        """ Creates a new device with the provided attributes. Mandatory
            attributes:
            - protocol : a string representing the protocol
            - protocol_id :

        """
        if 'repr' in kwargs:
            self.uid = kwargs['repr']['uid']
            self.protocol = kwargs['repr']['protocol']
            self.protocol_id = kwargs['repr']['protocol_id']
            self.features= kwargs['repr']['features']
            self.private= kwargs['repr']['private']
        else:
            self.uid = None
            self.protocol = str(kwargs['protocol'])
            self.protocol_id = kwargs['protocol_id']
            self.features = []
            self.private = {}

    def set_features(self, *args):
        """ Sets the list of features supported by the device. Parameters are
            strings representing supported features. Available features are:
            - temperature
            - humidity
            - power_switch
        """
        for arg in args:
            self.features.append(arg)

        return self

    def set_private(self, private):
        """ Sets the private data of the device. private is a dict.
        """
        self.private = private
        return self

    def __repr__(self):
        ret = '{'
        if self.uid != None:
            ret += '\'uid\':\'' + self.uid + '\','
        else:
            ret += '\'uid\':\'None\','
        ret += '\'protocol\':\'' + self.protocol + '\','
        ret += '\'protocol_id\':\'' + str(self.protocol_id) + '\','
        ret += '\'features\':' + repr(self.features) + ','
        ret += '\'private\':' + repr(self.private)
        ret += '}'
        return ret

class Roster(object):
    roster_instance = None

    def __init__(self, file=None):
        """ Creates a new device roster. A path to the roster save path can be
            provided. The default path is '~/.flock_roster'
        """
        if file == None:
            self._file = os.path.expanduser('~') + '/.flock_roster'
        else:
            self._file = file
        self._device_dict = {}
        self._load()
        return

    @staticmethod
    def instantiate(filepath = None):
        """ Returns the singleton instance of the device roster. Always use
            this method to get the reference to the roster.
        """
        if Roster.roster_instance == None:
            Roster.roster_instance = Roster(filepath)
        return Roster.roster_instance

    def add_device(self, device):
        """ Adds a device to the roster. Return 0 if success, None otherwise.
        """
        uid = self._get_id()
        if uid is None:
            return None

        device.uid = uid
        self._device_dict[uid] = device

        return self._save()

    def del_device(self, uid):
        """ Removes a device from the roster.
        """
        self._device_dict.pop(uid, None)

    def get_device(self, id, protocol = None):
        """ Returns the device matching the provided id or None if the id is
            not valid. If only an id is provided, then it is a device uid. If a
            protocol is also provided then the id is the protocol id.
        """
        if protocol == None:
            if id in self._device_dict:
                return self._device_dict[id]
        else:
            for key in self._device_dict:
                device = self._device_dict[key]
                if device.protocol == protocol and device.protocol_id == id:
                    return device
        return None

    def get_device_list(self):
        list = []
        for key in self._device_dict:
            list.append(self._device_dict[key])
        return list

    def _get_id(self):
        i = 30
        while i > 0:
            id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
            if not id in self._device_dict:
                return id
            i-=1
        return None

    def _save(self):
        json_list = json.dumps(self.get_device_list(),
                default=lambda o: o.__dict__,
                sort_keys=True,
                indent=4,
                separators=(',', ': '))
        f = open(self._file, 'w+')
        f.write(json_list)
        f.close()
        d = defer.Deferred()
        reactor.callLater(0, d.callback, 0)
        return d

    def _load(self):
        if os.path.isfile(self._file) == False:
            return
        f = open(self._file, 'r')
        json_list = f.read()
        f.close()
        if json_list != '':
            devices = json.loads(json_list)
            for repr in devices:
                device = Device(repr=repr)
                self._device_dict[device.uid] = device

