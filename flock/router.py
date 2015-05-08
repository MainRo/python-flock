import logging
from flock.roster import Roster

class Router(object):
    router_instance = None

    def __init__(self):
        """ Constructor. Never instantiate a controller router directly : Use
            the instantiate method instead.
        """
        self.started = False
        self.handlers = []
        self.frontends = []
        return

    @staticmethod
    def instantiate():
        """ Returns the singleton instance of the message router. Always use
            this method to get the reference to the router.
        """
        if Router.router_instance == None:
            Router.router_instance = Router()
        return Router.router_instance

    def attach_handler(self, handler):
        """ Add a handler to the router. The router must be stopped to call
            this method.
            returns 0 if success, -1 otherwise
        """
        if self.started == True:
            return -1
        self.handlers.append(handler)
        logging.debug("attached handler" + str(handler))
        return 0

    def detach_handler(self, handler):
        """ Removes a handler from the router. The router must be stopped to
            call this method.
            returns 0 if success, -1 otherwise
        """
        if self.started == True:
            return -1
        self.handlers.remove(handler)
        logging.debug("detached handler" + str(handler))
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

    def publish(self, message):
        """ publish a message to all frontends.
        """

        logging.debug('publishing message' + str(message))
        for frontend in self.frontends:
            frontend.event(message)

    def call(self, message):
        """ route a message to the appropriate handler.
            Returns a deferred if the message is routed.
            Returns None otherwise.
        """
        roster = Roster.instantiate()
        device = roster.get_device(message.uid)
        message.device = device

        for handler in self.handlers:
            d = handler.invoke(message)
            if d != None:
                return d

        return None

