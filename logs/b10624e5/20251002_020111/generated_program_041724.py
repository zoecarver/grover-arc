```python
def flip_horizontal(p: List[List[int]]) -> List[List[int]]:
    return [row[::-1] for row in p]

def flip_vertical(p: List[List[int]]) -> List[List[int]]:
    return p[::-1]

def flip_180(p: List[List[int]]) -> List[List[int]]:
    return flip_horizontal(flip_vertical(p))

def overlay_pattern(g: List[List[int]], pattern: List[List[int]], row_start: int, col_start: int):
    n = 13
    for i in range(n):
        for j in range(n):
            p = pattern[i][j]
            if p != 4:
                r = row_start + i
                c = col_start + j
                if g[r][c] == 4:
                    g[r][c] = p

def program(g: List[List[int]]) -> List[List[int]]:
    g = [row[:] for row in g]
    top_left = [row[0:13] for row in g[0:13]]
    # Top-right: horizontal flip with row shift up to avoid conflict
    flipped_h = flip_horizontal(top_left)
    n = 13
    k = 0
    for possible_k in range(n):
        conflict = False
        for i in range(n):
            tr = i - possible_k
            if 0 <= tr < n:
                for j in range(n):
                    p = flipped_h[i][j]
                    if p != 4:
                        tc = 14 + j
                        current = g[tr][tc]
                        if current != 4 and current != p:
                            conflict = True
                            break
                if conflict:
                    break
        if not conflict:
            k = possible_k
            break
    # Place with shift k
    for i in range(n):
        tr = i - k
        if 0 <= tr < n:
            for j in range(n):
                p = flipped_h[i][j]
                if p != 4:
                    tc = 14 + j
                    current = g[tr][tc]
                    if current == 4 or current == p:
                        g[tr][tc] = p
    # Bottom-left: vertical flip, simple overlay
    flipped_v = flip_vertical(top_left)
    overlay_pattern(g, flipped_v, 14, 0)
    # Bottom-right: 180 flip, simple overlay
    flipped_180 = flip_180(top_left)
    overlay_pattern(g, flipped_180, 14, 14)
    return g
```