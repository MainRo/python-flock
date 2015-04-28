#! /usr/bin/python

from optparse import OptionParser
import logging
import os.path

from twisted.internet import reactor
from twisted.internet.protocol import Protocol

from flock.controller_factory import ControllerFactory
from flock.controller.rfxcom.protocol import RfxcomProtocol
from flock.controller.rfxcom.transport import RfxcomTransport
from flock.controller.enocean.protocol import EnoceanProtocol
from flock.controller.enocean.transport import EnoceanTransport

from flock.frontend.amp import Frontend
from flock.frontend.msgpack.server import FlockMsgServer


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

    factory = ControllerFactory(reactor)
    frontend = Frontend(options.port, reactor)
    msgpack_frontend = FlockMsgServer()
    reactor.run()
