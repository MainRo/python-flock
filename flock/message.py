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

    def __init__(self):
        """
        """
        self.reset()

    def reset(self):
        self.type = None
        self.device_id = None   # string containing the protocol unique id of the device.
        self.protocol = None    # communication protocol used.
        self.attributes = {}
        self.valid = False

    def set_valid(self, state):
        self.valid = state

    def is_valid(self):
        return self.valid

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


