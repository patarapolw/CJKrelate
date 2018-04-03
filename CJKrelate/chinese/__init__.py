import os
import yaml

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
        all_chars = []
        with open(os.path.join(ROOT, 'database', 'chinese', 'frequency', 'junda.txt')) as f:
            for row in f:
                contents = row.split('\t')
                all_chars.append((contents[1], int(contents[2])))

        all_count = sum([x[1] for x in all_chars])
        self.entries = dict()
        self.entries['junda'] = [['all', all_count, 1]]
        for char_pair in all_chars:
            self.entries['junda'].append([char_pair[0], char_pair[1], char_pair[1]/all_count])

        super().__init__()


class Sort(AbstractSort):
    def __init__(self, font: str=None, freq_limit=5000):
        if font is None:
            font = os.path.join(ROOT, 'font', 'NotoSansCJKtc-Regular.otf')
        super().__init__(font=font, frequency=Frequency(), freq_limit=freq_limit)


if __name__ == '__main__':
    print(Frequency().relative_freq('好'))
