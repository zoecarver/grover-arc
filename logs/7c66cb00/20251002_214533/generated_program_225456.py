```python
from typing import List
from collections import defaultdict

def find_bkg(g: List[List[int]]) -> int:
    count = defaultdict(int)
    for row in g:
        if len(set(row)) == 1:
            c = row[0]
            count[c] += 1
    if count:
        return max(count, key=count.get)
    return g[0][0] if g else 0

def is_bordered(row: List[int]) -> tuple:
    w = len(row)
    if w < 3 or row[0] != row[-1]:
        return False, None, None
    b = row[0]
    interior = row[1:w-1]
    if len(set(interior)) != 1 or interior[0] == b:
        return False, None, None
    i = interior[0]
    return True, b, i

def get_clusters(templs: List[tuple[int, List[int]]]) -> List[List[tuple[int, List[int]]]]:
    if not templs:
        return []
    templs = sorted(templs, key=lambda x: x[0])
    clusters: List[List[tuple[int, List[int]]]] = []
    current = [templs[0]]
    for t in templs[1:]:
        if t[0] == current[-1][0] + 1:
            current.append(t)
        else:
            clusters.append(current)
            current = [t]
    clusters.append(current)
    return clusters

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    height = len(g)
    width = len(g[0])
    bg = find_bkg(g)
    templates = defaultdict(list)
    for r in range(height):
        row = g[r]
        col_dict = defaultdict(list)
        for c in range(width):
            val = row[c]
            if val != bg:
                col_dict[val].append(c)
        for val, cols in col_dict.items():
            unique_cols = sorted(set(cols))
            if unique_cols:
                templates[val].append((r, unique_cols))
    large_blocks = []
    i = 0
    while i < height:
        bordered, b, fill = is_bordered(g[i])
        if bordered:
            start = i
            while i < height and is_bordered(g[i])[0] and g[i][0] == b and g[i][1] == fill:
                i += 1
            h = i - start
            if h >= 2:
                large_blocks.append((start, h, b, fill))
        else:
            i += 1
    out = [row[:] for row in g]
    large_ranges = [(s, s + h - 1) for s, h, _, _ in large_blocks]
    for r in range(height):
        if not any(s <= r <= e for s, e in large_ranges):
            out[r] = [bg] * width
    for start, h, b, fill in large_blocks:
        rel_templ = [t for t in templates.get(fill, []) if t[0] < start]
        clusters = get_clusters(rel_templ)
        if not clusters:
            continue
        main_clus = max(clusters, key=len)
        main_h = len(main_clus)
        for k in range(main_h):
            _, tcols = main_clus[k]
            br = start + h - main_h + k
            for c in tcols:
                if 0 < c < width - 1:
                    out[br][c] = b
        others = [cl for cl in clusters if cl != main_clus]
        others.sort(key=lambda cl: -cl[-1][0])
        for cl in others:
            sh = len(cl)
            for k in range(sh):
                _, tcols = cl[k]
                br = start + h - sh + k
                if 0 <= br < height:
                    for c in tcols:
                        if 0 < c < width - 1:
                            out[br][c] = b
    return out
```