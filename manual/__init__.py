import yaml
import os
import re
import string

from relatedCJKchar.dir import ROOT


class Manual:
    def __init__(self):
        try:
            with open(os.path.join(ROOT, 'database', 'manual_input.yaml')) as f:
                self.entries = yaml.safe_load(f)
        except FileNotFoundError:
            self.entries = dict()
        with open(os.path.join(ROOT, 'database', 'frequency', 'hanzi', 'hanzi_level_project.txt')) as f:
            self.hlp = f.read()

    def update(self, char, rel_char_list):
        self.entries.setdefault(char, []).extend(rel_char_list)
        self.entries[char] = list(set(self.entries[char]))
        for rel_char in rel_char_list:
            self.entries.setdefault(rel_char, []).append(char)
            self.entries[rel_char] = list(set(self.entries[rel_char]))

    def get(self, char):
        return self.entries.get(char, set())

    def dump(self):
        with open(os.path.join(ROOT, 'database', 'manual_input.yaml'), 'w') as f:
            yaml.dump(self.entries, stream=f, allow_unicode=True)

    def check_hlp(self):
        print(re.sub(r'([^{0}{1}])'.format(string.printable, ''.join(self.entries.keys())), ' ', self.hlp))
