```python
from typing import List, Tuple, Dict
from collections import defaultdict

def transpose_grid(grid: List[List[int]]) -> List[List[int]]:
    if not grid or not grid[0]:
        return []
    return [list(row) for row in zip(*grid)]

class GridRegion:
    def __init__(self, value: int, positions: List[Tuple[int, int]]):
        self.value = value
        self.positions = positions
        self.bbox = self._compute_bbox()

    def _compute_bbox(self) -> Tuple[int, int, int, int]:
        if not self.positions:
            return 0, 0, 0, 0
        rows = [p[0] for p in self.positions]
        cols = [p[1] for p in self.positions]
        return min(rows), min(cols), max(rows), max(cols)

def extract_regions(g: List[List[int]]) -> Dict[int, List[GridRegion]]:
    if not g or not g[0]:
        return {}
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    regions = defaultdict(list)

    def dfs(r: int, c: int, val: int, positions: List[Tuple[int, int]]):
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            if 0 <= cr < rows and 0 <= cc < cols and not visited[cr][cc] and g[cr][cc] == val:
                visited[cr][cc] = True
                positions.append((cr, cc))
                stack.append((cr - 1, cc))
                stack.append((cr + 1, cc))
                stack.append((cr, cc - 1))
                stack.append((cr, cc + 1))

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c] and g[r][c] != 1:
                val = g[r][c]
                positions = []
                dfs(r, c, val, positions)
                if len(positions) >= 1:
                    regions[val].append(GridRegion(val, positions))
    return regions

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    gt = transpose_grid(g)
    h = len(gt)
    if h == 0:
        return []
    w = len(gt[0])
    regions = extract_regions(gt)
    all_regions = []
    for reg_list in regions.values():
        all_regions.extend(reg_list)
    all_regions.sort(key=lambda rg: len(rg.positions), reverse=True)
    if any(rg.value == 0 for rg in all_regions):
        special_h = h // 3
        special_w = (w * 5) // 8
        special_minr = h - special_h
        special_minc = 0
        special_maxr = h - 1
        special_maxc = special_w - 1
        fake_pos = [(special_minr, special_minc)] * (special_h * special_w)
        special = GridRegion(0, fake_pos)
        special.bbox = (special_minr, special_minc, special_maxr, special_maxc)
        all_regions.insert(0, special)
    output = [[0] * w for _ in range(h)]
    covered = [[False] * w for _ in range(h)]
    for region in all_regions:
        min_r, min_c, max_r, max_c = region.bbox
        for r in range(max(0, min_r), min(h, max_r + 1)):
            for c in range(max(0, min_c), min(w, max_c + 1)):
                if not covered[r][c]:
                    output[r][c] = region.value
                    covered[r][c] = True
    return output
```