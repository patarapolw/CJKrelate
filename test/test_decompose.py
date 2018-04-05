import pytest

from CJKrelate.decompose import Decompose

decompose = Decompose()


@pytest.mark.parametrize("char, expected_sub, expected_super",
                         [['好', ['女', '子'], ['䒵', '孬', '恏', '𠲡', '𡘏', '𡤟', '𥁨', '𪀮', '𪥸', '𪦟', '𫚻']],
                          ['一', ['㇐'], ['𫝀', '𫝁', '𫝂', '𫠉', '𫠓']]])
def test_decompose(char, expected_sub, expected_super):
    assert decompose.get_sub(char) == expected_sub
    assert decompose.get_super(char) == expected_super


if __name__ == '__main__':
    print(decompose.get_sub('好'))
    print(decompose.get_super('好'))
