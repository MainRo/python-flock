
class FlockController(object):
    def __init__(self):
        return

    def start(self):
        return

    def stop(self):
        return

class FlockRoster(object):
    roster_instance = None

    def __init__(self):
        """ Constructor. Never instantiate a controller roster directly : Use
            the instantiate method instead.
        """
        self.started = False
        self.controllers = []
        return

    @staticmethod
    def instantiate():
        """ Returns the singleton instance of the controller roster. Always use
            this method to get the reference to the controller roster.
        """
        if FlockRoster.roster_instance == None:
            FlockRoster.roster_instance = FlockRoster()
        return FlockRoster.roster_instance

    def start(self):
        """ Start all controllers present in the roster.
        """
        if self.started == True:
            return -1

        for controller in self.controllers:
            controller.start()

        self.started = True
        return 0

    def stop(self):
        """ Stops all controllers present in the roster.
        """
        if self.started == False:
            return -1

        for controller in self.controllers:
            controller.stop()

        self.started = False
        return 0

    def attach(self, controller):
        """ Add a controller to the roster. The roster must be stopped to call
            this method.
            returns 0 if success, -1 otherwise
        """
        if self.started == True:
            return -1
        self.controllers.append(controller)
        return 0

    def detach(self, controller):
        """ Removes a controller from the roster. The roster must be stopped to
            call this method.
            returns 0 if success, -1 otherwise
        """
        if self.started == True:
            return -1
        self.controllers.remove(controller)
        return 0
