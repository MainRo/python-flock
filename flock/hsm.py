
class HsmState(object):
    def on_entry(self, hsm, old_state):
        return

    def on_exit(self, hsm, new_state):
        return

class Hsm(object):
    def __init__(self):
        self.current_state = None

    def dispatch(self, event, *args):
        """ Dispatches an event to the current state.
            - event is a bounded function to the current state.
            - optional arguments canbe provided in **kwargs
        """
        if(self.current_state != None):
            next_state = event(self, *args)
            if(next_state is not self.current_state):
                self.transition(next_state)
        return self.current_state


    def transition(self, new_state):
        if(self.current_state is new_state):
            return

        if(self.current_state != None):
            self.current_state.on_exit(self, new_state)
        if(new_state != None):
            new_state.on_entry(self, self.current_state)

        self.current_state = new_state
