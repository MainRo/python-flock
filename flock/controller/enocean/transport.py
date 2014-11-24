from twisted.internet.serialport import SerialPort


class EnoceanTransport(SerialPort):
    def __init__(self, protocol, deviceNameOrPortNumber, reactor):
        super(EnoceanTransport, self).__init__(protocol, deviceNameOrPortNumber,
            reactor, baudrate='57600')
