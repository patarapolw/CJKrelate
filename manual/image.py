from time import time
from datetime import timedelta

from CJKrelate.image import ImageDiffSimilar, CharacterSimilar

start = time()
engine = ImageDiffSimilar(font="/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc")
parent = "復"
print(parent)

sim = CharacterSimilar(parent, engine)

print(timedelta(seconds=time() - start))
print(sim.ranking())
print(sim.finalize())

print(timedelta(seconds=time() - start))
