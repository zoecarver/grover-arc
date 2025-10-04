```python
from typing import List
from collections import defaultdict

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    bg = g[0][0]

    def copy_grid(grid):
        return [row[:] for row in grid]

    new_g = copy_grid(g)

    def fill_diagonal(new_grid, orig_grid, min_r, max_r, key_val, is_main, color):
        for r in range(min_r, max_r + 1):
            if is_main:
                c = r - key_val
            else:
                c = key_val - r
            if 0 <= c < w and new_grid[r][c] == orig_grid[r][c] and orig_grid[r][c] != 6:
                new_grid[r][c] = color

    def fill_full(new_grid, key_val, is_anti, color, background):
        for r in range(h):
            if is_anti:
                c = key_val - r
            else:
                c = r - key_val
            if 0 <= c < w and new_grid[r][c] == background:
                new_grid[r][c] = color

    # Find 1 groups
    main_groups = defaultdict(list)
    anti_groups = defaultdict(list)
    for r in range(h):
        for c in range(w):
            if g[r][c] == 1:
                d = r - c
                s = r + c
                main_groups[d].append(r)
                anti_groups[s].append(r)

    filled_main = set()
    filled_anti = set()
    small_pairs = []

    # Handle main diagonals for 1's
    for d, rs in main_groups.items():
        rs = sorted(set(rs))
        if len(rs) >= 2:
            min_r = rs[0]
            max_r = rs[-1]
            fill_diagonal(new_g, g, min_r, max_r, d, True, 1)
            filled_main.add(d)
        elif len(rs) == 1:
            r1 = rs[0]
            c1 = r1 - d
            r6 = None
            for rr in range(r1 + 1, h):
                cc = rr - d
                if 0 <= cc < w and g[rr][cc] == 6:
                    r6 = rr
                    break
            if r6 is not None:
                delta = r6 - r1
                if delta >= 3:
                    min_r = r1
                    max_r = r6 - 1
                    fill_diagonal(new_g, g, min_r, max_r, d, True, 1)
                    filled_main.add(d)
                else:
                    # small, remove 1
                    new_g[r1][c1] = bg
                    small_pairs.append((delta, True))
            # else: single no 6 below, keep as is

    # Handle anti diagonals for 1's
    for s, rs in anti_groups.items():
        rs = sorted(set(rs))
        if len(rs) >= 2:
            min_r = rs[0]
            max_r = rs[-1]
            fill_diagonal(new_g, g, min_r, max_r, s, False, 1)
            filled_anti.add(s)
        elif len(rs) == 1:
            r1 = rs[0]
            c1 = s - r1
            r6 = None
            for rr in range(r1 + 1, h):
                cc = s - rr
                if 0 <= cc < w and g[rr][cc] == 6:
                    r6 = rr
                    break
            if r6 is not None:
                delta = r6 - r1
                if delta >= 3:
                    min_r = r1
                    max_r = r6 - 1
                    fill_diagonal(new_g, g, min_r, max_r, s, False, 1)
                    filled_anti.add(s)
                else:
                    # small, remove 1
                    new_g[r1][c1] = bg
                    small_pairs.append((delta, False))
            # else: keep

    # Trigger 6 full fills
    for r in range(h):
        for c in range(w):
            if g[r][c] == 6:
                d = r - c
                s = r + c
                triggered = False
                if d in filled_main:
                    fill_full(new_g, s, True, 6, bg)
                    triggered = True
                if s in filled_anti:
                    fill_full(new_g, d, False, 6, bg)
                    triggered = True

    # Process rows for 6 removal and add above
    for r in range(h):
        filled_cs = []
        orig_cs = []
        for c in range(w):
            if new_g[r][c] == 6:
                if g[r][c] != 6:
                    filled_cs.append(c)
                else:
                    orig_cs.append(c)
        if filled_cs:
            min_filled_c = min(filled_cs)
            for c in orig_cs:
                if c < min_filled_c:
                    new_g[r][c] = bg
                    if r > 0 and new_g[r - 1][c] == bg:
                        new_g[r - 1][c] = 6

    # Add short 1 fills for small pairs
    if small_pairs:
        if filled_main:
            primary = min(filled_main)
            max_r = -1
            for rr in range(h):
                cc = rr - primary
                if 0 <= cc < w and new_g[rr][cc] in (1, 6):
                    max_r = max(max_r, rr)
            start_r = max_r + 1
            current_r = start_r
            for length, is_m in small_pairs:
                if not is_m:
                    continue  # skip for anti small, no example
                for _ in range(length):
                    if current_r >= h:
                        break
                    cc = current_r - primary
                    if 0 <= cc < w and new_g[current_r][cc] == bg:
                        new_g[current_r][cc] = 1
                    current_r += 1
        # similarly for anti if wanted, but skip for now

    return new_g
```