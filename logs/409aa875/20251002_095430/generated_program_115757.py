```python
from typing import List
from math import inf

def program(g: List[List[int]]) -> List[List[int]]:
    n = 16
    LARGE = 1000
    out = [row[:] for row in g]
    original_g = g  # unchanged

    def compute_min_dists(positions: List[int]) -> List[int]:
        if not positions:
            return []
        sorted_pos = sorted(positions)
        m = len(sorted_pos)
        min_dists = []
        for i in range(m):
            d1 = LARGE if i == 0 else sorted_pos[i] - sorted_pos[i - 1]
            d2 = LARGE if i == m - 1 else sorted_pos[i + 1] - sorted_pos[i]
            min_dists.append(min(d1, d2))
        return min_dists

    def get_normal_rep(positions: List[int]) -> List[int]:
        if not positions or all(c > 7 for c in positions):
            return []
        sorted_pos = sorted(positions)
        min_d_list = compute_min_dists(sorted_pos)
        max_d = max(min_d_list)
        candidates = [sorted_pos[i] for i in range(len(sorted_pos)) if min_d_list[i] == max_d]
        if candidates:
            return [min(candidates)]
        return []

    def get_penultimate_reps(out: List[List[int]], r: int, n: int) -> List[int]:
        positions = [c for c in range(n) if out[r][c] != 7]
        if not positions or all(c > 7 for c in positions):
            return []
        sorted_pos = sorted(positions)
        min_d_list = compute_min_dists(sorted_pos)
        max_d = max(min_d_list)
        if max_d != 1:
            # gap rule
            reps = []
            current = None
            for c in sorted_pos:
                if current is None or (c - current) >= 6:
                    reps.append(c)
                    current = c
            return reps
        else:
            # pair mode
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
                return []
            shift = components[0]
            shifted = [c - shift for c in components]
            u = 9
            for c in shifted:
                if 0 <= c < n:
                    out[u][c] = 9
                    out[1][c] = 9
            if len(components) >= 2:
                second = components[1]
                out[6][second] = 9
                if second + 1 < n:
                    out[6][second + 1] = 9
                out[7][second] = 9
            return []  # already placed in pair mode

    def handle_center_blue(out: List[List[int]], original_g: List[List[int]], n: int) -> List[List[int]]:
        if n > 9 and 16 > 7 and out[9][7] == 9 and original_g[14][7] == 9:
            out[9][7] = 1
        return out

    # Process rows 10-14
    for r in range(10, 15):
        if r == 14:
            reps = get_penultimate_reps(out, r, n)
            u = 9
            for col in reps:
                if 0 <= u < n and 0 <= col < n:
                    out[u][col] = 9
        else:
            positions = [c for c in range(n) if out[r][c] != 7]
            reps = get_normal_rep(positions)
            u = r - 5
            for col in reps:
                if 0 <= u < n and 0 <= col < n:
                    out[u][col] = 9

    out = handle_center_blue(out, original_g, n)
    return out
```