import pytest

from no_maths import no_maths, ribbon_length


@pytest.mark.parametrize('parcel_size, paper_feet', [
    ('2x3x4', 58),
    ('1x1x10', 43)
])
def test_no_maths(parcel_size, paper_feet):
    assert no_maths(parcel_size) == paper_feet


@pytest.mark.parametrize('parcel_size, ribbon_feet', [
    ('2x3x4', 34),
    ('1x1x10', 14)
])
def test_ribbon_length(parcel_size, ribbon_feet):
    assert ribbon_length(parcel_size) == ribbon_feet
