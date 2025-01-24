import random
import time
from functools import lru_cache

N = 100_000
array = [random.randint(1, 1000) for _ in range(N)]

Q = 50_000
queries = [
    ('Range', random.randint(0, N - 1), random.randint(0, N - 1)) if random.random() < 0.7 else
    ('Update', random.randint(0, N - 1), random.randint(1, 1000))
    for _ in range(Q)
]

class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (2 * self.n)
        self._build(data)

    def _build(self, data):
        for i in range(self.n):
            self.tree[self.n + i] = data[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[i * 2] + self.tree[i * 2 + 1]

    def update(self, index, value):
        index += self.n
        self.tree[index] = value
        while index > 1:
            index //= 2
            self.tree[index] = self.tree[index * 2] + self.tree[index * 2 + 1]

    def range_sum(self, L, R):
        L += self.n
        R += self.n
        sum_ = 0
        while L <= R:
            if L % 2 == 1:
                sum_ += self.tree[L]
                L += 1
            if R % 2 == 0:
                sum_ += self.tree[R]
                R -= 1
            L //= 2
            R //= 2
        return sum_

def range_sum_no_cache(array, L, R):
    return sum(array[L:R + 1])

def update_no_cache(array, index, value):
    array[index] = value

segment_tree = SegmentTree(array)

@lru_cache(maxsize=1000)
def range_sum_with_cache(L, R):
    return segment_tree.range_sum(L, R)

def update_with_cache(index, value):
    segment_tree.update(index, value)
    range_sum_with_cache.cache_clear()

def performance_test():
    start_no_cache = time.time()
    for query in queries:
        if query[0] == 'Range':
            _, L, R = query
            if L > R: L, R = R, L
            range_sum_no_cache(array, L, R)
        elif query[0] == 'Update':
            _, index, value = query
            update_no_cache(array, index, value)
    end_no_cache = time.time()
    print(f"Час виконання без кешування: {end_no_cache - start_no_cache:.2f} секунд")

    start_with_cache = time.time()
    for query in queries:
        if query[0] == 'Range':
            _, L, R = query
            if L > R: L, R = R, L
            range_sum_with_cache(L, R)
        elif query[0] == 'Update':
            _, index, value = query
            update_with_cache(index, value)
    end_with_cache = time.time()
    print(f"Час виконання з LRU-кешем: {end_with_cache - start_with_cache:.2f} секунд")

if __name__ == "__main__":
    performance_test()
