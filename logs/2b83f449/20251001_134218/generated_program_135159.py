```python
def process_pattern(row: List[int]) -> List[int]:
    new_row = row.copy()
    i = 0
    while i < len(row) - 2:
        if new_row[i] == 7 and new_row[i + 1] == 7 and new_row[i + 2] == 7:
            new_row[i] = 8
            new_row[i + 1] = 6
            new_row[i + 2] = 8
            i += 3
        else:
            i += 1
    return new_row

def get_6_overlay(g: List[List[int]], out: List[List[int]], j: int, n: int) -> List[int]:
    new_row = [0 if g[j][k] == 0 else 8 for k in range(n)]
    has_upper = j > 0
    has_lower = j < len(g) - 1
    for k in range(n):
        from_upper = has_upper and out[j - 1][k] == 6
        from_lower = has_lower and out[j + 1][k] == 6
        if from_upper or from_lower:
            new_row[k] = 6
    return new_row

def add_0_adjacent(temp: List[int], out: List[List[int]], j: int, n: int, is_bottom: bool) -> List[int]:
    has_upper = j > 0
    new_row = temp.copy()
    # after 0
    for i in range(n):
        if new_row[i] == 0 and i + 1 < n and new_row[i + 1] != 0:
            # find leftmost 6 after i
            left6 = None
            k = i + 1
            while k < n and new_row[k] != 0:
                if new_row[k] == 6:
                    left6 = k
                    break
                k += 1
            if left6 is not None and has_upper and out[j - 1][left6] == 6:
                new_row[i + 1] = 3
    # before 0 if not bottom
    if not is_bottom:
        for i in range(n):
            if new_row[i] == 0 and i > 0 and new_row[i - 1] != 0:
                # find rightmost 6 before i
                right6 = None
                k = i - 1
                while k >= 0 and new_row[k] != 0:
                    if new_row[k] == 6:
                        right6 = k
                        break
                    k -= 1
                if right6 is not None and has_upper and out[j - 1][right6] == 6:
                    new_row[i - 1] = 3
    return new_row

def add_border_3s(temp: List[int], g: List[List[int]], out: List[List[int]], j: int, n: int, is_bottom: bool) -> List[int]:
    new_row = temp.copy()
    has_upper = j > 0
    # find leftmost 6 pos
    left6_pos = -1
    for k in range(n):
        if new_row[k] == 6:
            left6_pos = k
            break
    # find rightmost 6 pos
    right6_pos = -1
    for k in range(n - 1, -1, -1):
        if new_row[k] == 6:
            right6_pos = k
            break
    # left end pos 0
    set_left = False
    if left6_pos != -1 and has_upper and out[j - 1][left6_pos] == 6:
        set_left = True
        if g[j][0] == 3 and new_row[0] != 6:
            new_row[0] = 3
        elif new_row[0] == 8:
            # check if first segment contains left6_pos
            r = 0
            while r < n and new_row[r] != 0:
                r += 1
            r -= 1
            if r >= 0 and left6_pos <= r:
                new_row[0] = 3
    else:
        if g[j][0] == 3 and new_row[0] != 6:
            new_row[0] = 8
    # right end pos n-1
    set_right = False
    if right6_pos != -1 and has_upper and out[j - 1][right6_pos] == 6:
        set_right = True
        if g[j][n - 1] == 3 and new_row[n - 1] != 6:
            new_row[n - 1] = 3
        elif new_row[n - 1] == 8:
            # check if last segment contains right6_pos
            s = n - 1
            while s >= 0 and new_row[s] != 0:
                s -= 1
            s += 1
            if s < n and right6_pos >= s:
                new_row[n - 1] = 3
    else:
        if g[j][n - 1] == 3 and new_row[n - 1] != 6:
            new_row[n - 1] = 8
    return new_row

def add_extension(temp: List[int], j: int, n: int, is_bottom: bool) -> List[int]:
    new_row = temp.copy()
    # check if has no 0s
    has_zero = False
    for x in new_row:
        if x == 0:
            has_zero = True
            break
    if has_zero or is_bottom or n < 2:
        return new_row
    # left
    if new_row[0] == 3 and new_row[1] == 8:
        new_row[1] = 3
    # right
    if new_row[n - 1] == 3 and new_row[n - 2] == 8:
        new_row[n - 2] = 3
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    n = len(g[0])
    out = [row.copy() for row in g]
    # process pattern rows
    for j in range(1, h, 2):
        out[j] = process_pattern(out[j])
    # process frame rows
    for j in range(0, h, 2):
        temp = get_6_overlay(g, out, j, n)
        temp = add_0_adjacent(temp, out, j, n, is_bottom=(j == h - 1))
        temp = add_border_3s(temp, g, out, j, n, is_bottom=(j == h - 1))
        temp = add_extension(temp, j, n, is_bottom=(j == h - 1))
        out[j] = temp
    return out
```