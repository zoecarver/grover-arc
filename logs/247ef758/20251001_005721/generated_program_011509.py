```python
from typing import List, Dict
from collections import defaultdict

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    n = len(grid)
    m = len(grid[0]) if n > 0 else 0
    if n < 3 or m < 2:
        return grid
    middle_rows = list(range(1, n - 1))
    # Find spine column
    spine = -1
    max_count = 0
    for j in range(m):
        colors = [grid[i][j] for i in middle_rows]
        non_zero_colors = [col for col in colors if col != 0]
        if non_zero_colors and len(set(non_zero_colors)) == 1:
            count = len(non_zero_colors)
            if count > max_count:
                max_count = count
                spine = j
    if spine == -1:
        # Fallback to first constant non-zero column
        for j in range(m):
            colors = [grid[i][j] for i in middle_rows]
            if all(c == colors[0] for c in colors) and colors[0] != 0:
                spine = j
                break
    row_color_col = spine + 1 if spine != -1 else 0
    # Used row colors
    used_row_colors: set = set()
    for i in middle_rows:
        c = grid[i][row_color_col]
        if c != 0:
            used_row_colors.add(c)
    # Clear left
    for i in middle_rows:
        for j in range(spine):
            c = grid[i][j]
            if c != 0 and c in used_row_colors:
                grid[i][j] = 0
    # Set last column
    for i in middle_rows:
        grid[i][m - 1] = grid[i][row_color_col]
    # R_cs
    r_cs: Dict[int, List[int]] = defaultdict(list)
    for i in middle_rows:
        c = grid[i][row_color_col]
        if c != 0:
            r_cs[c].append(i)
    # Special positions in top
    special = []
    for j in range(row_color_col + 1, m - 1):
        c = grid[0][j]
        if c != 0 and c != grid[0][j - 1] and c != grid[0][j + 1]:
            special.append(j)
    # Groups of adjacent specials
    groups = []
    if special:
        current = [special[0]]
        for j in special[1:]:
            if j == current[-1] + 1:
                current.append(j)
            else:
                groups.append(current)
                current = [j]
        groups.append(current)
    # Function to do single fill
    def do_single(p: int, c: int):
        if p < m // 2:
            return
        count_c = sum(1 for jj in range(m) if grid[0][jj] == c)
        fill_center = count_c >= 2
        for r in r_cs[c]:
            # Sides in r
            for dj in [-1, 1]:
                jj = p + dj
                if row_color_col < jj < m - 1 and grid[r][jj] == 0:
                    grid[r][jj] = c
            # Center in r if condition
            if fill_center and grid[r][p] == 0:
                grid[r][p] = c
            # Centers in adjacent
            for dr in [-1, 1]:
                nr = r + dr
                if 1 <= nr <= n - 2 and grid[nr][p] == 0:
                    grid[nr][p] = c
    # Process groups
    for group in groups:
        if len(group) == 1:
            do_single(group[0], grid[0][group[0]])
        elif len(group) == 2:
            p1 = group[0]
            c1 = grid[0][p1]
            p2 = group[1]
            c2 = grid[0][p2]
            if len(r_cs[c1]) == 1 and len(r_cs[c2]) == 1:
                r1 = r_cs[c1][0]
                r2 = r_cs[c2][0]
                # Full in r1 for p1
                for jj in range(p1 - 1, p1 + 2):
                    if row_color_col < jj < m - 1 and grid[r1][jj] == 0:
                        grid[r1][jj] = c1
                # Full in r2 for p2
                for jj in range(p2 - 1, p2 + 2):
                    if row_color_col < jj < m - 1 and grid[r2][jj] == 0:
                        grid[r2][jj] = c2
                # Adjacent centers for first
                for dr in [-1, 1]:
                    nr = r1 + dr
                    if 1 <= nr <= n - 2 and grid[nr][p1] == 0:
                        grid[nr][p1] = c1
                # Adjacent centers for second
                for dr in [-1, 1]:
                    nr = r2 + dr
                    if 1 <= nr <= n - 2 and grid[nr][p2] == 0:
                        grid[nr][p2] = c2
                # Additional lower full for second
                nr = r2 + 1
                if 1 <= nr <= n - 2:
                    for jj in range(p2 - 1, p2 + 2):
                        if row_color_col < jj < m - 1 and grid[nr][jj] == 0:
                            grid[nr][jj] = c2
                # Common if applicable
                if r1 + 1 == r2 - 1:
                    common_r = r1 + 1
                    # Additional right side for second
                    if p2 + 1 < m - 1 and grid[common_r][p2 + 1] == 0:
                        grid[common_r][p2 + 1] = c2
            else:
                # Treat as two singles
                do_single(p1, c1)
                do_single(p2, c2)
        else:
            # Treat as singles
            for p in group:
                do_single(p, grid[0][p])
    return grid
```