import re
import os

from CJKrelate.dir import ROOT


class Decompose:
    def __init__(self, sorter=None):
        """
        Decompose and super-compose CJK char
        :type sorter: Sort ImageDiff object
        """
        self.entries = dict()
        self.super_entries = dict()
        self.sort = sorter
        with open(os.path.join(ROOT, 'database', 'cjk-decomp.txt')) as f:
            for row in f:
                entry, _, components = re.match('(.+):(.+)\((.*)\)', row).groups()
                comp_list = components.split(',')
                self.entries[entry] = comp_list
                for comp in comp_list:
                    self.super_entries.setdefault(comp, []).append(entry)

    def get_sub(self, char):
        # return self.sort.sort(char, self.entries.get(char, []))  # radicals must not be sorted
        return self.entries.get(char, [])

    def get_super(self, char):
        if self.sort:
            return self.sort.sort(char, self.super_entries.get(char, []))
        else:
            return self.super_entries.get(char, [])

    def similar(self, char):
        result = []
        sub = self.get_sub(char)
        sup = self.get_super(char)
        for item in sub:
            result.extend(self.get_super(item))
        for item in sup:
            result.extend(self.get_sub(item))
        result.extend(sub)
        result.extend(sup)

        if self.sort:
            return self.sort.sort(char, result)
        else:
            return char, result


if __name__ == '__main__':
    d = Decompose()
    print(d.similar('做'))
