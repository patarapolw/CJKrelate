import math

from relatedCJKchar.image import ImageDiff
from relatedCJKchar.frequency import Frequency


class Sort(ImageDiff):
    def __init__(self, lang='cn'):
        super().__init__(lang=lang)
        self.freq = Frequency(lang=lang)

    def details(self, char_base, char_list, freq_limit=5000):
        def sort_iter():
            for char2 in char_list:
                rel_freq = self.freq.relative_freq(char2)
                listing = self.freq.listing(char2)
                rms = self.diff(char_base, char2)
                try:
                    adjusted = math.log(math.e + rms) / rel_freq
                except ZeroDivisionError:
                    adjusted = math.inf
                if adjusted >= 0 and 0 <= listing < freq_limit:
                    yield adjusted, rms, listing, char2
        return sorted(sort_iter())

    def sort(self, char_base, char_list, freq_limit=5000):
        return [char2 for adjusted, rms, listing, char2 in self.details(char_base, char_list, freq_limit)]

    def rate(self, char_base, char_list, limits: dict=None):
        if limits is None:
            limits = {
                'overall': 1,
                'visual': 130,
                'frequency': 5000
            }

        result = {
            'good': [],
            'poor': {
                'overall': [],
                'visual': [],
                'frequency': []
            }
        }
        for adjusted, rms, listing, char2 in self.details(char_base, char_list):
            if listing > limits['frequency']:
                result['poor']['frequency'].append((char2, listing))
            elif rms > limits['visual']:
                result['poor']['visual'].append((char2, rms))
            elif adjusted > limits['overall']:
                result['poor']['overall'].append((char2, adjusted))
            else:
                result['good'].append((char2, adjusted))

        return result
