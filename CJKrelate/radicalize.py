import os
import re

from CJKrelate.dir import ROOT


class Krad:
    def __init__(self, databases=None):
        if databases is None:
            databases = [os.path.join(ROOT, 'database', 'kradzip', item)
                         for item in ['kradfile', 'kradfile2']]

        self.entries = dict()
        for database in databases:
            for k, v in self._load(database):
                self.entries[k] = v

    @staticmethod
    def _load(database):
        with open(database, encoding='euc-jp') as f:
            for row in f:
                _ = re.match(r'(\w) : (.*)', row)
                if _ is not None:
                    char, radicals = _.groups()
                    yield char, re.findall(r'\w', radicals)

    def get(self, character):
        return self.entries.get(character, [])

    def similar(self, character, distance=0):
        set1 = set(self.get(character))
        for k, list2 in self.entries.items():
            if len(set1.symmetric_difference(list2)) <= distance:
                yield k


if __name__ == '__main__':
    print(list(Krad().similar('日')))
