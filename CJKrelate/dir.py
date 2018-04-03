import os
import inspect

ROOT = os.path.abspath(os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename))


if __name__ == '__main__':
    print(ROOT)
