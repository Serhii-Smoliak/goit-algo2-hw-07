import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n-1) + fibonacci_lru(n-2)

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _rotate(self, x):
        parent = x.parent
        grandparent = parent.parent if parent else None
        if parent.left == x:
            parent.left = x.right
            if x.right:
                x.right.parent = parent
            x.right = parent
        else:
            parent.right = x.left
            if x.left:
                x.left.parent = parent
            x.left = parent
        parent.parent = x
        x.parent = grandparent
        if grandparent:
            if grandparent.left == parent:
                grandparent.left = x
            else:
                grandparent.right = x
        if x.parent is None:
            self.root = x

    def _splay(self, x):
        while x.parent:
            parent = x.parent
            grandparent = parent.parent if parent else None
            if grandparent:
                if (parent.left == x) == (grandparent.left == parent):
                    self._rotate(parent)
                else:
                    self._rotate(x)
            self._rotate(x)

    def insert(self, key, value):
        if not self.root:
            self.root = Node(key, value)
            return
        node = self.root
        while node:
            if key < node.key:
                if node.left:
                    node = node.left
                else:
                    node.left = Node(key, value)
                    node.left.parent = node
                    self._splay(node.left)
                    break
            elif key > node.key:
                if node.right:
                    node = node.right
                else:
                    node.right = Node(key, value)
                    node.right.parent = node
                    self._splay(node.right)
                    break
            else:
                node.value = value
                self._splay(node)
                break

    def find(self, key):
        node = self.root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return node.value
        return None

def fibonacci_splay(n, tree):
    cached_value = tree.find(n)
    if cached_value is not None:
        return cached_value
    if n <= 1:
        tree.insert(n, n)
        return n
    value = fibonacci_splay(n-1, tree) + fibonacci_splay(n-2, tree)
    tree.insert(n, value)
    return value

ns = list(range(0, 1000, 50))

tree = SplayTree()

lru_times = []
for n in ns:
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=10)
    lru_times.append(lru_time)  # Час у секундах

splay_times = []
for n in ns:
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=10)
    splay_times.append(splay_time)  # Час у секундах

plt.plot(ns, lru_times, label='LRU Cache')
plt.plot(ns, splay_times, label='Splay Tree')
plt.xlabel('Число Фібоначчі (n)')
plt.ylabel('Середній час виконання (секунди)')
plt.title('Порівняння методів обчислення чисел Фібоначчі')
plt.legend()
plt.grid(True)

plt.show()

print(f"{'n':<10}{'Час LRU Cache (с)':<25}{'Час Splay Tree (с)'}")
print("-" * 50)
for n, lru, splay in zip(ns, lru_times, splay_times):
    print(f"{n:<10}{lru:<25}{splay}")
