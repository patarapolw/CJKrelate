import re
import os

from relatedCJKchar.dir import ROOT


class Decompose:
    def __init__(self):
        self.entries = dict()
        self.super_entries = dict()
        with open(os.path.join(ROOT, 'database', 'cjk-decomp.txt')) as f:
            for row in f:
                entry, _, components = re.match('(.+):(.+)\((.*)\)', row).groups()
                comp_list =  components.split(',')
                self.entries[entry] = comp_list
                for comp in comp_list:
                    self.super_entries.setdefault(comp, []).append(entry)

    def get_sub(self, char):
        return self.entries[char]

    def get_super(self, char):
        return self.super_entries[char]

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

        return result


if __name__ == '__main__':
    d = Decompose()
    print(d.entries['日'], d.super_entries['日'])
