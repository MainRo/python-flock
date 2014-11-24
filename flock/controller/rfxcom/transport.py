from twisted.internet.serialport import SerialPort


class RfxcomTransport(SerialPort):
    def __init__(self, protocol, deviceNameOrPortNumber, reactor):
        super(RfxcomTransport, self).__init__(protocol, deviceNameOrPortNumber,
            reactor, baudrate='38400')
