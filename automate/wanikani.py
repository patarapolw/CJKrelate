import os

from automate import Output

from CJKrelate.dir import ROOT
from CJKrelate.decompose import Decompose


def printable_radicals():
    with open(os.path.join('radicals', 'wanikani.txt')) as f:
        for row in f:
            contents = row.split('\t')
            if contents[1] == 'radical':
                yield contents[2]
            else:
                break


def radical_to_hanzi():
    out = Output(os.path.join(ROOT, 'database', 'human.yaml'))
    decom = Decompose()

    for radical in printable_radicals():
        out.update(radical, decom.get_super(radical))

    out.dump()


if __name__ == '__main__':
    radical_to_hanzi()
