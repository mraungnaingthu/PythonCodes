from typing import Dict, Generator
from functools import lru_cache

#Method 1
def fib0(n: int) -> int:
    #print("calling time:", n)
    if n < 2:
        return n
    return fib0(n - 2) + fib0(n - 1)

# Method 2
memo: Dict[int, int] = {0: 0, 1: 1}
def fib1(n: int) -> int:
    #print("calling time:", n)
    if n not in memo:
        memo[n] = fib1(n - 1) + fib1(n - 2)

    return memo[n]

#Method 3
@lru_cache(maxsize=None)
def fib3(n: int) -> int:
    #print("calling time:", n)
    if n < 2:
        return n
    return fib3(n - 2) + fib3(n - 1)

#Method 4
def fib4(n: int) -> int:
    #print("calling time:", n)
    if n == 0: return n  # special case
    last: int = 0  # initially set to fib(0)
    next: int = 1  # initially set to fib(1)
    for _ in range(1, n):
        last, next = next, last + next
        return next

#Method 5
def fib5(n: int) -> Generator[int, None, None]:
    yield 0
    if n > 0: yield 1
    last: int = 0
    next: int = 1
    for _ in range(1, n):
        last, next = next, last + next
        yield next

#Main Function to call each mehtod
if __name__ == "__main__":
    print(fib0(20))
    print(fib1(20))
    print(fib3(20))
    print(fib4(20))

    for i in fib5(20):
        print(i)


