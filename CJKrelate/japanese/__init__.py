import os
import yaml
import json

from CJKrelate import Related as Rel
from CJKrelate.dir import ROOT
from CJKrelate.sort import AbstractSort
from CJKrelate.frequency import AbstractFrequency


class Related(Rel):
    def __init__(self, font: str=None, freq_limit=5000):
        """
        font: path to font file
        """
        super().__init__(sorter=Sort(font=font, freq_limit=freq_limit))


class RelatedHuman:
    def __init__(self):
        with open(os.path.join(ROOT, 'database', 'chinese', 'human.yaml')) as f:
            self.entries = yaml.safe_load(f)

    def get(self, hanzi):
        return self.entries.get(hanzi, [])


class Frequency(AbstractFrequency):
    def __init__(self):
        self.entries = dict()
        sources = ['aozora.json', 'news.json', 'twitter.json', 'wikipedia.json']
        for source in sources:
            with open(os.path.join(ROOT, 'database', 'japanese', 'frequency', source)) as f:
                self.entries[os.path.splitext(source)[0]] = json.load(f)

        super().__init__()


class Sort(AbstractSort):
    def __init__(self, font: str=None, freq_limit=5000):
        if font is None:
            font = os.path.join(ROOT, 'font', 'NotoSansCJKjp-Regular.otf')
        super().__init__(font=font, frequency=Frequency(), freq_limit=freq_limit)


if __name__ == '__main__':
    from test import SpeedTest

    with SpeedTest('__init__'):
        # 0.04 sec
        f = Frequency()

    with SpeedTest('merge_sources'):
        # merge_sources in: 0.1360 seconds
        print(dict(f.listing('好')))
