```python
from typing import List, Dict, Tuple
from collections import Counter, defaultdict

def find_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def extract_positions(g: List[List[int]], bg: int) -> Dict[int, List[Tuple[int, int]]]:
    positions = defaultdict(list)
    h = len(g)
    w = len(g[0])
    for r in range(h):
        for c in range(w):
            if g[r][c] != bg:
                positions[g[r][c]].append((r, c))
    return dict(positions)

def has_special_colors(positions: Dict[int, List[Tuple[int, int]]]) -> Tuple[bool, bool]:
    return 7 in positions, 9 in positions

def decide_placement(c: int, has7: bool, has9: bool) -> str:
    if c in (3, 7, 9):
        return 'top'
    if c == 4:
        return 'bottom'
    if c == 1:
        return 'bottom' if has9 else 'top'
    if c == 2:
        return 'top' if has7 else 'bottom'
    return 'top'

def compute_shift(pos: List[Tuple[int, int]], placement: str, h: int) -> int:
    if not pos:
        return 0
    rs = [r for r, _ in pos]
    min_r = min(rs)
    max_r = max(rs)
    if placement == 'top':
        return -min_r
    return h - 1 - max_r

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    bg = find_background(g)
    positions = extract_positions(g, bg)
    has7, has9 = has_special_colors(positions)
    out = [[bg] * w for _ in range(h)]
    for c, pos in positions.items():
        placement = decide_placement(c, has7, has9)
        delta = compute_shift(pos, placement, h)
        for r, col in pos:
            nr = r + delta
            if 0 <= nr < h:
                out[nr][col] = c
    return out
```