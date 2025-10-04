```python
from typing import List
from collections import defaultdict

def find_bkg(g: List[List[int]]) -> int:
    count = {}
    for row in g:
        if len(set(row)) == 1:
            c = row[0]
            count[c] = count.get(c, 0) + 1
    if count:
        return max(count, key=count.get)
    return g[0][0] if g and g[0] else 0

def is_bordered(row: List[int]) -> tuple:
    if len(row) < 3 or row[0] != row[-1]:
        return False, None, None
    b = row[0]
    i = row[1]
    if all(x == i for x in row[1:-1]) and b != i:
        return True, b, i
    return False, None, None

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    grid = [row[:] for row in g]
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    bkg = find_bkg(g)
    # Extract templates from original irregular rows
    templates = defaultdict(list)
    for r in range(height):
        orig_row = g[r]
        if all(x == bkg for x in orig_row):
            continue
        col_dict = defaultdict(list)
        for c in range(width):
            val = orig_row[c]
            if val != bkg:
                col_dict[val].append(c)
        for val, cols in col_dict.items():
            templates[val].append((r, sorted(set(cols))))
    # Fill irregular rows with bkg
    for r in range(height):
        row = grid[r]
        if not all(x == bkg for x in row):
            grid[r] = [bkg] * width
    # Process groups of consecutive identical rows
    r = 0
    while r < height:
        start = r
        content = tuple(grid[r])
        while r < height and tuple(grid[r]) == content:
            r += 1
        l = r - start
        is_b, b, i = is_bordered(list(content))
        if l > 1 and is_b and i is not None and i != bkg:
            if i in templates:
                temp_list = templates[i]
                if temp_list:
                    temp_list = sorted(temp_list, key=lambda x: x[0])
                    # Find clusters (consecutive r groups)
                    clusters = []
                    curr = []
                    prev_r = -100
                    for tr, cols in temp_list:
                        if tr > prev_r + 1:
                            if curr:
                                clusters.append(curr)
                            curr = []
                        curr.append((tr, cols))
                        prev_r = tr
                    if curr:
                        clusters.append(curr)
                    if clusters:
                        # Main cluster: longest
                        main_clus = max(clusters, key=len)
                        m = len(main_clus)
                        if m > 0:
                            mod_start = start + l - m
                            for j in range(m):
                                block_r = mod_start + j
                                if 0 <= block_r < height:
                                    _, temp_cols = main_clus[j]
                                    for c in temp_cols:
                                        if 0 <= c < width:
                                            grid[block_r][c] = b
                        # Other clusters: overlay on last h_small rows of block
                        for clus in clusters:
                            if clus is main_clus:
                                continue
                            h_small = len(clus)
                            if h_small > 0:
                                block_end = start + l - 1
                                for j in range(h_small):
                                    block_r = block_end - h_small + 1 + j
                                    if 0 <= block_r < height:
                                        _, temp_cols = clus[j]
                                        for c in temp_cols:
                                            if 0 <= c < width:
                                                grid[block_r][c] = b
    return grid
```