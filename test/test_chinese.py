import pytest

from test import SpeedTest
from CJKrelate.chinese import Related, RelatedHuman, Sort


@pytest.mark.parametrize("char", ['好'])
def test_related(char):
    with SpeedTest('Related.__init__'):
        # Related.__init__ in: 0.6583 seconds
        r = Related()

    with SpeedTest('Related.similar_merged'):
        # Related.similar_merged in: 6.9208 seconds
        # 好: 129
        result = r.similar_merged(char)
        print(result)
        assert len(result) > 0

    with SpeedTest('Related.similar'):
        # Related.similar in: 6.2610 seconds
        print(r.similar(char))


@pytest.mark.parametrize("char", ['好'])
def test_related_human(char):
    with SpeedTest('RelatedHuman.__init__'):
        # RelatedHuman.__init__ in: 1.7959 seconds
        r = RelatedHuman()

    with SpeedTest('RelatedHuman.get'):
        # RelatedHuman.get in: 0.0000 seconds
        result = r.get(char)
        assert len(result) > 0


@pytest.mark.parametrize("char_base, char_list", [('好', ['好', '子', '学', '女', '安', '要', '始', '字', '委', '姿', '嫌', '季', '如', '娘', '嬉', '妻', '婦', '婚', '奴', '姉', '厚', '妙', '妹', '姫', '威', '孫', '孝'])])
def test_sort(char_base, char_list):
    with SpeedTest('Sort.__init__'):
        # Sort.__init__ in: 0.0455 seconds
        s = Sort()

    with SpeedTest('Sort.details'):
        # Sort.details in: 0.0876 seconds
        print(s.details(char_base, char_list))

    with SpeedTest('Sort.rate'):
        # Sort.rate in: 0.0940 seconds
        limits = {
            'overall': 13,
            'visual': 130,
            'frequency': 5000
        }
        print(s.rate(char_base, char_list, limits=limits))


if __name__ == '__main__':
    test_sort('好', ['好', '子', '学', '女', '安', '要', '始', '字', '委', '姿', '嫌', '季', '如', '娘', '嬉', '妻', '婦', '婚', '奴', '姉', '厚', '妙', '妹', '姫', '威', '孫', '孝'])

