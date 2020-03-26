class Event(object):
    def __init__(self, send_to, message):
        self.send_to = send_to
        self.message = message

    def get_message(self):
        return self.message

    def get_send_to(self):
        return self.send_to

