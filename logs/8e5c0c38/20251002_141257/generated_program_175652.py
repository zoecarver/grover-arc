```python
from typing import List
from collections import Counter, deque

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def rotate90(p: List[List[int]]) -> List[List[int]]:
    return [list(row) for row in zip(*p[::-1])]

def flatten(p: List[List[int]]) -> tuple:
    return tuple(sum(p, []))

def generate_patterns(bases: List[List[List[int]]]) -> set:
    patterns = set()
    for base in bases:
        current = base
        for _ in range(4):
            patterns.add(flatten(current))
            current = rotate90(current)
    return patterns

def extract_3x3_pattern(g: List[List[int]], i: int, j: int, color: int) -> List[List[int]]:
    h, w = len(g), len(g[0])
    p = []
    for di in range(-1, 2):
        row = []
        for dj in range(-1, 2):
            ni, nj = i + di, j + dj
            row.append(1 if 0 <= ni < h and 0 <= nj < w and g[ni][nj] == color else 0)
        p.append(row)
    return p

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    bg = get_background(g)
    h, w = len(g), len(g[0])
    bases = [
        [[0, 0, 0], [0, 1, 0], [0, 1, 0]],  # vertical pair top
        [[0, 0, 0], [0, 1, 1], [0, 0, 0]],  # horizontal left end no below
        [[0, 0, 1], [0, 1, 1], [0, 1, 1]],  # L bottom left
        [[0, 1, 1], [0, 1, 1], [0, 0, 0]],  # L upper left
        [[0, 0, 0], [1, 1, 1], [0, 1, 1]],  # horizontal 3 with below right 2
        [[0, 0, 0], [1, 1, 0], [1, 1, 0]],  # horizontal end with below
        [[1, 1, 0], [0, 1, 1], [0, 0, 0]],  # flipped L
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]   # single
    ]
    bad_patterns = generate_patterns(bases)
    out = [row[:] for row in g]
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            if g[i][j] != bg:
                p = extract_3x3_pattern(g, i, j, g[i][j])
                flat = flatten(p)
                if flat in bad_patterns:
                    out[i][j] = bg
    return out
```