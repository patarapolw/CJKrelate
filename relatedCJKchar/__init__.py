from relatedCJKchar.image import ImageDiffSimilar, ImageDiff
from relatedCJKchar.radicalize import Krad
from relatedCJKchar.variant import Variant
from relatedCJKchar.decompose import Decompose


class Related:
    def __init__(self, font=None, visually_similar=False):
        if visually_similar:
            self.visual = ImageDiffSimilar(font=font)
        self.krad = Krad()
        self.variant = Variant()
        self.decompose = Decompose()
        self.sorter = ImageDiff(font=font)

    def format(self, character):
        result = {
            # 'radical': list(self.krad.similar(character)),
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
        return self.sorter.sort(character, set(result))


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
