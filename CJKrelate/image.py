from PIL import ImageChops, Image, ImageFont, ImageDraw
import math
import os
import pickle
from io import BytesIO


class ImageDiff:
    def __init__(self, font: str, font_size=50):
        self.font = ImageFont.truetype(font, font_size)

    def get_dimension(self, character):
        return ImageDraw.Draw(Image.new('LA', (0, 0))).textsize(character, font=self.font)

    def char_to_image(self, character):
        image = Image.new('L', self.get_dimension(character), "white")
        ImageDraw.Draw(image).text((0, 0), character, fill="black", font=self.font)
        return image

    def diff_im(self, im1, im2):
        h = ImageChops.difference(im1, im2).histogram()
        rms = math.sqrt(sum(map(lambda h, i: h * (i ** 2), h, range(256))) / (float(im1.size[0]) * im1.size[1]))
        return rms

    def diff(self, char1, char2):
        return self.diff_im(self.char_to_image(char1), self.char_to_image(char2))


class ImageDiffSimilar(ImageDiff):
    def __init__(self, font: str, font_size=50, cache=True):
        """Font list generator

        Args:
            font (str): path to font file (`fc-list | grep noto | grep JP` in Linux)
            font_size (int, optional): Font Size. Defaults to 50.
            cache (bool, optional): Defaults to True.
        """
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
        im = self.char_to_image(character)
        for diff_char, diff in self.diff_dict.items():
            rms = self.diff_im(im, Image.open(diff))
            yield rms, diff_char

class CharacterSimilar:
    def __init__(self, character: str, engine: ImageDiffSimilar) -> None:
        self.c = character
        self.engine = engine
        self.im = self.engine.char_to_image(self.c)

    def __iter__(self):
        for diff_char, diff in self.engine.diff_dict.items():
            rms = self.engine.diff_im(self.im, Image.open(diff))
            yield rms, diff_char

    def finalize(self) -> list[str]:
        return [char for _, char in sorted(self)]
