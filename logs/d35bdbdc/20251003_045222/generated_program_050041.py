```python
from collections import defaultdict
from typing import List

class Sandwich:
    def __init__(self, r: int, c: int, A: int, B: int):
        self.r = r
        self.c = c
        self.A = A
        self.B = B
        self.center_r = r + 1
        self.center_c = c + 1
        self.next = None

def clear_sandwich(grid: List[List[int]], s: Sandwich):
    for dr in range(3):
        for dc in range(3):
            grid[s.r + dr][s.c + dc] = 0

def process_chain(grid: List[List[int]], current: Sandwich):
    if current is None:
        return
    if current.next is None:
        clear_sandwich(grid, current)
        return
    next_s = current.next
    grid[current.center_r][current.center_c] = next_s.B
    clear_sandwich(grid, next_s)
    process_chain(grid, next_s.next)

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    n = len(grid)
    sandwiches = []
    color_to_sand = {}
    for r in range(n - 2):
        for c in range(n - 2):
            positions = [
                (r, c), (r, c + 1), (r, c + 2),
                (r + 1, c), (r + 1, c + 2),
                (r + 2, c), (r + 2, c + 1), (r + 2, c + 2)
            ]
            center = (r + 1, c + 1)
            vals = [grid[pr][pc] for pr, pc in positions]
            cval = grid[center[0]][center[1]]
            if cval == 0:
                continue
            A = vals[0]
            if A == 0 or A == cval or not all(v == A for v in vals):
                continue
            sand = Sandwich(r, c, A, cval)
            sandwiches.append(sand)
            color_to_sand[A] = sand
    for sand in sandwiches:
        if sand.B in color_to_sand:
            sand.next = color_to_sand[sand.B]
    incoming = defaultdict(list)
    for sand in sandwiches:
        if sand.next:
            incoming[sand.next].append(sand)
    roots = [s for s in sandwiches if not incoming[s]]
    for root in roots:
        process_chain(grid, root)
    return grid
```