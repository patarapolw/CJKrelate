import math

from relatedCJKchar.image import ImageDiff
from relatedCJKchar.frequency import Frequency


class Sort(ImageDiff):
    def __init__(self, lang='cn'):
        super().__init__(lang=lang)
        self.freq = Frequency(lang=lang)

    def details(self, char_base, char_list):
        def sort_iter():
            for char2 in char_list:
                rel_freq = self.freq.relative_freq(char2)
                listing = self.freq.listing(char2)
                rms = self.diff(char_base, char2)
                try:
                    adjusted = math.log(math.e + rms) / rel_freq
                except ZeroDivisionError:
                    adjusted = math.inf
                if adjusted >= 0 and listing >= 0:
                    yield adjusted, rms, listing, char2
        return sorted(sort_iter())

    def sort(self, char_base, char_list):
        return [char2 for adjusted, rms, listing, char2 in self.details(char_base, char_list)]
