from CJKrelate.image import ImageDiffSimilar, ImageDiff
from CJKrelate.radicalize import Krad
from CJKrelate.variant import Variant
from CJKrelate.decompose import Decompose
from CJKrelate.sort import Sort


class Related:
    def __init__(self, font=None, visually_similar=False):
        if visually_similar:
            self.visual = ImageDiffSimilar(font=font)
        self.krad = Krad()
        self.variant = Variant()
        self.decompose = Decompose()
        self.sort = Sort()

    def format(self, character):
        result = {
            'composition': self.decompose.similar(character),
        }
        if 'image_diff' in self.__dict__.keys():
            result['visual']: self.visual.similar(character)
        return result

    def similar(self, character):
        result = {
            character: self.format(character)
        }
        for char in self.variant.get(character):
            result.update({
                char: self.format(char)
            })
        return result

    def similar_merged(self, character):
        result = []
        for item in self.similar(character).values():
            for x in item.values():
                result.extend(x)
        return self.sort.sort(character, set(result))


if __name__ == '__main__':
    from time import time

    start = time()
    r = Related()
    print(time() - start)

    start = time()
    print(r.similar('持'))
    print(time() - start)

    start = time()
    for item in r.similar_merged('持'):
        print(item)
    print(time() - start)
