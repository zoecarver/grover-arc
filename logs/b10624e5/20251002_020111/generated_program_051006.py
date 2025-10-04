```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    norm_g = normalize(g)
    norm_g = fill_upper_right(norm_g)
    norm_g = fill_180(norm_g)
    norm_g = complete_lower_left(norm_g)
    return denormalize(norm_g)

def normalize(g: List[List[int]]) -> List[List[int]]:
    map_to = {4: 0, 1: 1, 2: 2, 3: 3, 8: 5, 9: 4}
    return [[map_to.get(cell, cell) for cell in row] for row in g]

def denormalize(g: List[List[int]]) -> List[List[int]]:
    map_back = {0: 4, 1: 1, 2: 2, 3: 3, 4: 9, 5: 8}
    return [[map_back.get(cell, cell) for cell in row] for row in g]

def fill_upper_right(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    h, w = len(new_g), len(new_g[0])
    for r in range(13):
        c = 0
        while c < 13:
            if new_g[r][c] == 0:
                c += 1
                continue
            color = new_g[r][c]
            start_c = c
            while c < 13 and new_g[r][c] == color:
                c += 1
            end_c = c - 1
            target_start = w - 1 - end_c
            target_end = w - 1 - start_c
            can_set = all(new_g[r][tc] == 0 or new_g[r][tc] == color for tc in range(target_start, target_end + 1))
            if can_set:
                for tc in range(target_start, target_end + 1):
                    if new_g[r][tc] == 0:
                        new_g[r][tc] = color
            else:
                found = False
                for k in range(1, r + 1):
                    sr = r - k
                    if sr < 0:
                        break
                    if all(new_g[sr][tc] == 0 for tc in range(target_start, target_end + 1)):
                        for tc in range(target_start, target_end + 1):
                            new_g[sr][tc] = color
                        found = True
                        break
                if not found:
                    for k in range(1, 13 - r):
                        sr = r + k
                        if sr > 12:
                            break
                        if all(new_g[sr][tc] == 0 for tc in range(target_start, target_end + 1)):
                            for tc in range(target_start, target_end + 1):
                                new_g[sr][tc] = color
                            found = True
                            break
    return new_g

def fill_180(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    h, w = len(new_g), len(new_g[0])
    for r in range(13):
        for c in range(13):
            color = new_g[r][c]
            if color == 0:
                continue
            tr = h - 1 - r
            tc = w - 1 - c
            if new_g[tr][tc] == 0:
                new_g[tr][tc] = color
    return new_g

def complete_lower_left(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    h, w = len(new_g), len(new_g[0])
    for r in range(14, h):
        for c in range(13):
            if new_g[r][c] == 2 and is_single(new_g, r, c):
                if c + 1 < 13 and new_g[r][c + 1] == 0:
                    new_g[r][c + 1] = 3
                if r + 1 < h and new_g[r + 1][c] == 0:
                    new_g[r + 1][c] = 5
    return new_g

def is_single(g: List[List[int]], r: int, c: int) -> bool:
    h, w = len(g), len(g[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < h and 0 <= nc < w and g[nr][nc] == 2:
            return False
    return True
```