class FlockMessage(object):
    """ A FlockMessage identifies the data received from a device or a command to
        send.
        This class must be overloaded. Overloaded classes must implement a load
        and a dump method to respectively load a message from a packet or
        generate a packet from a message.
    """

    class Type(object):
        # controller messages
        report = 0
        set  = 1
        pair = 2
        # system messages

    MSG_TYPE_REPORT = 0
    MSG_TYPE_ACTION = 1

    """ Celcius degree temperature (float). """
    MSG_ATTRIBUTE_TEMPERATURE = 0
    """ Humidity in percent (int). """
    MSG_ATTRIBUTE_HUMIDITY = 1
    """ switch state (boolean) """
    MSG_ATTRIBUTE_SWITCH_BISTATE= 2

    def __init__(self):
        self.reset()

    def reset(self):
        self.type = None
        self.uid = None
        self.device = None
        self.namespace = None

        # obsolete fields. @todo : remove
        self.attributes = {}

    def __eq__(self, other):
        if isinstance(other, FlockMessage):
            return self.type == other.type and \
                    self.uid == other.uid and \
                    self.device == other.device and \
                    self.namespace == other.namespace
        return NotImplemented

    def __str__(self):
        result  = "type: " + str(self.type) + ","
        result += "uid: " + self.uid+ ","
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


