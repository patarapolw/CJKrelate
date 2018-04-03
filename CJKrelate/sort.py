import math

from CJKrelate.image import ImageDiff


class AbstractSort(ImageDiff):
    def __init__(self, frequency, freq_limit, font):
        """
        frequency: Frequency Object
        font: path to font file
        """
        super().__init__(font=font)

        self.freq = frequency
        self.freq_limit = freq_limit

    def details(self, char_base, char_list):
        def sort_iter():
            for char2 in char_list:
                rel_freq = self.freq.relative_freq(char2)
                listing = dict(self.freq.listing(char2))
                try:
                    min_listing = min(listing.values())
                except ValueError:
                    min_listing = math.inf

                rms = self.diff(char_base, char2)
                try:
                    adjusted = math.log(rms / rel_freq)
                except (ValueError, ZeroDivisionError) as e:
                    if str(e) == 'math domain error':
                        adjusted = 0
                    elif str(e) == 'float division by zero':
                        adjusted = math.inf
                    else:
                        raise
                if adjusted >= 0 and min_listing < self.freq_limit:
                    yield adjusted, rms, listing, char2
        return sorted(sort_iter())

    def sort(self, char_base, char_list):
        return [char2 for adjusted, rms, listing, char2 in self.details(char_base, char_list)]

    def rate(self, char_base: str, char_list: list, limits: dict=None):
        """
        char_base:
        typical limits for Chinese:
        limits = {
            'overall': 1,
            'visual': 130,
            'frequency': 5000
        }
        :param char_base: single character string for sorting the character list
        :param char_list: a list of single character strings
        :type limits: dict
        """
        if limits is None:
            raise NotImplementedError

        result = {
            'good': [],
            'poor': {
                'overall': [],
                'visual': [],
                'frequency': []
            }
        }
        for adjusted, rms, listing, char2 in self.details(char_base, char_list):
            try:
                min_listing = min(listing.values())
            except ValueError:
                min_listing = math.inf

            if min_listing > limits['frequency']:
                result['poor']['frequency'].append((char2, listing))
            elif rms > limits['visual']:
                result['poor']['visual'].append((char2, rms))
            elif adjusted > limits['overall']:
                result['poor']['overall'].append((char2, adjusted))
            else:
                result['good'].append((char2, adjusted))

        return result
