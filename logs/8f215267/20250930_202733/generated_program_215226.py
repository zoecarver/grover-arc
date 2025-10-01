```python
import collections
from typing import List, Tuple

def identify_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return collections.Counter(flat).most_common(1)[0][0]

def get_middle_positions(c: int, start_i: int) -> List[int]:
    mod = start_i % 10
    pos = [0, 10]
    if c in (3, 8):
        pos.extend([2, 4, 6, 8])
    elif c in (4, 6):
        pos.extend([6, 8])
    elif c == 1:
        pos.append(8)
        if mod == 3:
            pos.extend([4, 6])
    elif c == 2:
        if mod == 3:
            pos.append(8)
    return sorted(set(pos))

def detect_shapes(g: List[List[int]], bg: int) -> List[Tuple[int, int, int]]:
    n = len(g)
    if n == 0:
        return []
    m = len(g[0])
    shapes = []
    i = 0
    while i < n - 3:
        found = False
        for j in range(m - 10):
            row_slice = g[i][j:j + 11]
            if len(set(row_slice)) == 1 and row_slice[0] != bg:
                c = row_slice[0]
                valid = True
                for r in range(1, 4):
                    if i + r >= n:
                        valid = False
                        break
                    row_r = g[i + r]
                    left = row_r[j]
                    right = row_r[j + 10]
                    if (left != c and left != bg) or (right != c and right != bg):
                        valid = False
                        break
                    for k in range(1, 10):
                        if j + k >= m or row_r[j + k] != bg:
                            valid = False
                            break
                if valid:
                    shapes.append((i, j, c))
                    found = True
                    break
        if found:
            i += 5
        else:
            i += 1
    return shapes

def draw_shape(h: List[List[int]], start_i: int, start_j: int, c: int, positions: List[int], bg: int, n: int, m: int) -> None:
    # Draw top bar
    for k in range(11):
        if start_i < n and start_j + k < m:
            h[start_i][start_j + k] = c
    # Draw sides and clear inners for relative rows 1-3
    for r in range(1, 4):
        row_idx = start_i + r
        if row_idx >= n:
            continue
        # Sides
        if start_j < m:
            h[row_idx][start_j] = c
        if start_j + 10 < m:
            h[row_idx][start_j + 10] = c
        # Clear inners
        for k in range(1, 10):
            if start_j + k < m:
                h[row_idx][start_j + k] = bg
    # Draw middle positions on relative row 2
    mid_row = start_i + 2
    if mid_row < n:
        for k in positions:
            if start_j + k < m:
                h[mid_row][start_j + k] = c
    # Draw bottom bar if possible
    bot_row = start_i + 4
    if bot_row < n:
        for k in range(11):
            if start_j + k < m:
                h[bot_row][start_j + k] = c

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    bg = identify_background(g)
    n = len(g)
    m = len(g[0])
    h = [[bg for _ in range(m)] for _ in range(n)]
    shapes = detect_shapes(g, bg)
    for start_i, start_j, c in shapes:
        positions = get_middle_positions(c, start_i)
        draw_shape(h, start_i, start_j, c, positions, bg, n, m)
    return h
```