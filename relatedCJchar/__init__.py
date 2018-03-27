from relatedCJchar.image import ImageDiff
from relatedCJchar.radicalize import Krad
from relatedCJchar.variant import Variant


class Related:
    def __init__(self, font=None, use_image_diff=False):
        if use_image_diff:
            self.image_diff = ImageDiff(font=font)
        self.krad = Krad()
        self.variant = Variant()

    def format(self, character):
        result = {
            'radical': list(self.krad.similar(character))
        }
        if 'image_diff' in self.__dict__.keys():
            result['visual']: self.image_diff.similar(character)
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


if __name__ == '__main__':
    r = Related(use_image_diff=True)
    print(r.similar('么'))
