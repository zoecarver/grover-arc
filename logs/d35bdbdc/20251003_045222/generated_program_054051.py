```python
from typing import List
from collections import defaultdict

class Sandwich:
    def __init__(self, r: int, c: int, A: int, B: int):
        self.r = r  # Top-left row
        self.c = c  # Top-left col
        self.A = A  # Border value
        self.B = B  # Center value
        self.center_r = r + 1
        self.center_c = c + 1
        self.next: 'Sandwich' = None  # Linked next sandwich

def detect_sandwiches(grid: List[List[int]]) -> List[Sandwich]:
    """
    Detects all 3x3 sandwiches in the grid where the 8 border cells are uniform A > 0
    and center is B > 0 != A. Scans in row-major order.
    """
    n = len(grid)
    sandwiches: List[Sandwich] = []
    border_offsets = [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)]  # 8 border positions
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
    """
    Finds the closest sandwich by Manhattan distance from (target_r, target_c).
    In case of ties, prefers the one with largest center_r, then largest center_c
    (bottom-right most, suggesting forward chaining direction).
    """
    if not candidates:
        return None
    min_dist = float('inf')
    closest = None
    best_r = -float('inf')
    best_c = -float('inf')
    for cand in candidates:
        d = abs(cand.center_r - target_r) + abs(cand.center_c - target_c)
        if d < min_dist:
            min_dist = d
            closest = cand
            best_r = cand.center_r
            best_c = cand.center_c
        elif d == min_dist:
            if (cand.center_r > best_r) or (cand.center_r == best_r and cand.center_c > best_c):
                closest = cand
                best_r = cand.center_r
                best_c = cand.center_c
    return closest

def assign_nexts(sandwiches: List[Sandwich]) -> None:
    """
    Assigns the 'next' sandwich for each by linking B to the closest sandwich with matching A.
    Builds color_to_list in detection order, then uses get_closest for selection.
    """
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
    """
    Identifies root sandwiches (no incoming links) using incoming degree count.
    Returns in order of appearance in sandwiches list (row-major).
    """
    incoming = defaultdict(list)
    for s in sandwiches:
        if s.next:
            incoming[s.next].append(s)
    roots = [s for s in sandwiches if len(incoming[s]) == 0]
    return roots

def clear_sandwich(grid: List[List[int]], s: Sandwich) -> None:
    """
    Clears the entire 3x3 area of the sandwich to 0.
    """
    for dr in range(3):
        for dc in range(3):
            grid[s.r + dr][s.c + dc] = 0

def process_chain(grid: List[List[int]], current: Sandwich) -> None:
    """
    Recursively processes a chain: updates current center to next.B, clears next,
    and continues on the subsequent chain. Clears terminals entirely.
    """
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
    """
    Processes all root chains independently, in the order of roots.
    """
    for root in roots:
        process_chain(grid, root)

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main function: copies grid, detects sandwiches, builds chains via closest linking,
    finds roots, processes all chains to update centers and clear linked sandwiches.
    """
    grid = [row[:] for row in g]
    sandwiches = detect_sandwiches(grid)
    assign_nexts(sandwiches)
    roots = find_roots(sandwiches)
    process_all_chains(grid, roots)
    return grid
```