```python
from typing import List

def find_eights_rect(g: List[List[int]]) -> tuple:
    min_r = 30
    max_r = -1
    min_c = 30
    max_c = -1
    for r in range(30):
        for c in range(30):
            if g[r][c] == 8:
                min_r = min(min_r, r)
                max_r = max(max_r, r)
                min_c = min(min_c, c)
                max_c = max(max_c, c)
    return min_r, max_r, min_c, max_c

def get_mod_lists(size: int, dim: int = 30) -> List[List[int]]:
    mod_lists = [[] for _ in range(size)]
    for pos in range(dim):
        mod_lists[pos % size].append(pos)
    return mod_lists

def get_mode(vals: List[int]) -> int:
    if not vals:
        return 0
    count_dict = {}
    for v in vals:
        count_dict[v] = count_dict.get(v, 0) + 1
    max_count = max(count_dict.values())
    candidates = [k for k in sorted(count_dict) if count_dict[k] == max_count]
    return candidates[0]

def program(g: List[List[int]]) -> List[List[int]]:
    rect = find_eights_rect(g)
    min_r, max_r, min_c, max_c = rect
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    row_mods = get_mod_lists(h)
    col_mods = get_mod_lists(w)
    output = []
    for i in range(h):
        rmod = (min_r + i) % h
        rs = row_mods[rmod]
        row_out = []
        for j in range(w):
            cmod = (min_c + j) % w
            cs = col_mods[cmod]
            vals = []
            for r in rs:
                for c in cs:
                    if g[r][c] != 8:
                        vals.append(g[r][c])
            mode = get_mode(vals)
            row_out.append(mode)
        output.append(row_out)
    return output
```