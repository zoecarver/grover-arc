```python
from typing import List
from math import inf
from copy import deepcopy

def get_positions(g: List[List[int]], r: int, n: int) -> List[int]:
    """Extract non-7 positions in row r."""
    return [c for c in range(n) if g[r][c] != 7]

def compute_min_dists(positions: List[int]) -> List[float]:
    """Compute min distance to nearest neighbors for each sorted position."""
    if not positions:
        return []
    sorted_pos = sorted(positions)
    m = len(sorted_pos)
    min_dists = []
    LARGE = float('inf')
    for i in range(m):
        d1 = LARGE if i == 0 else sorted_pos[i] - sorted_pos[i - 1]
        d2 = LARGE if i == m - 1 else sorted_pos[i + 1] - sorted_pos[i]
        min_dists.append(min(d1, d2))
    return min_dists

def get_normal_rep(positions: List[int]) -> List[int]:
    """Get leftmost position with maximum min-distance, skipping if all positions >7."""
    if not positions or all(c > 7 for c in positions):
        return []
    sorted_pos = sorted(positions)
    min_d_list = compute_min_dists(sorted_pos)
    max_d = max(min_d_list)
    candidates = [sorted_pos[i] for i in range(len(sorted_pos)) if min_d_list[i] == max_d]
    if candidates:
        return [min(candidates)]
    return []

def process_normal_row(out: List[List[int]], g: List[List[int]], r: int, n: int) -> None:
    """Process a normal row (10-13): compute rep and place 9 in row r-5."""
    positions = get_positions(g, r, n)
    reps = get_normal_rep(positions)
    u = r - 5
    if 0 <= u < n:
        for rep in reps:
            if 0 <= rep < n:
                out[u][rep] = 9

def get_penultimate_reps_and_place(out: List[List[int]], g: List[List[int]], r: int, n: int) -> None:
    """Process penultimate row (14): gap or pair mode, place directly in relevant rows."""
    positions = get_positions(g, r, n)
    if not positions or all(c > 7 for c in positions):
        return
    sorted_pos = sorted(positions)
    min_d_list = compute_min_dists(sorted_pos)
    max_d = max(min_d_list)
    if max_d != 1:
        # Gap rule: greedy reps every >=6
        reps = []
        current = None
        for c in sorted_pos:
            if current is None or (c - current) >= 6:
                reps.append(c)
                current = c
        u = r - 5  # 9
        for rep in reps:
            if 0 <= rep < n:
                out[u][rep] = 9
    else:
        # Pair mode: find size-2 components, shift and place in rows 1,9; extras in 6,7
        components = []
        i = 0
        m = len(sorted_pos)
        while i < m:
            start = i
            j = i + 1
            while j < m and sorted_pos[j] == sorted_pos[j - 1] + 1:
                j += 1
            comp_size = j - start
            if comp_size == 2:
                components.append(sorted_pos[start])
            i = j
        if not components:
            return
        shift = components[0]
        shifted = [c - shift for c in components]
        for c in shifted:
            if 0 <= c < n:
                out[9][c] = 9
                out[1][c] = 9
        if len(components) >= 2:
            second = components[1]
            out[6][second] = 9
            if second + 1 < n:
                out[6][second + 1] = 9
            out[7][second] = 9

def handle_center_override(out: List[List[int]], original_g: List[List[int]], n: int) -> None:
    """Override center in row 9 col 7 from 9 to 1 if conditions met."""
    if n > 7 and out[9][7] == 9 and original_g[14][7] == 9:
        out[9][7] = 1

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: copy grid, process rows 10-14, apply center override."""
    n = 16
    out = [row[:] for row in g]
    original_g = [row[:] for row in g]
    for r in range(10, 14):
        process_normal_row(out, g, r, n)
    get_penultimate_reps_and_place(out, g, 14, n)
    handle_center_override(out, original_g, n)
    return out
```