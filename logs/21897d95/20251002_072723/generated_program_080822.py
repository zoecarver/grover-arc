```python
from typing import List, Tuple, Dict
from collections import defaultdict

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
        return min(rows), max(rows), min(cols), max(cols)

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
            if not visited[r][c]:
                val = g[r][c]
                positions = []
                dfs(r, c, val, positions)
                if len(positions) >= 3:
                    regions[val].append(GridRegion(val, positions))
    return regions

def fill_large_regions(g: List[List[int]], regions: Dict[int, List[GridRegion]]) -> List[List[int]]:
    all_regions = []
    for val, reg_list in regions.items():
        all_regions.extend(reg_list)
    all_regions.sort(key=lambda rg: len(rg.positions), reverse=True)
    h, w = len(g), len(g[0]) if g else 0
    output = [[0] * w for _ in range(h)]
    for region in all_regions:
        min_r, max_r, min_c, max_c = region.bbox
        for rr in range(min_r, max_r + 1):
            for cc in range(min_c, max_c + 1):
                if 0 <= rr < h and 0 <= cc < w:
                    output[rr][cc] = region.value
    return output

def transpose_grid(grid: List[List[int]]) -> List[List[int]]:
    if not grid or not grid[0]:
        return []
    return [list(row) for row in zip(*grid)]

def program(g: List[List[int]]) -> List[List[int]]:
    regions = extract_regions(g)
    filled = fill_large_regions(g, regions)
    return transpose_grid(filled)
```