import atexit

OUTPUT_FILE = 'logger.txt'


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
    # TODO: rewrite to use as caching when offline, and use webhandler when the machine has internet again

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
