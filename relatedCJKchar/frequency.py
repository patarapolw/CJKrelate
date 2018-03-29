import os
import json
import math

from relatedCJKchar.dir import ROOT


class Frequency:
    def __init__(self, lang='cn'):
        self.freq = ''
        self.count = []
        if lang.lower() in ['cn', 'chinese', 'hanzi']:
            with open(os.path.join(ROOT, 'database', 'frequency', 'hanzi', 'junda.txt')) as f:
                for row in f:
                    contents = row.split('\t')
                    self.freq += contents[1]
                    self.count.append(int(contents[2]))
        else:
            with open(os.path.join(ROOT, 'database', 'frequency', 'kanji', 'news.json')) as f:
                for i, row in enumerate(json.load(f)):
                    if i != 0:
                        self.freq += row[0]
                        self.count.append(row[1])

    def relative_freq(self, char):
        try:
            return math.log(math.e * self.count[self.freq.index(char)])
        except ValueError:
            return 0

    def listing(self, char):
        try:
            return self.freq.index(char)
        except ValueError:
            return -1
