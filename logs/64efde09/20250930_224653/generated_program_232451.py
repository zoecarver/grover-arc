```python
from typing import List, Dict, Tuple
from collections import defaultdict

def count_non_blanks(g: List[List[int]]) -> Dict[int, int]:
    h = len(g)
    if h == 0:
        return {}
    w = len(g[0])
    counts = defaultdict(int)
    for i in range(h):
        for j in range(w):
            c = g[i][j]
            if c != 8:
                counts[c] += 1
    return counts

def find_singleton_positions(g: List[List[int]], singletons: List[int]) -> Dict[int, Tuple[int, int]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    pos_dict: Dict[int, Tuple[int, int]] = {}
    for i in range(h):
        for j in range(w):
            cc = g[i][j]
            if cc in singletons:
                pos_dict[cc] = (i, j)
    return pos_dict

def find_stems(g: List[List[int]], h: int, w: int) -> List[Tuple[int, int, int, int]]:
    runs = []
    for col in range(w):
        i = 0
        while i < h:
            val = g[i][col]
            if val == 1 or val == 2:
                cl = val
                start_i = i
                i += 1
                while i < h and g[i][col] == cl:
                    i += 1
                length = i - start_i
                if length >= 4:
                    runs.append((start_i, i, col, cl))
            else:
                i += 1
    return runs

def is_isolated(stem: Tuple[int, int, int, int], all_stems: List[Tuple[int, int, int, int]]) -> bool:
    sr, er, c, typ = stem
    opp = 3 - typ
    for osr, oer, oc, otyp in all_stems:
        if otyp != opp or oc not in (c - 1, c + 1):
            continue
        if max(sr, osr) < min(er, oer):
            return False
    return True

def fill_horizontal(grid: List[List[int]], r: int, c: int, direction: int, color: int, w: int) -> None:
    col = c + direction
    while 0 <= col < w and grid[r][col] == 8:
        grid[r][col] = color
        col += direction

def process_stems(grid: List[List[int]], h: int, w: int, s1: int, s2: int, s3: int) -> None:
    stems = find_stems(grid, h, w)
    processed_stems = [stem for stem in stems if is_isolated(stem, stems)]
    for sr, er, c, typ in processed_stems:
        l = er - sr
        if typ == 1:
            offsets = [1, 3, 5]
            colors = [s1, s2, s3]
        else:
            offsets = [0, 3, l - 2]
            colors = [s3, s2, s1]
        for off_idx, off in enumerate(offsets):
            r = sr + off
            if not (0 <= r < h):
                continue
            colr = colors[off_idx]
            fill_horizontal(grid, r, c, -1, colr, w)
            fill_horizontal(grid, r, c, 1, colr, w)

def place_top_pattern(grid: List[List[int]], h: int, w: int, pos_dict: Dict[int, Tuple[int, int]], s1: int, s2: int, s3: int) -> None:
    for color, (r, c) in pos_dict.items():
        if r != 0:
            continue
        if color == s1:
            if c < 4:
                continue
            anchor = c - 4
            pat_cols = [anchor, anchor + 1, anchor + 4]
            pat_colors = [s3, s2, s1]
        elif color == s2:
            if c < 2:
                continue
            anchor = c - 2
            pat_cols = [anchor, anchor + 2, anchor + 4]
            pat_colors = [s3, s2, s1]
        elif color == s3:
            pat_cols = [c, c + 1, c + 4]
            pat_colors = [s3, s2, s1]
        else:
            continue
        # Starting row 0 partial fill
        for i, pc in enumerate(pat_cols):
            if 0 <= pc < w and grid[0][pc] == 8:
                grid[0][pc] = pat_colors[i]
        # Propagate down
        current_r = 1
        while current_r < h:
            if not all(0 <= pc < w and grid[current_r][pc] == 8 for pc in pat_cols):
                break
            for i, pc in enumerate(pat_cols):
                grid[current_r][pc] = pat_colors[i]
            current_r += 1

def place_bottom_pattern(grid: List[List[int]], h: int, w: int, pos_dict: Dict[int, Tuple[int, int]], s1: int, s2: int, s3: int) -> None:
    for color, (r, c) in pos_dict.items():
        if r != h - 1:
            continue
        if color == s1:
            pat_cols = [c, c + 1, c + 4]
            pat_colors = [s1, s2, s3]
        elif color == s2:
            if c < 1:
                continue
            anchor = c - 1
            pat_cols = [anchor, anchor + 1, anchor + 4]
            pat_colors = [s1, s2, s3]
        elif color == s3:
            if c < 4:
                continue
            anchor = c - 4
            pat_cols = [anchor, anchor + 1, anchor + 4]
            pat_colors = [s1, s2, s3]
        else:
            continue
        # Starting row h-1 partial fill
        start_r = h - 1
        for i, pc in enumerate(pat_cols):
            if 0 <= pc < w and grid[start_r][pc] == 8:
                grid[start_r][pc] = pat_colors[i]
        # Propagate up
        current_r = h - 2
        while current_r >= 0:
            if not all(0 <= pc < w and grid[current_r][pc] == 8 for pc in pat_cols):
                break
            for i, pc in enumerate(pat_cols):
                grid[current_r][pc] = pat_colors[i]
            current_r -= 1

def extend_middle(grid: List[List[int]], h: int, w: int, pos_dict: Dict[int, Tuple[int, int]], singletons: List[int]) -> None:
    for color in singletons:
        if color not in pos_dict:
            continue
        r, c = pos_dict[color]
        if r == 0 or r == h - 1:
            continue
        # left
        col = c - 1
        while col >= 0 and grid[r][col] == 8:
            grid[r][col] = color
            col -= 1
        # right
        col = c + 1
        while col < w and grid[r][col] == 8:
            grid[r][col] = color
            col += 1

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    w = len(g[0])
    grid = [row[:] for row in g]
    counts = count_non_blanks(grid)
    singletons = [c for c in counts if counts[c] == 1]
    if len(singletons) != 3:
        return grid
    singletons.sort()
    s1, s2, s3 = singletons
    pos = find_singleton_positions(grid, singletons)
    # Process stems first
    process_stems(grid, h, w, s1, s2, s3)
    # Process top patterns
    place_top_pattern(grid, h, w, pos, s1, s2, s3)
    # Process bottom patterns
    place_bottom_pattern(grid, h, w, pos, s1, s2, s3)
    # Process middle horizontals
    extend_middle(grid, h, w, pos, singletons)
    return grid
```