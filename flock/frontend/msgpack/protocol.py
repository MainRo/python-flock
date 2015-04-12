from twisted.internet.protocol import Protocol

class MsgPackProtocol(Protocol):
    """ MsgPackProtocol is the base protocol for transerfing MsgPack buffers
        other a transport. The transmission protocol is the following:
        - 32 bits big endian unsinged integer : synchronization pattern
        - 32 bits big endian unsigned integer : message lenght
        - the message payload
    """


    def dataReceived(self, data):
        return

    def msg_received(self, message):
        """ Called each time a complete MsgPack object has been received.
            This method must be overriden by inherited classes.
        """
        return

    def send_msg(self, message)
