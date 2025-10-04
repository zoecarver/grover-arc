```python
from typing import List, Dict, Tuple
import collections

def find_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return collections.Counter(flat).most_common(1)[0][0]

def extract_color_positions(g: List[List[int]], bg: int) -> Dict[int, List[Tuple[int, int]]]:
    positions = collections.defaultdict(list)
    h = len(g)
    w = len(g[0])
    for r in range(h):
        for c in range(w):
            val = g[r][c]
            if val != bg:
                positions[val].append((r, c))
    return dict(positions)

def compute_flags(positions: Dict[int, List[Tuple[int, int]]]) -> Tuple[bool, bool]:
    has7 = 7 in positions
    has9 = 9 in positions
    return has7, has9

def decide_placement(color: int, has7: bool, has9: bool) -> str:
    if color == 3:
        return 'top'
    if color == 4:
        return 'bottom'
    if color == 1:
        return 'bottom' if has9 else 'top'
    if color == 2:
        return 'top' if has7 else 'bottom'
    if color in (7, 9):
        return 'top'
    return 'top'

def get_min_max(pos: List[Tuple[int, int]]) -> Tuple[int, int]:
    if not pos:
        return 0, 0
    rs = [r for r, _ in pos]
    return min(rs), max(rs)

def compute_delta(placement: str, min_r: int, max_r: int, h: int) -> int:
    if placement == 'top':
        return -min_r
    return h - 1 - max_r

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h = len(g)
    w = len(g[0])
    bg = find_background(g)
    positions = extract_color_positions(g, bg)
    has7, has9 = compute_flags(positions)
    out = [[bg] * w for _ in range(h)]
    for color, pos in positions.items():
        placement = decide_placement(color, has7, has9)
        min_r, max_r = get_min_max(pos)
        delta = compute_delta(placement, min_r, max_r, h)
        for r, c in pos:
            nr = r + delta
            if 0 <= nr < h:
                out[nr][c] = color
    return out
```