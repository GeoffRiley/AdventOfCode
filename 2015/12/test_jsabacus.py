import pytest

from jsabacus import jsabacus


@pytest.mark.parametrize('doc, value', [
    ('[1,2,3]', 6),
    ('{"a":2,"b":4}', 6),
    ('[[[3]]]', 3),
    ('{"a":{"b":4},"c":-1}', 3),
    ('[]', 0),
    ('{}', 0),
    ('[1,{"c":"red","b":2},3]', 4),
    ('{"d":"red","e":[1,2,3,4],"f":5}', 0),
    ('[1,"red",5]', 6)
])
def test_jsabacus(doc, value):
    assert jsabacus(doc, skip_dicts_with='red') == value