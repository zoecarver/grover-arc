```python
from typing import List
from copy import deepcopy

def get_dimensions(g: List[List[int]]) -> tuple[int, int]:
    if not g:
        return 0, 0
    return len(g), len(g[0]) if g else 0

def program(g: List[List[int]]) -> List[List[int]]:
    h, w = get_dimensions(g)
    g_out = deepcopy(g)
    for i in range(h - 1):  # Skip the bottom row
        j = 0
        while j < w:
            if g_out[i][j] != 8:
                j += 1
                continue
            start = j
            while j < w and g_out[i][j] == 8:
                j += 1
            end = j - 1
            # Find left bound
            l = start - 1
            while l >= 0 and g_out[i][l] == 8:
                l -= 1
            left_c = g_out[i][l] if l >= 0 else 0
            # Find right bound
            r = end + 1
            while r < w and g_out[i][r] == 8:
                r += 1
            right_c = g_out[i][r] if r < w else 0
            if left_c == right_c and left_c > 1:
                for k in range(start, end + 1):
                    g_out[i][k] = left_c
            elif left_c == 1 and right_c == 1:
                length = end - start + 1
                if length == 1:
                    # Use left clue
                    left_n = 0
                    kk = start - 1
                    while kk >= 0:
                        if g_out[i][kk] == 1:
                            kk -= 1
                            continue
                        if 2 <= g_out[i][kk] <= 9:
                            left_n = g_out[i][kk]
                            break
                        kk -= 1
                    n = left_n
                else:
                    # Count consecutive 1s immediately left
                    num_left_1s = 0
                    ll = start - 1
                    while ll >= 0 and g_out[i][ll] == 1:
                        num_left_1s += 1
                        ll -= 1
                    if num_left_1s == 1:
                        # Use right clue
                        right_n = 0
                        kk = end + 1
                        while kk < w:
                            if g_out[i][kk] == 1:
                                kk += 1
                                continue
                            if 2 <= g_out[i][kk] <= 9:
                                right_n = g_out[i][kk]
                                break
                            kk += 1
                        n = right_n
                    else:
                        # Use left clue
                        left_n = 0
                        kk = start - 1
                        while kk >= 0:
                            if g_out[i][kk] == 1:
                                kk -= 1
                                continue
                            if 2 <= g_out[i][kk] <= 9:
                                left_n = g_out[i][kk]
                                break
                            kk -= 1
                        n = left_n
                if n > 1:
                    for k in range(start, end + 1):
                        g_out[i][k] = n
    return g_out
```