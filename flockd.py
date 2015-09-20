#! /usr/bin/python

import logging
import os.path
import argparse

from twisted.internet import reactor
from twisted.internet.protocol import Protocol

from flock.roster import Roster

from flock.controller_factory import ControllerFactory
from flock.controller.rfxcom.protocol import RfxcomProtocol
from flock.controller.rfxcom.transport import RfxcomTransport
from flock.controller.enocean.protocol import EnoceanProtocol
from flock.controller.enocean.transport import EnoceanTransport

from flock.frontend.amp import Frontend
from flock.frontend.msgpack.server import FlockMsgServer


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='configuration file')
    parser.add_argument('-v', '--verbose', help='verbose level', nargs='?', default=0)
    parser.add_argument('-p', '--port', help="tcp frontend server port", default=7109)
    args = parser.parse_args()

    if args.verbose == '1':
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbose == '2':
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.CRITICAL)

    Roster.instantiate(args.config)
    factory = ControllerFactory(reactor)
    frontend = Frontend(args.port, reactor)
    msgpack_frontend = FlockMsgServer()
    reactor.run()
