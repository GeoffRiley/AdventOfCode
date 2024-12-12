import pytest
# import string
from aoc.binary_feeder import BinaryFeeder


@pytest.mark.parametrize(
    "hex_input,expected_total_bits",
    [
        ("A", 4),
        ("FF", 8),
        ("1234", 16),
    ],
    ids=["single_hex", "two_hex", "four_hex"],
)
def test_binary_feeder_initialization(hex_input, expected_total_bits):
    # Arrange

    # Act
    feeder = BinaryFeeder(hex_input)

    # Assert
    assert feeder.total_bits == expected_total_bits


@pytest.mark.parametrize(
    "hex_input,num_bits,expected_value",
    [
        ("A", 4, 10),
        ("F", 4, 15),
        ("1", 4, 1),
        ("23", 8, 35),
    ],
    ids=["partial_byte", "max_hex_value", "low_value", "multi_byte"],
)
def test_get_bits(hex_input, num_bits, expected_value):
    # Arrange
    feeder = BinaryFeeder(hex_input)

    # Act
    result = feeder.get_bits(num_bits)

    # Assert
    assert result == expected_value


@pytest.mark.parametrize(
    "hex_input,expected_literal",
    [
        ("D0", 0),
        ("A0", 10),
        ("F0", 15),
    ],
    ids=["zero_literal", "mid_literal", "max_literal"],
)
def test_get_literal(hex_input, expected_literal):
    # Arrange
    feeder = BinaryFeeder(hex_input)

    # Act
    result = feeder.get_literal()

    # Assert
    assert result == expected_literal


def test_bit_index_tracking():
    # Arrange
    feeder = BinaryFeeder("A3")

    # Act
    feeder.get_bits(3)

    # Assert
    assert feeder.bit_index == 3


def test_bits_remaining():
    # Arrange
    feeder = BinaryFeeder("A3")

    # Act
    feeder.get_bits(2)

    # Assert
    assert feeder.bits_remaining == 6


def test_invalid_hex_input():
    # Arrange / Act / Assert
    with pytest.raises(AssertionError):
        BinaryFeeder("XG")
