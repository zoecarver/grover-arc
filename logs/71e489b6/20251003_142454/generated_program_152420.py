```python
def num_1_neighbors(r: int, c: int, g: List[List[int]], rows: int, cols: int) -> int:
    count = 0
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in dirs:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 1:
            count += 1
    return count


def is_isolated_blue(r: int, c: int, g: List[List[int]], rows: int, cols: int) -> bool:
    if g[r][c] != 1:
        return False
    return num_1_neighbors(r, c, g, rows, cols) == 0


def fill_isolated_blues(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    output = [row[:] for row in g]
    for r in range(rows):
        for c in range(cols):
            if is_isolated_blue(r, c, g, rows, cols):
                output[r][c] = 0
    return output


def is_small_hole_center(r: int, c: int, g: List[List[int]], rows: int, cols: int) -> bool:
    if g[r][c] != 0:
        return False
    return num_1_neighbors(r, c, g, rows, cols) >= 3


def apply_horizontal_highlight(r: int, c: int, output: List[List[int]], g: List[List[int]], cols: int) -> None:
    if c - 1 >= 0 and g[r][c - 1] == 1:
        output[r][c - 1] = 7
    if c + 1 < cols and g[r][c + 1] == 1:
        output[r][c + 1] = 7


def apply_vertical_highlight(r: int, c: int, output: List[List[int]], g: List[List[int]], rows: int, cols: int, direction: int) -> None:
    tr = r + direction
    if 0 <= tr < rows:
        for k in [-1, 0, 1]:
            tc = c + k
            if 0 <= tc < cols:
                if g[tr][tc] == 1:
                    output[tr][tc] = 7
                elif g[tr][tc] == 0 and num_1_neighbors(tr, tc, g, rows, cols) <= 1:
                    output[tr][tc] = 7


def highlight_small_holes(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    output = [row[:] for row in g]
    for r in range(rows):
        for c in range(cols):
            if is_small_hole_center(r, c, g, rows, cols):
                apply_horizontal_highlight(r, c, output, g, cols)
                apply_vertical_highlight(r, c, output, g, rows, cols, -1)
                apply_vertical_highlight(r, c, output, g, rows, cols, 1)
    return output


def program(g: List[List[int]]) -> List[List[int]]:
    temp = fill_isolated_blues(g)
    return highlight_small_holes(temp)
```