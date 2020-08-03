import ctypes

_win_api = ctypes.windll.user32


class WindowCatcher:
    visible_windows = []
    hidden_windows = []

    IGNORED = ('Default', 'MSCTFIME')

    def _foreach_window(self, hwnd, _):
        length = _win_api.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        _win_api.GetWindowTextW(hwnd, buff, length + 1)
        name = buff.value
        if name and _win_api.IsWindowVisible(hwnd):
            self.visible_windows.append(name)
        elif name and not name.startswith(self.IGNORED):
            self.hidden_windows.append(name)

    def collect(self):
        enum_windows_proc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int),
                                               ctypes.POINTER(ctypes.c_int))
        _win_api.EnumWindows(enum_windows_proc(self._foreach_window), 0)
        return set(self.visible_windows), set(self.hidden_windows)


def main():
    wc = WindowCatcher()
    print(wc.collect())


if __name__ == "__main__":
    main()
