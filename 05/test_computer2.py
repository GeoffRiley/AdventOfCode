import pytest

from computer2 import Processor


@pytest.mark.parametrize('cells, result', [
    ('1,0,0,0,99', '2,0,0,0,99'),
    ('2,3,0,3,99', '2,3,0,6,99'),
    ('2,4,4,5,99,0', '2,4,4,5,99,9801'),
    ('1,1,1,4,99,5,6,0,99', '30,1,1,4,2,5,6,0,99')
])
def test_computer(cells, result):
    p=Processor(cells)
    p.simulate(trace=True)
    assert ','.join(str(v) for v in p.core) == result
