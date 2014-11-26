import os, string

from flock.controller.rfxcom.protocol import RfxcomProtocol
from flock.controller.rfxcom.transport import RfxcomTransport
from flock.controller.enocean.protocol import EnoceanProtocol
from flock.controller.enocean.transport import EnoceanTransport
from flock.roster import FlockRoster, Controller

class ControllerFactory(object):
    def __init__(self, reactor):
        self.reactor = reactor
        self.cold_plug()

    def cold_plug(self):
        usb_serial_path = '/dev/serial/by-id/'
        if os.path.exists(usb_serial_path):
            usb_controllers = os.listdir(usb_serial_path)
            for controller_path in usb_controllers:
                self.controller_added(usb_serial_path+controller_path)

    def controller_added(self, path):
        controller = None
        if string.find(path, 'RFXCOM_RFXtrx433') >= 0:
            protocol = RfxcomProtocol()
            RfxcomTransport(protocol, path, self.reactor)
            controller = Controller(path, 'rfxcom', protocol)
        elif string.find(path, 'EnOcean_GmbH_EnOcean_USB_300') >= 0:
            protocol = EnoceanProtocol()
            EnoceanTransport(protocol, path, self.reactor)
            controller = Controller(path, 'enocean', protocol)

        if controller != None:
            roster = FlockRoster.instantiate()
            roster.attach_controller(controller)

    def controller_removed(self, path):
        roster = FlockRoster.instantiate()
        roster.detach_controller(path)

