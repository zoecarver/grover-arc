```python
from typing import List, Tuple

def find_u_candidates(g: List[List[int]]) -> List[Tuple[int, int, int]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    candidates = []
    for r in range(h - 2):
        for c in range(w - 1):
            if g[r][c] == 0:
                continue
            color = g[r][c]
            # Find vertical length down from (r, c)
            v_len = 1
            rr = r + 1
            while rr < h and g[rr][c] == color:
                v_len += 1
                rr += 1
            if v_len < 3:
                continue
            # Arm at bottom level
            bottom1 = r + v_len - 1
            arm1 = 1  # includes the vertical cell
            cc = c + 1
            while cc < w and g[bottom1][cc] == color:
                arm1 += 1
                cc += 1
            # Arm at second bottom level
            bottom2 = r + v_len - 2
            arm2 = 1
            cc = c + 1
            while cc < w and g[bottom2][cc] == color:
                arm2 += 1
                cc += 1
            l = max(arm1, arm2)
            if l >= 2 and l == color + 1:
                area = v_len * l
                candidates.append((area, l, color))
    return candidates

def create_u_pattern(l: int, color: int) -> List[List[int]]:
    width = 2 * l
    height = 3
    grid = [[0] * width for _ in range(height)]
    for j in range(width):
        grid[0][j] = color
        grid[height - 1][j] = color
    grid[1][0] = color
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    candidates = find_u_candidates(g)
    if not candidates:
        return [[0]]
    # Select the one with maximum area
    candidates.sort(reverse=True)
    _, l, color = candidates[0]
    return create_u_pattern(l, color)
```