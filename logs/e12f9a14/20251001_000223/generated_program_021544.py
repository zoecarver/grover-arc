```python
from typing import List
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def find_blocks(g: List[List[int]], bg: int) -> List[tuple[int, int, int]]:
    blocks = []
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    for r in range(h - 1):
        for k in range(w - 1):
            c = g[r][k]
            if c != bg and c != 3 and g[r][k + 1] == c and g[r + 1][k] == c and g[r + 1][k + 1] == c:
                blocks.append((r, k, c))
    return sorted(blocks, key=lambda x: (x[0], x[1]))

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    bg = get_background(g)
    current = [row[:] for row in g]
    while True:
        blocks = find_blocks(current, bg)
        if not blocks:
            break
        temp = [row[:] for row in current]
        changed = False
        for r, k, c in blocks:
            # horizontal on both rows
            for rr in [r, r + 1]:
                # left
                cc = k - 1
                while cc >= 0:
                    cell = temp[rr][cc]
                    if cell == bg:
                        temp[rr][cc] = c
                        changed = True
                    elif cell != c:
                        break
                    cc -= 1
                # right
                cc = k + 2
                while cc < w:
                    cell = temp[rr][cc]
                    if cell == bg:
                        temp[rr][cc] = c
                        changed = True
                    elif cell != c:
                        break
                    cc += 1
            # vertical on both columns
            for col in [k, k + 1]:
                # up
                rr = r - 1
                while rr >= 0:
                    cell = temp[rr][col]
                    if cell == bg:
                        temp[rr][col] = c
                        changed = True
                    elif cell != c:
                        break
                    rr -= 1
                # down
                rr = r + 2
                while rr < h:
                    cell = temp[rr][col]
                    if cell == bg:
                        temp[rr][col] = c
                        changed = True
                    elif cell != c:
                        break
                    rr += 1
            # diagonals
            diag_starts = [(r - 1, k - 1, -1, -1), (r - 1, k + 2, -1, 1), (r + 2, k - 1, 1, -1), (r + 2, k + 2, 1, 1)]
            for sr, sc, dr, dc in diag_starts:
                rr = sr
                cc = sc
                while 0 <= rr < h and 0 <= cc < w:
                    cell = temp[rr][cc]
                    if cell == bg:
                        temp[rr][cc] = c
                        changed = True
                    elif cell != c:
                        break
                    rr += dr
                    cc += dc
        current = temp
        if not changed:
            break
    return current
```