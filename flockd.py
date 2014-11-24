#! /usr/bin/python

from optparse import OptionParser
import logging
import os.path

from twisted.internet import reactor
from twisted.internet.protocol import Protocol

from flock.controller.rfxcom.protocol import RfxcomProtocol
from flock.controller.rfxcom.transport import RfxcomTransport
from flock.controller.enocean.protocol import EnoceanProtocol
from flock.controller.enocean.transport import EnoceanTransport

from flock.frontend import Frontend


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-v", "--verbose", dest="verbose", default=0,
            help="verbose level 0-2")
    parser.add_option("-w", "--http", dest="http", default=None,
            help="http frontend server url")
    parser.add_option("-p", "--port", dest="port", default=7109,
            help="tcp frontend server port")

    (options, args) = parser.parse_args()

    if options.verbose == '1':
        logging.getLogger().setLevel(logging.INFO)
    elif options.verbose == '2':
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.CRITICAL)

    frontend = Frontend(options.port, reactor)
    rfxcom = RfxcomProtocol()
    rfxcom.set_frontend(frontend)

    enocean = EnoceanProtocol()
    enocean.set_frontend(frontend)

    if os.path.isfile('/dev/serial/by-id/usb-RFXCOM_RFXtrx433_A1XR4Q78-if00-port0'):
        RfxcomTransport(rfxcom, '/dev/serial/by-id/usb-RFXCOM_RFXtrx433_A1XR4Q78-if00-port0', reactor)
    if os.path.isfile('/dev/serial/by-id/usb-EnOcean_GmbH_EnOcean_USB_300_DA_FTVJ66M0-if00-port0'):
        EnoceanTransport(enocean,'/dev/serial/by-id/usb-EnOcean_GmbH_EnOcean_USB_300_DA_FTVJ66M0-if00-port0', reactor)
    if os.path.isfile('/dev/serial/by-id/usb-EnOcean_GmbH_EnOcean_USB_300_DA_FTWTOMA2-if00-port0'):
        EnoceanTransport(enocean,'/dev/serial/by-id/usb-EnOcean_GmbH_EnOcean_USB_300_DA_FTWTOMA2-if00-port0', reactor)
    reactor.run()
