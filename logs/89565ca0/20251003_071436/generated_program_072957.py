```python
from typing import List, Dict, Set, Tuple

def find_non_zero_colors(g: List[List[int]]) -> Set[int]:
    """Find all distinct non-zero colors in the grid."""
    colors: Set[int] = set()
    for row in g:
        for cell in row:
            if cell != 0:
                colors.add(cell)
    return colors

def max_component_size(g: List[List[int]], c: int) -> int:
    """Compute the size of the largest 8-connected component for color c in the grid."""
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
            cx: int
            cy: int
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
    """Compute the max component size metric for each non-zero color."""
    colors: Set[int] = find_non_zero_colors(g)
    metrics: Dict[int, int] = {}
    for c in colors:
        metrics[c] = max_component_size(g, c)
    return metrics

def select_filler(metrics: Dict[int, int]) -> int:
    """Select the filler color as the one with the highest metric, breaking ties by max color value."""
    if not metrics:
        return 0
    max_metric: int = max(metrics.values())
    candidates: List[int] = [c for c, m in metrics.items() if m == max_metric]
    return max(candidates)

def get_other_colors_sorted(metrics: Dict[int, int], filler: int) -> List[int]:
    """Get non-filler colors sorted by increasing metric, then by increasing color value."""
    others: List[int] = [c for c in metrics if c != filler]
    def sort_key(c: int) -> Tuple[int, int]:
        return (metrics[c], c)
    others.sort(key=sort_key)
    return others

def build_output_row(c: int, metric: int, filler: int) -> List[int]:
    """Build a single output row for color c with width min(metric, 4), padded with filler to width 4."""
    w: int = min(metric, 4)
    return [c] * w + [filler] * (4 - w)

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: compute metrics, select filler, sort others, build output rows."""
    if not g:
        return []
    has_colors: bool = any(any(cell != 0 for cell in row) for row in g)
    if not has_colors:
        return []
    metrics: Dict[int, int] = compute_metrics(g)
    filler: int = select_filler(metrics)
    others: List[int] = get_other_colors_sorted(metrics, filler)
    output: List[List[int]] = []
    for c in others:
        row: List[int] = build_output_row(c, metrics[c], filler)
        output.append(row)
    return output
```