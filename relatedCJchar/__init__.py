from relatedCJchar.image import ImageDiff
from relatedCJchar.radicalize import Krad
from relatedCJchar.variant import Variant


class Related:
    def __init__(self, font=None):
        self.image_diff = ImageDiff(font=font)
        self.krad = Krad()
        self.variant = Variant()

    def similar(self, character):
        result = {
            character: {
                'radical': list(self.krad.similar(character)),
                'visual': self.image_diff.similar(character)
            }
        }
        for char in self.variant.get(character):
            result.update({
                char: {
                    'radical': list(self.krad.similar(char)),
                    'visual': self.image_diff.similar(char)
                }
            })
        return result


if __name__ == '__main__':
    r = Related()
    print(r.similar('日'))
