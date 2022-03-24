from CJKrelate.image import ImageDiff, ImageDiffSimilar
from time import time
from datetime import timedelta

start = time()
d = ImageDiffSimilar(font='/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc')
print(timedelta(seconds=time()-start))

parent = '復'
print(parent)
print()

for c in d.iter_similar(parent):
    print(c)

print(timedelta(seconds=time()-start))
