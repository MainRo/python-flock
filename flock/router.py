import logging

class Controller(object):
    def __init__(self, path, protocol_name, protocol):
        self.path = path
        self.protocol_name = protocol_name
        self.protocol = protocol

class Router(object):
    router_instance = None

    def __init__(self):
        """ Constructor. Never instantiate a controller router directly : Use
            the instantiate method instead.
        """
        self.started = False
        self.controllers = []
        self.frontends = []
        return

    @staticmethod
    def instantiate():
        """ Returns the singleton instance of the controller router. Always use
            this method to get the reference to the controller router.
        """
        if Router.router_instance == None:
            Router.router_instance = Router()
        return Router.router_instance

    def attach_controller(self, controller):
        """ Add a controller to the router. The router must be stopped to call
            this method.
            returns 0 if success, -1 otherwise
        """
        if self.started == True:
            return -1
        self.controllers.append(controller)
        logging.debug("attached controller " + controller.path)
        return 0

    def detach_controller(self, path):
        return

    def detach_controller(self, controller):
        """ Removes a controller from the router. The router must be stopped to
            call this method.
            returns 0 if success, -1 otherwise
        """
        if self.started == True:
            return -1
        self.controllers.remove(controller)
        logging.debug("detached controller " + controller.path)
        return 0

    def attach_frontend(self, frontend):
        """ Add a frontend to the router. The router must be stopped to call
            this method.
            returns 0 if success, -1 otherwise
        """
        if self.started == True:
            return -1
        self.frontends.append(frontend)
        logging.debug("attached frontend")
        return 0

    def detach_frontend(self, frontend):
        """ Removes a frontend from the router. The router must be stopped to
            call this method.
            returns 0 if success, -1 otherwise
        """
        if self.started == True:
            return -1
        self.frontends.remove(frontend)
        logging.debug("detached frontend")
        return 0

    def send_report(self, message):
        """ Send a report to all frontends.
        """
        for frontend in self.frontends:
            frontend.report_received(message)

    def send_message(self, message):
        """ Send a message to the first controller that suppports the message
            protocol.
        """
        for controller in self.controllers:
            if controller.protocol_name == message.protocol:
                controller.protocol.send_message(message)
                break
