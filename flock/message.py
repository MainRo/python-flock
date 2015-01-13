class FlockMessage(object):
    """ A FlockMessage identifies the data received from a device or a command to
        send.
        This class must be overloaded. Overloaded classes must implement a load
        and a dump method to respectively load a message from a packet or
        generate a packet from a message.
    """
    MSG_TYPE_REPORT = 0
    MSG_TYPE_ACTION = 1

    """ Celcius degree temperature (float). """
    MSG_ATTRIBUTE_TEMPERATURE = 0
    """ Humidity in percent (int). """
    MSG_ATTRIBUTE_HUMIDITY = 1
    """ switch state (boolean) """
    MSG_ATTRIBUTE_SWITCH_BISTATE= 2

    def __init__(self, message = None):
        self.reset()
        if message != None:
            self.__init_from(message)

    def reset(self):
        self.type = None
        self.device_id = None   # string containing the protocol unique id of the device.
        self.protocol = None    # communication protocol used.
        self.attributes = {}
        self.private_data = None
        self.__valid = False

    def __init_from(self, message):
        self.type = message.type
        self.device_id = message.device_id
        self.protocol = message.protocol
        self.private_data = message.private_data
        self.set_valid(message.is_valid())
        self.attributes = message.attributes.copy()

    def set_valid(self, state):
        self.__valid = state

    def is_valid(self):
        return self.__valid

    def __str__(self):
        result  = "type: " + str(self.type) + ","
        result += "device_id: " + self.device_id + ","
        result += "protocol: " + self.protocol + ","
        result += "attributes : ["
        first = True
        for key, value in self.attributes.iteritems():
            if first == False:
               result += ","
            else:
               first = False
            result += str(key) + " : " + str(value) + ""
        result += "]"
        return result


