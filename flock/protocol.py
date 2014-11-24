from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from collections import deque

from flock.frontend import Frontend

class FlockProtocol(Protocol):
    """ The FlockProtocol class is the base class for all Smart Home controllers.
        A FlockProtocol translates FlockMessage object to/from a specific
        controller.
    """

    def __init__(self):
        self.frontend = None

    def dataReceived(self, data):
        """ Process some data received on the controller to process them. This
            base implementation forward each byte to the byte_received.
            Inherited classes must either overload this method if they can
            process multiple bytes at once, or overload byte_received.
            Received messages must be pushed to the protocol queue by calling
            the push_message method.
        """
        count = len(data)
        i = 0
        while i < count:
            self.byte_received(data[i])
            i += 1

    def byte_received(self, data):
        """ Processes a byte received from the controller.
            This method must be overriden by inherited classes to process the
            data byte per byte.
            Received messages must be pushed to the protocol queue by calling
            the push_message method.
        """
        return None

    def set_frontend(self, frontend):
        self.frontend = frontend

    def push_message(self, message):
        """ Pushes a message to the message list.
        """
        if self.frontend != None:
            self.frontend.message_received(message)

