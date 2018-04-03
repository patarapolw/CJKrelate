import pytest

from test import SpeedTest
from CJKrelate.japanese import Related, RelatedHuman, Sort


@pytest.mark.parametrize("char", ['好'])
def test_related(char):
    with SpeedTest('Related.__init__'):
        # Related.__init__ in: 0.7907 seconds
        r = Related()

    with SpeedTest('Related.similar_merged'):
        # Related.similar_merged in: 15.7123 seconds
        # 好: 129
        result = r.similar_merged(char)
        print(result)
        assert len(result) > 0

    with SpeedTest('Related.similar'):
        # Related.similar in: 15.0025 seconds
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


@pytest.mark.parametrize("char_base, char_list", [('好', ['好', '子', '学', '女', '安', '要', '始', '字', '委', '嫌', '姿', '如', '季', '娘', '婦', '奴', '婚', '嬉', '妻', '姉', '妙', '妹', '厚', '姫', '威', '姓', '妖', '孫', '孝'])])
def test_sort(char_base, char_list):
    with SpeedTest('Sort.__init__'):
        # Sort.__init__ in: 0.0950 seconds
        s = Sort()

    with SpeedTest('Sort.details'):
        # Sort.details in: 0.1859 seconds
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
    # pytest.main()
    test_sort('好', ['好', '子', '学', '女', '安', '要', '始', '字', '委', '嫌', '姿', '如', '季', '娘', '婦', '奴', '婚', '嬉', '妻', '姉', '妙', '妹', '厚', '姫', '威', '姓', '妖', '孫', '孝'])

