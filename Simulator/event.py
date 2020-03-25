class Event(object):
    def __init__(self, send_to, message):
        self._send_to = send_to
        self._message = message

