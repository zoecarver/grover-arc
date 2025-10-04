```python
from typing import List, Dict, Set, Tuple

def find_non_zero_colors(g: List[List[int]]) -> Set[int]:
    colors: Set[int] = set()
    for row in g:
        for cell in row:
            if cell != 0:
                colors.add(cell)
    return colors

def max_component_size(g: List[List[int]], c: int) -> int:
    if not g:
        return 0
    rows: int = len(g)
    cols: int = len(g[0])
    visited: List[List[bool]] = [[False] * cols for _ in range(rows)]
    max_size: int = 0
    directions: List[Tuple[int, int]] = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    def dfs(x: int, y: int) -> int:
        stack: List[Tuple[int, int]] = [(x, y)]
        visited[x][y] = True
        size: int = 1
        while stack:
            cx, cy = stack.pop()
            for dx, dy in directions:
                nx: int = cx + dx
                ny: int = cy + dy
                if 0 <= nx < rows and 0 <= ny < cols and g[nx][ny] == c and not visited[nx][ny]:
                    visited[nx][ny] = True
                    stack.append((nx, ny))
                    size += 1
        return size
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == c and not visited[i][j]:
                comp_size: int = dfs(i, j)
                if comp_size > max_size:
                    max_size = comp_size
    return max_size

def compute_metrics(g: List[List[int]]) -> Dict[int, int]:
    colors: Set[int] = find_non_zero_colors(g)
    metrics: Dict[int, int] = {}
    for c in colors:
        metrics[c] = max_component_size(g, c)
    return metrics

def select_filler(metrics: Dict[int, int]) -> int:
    if not metrics:
        return 0
    max_metric: int = max(metrics.values())
    candidates: List[int] = [c for c, m in metrics.items() if m == max_metric]
    return max(candidates)

def build_output_row(c: int, size: int, filler: int) -> List[int]:
    effective_size = min(size, 4)
    return [c] * effective_size + [filler] * (4 - effective_size)

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    has_colors = any(any(cell != 0 for cell in row) for row in g)
    if not has_colors:
        return []
    metrics = compute_metrics(g)
    filler = select_filler(metrics)
    non_filler_colors = [c for c in metrics if c != filler]
    non_filler_colors.sort(key=lambda c: (metrics[c], c))
    output = []
    for c in non_filler_colors:
        row = build_output_row(c, metrics[c], filler)
        output.append(row)
    return output
```