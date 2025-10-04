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
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    def dfs(r: int, c: int, val: int, positions: List[Tuple[int, int]]):
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            if 0 <= cr < rows and 0 <= cc < cols and not visited[cr][cc] and g[cr][cc] == val:
                visited[cr][cc] = True
                positions.append((cr, cc))
                for dr, dc in directions:
                    stack.append((cr + dr, cc + dc))

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c] and g[r][c] != 1:
                val = g[r][c]
                positions = []
                dfs(r, c, val, positions)
                if len(positions) >= 1:
                    regions[val].append(GridRegion(val, positions))
    return regions

def fill_regions(g: List[List[int]], regions: Dict[int, List[GridRegion]]) -> List[List[int]]:
    all_regions = []
    for val, reg_list in regions.items():
        all_regions.extend(reg_list)
    all_regions.sort(key=lambda rg: len(rg.positions), reverse=True)
    h, w = len(g), len(g[0]) if g else 0
    output = [[0] * w for _ in range(h)]
    for region in all_regions:
        min_r, max_r, min_c, max_c = region.bbox
        for rr in range(max(0, min_r), min(h, max_r + 1)):
            for cc in range(max(0, min_c), min(w, max_c + 1)):
                output[rr][cc] = region.value
    return output

def transpose_grid(grid: List[List[int]]) -> List[List[int]]:
    if not grid or not grid[0]:
        return []
    return [list(row) for row in zip(*grid)]

def program(g: List[List[int]]) -> List[List[int]]:
    regions = extract_regions(g)
    filled = fill_regions(g, regions)
    result = transpose_grid(filled)
    return result
```