from secrets import token_bytes
from typing import Tuple

def randomKey(length: int) -> int:
    tb: bytes = token_bytes(length)
    print(tb)
    return int.from_bytes(tb, "big")

if __name__ == "__main__":
    randomKey(5)