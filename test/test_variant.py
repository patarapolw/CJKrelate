import pytest

from CJKrelate.variant import Variant

variant = Variant()


@pytest.mark.parametrize('char, expected',
                         [('好', []),
                          ('么', ['幺', '麼', '麽'])])
def test_variant(char, expected):
    assert variant.get(char) == expected


if __name__ == '__main__':
    print(variant.get('么'))
