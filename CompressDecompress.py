
class CompressedData:
    def __init__(self, data: str) -> None:
        self.original_data = data
        self._compress(data)

    def _compress(self, data: str):
        self.bit_string: int = 1

        for character in data.upper():
            self.bit_string <<= 2
            if character == "A":
                self.bit_string |= 0b00
            elif character == "C":
                self.bit_string |= 0b01
            elif character == "G":
                self.bit_string |= 0b10
            elif character == "T":
                self.bit_string |= 0b11
            else:
                raise ValueError ("Invalid dataString: {}".format(data))

    def decompress(self) -> str:
        bit_string = self.bit_string
        decompressed_data = []

        # Stop when bit_string reaches the sentinel value (1)
        while bit_string > 1:
            # Extract the last 2 bits
            last_two_bits = bit_string & 0b11  # Mask to get the last 2 bits
            # Map the 2-bit value back to the corresponding character
            if last_two_bits == 0b00:
                decompressed_data.append("A")
            elif last_two_bits == 0b01:
                decompressed_data.append("C")
            elif last_two_bits == 0b10:
                decompressed_data.append("G")
            elif last_two_bits == 0b11:
                decompressed_data.append("T")
            # Shift right by 2 bits to process the next character
            bit_string >>= 2

        # Reverse the list to get the original string (since we processed from LSB to MSB)
        decompressed_data.reverse()
        return "".join(decompressed_data)

    def get_before_compression_size(self) -> int:
        # Each character uses 1 byte (8 bits)
        return len(self.original_data) * 8

    def get_after_compression_size(self) -> int:
        # Each character is compressed into 2 bits, plus 1 bit for the sentinel value
        return len(self.original_data) * 2 + 1


# Example usage
if __name__ == "__main__":
    data = "ACGTACGT"
    compressed = CompressedData(data)

    print("Original data:", data)
    print("Compressed bit string (in binary):", bin(compressed.bit_string))
    print("Decompressed data:", compressed.decompress())

    # Size calculations
    before_size = compressed.get_before_compression_size()
    after_size = compressed.get_after_compression_size()

    print("\nSize Before Compression (in bits):", before_size)
    print("Size After Compression (in bits):", after_size)
    print("Compression Ratio:", before_size / after_size)