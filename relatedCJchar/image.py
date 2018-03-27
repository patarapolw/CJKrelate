from PIL import ImageChops, Image, ImageFont, ImageDraw
import math
import os
import sys
import pickle

from relatedCJchar.dir import ROOT


class ImageDiff:
    def __init__(self, font: str = None, font_size=50, temp=True):
        if font is None:
            font = {
                'win32': 'PmingLiu',
                'darwin': 'LiSong Pro'
            }.get(sys.platform, 'UMingTW')
        self.font = ImageFont.truetype(font, font_size)
        if temp:
            raw_path = os.path.splitext(font)[0] + '.pkl'
            if not os.path.exists(raw_path):
                self.diff_dict = dict(self.load())
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

    def get_dimension(self, character):
        return ImageDraw.Draw(Image.new('RGB', (0, 0))).textsize(character, font=self.font)

    def char_to_image(self, character):
        image = Image.new('RGB', self.get_dimension(character), "white")
        ImageDraw.Draw(image).text((0, 0), character, fill="black", font=self.font)
        return image

    def _rmsdiff(self, character, diff):
        "Calculate the root-mean-square difference between two images"

        im1 = self.char_to_image(character)
        h = ImageChops.difference(im1, diff).histogram()

        # calculate rms
        return math.sqrt(sum(map(lambda h, i: h*(i**2), h, range(256))) / (float(im1.size[0]) * im1.size[1]))

    def similar(self, character, threshold=100):
        def iter_similar():
            for diff_char, diff in self.diff_dict.items():
                rms = self._rmsdiff(character, diff)
                if rms < threshold:
                    yield rms, diff_char
        return [diff_char for rms, diff_char in sorted(iter_similar())]


if __name__ == '__main__':
    from time import time
    start = time()
    d = ImageDiff()
    print(time()-start)

    start = time()
    print(d.similar('日'))
    print(time()-start)
