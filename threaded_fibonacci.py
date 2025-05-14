"""
Not used during the talk. This is the kind of demo you may see on Youtube.

But maybe you want to check for yourself
that using GIL vs NoGIL is different at the fibonacci level.

This script runs fibonacci(n) in <count> number of threads.

The prints will look the same, but the time it takes will differ between GIL and NoGIL.
The reason is that threads are run one by one, then the prints are shown.
Since this function is CPU-bound, switching between threads doesn't make them faster,
only running them in parallel in different CPUs.

Try for example running this script like this:
`python threaded_fibonacci.py 35 3`
GIL will take roughly 3 times as long to run as NoGIL.
"""

import sys
from fibonacci import fibonacci
import time
import threading

def verbose_fibonacci(n: int) -> None:
    print(f"Starting fibonacci({n})")
    result = fibonacci(n)
    print(f"Ended fibonacci({n}) with result {result}")

def threaded_fibonacci(n: int, count: int) -> None:
    threads = []
    for _ in range(count):
        threads.append(threading.Thread(target=verbose_fibonacci, args=(n,),))

    start = time.perf_counter()
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    print(f"Threaded Fibonacci took {time.perf_counter() - start} seconds")


if __name__ == "__main__":
    threaded_fibonacci(n=int(sys.argv[1]), count=int(sys.argv[2]))

