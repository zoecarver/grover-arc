```python
from typing import List
from math import inf
from copy import deepcopy

def get_positions(g: List[List[int]], r: int) -> List[int]:
    """Extract non-7 positions in row r."""
    return [c for c in range(16) if g[r][c] != 7]

def compute_min_dists(positions: List[int]) -> List[float]:
    """Compute min distance to nearest neighbors for each position in sorted positions."""
    if not positions:
        return []
    sorted_pos = sorted(positions)
    n = len(sorted_pos)
    min_dists = []
    for i in range(n):
        d1 = inf if i == 0 else sorted_pos[i] - sorted_pos[i - 1]
        d2 = inf if i == n - 1 else sorted_pos[i + 1] - sorted_pos[i]
        min_dists.append(min(d1, d2))
    return min_dists

def get_normal_reps(positions: List[int]) -> List[int]:
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

def lift_normal_reps(g: List[List[int]], out: List[List[int]]) -> None:
    """Lift normal representatives from rows 10-13 to rows 5-8."""
    for r in range(10, 14):
        positions = get_positions(g, r)
        reps = get_normal_reps(positions)
        if reps:
            u = r - 5
            out[u][reps[0]] = 9

def handle_penultimate(g: List[List[int]], out: List[List[int]]) -> None:
    """Handle special rules for row 14: gap reps to row 9 or pair mode multi-placements."""
    r = 14
    positions = get_positions(g, r)
    if not positions or all(c > 7 for c in positions):
        return
    sorted_pos = sorted(positions)
    min_d_list = compute_min_dists(sorted_pos)
    max_d = max(min_d_list)
    if max_d != 1:
        # Gap mode: greedy reps every >=6
        reps = []
        current = None
        for c in sorted_pos:
            if current is None or (c - current) >= 6:
                reps.append(c)
                current = c
        for c in reps:
            out[9][c] = 9
    else:
        # Pair mode: find size-2 components, shift and place in rows 1,9; extras in 6,7 for second
        components = []
        i = 0
        n_len = len(sorted_pos)
        while i < n_len:
            start = i
            j = i + 1
            while j < n_len and sorted_pos[j] == sorted_pos[j - 1] + 1:
                j += 1
            comp_size = j - start
            if comp_size == 2:
                components.append(sorted_pos[start])
            i = j
        if components:
            shift = components[0]
            shifted = [c - shift for c in components]
            for c in shifted:
                if 0 <= c < 16:
                    out[9][c] = 9
                    out[1][c] = 9
            if len(components) >= 2:
                second = components[1]
                out[6][second] = 9
                if second + 1 < 16:
                    out[6][second + 1] = 9
                out[7][second] = 9

def apply_center_override(out: List[List[int]], original_g: List[List[int]]) -> None:
    """Override row 9 col 7 from 9 to 1 if conditions met."""
    if out[9][7] == 9 and original_g[14][7] == 9:
        out[9][7] = 1

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    original_g = [row[:] for row in g]
    lift_normal_reps(g, out)
    handle_penultimate(g, out)
    apply_center_override(out, original_g)
    return out
```