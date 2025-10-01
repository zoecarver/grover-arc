```python
from typing import List
from collections import defaultdict

def find_spine(grid: List[List[int]], middle_rows: List[int], m: int) -> int:
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
        for j in range(m):
            colors = [grid[i][j] for i in middle_rows]
            if all(c == colors[0] for c in colors) and colors[0] != 0:
                spine = j
                break
    return spine

def find_specials(grid: List[List[int]], row_color_col: int, m: int) -> List[int]:
    special = []
    for j in range(row_color_col + 1, m - 1):
        c = grid[0][j]
        if c != 0 and c != grid[0][j - 1] and c != grid[0][j + 1]:
            special.append(j)
    return special

def group_specials(special: List[int]) -> List[List[int]]:
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
    return groups

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    n = len(grid)
    if n < 3:
        return grid
    m = len(grid[0])
    middle_rows = list(range(1, n - 1))
    spine = find_spine(grid, middle_rows, m)
    if spine == -1 or spine >= m - 1:
        return grid
    row_color_col = spine + 1
    # Set last column for middle rows
    for i in middle_rows:
        grid[i][m - 1] = grid[i][row_color_col]
    # Forbidden colors from top and bottom in columns >= spine
    forbidden = set()
    for ii in [0, n - 1]:
        for jj in range(spine, m):
            cc = grid[ii][jj]
            if cc != 0:
                forbidden.add(cc)
    # Clear conflicting colors left of spine in all rows
    for i in range(n):
        for j in range(spine):
            cc = grid[i][j]
            if cc != 0 and cc in forbidden:
                grid[i][j] = 0
    # r_cs: color to list of middle row indices with that color in row_color_col
    r_cs = defaultdict(list)
    for i in middle_rows:
        cc = grid[i][row_color_col]
        if cc != 0:
            r_cs[cc].append(i)
    # Find specials in updated top row
    specials = find_specials(grid, row_color_col, m)
    # Group adjacent specials
    groups = group_specials(specials)
    # Process each group from left to right
    for group in groups:
        glen = len(group)
        if glen == 1:
            j = group[0]
            c = grid[0][j]
            mains = [ii for ii in r_cs[c] if ii <= j]
            if not mains:
                continue
            is_near_end = (j >= m - 3)
            left = max(row_color_col, j - 1)
            right = min(m - 2, j + 1)
            for i in mains:
                for k in range(left, right + 1):
                    if is_near_end and k == j:
                        continue
                    if grid[i][k] == 0:
                        grid[i][k] = c
            # Adjacent centers
            for i in mains:
                for di in [-1, 1]:
                    k = i + di
                    if 1 <= k <= n - 2 and grid[k][j] == 0:
                        grid[k][j] = c
        elif glen == 2:
            j1 = group[0]
            j2 = group[1]
            c1 = grid[0][j1]
            c2 = grid[0][j2]
            mains1 = [ii for ii in r_cs[c1] if ii <= j1]
            mains2 = [ii for ii in r_cs[c2] if ii <= j2]
            # Fill for first
            for i1 in mains1:
                left1 = max(row_color_col, j1 - 1)
                right1 = min(m - 2, j1 + 1)
                for k in range(left1, right1 + 1):
                    if grid[i1][k] == 0:
                        grid[i1][k] = c1
                # Adjacent centers for first
                for di in [-1, 1]:
                    k = i1 + di
                    if 1 <= k <= n - 2 and grid[k][j1] == 0:
                        grid[k][j1] = c1
            # Fill for second
            for i2 in mains2:
                left2 = max(row_color_col, j2 - 1)
                right2 = min(m - 2, j2 + 1)
                for k in range(left2, right2 + 1):
                    if grid[i2][k] == 0:
                        grid[i2][k] = c2
                # Adjacent centers for second
                for di in [-1, 1]:
                    k = i2 + di
                    if 1 <= k <= n - 2 and grid[k][j2] == 0:
                        grid[k][j2] = c2
            # Extra sides for second's adjacent rows
            for i2 in mains2:
                for di in [-1, 1]:
                    k = i2 + di
                    if 1 <= k <= n - 2:
                        # left side
                        kl = j2 - 1
                        if kl >= row_color_col and grid[k][kl] == 0:
                            grid[k][kl] = c2
                        # right side
                        kr = j2 + 1
                        if kr <= m - 2 and grid[k][kr] == 0:
                            grid[k][kr] = c2
        elif glen == 3:
            j1, j2, j3 = group
            c1 = grid[0][j1]
            c2 = grid[0][j2]
            c3 = grid[0][j3]
            if c1 == c3 and c1 != c2:
                # Symmetric triple, handle middle only
                mains = [ii for ii in r_cs[c2] if ii <= j2]
                for i in mains:
                    kl = j2 - 1
                    kr = j2 + 1
                    if kl >= row_color_col and grid[i][kl] == 0:
                        grid[i][kl] = c2
                    if kr <= m - 2 and grid[i][kr] == 0:
                        grid[i][kr] = c2
                # Adjacent centers for middle
                for i in mains:
                    for di in [-1, 1]:
                        k = i + di
                        if 1 <= k <= n - 2 and grid[k][j2] == 0:
                            grid[k][j2] = c2
            else:
                # Treat as three singles
                for jj in group:
                    cc = grid[0][jj]
                    mainss = [iii for iii in r_cs[cc] if iii <= jj]
                    if not mainss:
                        continue
                    is_near = (jj >= m - 3)
                    l = max(row_color_col, jj - 1)
                    r = min(m - 2, jj + 1)
                    for ii in mainss:
                        for kk in range(l, r + 1):
                            if is_near and kk == jj:
                                continue
                            if grid[ii][kk] == 0:
                                grid[ii][kk] = cc
                    for ii in mainss:
                        for ddi in [-1, 1]:
                            kk = ii + ddi
                            if 1 <= kk <= n - 2 and grid[kk][jj] == 0:
                                grid[kk][jj] = cc
        else:
            # Longer groups, treat as singles
            for jj in group:
                cc = grid[0][jj]
                mainss = [iii for iii in r_cs[cc] if iii <= jj]
                if not mainss:
                    continue
                is_near = (jj >= m - 3)
                l = max(row_color_col, jj - 1)
                r = min(m - 2, jj + 1)
                for ii in mainss:
                    for kk in range(l, r + 1):
                        if is_near and kk == jj:
                            continue
                        if grid[ii][kk] == 0:
                            grid[ii][kk] = cc
                for ii in mainss:
                    for ddi in [-1, 1]:
                        kk = ii + ddi
                        if 1 <= kk <= n - 2 and grid[kk][jj] == 0:
                            grid[kk][jj] = cc
    return grid
```