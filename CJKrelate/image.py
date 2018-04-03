from PIL import ImageChops, Image, ImageFont, ImageDraw
import math
import os
import pickle
from io import BytesIO


class ImageDiff:
    def __init__(self, font, font_size=50):
        self.font = ImageFont.truetype(font, font_size)

    def get_dimension(self, character):
        return ImageDraw.Draw(Image.new('LA', (0, 0))).textsize(character, font=self.font)

    def char_to_image(self, character):
        image = Image.new('L', self.get_dimension(character), "white")
        ImageDraw.Draw(image).text((0, 0), character, fill="black", font=self.font)
        return image

    def _diff(self, char1, im2):
        # methods = [cv2.TM_CCOEFF,
        #            cv2.TM_CCOEFF_NORMED,
        #            cv2.TM_CCORR,
        #            cv2.TM_CCORR_NORMED,
        #            cv2.TM_SQDIFF,
        #            cv2.TM_SQDIFF_NORMED
        #            ]
        # method = methods[5]
        # res = cv2.matchTemplate(numpy.array(self.char_to_image(char1)),
        #                         numpy.array(im2), method)
        #
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        #
        # if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]
        #     return min_val
        # else:
        #     return max_val

        im1 = self.char_to_image(char1)
        h = ImageChops.difference(im1, im2).histogram()

        rms = math.sqrt(sum(map(lambda h, i: h * (i ** 2), h, range(256))) / (float(im1.size[0]) * im1.size[1]))

        return rms

    def diff(self, char1, char2):
        return self._diff(char1, self.char_to_image(char2))


class ImageDiffSimilar(ImageDiff):
    def __init__(self, font: str = None, font_size=50, cache=True):
        super().__init__(font, font_size)
        self.diff_dict = dict()
        if cache:
            raw_path = 'font_image.pkl'
            if not os.path.exists(raw_path):
                for k, v in self.load():
                    raw = BytesIO()
                    v.save(raw, 'jpeg')
                    self.diff_dict[k] = raw
                with open(raw_path, 'wb') as f:
                    pickle.dump(self.diff_dict, f)
            else:
                with open(raw_path, 'rb') as f:
                    self.diff_dict = pickle.load(f)
        else:
            self.diff_dict = dict(self.load())

    def load(self):
        for u in range(0x4E00, 0x9FFF):
            yield chr(u), self.char_to_image(chr(u))

    def similar(self, character):
        return [char for _, char in sorted(self.iter_similar(character))]

    def iter_similar(self, character):
        for diff_char, diff in self.diff_dict.items():
            rms = self._diff(character, Image.open(diff))
            yield rms, diff_char


if __name__ == '__main__':
    # d = ImageDiff()
    # print(d.diff('日', '鈤'))

    from time import time
    start = time()
    d = ImageDiffSimilar()
    print(time()-start)

    start = time()
    print(d.similar('日'))
    print(time()-start)
