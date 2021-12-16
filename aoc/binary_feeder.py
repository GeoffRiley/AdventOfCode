import string


class BinaryFeeder:
    def __init__(self, hex_string: str):
        assert all(d in string.hexdigits for d in hex_string)
        self.hex_string = hex_string
        self._position = 0
        self._current_byte = f"{int(hex_string[0], 16):04b}"
        self._current_bit = 0
        self._bit_count = 0
        self._total_bits = 4 * len(hex_string)

    def _next_bit(self) -> int:
        if self._current_bit >= 4:
            self._position += 1
            self._current_byte = f"{int(self.hex_string[self._position], 16):04b}"
            self._current_bit = 0
        ret_val = self._current_byte[self._current_bit]
        self._current_bit += 1
        self._bit_count += 1
        return int(ret_val)

    def get_bits(self, number_of_bits: int) -> int:
        ret_val = 0
        for _ in range(number_of_bits):
            ret_val = ret_val * 2 + self._next_bit()
        return ret_val

    def get_literal(self) -> int:
        ret_val = 0
        while True:
            c_flag = self._next_bit()
            part = self.get_bits(4)
            ret_val = (ret_val << 4) + part
            if not c_flag:
                return ret_val

    @property
    def bit_index(self) -> int:
        return self._bit_count

    @property
    def total_bits(self):
        return self._total_bits

    @property
    def bits_remaining(self) -> int:
        return self.total_bits - self.bit_index
