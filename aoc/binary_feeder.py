import string


class BinaryFeeder:
    """
    A utility class for parsing and extracting bits from a hexadecimal
    string representation.
    This class provides methods to sequentially read and convert hexadecimal
    data into binary bits and values.

    Attributes:
        hex_string (str): The input hexadecimal string to be parsed.

    Methods:
        get_bits(number_of_bits): Retrieves a specified number of bits
        as an integer.
        get_literal(): Extracts a literal value from the binary stream.
        bit_index: Property returning the current bit position.
        total_bits: Property returning the total number of bits in the stream.
        bits_remaining: Property returning the number of unread bits.
    """

    def __init__(self, hex_string: str):
        """
        Initializes a BinaryFeeder instance with a hexadecimal string for bit-level parsing.
        Validates the input hex string and sets up initial parsing state for sequential bit extraction.

        Args:
            hex_string (str): A string containing valid hexadecimal digits to be parsed.

        Raises:
            AssertionError: If the input string contains non-hexadecimal characters.
        """
        assert all(d in string.hexdigits for d in hex_string)
        self.hex_string = hex_string
        self._position = 0
        self._current_byte = f"{int(hex_string[0], 16):04b}"
        self._current_bit = 0
        self._bit_count = 0
        self._total_bits = 4 * len(hex_string)

    def _next_bit(self) -> int:
        """
        Retrieves the next bit from the hexadecimal string being parsed.
        Advances through the hex string and manages bit-level tracking during extraction.

        Returns:
            int: The next bit (0 or 1) from the current byte being processed.
        """
        if self._current_bit >= 4:
            self._position += 1
            self._current_byte = f"{int(self.hex_string[self._position], 16):04b}"
            self._current_bit = 0
        ret_val = self._current_byte[self._current_bit]
        self._current_bit += 1
        self._bit_count += 1
        return int(ret_val)

    def get_bits(self, number_of_bits: int) -> int:
        """
        Extracts a specified number of bits from the binary stream and converts them to an integer.
        Sequentially reads bits and constructs an integer value using bitwise operations.

        Args:
            number_of_bits (int): The number of bits to extract from the stream.

        Returns:
            int: An integer representation of the extracted bits.
        """
        ret_val = 0
        for _ in range(number_of_bits):
            ret_val = ret_val * 2 + self._next_bit()
        return ret_val

    def get_literal(self) -> int:
        """
        Extracts a multi-part literal value from the binary stream using a continuation flag mechanism.
        Reads 4-bit segments and combines them into a complete integer value, stopping when the continuation flag indicates the end.

        Returns:
            int: The complete literal value extracted from the binary stream.
        """
        ret_val = 0
        while True:
            c_flag = self._next_bit()
            part = self.get_bits(4)
            ret_val = (ret_val << 4) + part
            if not c_flag:
                return ret_val

    @property
    def bit_index(self) -> int:
        """
        Provides the current bit position in the binary stream.
        Returns the total number of bits that have been read so far.

        Returns:
            int: The current bit index in the stream.
        """
        return self._bit_count

    @property
    def total_bits(self):
        """
        Retrieves the total number of bits in the binary stream.
        Provides the complete bit length of the original hexadecimal input.

        Returns:
            int: The total number of bits in the stream.
        """
        return self._total_bits

    @property
    def bits_remaining(self) -> int:
        """
        Calculates the number of unread bits in the binary stream.
        Determines the remaining bits by subtracting the current bit index from the total bit count.

        Returns:
            int: The number of bits yet to be processed in the stream.
        """
        return self.total_bits - self.bit_index
