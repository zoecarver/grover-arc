```python
from typing import List
from collections import defaultdict

class Sandwich:
    def __init__(self, r: int, c: int, A: int, B: int):
        self.r = r
        self.c = c
        self.A = A
        self.B = B
        self.center_r = r + 1
        self.center_c = c + 1
        self.next: Sandwich = None

def detect_sandwiches(grid: List[List[int]]) -> List[Sandwich]:
    n = len(grid)
    sandwiches: List[Sandwich] = []
    border_offsets = [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)]
    for i in range(n - 2):
        for j in range(n - 2):
            border_pos = [(i + dx, j + dy) for dx, dy in border_offsets]
            center_pos = (i + 1, j + 1)
            border_vals = [grid[x][y] for x, y in border_pos]
            A = border_vals[0]
            if A == 0 or not all(v == A for v in border_vals):
                continue
            B = grid[center_pos[0]][center_pos[1]]
            if B != 0 and B != A:
                s = Sandwich(i, j, A, B)
                sandwiches.append(s)
    return sandwiches

def get_closest(candidates: List[Sandwich], target_r: int, target_c: int) -> Sandwich:
    if not candidates:
        return None
    min_dist = float('inf')
    closest = None
    for cand in candidates:
        d = abs(cand.center_r - target_r) + abs(cand.center_c - target_c)
        if d < min_dist:
            min_dist = d
            closest = cand
    return closest

def assign_nexts(sandwiches: List[Sandwich]) -> None:
    color_to_list = defaultdict(list)
    for s in sandwiches:
        color_to_list[s.A].append(s)
    for s in sandwiches:
        target = s.B
        cands = color_to_list[target]
        if cands:
            s.next = get_closest(cands, s.center_r, s.center_c)
        else:
            s.next = None

def find_roots(sandwiches: List[Sandwich]) -> List[Sandwich]:
    incoming = defaultdict(list)
    for s in sandwiches:
        if s.next:
            incoming[s.next].append(s)
    roots = [s for s in sandwiches if len(incoming[s]) == 0]
    return roots

def clear_sandwich(grid: List[List[int]], s: Sandwich) -> None:
    for dr in range(3):
        for dc in range(3):
            grid[s.r + dr][s.c + dc] = 0

def process_chain(grid: List[List[int]], current: Sandwich) -> None:
    if current is None:
        return
    if current.next is None:
        clear_sandwich(grid, current)
        return
    next_s = current.next
    grid[current.center_r][current.center_c] = next_s.B
    clear_sandwich(grid, next_s)
    process_chain(grid, next_s.next)

def process_all_chains(grid: List[List[int]], roots: List[Sandwich]) -> None:
    for root in roots:
        process_chain(grid, root)

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    sandwiches = detect_sandwiches(grid)
    assign_nexts(sandwiches)
    roots = find_roots(sandwiches)
    process_all_chains(grid, roots)
    return grid
```