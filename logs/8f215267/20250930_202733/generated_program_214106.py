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

def get_middle_positions(c: int, start_row: int) -> List[int]:
    mod = start_row % 10
    pos = [0, 10]
    if c == 1:
        pos.append(8)
        if mod == 3:
            pos.append(6)
    elif c == 2:
        if mod == 3:
            pos.append(8)
    elif c == 3:
        pos.extend([2, 4, 6, 8])
    elif c == 4:
        pos.extend([6, 8])
    elif c == 6:
        pos.extend([4, 6, 8])
    elif c == 8:
        pos.extend([2, 4, 6, 8])
    return sorted(set(pos))

def detect_shapes(g: List[List[int]], bg: int) -> List[Tuple[int, int, int]]:
    n = len(g)
    if n == 0:
        return []
    m = len(g[0])
    shapes = []
    i = 0
    while i < n - 4:
        found = False
        for j in range(m - 10):
            row_slice = g[i][j:j+11]
            if len(set(row_slice)) == 1 and row_slice[0] != bg:
                c = row_slice[0]
                valid = True
                for r in range(1, 4):
                    if i + r >= n:
                        valid = False
                        break
                    row_r = g[i + r]
                    if (row_r[j] != c and row_r[j] != bg) or (row_r[j + 10] != c and row_r[j + 10] != bg):
                        valid = False
                        break
                    for k in range(1, 10):
                        if row_r[j + k] != bg:
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
        if start_j + k < m:
            h[start_i][start_j + k] = c
    # Draw sides and clear middles for rows 1-3 relative
    for r in range(1, 4):
        if start_i + r >= n:
            return
        # Sides
        if start_j < m:
            h[start_i + r][start_j] = c
        if start_j + 10 < m:
            h[start_i + r][start_j + 10] = c
        # Clear inner positions
        for k in range(1, 10):
            if start_j + k < m:
                h[start_i + r][start_j + k] = bg
    # Draw middle positions on relative row 2
    for k in positions:
        if start_i + 2 < n and start_j + k < m:
            h[start_i + 2][start_j + k] = c
    # Draw bottom bar if possible
    if start_i + 4 < n:
        for k in range(11):
            if start_j + k < m:
                h[start_i + 4][start_j + k] = c

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