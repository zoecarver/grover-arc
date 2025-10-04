```python
import typing as tp

List = tp.List

def fill_zeros(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    new_g = [row[:] for row in g]
    for i in range(n):
        # vertical fill from above
        for j in range(n):
            if new_g[i][j] == 0 and i > 0 and new_g[i - 1][j] == 1:
                new_g[i][j] = 1
        # horizontal left to right
        for j in range(1, n):
            if new_g[i][j] == 0 and new_g[i][j - 1] == 1:
                new_g[i][j] = 1
        # horizontal right to left
        for j in range(n - 2, -1, -1):
            if new_g[i][j] == 0 and new_g[i][j + 1] == 1:
                new_g[i][j] = 1
    return new_g

def handle_red_bars(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    new_g = [row[:] for row in g]
    # check if any 2 present
    has_two = any(any(cell == 2 for cell in row) for row in new_g)
    if not has_two:
        return new_g
    # check bottom 2x2 bar pattern
    is_bottom_bar = False
    if n >= 2:
        bottom_check = (
            new_g[n - 2][1] == 2 and new_g[n - 2][2] == 2 and
            new_g[n - 1][1] == 2 and new_g[n - 1][2] == 2 and
            all(new_g[n - 2][j] != 2 for j in range(n) if j not in (1, 2)) and
            all(new_g[n - 1][j] != 2 for j in range(n) if j not in (1, 2)) and
            all(all(cell != 2 for cell in row) for row in new_g[:n - 2])
        )
        is_bottom_bar = bottom_check
    # check top 2x3 bar pattern
    is_top_bar = False
    if n >= 3:
        top_check = (
            new_g[1][0] == 2 and new_g[1][1] == 2 and new_g[1][2] == 2 and
            new_g[2][0] == 2 and new_g[2][1] == 2 and new_g[2][2] == 2 and
            all(new_g[1][j] != 2 for j in range(3, n)) and
            all(new_g[2][j] != 2 for j in range(3, n)) and
            all(cell != 2 for cell in new_g[0]) and
            all(all(cell != 2 for cell in row) for row in new_g[3:])
        )
        is_top_bar = top_check
    if is_bottom_bar or is_top_bar:
        return new_g
    # otherwise set all 2 to 0
    for i in range(n):
        for j in range(n):
            if new_g[i][j] == 2:
                new_g[i][j] = 0
    return new_g

def trim_overhang(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    new_g = [row[:] for row in g]
    # compute initial max col with 1 for each row
    max_cols = [-1] * n
    for i in range(n):
        for j in range(n - 1, -1, -1):
            if new_g[i][j] == 1:
                max_cols[i] = j
                break
    for i in range(1, n):
        if max_cols[i] == -1:
            continue
        # min of previous max_cols where >=0
        prev_maxes = [max_cols[k] for k in range(i) if max_cols[k] >= 0]
        if not prev_maxes:
            min_prev = n
        else:
            min_prev = min(prev_maxes)
        allowed_end = min_prev + 1
        # trim all 1's after allowed_end
        for j in range(allowed_end + 1, n):
            if new_g[i][j] == 1:
                new_g[i][j] = 0
    return new_g

def separation_trim(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    new_g = [row[:] for row in g]
    for ii in range(n - 1, -1, -1):
        i = ii
        j = 1
        while j < n - 1:
            if new_g[i][j - 1] == 1 and new_g[i][j] == 3 and new_g[i][j + 1] == 1:
                start_right = j + 1
                end_right = start_right
                while end_right < n and new_g[i][end_right] == 1:
                    end_right += 1
                l = end_right - start_right
                if l >= 3:
                    # erase right run in current
                    for jj in range(start_right, end_right):
                        new_g[i][jj] = 0
                    # propagate up l-1 rows
                    for k in range(1, l):
                        if i - k >= 0:
                            for jj in range(start_right, end_right):
                                if new_g[i - k][jj] == 1:
                                    new_g[i - k][jj] = 0
                j = end_right
            else:
                j += 1
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    new_g = fill_zeros(new_g)
    new_g = handle_red_bars(new_g)
    new_g = trim_overhang(new_g)
    new_g = separation_trim(new_g)
    return new_g
```