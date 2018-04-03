from time import time


class SpeedTest:
    def __init__(self, testName):
        self.funcName = testName

    def __enter__(self):
        print('Started: {}'.format(self.funcName))
        self.init_time = time()
        return self

    def __exit__(self, type, value, tb):
        print('Finished: {} in: {:.4f} seconds'.format(self.funcName, time() - self.init_time))


def speed_wrapper(func):
    def wrapper(*args, **kwargs):
        with SpeedTest(func.__qualname__):
            return func(*args, **kwargs)
    return wrapper
