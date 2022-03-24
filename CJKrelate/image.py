import math
import os
import pickle
from io import BytesIO
from typing import Union

from PIL import ImageChops, Image, ImageFont, ImageDraw

__all__ = ("ImageDiffSimilar", "CharacterSimilar")


class ImageDiff:
    def __init__(self, font: str, font_size=50):
        self.font = ImageFont.truetype(font, font_size)

    def get_dimension(self, character):
        return ImageDraw.Draw(Image.new("LA", (0, 0))).textsize(
            character, font=self.font
        )

    def char_to_image(self, character):
        image = Image.new("L", self.get_dimension(character), "white")
        ImageDraw.Draw(image).text((0, 0), character, fill="black", font=self.font)
        return image

    def diff_im(self, im1, im2):
        h = ImageChops.difference(im1, im2).histogram()
        rms = math.sqrt(
            sum(map(lambda h, i: h * (i**2), h, range(256)))
            / (float(im1.size[0]) * im1.size[1])
        )
        return rms

    def diff(self, char1, char2):
        return self.diff_im(self.char_to_image(char1), self.char_to_image(char2))


class ImageDiffSimilar(ImageDiff):
    def __init__(
        self, font: str, font_size=50, rms_limit: Union[int, None] = 100, cache=True
    ):
        """Font list generator

        Args:
            font (str): path to font file (`fc-list | grep noto | grep JP` in Linux)
            font_size (int, optional): Font Size. Defaults to 50.
            rms_limit (Union[int, None], optional): Limit of similarity (in root-mean-square). Defaults to 100.
                The higher, the more difference. Set to 0 or None for no limit.
            cache (bool, optional): _description_. Defaults to True.
        """
        super().__init__(font, font_size)
        self.rms_limit = rms_limit

        self.diff_dict = dict()
        if cache:
            raw_path = "font_image.pkl"
            if not os.path.exists(raw_path):
                for k, v in self.load():
                    raw = BytesIO()
                    v.save(raw, "jpeg")
                    self.diff_dict[k] = raw
                with open(raw_path, "wb") as f:
                    pickle.dump(self.diff_dict, f)
            else:
                with open(raw_path, "rb") as f:
                    self.diff_dict = pickle.load(f)
        else:
            self.diff_dict = dict(self.load())

    def load(self):
        for u in range(0x4E00, 0x9FFF):
            yield chr(u), self.char_to_image(chr(u))


class CharacterSimilar:
    def __init__(self, character: str, engine: ImageDiffSimilar):
        self.c = character
        self.engine = engine
        self.im = self.engine.char_to_image(self.c)
        self._ranking = None

    def __iter__(self):
        for diff_char, diff in self.engine.diff_dict.items():
            rms = self.engine.diff_im(self.im, Image.open(diff))
            if self.engine.rms_limit and rms > self.engine.rms_limit:
                continue
            yield rms, diff_char

    def ranking(self):
        if not self._ranking:
            self._ranking = sorted(self)

        return self._ranking

    def finalize(self) -> list[str]:
        return [char for _, char in self.ranking()]


if __name__ == "__main__":
    from time import time
    from datetime import timedelta

    start = time()
    engine = ImageDiffSimilar(font="/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc")
    parent = "復"
    print(parent)

    sim = CharacterSimilar(parent, engine)

    print(timedelta(seconds=time() - start))
    print(sim.ranking())
    print(sim.finalize())

    print(timedelta(seconds=time() - start))
