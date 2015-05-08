import os, string

from flock.handler.rfxcom.rfy import RfyHandler
from flock.controller.rfxcom.transport import RfxcomTransport
from flock.handler.enocean import EnoceanHandler
from flock.controller.enocean.transport import EnoceanTransport
from flock.router import Router

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
        handler = None
        if string.find(path, 'RFXCOM_RFXtrx433') >= 0:
            handler = RfyHandler(self.reactor)
            RfxcomTransport(handler, path, self.reactor)
        elif string.find(path, 'EnOcean_GmbH_EnOcean_USB_300') >= 0:
            handler = EnoceanHandler(self.reactor)
            EnoceanTransport(handler, path, self.reactor)

        if handler != None:
            router = Router.instantiate()
            router.attach_handler(handler)

    def controller_removed(self, path):
        router = Router.instantiate()
        router.detach_controller(path)

