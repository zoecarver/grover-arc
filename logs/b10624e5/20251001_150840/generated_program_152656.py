```python
import copy
from typing import List, Tuple

def program(g: List[List[int]]) -> List[List[int]]:
    grid = copy.deepcopy(g)
    SIZE = 27
    CENTER = 13
    has_nine = any(9 in row for row in g)

    # Upper half rules (always applied)
    # Compute changed_rows for spread condition using original g
    changed_rows = set()
    for r in range(1, CENTER):
        for c in range(0, CENTER - 1, 2):
            c1, c2 = c, c + 1
            if c2 < CENTER and g[r - 1][c1] == 8 and g[r - 1][c2] == 8 and g[r][c1] == 2 and g[r][c2] == 2:
                changed_rows.add(r)

    # Reflect upper left to right using original g, set if target 4
    for r in range(CENTER):
        for c in range(CENTER):
            tc = SIZE - 1 - c
            if g[r][tc] == 4 and g[r][c] != 4:
                grid[r][tc] = g[r][c]

    # Apply spread down in left for changed rows
    for r in changed_rows:
        for c in range(0, CENTER - 1, 2):
            c1, c2 = c, c + 1
            if c2 < CENTER:
                grid[r][c1] = 8
                grid[r][c2] = 8

    # Remove all 3's in changed rows left
    for r in changed_rows:
        for c in range(CENTER):
            if grid[r][c] == 3:
                grid[r][c] = 4

    # Spread up right one step
    for r in range(CENTER - 1):
        for c in range(14, SIZE - 1, 2):
            c1, c2 = c, c + 1
            if c2 < SIZE and grid[r + 1][c1] == 8 and grid[r + 1][c2] == 8 and grid[r][c1] == 4 and grid[r][c2] == 4:
                grid[r][c1] = 8
                grid[r][c2] = 8

    # Exception clear for rows below changed with specific pattern (using original g)
    if changed_rows:
        max_changed = max(changed_rows)
        for r in range(max_changed + 1, CENTER):
            if g[r][5] == 2 and g[r][6] == 2 and g[r][7] == 3 and g[r][8] == 3:
                for tc in range(18, 22):
                    grid[r][tc] = 4

    # Now lower half
    if has_nine:
        # Clear lower
        for r in range(CENTER + 1, SIZE):
            for c in range(SIZE):
                grid[r][c] = 1 if c == CENTER else 4

        # Place left doubled using unique patterns
        unique = []
        seen = set()
        for r in range(CENTER):
            pat = tuple(grid[r][0:CENTER])
            if pat not in seen and any(x != 4 for x in grid[r][0:CENTER]):
                seen.add(pat)
                unique.append(r)
        # Place from bottom
        current_row = SIZE - 1
        for k in range(len(unique)):
            rep_r = unique[k]
            num_rows = 1 << k
            # Compute doubled for rep_r
            row_data = grid[rep_r][0:CENTER]
            blocks = []
            i = 0
            n_non4 = 0
            first_non4 = -1
            while i < CENTER:
                if row_data[i] == 4:
                    i += 1
                    continue
                if first_non4 == -1:
                    first_non4 = i
                col = row_data[i]
                j = i
                while j < CENTER and row_data[j] == col:
                    j += 1
                l = j - i
                blocks.append((col, l))
                n_non4 += l
                i = j
            if not blocks:
                continue
            shift = n_non4 // 2
            start_col = max(0, first_non4 - shift)
            new_seq = []
            for col, l in blocks:
                new_seq.extend([col] * (l * 2))
            new_length = len(new_seq)
            # Place
            placed = 0
            for ii in range(num_rows):
                pr = current_row - ii
                if pr < CENTER + 1:
                    break
                # Clear left
                for cc in range(CENTER):
                    grid[pr][cc] = 4
                # Place seq
                pos = start_col
                for val in new_seq:
                    if pos < CENTER:
                        grid[pr][pos] = val
                        pos += 1
                placed += 1
            current_row -= placed

        # Place right shifted reflection for each r with non4 left
        for r in range(CENTER):
            row_data = grid[r][0:CENTER]
            target_r = 27 - r
            if not (CENTER + 1 <= target_r < SIZE):
                continue
            has_non4 = any(x != 4 for x in row_data)
            if has_non4:
                for c in range(CENTER):
                    if row_data[c] != 4:
                        tc = 26 - c - 1
                        if CENTER + 1 <= tc < SIZE:
                            grid[target_r][tc] = row_data[c]

    else:
        # No 9 case lower rules
        # Point reflection upper left to lower right, no shift, set if 4
        for r in range(CENTER):
            for c in range(CENTER):
                r2 = 26 - r
                c2 = 26 - c
                if r2 >= CENTER + 1 and c2 >= CENTER + 1 and grid[r2][c2] == 4:
                    grid[r2][c2] = grid[r][c]

        # Add 3's inner to 2 blocks in lower
        for r in range(CENTER + 1, SIZE):
            i = 0
            while i < SIZE:
                if grid[r][i] != 2:
                    i += 1
                    continue
                j = i
                while j < SIZE and grid[r][j] == 2:
                    j += 1
                length = j - i
                if j - 1 < CENTER:  # left block
                    add_start = j
                    add_end = j + length - 1
                    if add_end < CENTER:
                        for cc in range(add_start, add_end + 1):
                            if grid[r][cc] == 4:
                                grid[r][cc] = 3
                elif i > CENTER:  # right block
                    add_start = i - length
                    add_end = i - 1
                    if add_start >= CENTER + 1:
                        for cc in range(add_start, add_end + 1):
                            if grid[r][cc] == 4:
                                grid[r][cc] = 3
                i = j

        # Special isolated 2 in lower left set below to 8
        for r in range(CENTER + 1, SIZE - 1):
            for c in range(CENTER):
                if grid[r][c] == 2:
                    left2 = c > 0 and grid[r][c - 1] == 2
                    right2 = c < CENTER - 1 and grid[r][c + 1] == 2
                    if not left2 and not right2:
                        if grid[r + 1][c] == 4:
                            grid[r + 1][c] = 8

        # 8 block spread in lower right
        # Find upper left 8 block
        min_r8 = SIZE
        max_r8 = -1
        min_c8 = SIZE
        max_c8 = -1
        for r in range(CENTER):
            for c in range(CENTER):
                if g[r][c] == 8:  # original
                    min_r8 = min(min_r8, r)
                    max_r8 = max(max_r8, r)
                    min_c8 = min(min_c8, c)
                    max_c8 = max(max_c8, c)
        if min_r8 <= max_r8:
            height = max_r8 - min_r8 + 1
            min_tc = 26 - max_c8
            max_tc = 26 - min_c8
            # Spread left one step in the reflected rows
            left_col = min_tc - 1
            if left_col >= CENTER + 1:
                min_r2 = 26 - max_r8
                max_r2 = 26 - min_r8
                for rr in range(min_r2, max_r2 + 1):
                    if grid[rr][left_col] == 4:
                        grid[rr][left_col] = 8
                min_tc = left_col
            # Now down spread height times the block min_tc to max_tc
            for step in range(height):
                next_r = max_r2 + 1 + step
                if next_r >= SIZE:
                    break
                all_four = all(grid[next_r][cc] == 4 for cc in range(min_tc, max_tc + 1))
                if all_four:
                    for cc in range(min_tc, max_tc + 1):
                        grid[next_r][cc] = 8
                else:
                    break

    return grid
```