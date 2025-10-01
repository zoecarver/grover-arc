```python
from typing import List, Tuple

def is_all_filled(row: List[int]) -> bool:
    """Check if a row consists entirely of filled cells (1 or 7)."""
    return all(cell == 1 or cell == 7 for cell in row)

def remove_large_filled_row_blocks(grid: List[List[int]], min_block: int = 3) -> List[List[int]]:
    """Remove blocks of min_block or more consecutive all-filled rows, preserving smaller blocks and non-filled rows."""
    if not grid:
        return []
    n = len(grid)
    result = []
    i = 0
    while i < n:
        if is_all_filled(grid[i]):
            start = i
            while i < n and is_all_filled(grid[i]):
                i += 1
            block_size = i - start
            if block_size >= min_block:
                continue
            else:
                result.extend(grid[j] for j in range(start, i))
        else:
            result.append(grid[i])
            i += 1
    return result

def transpose(grid: List[List[int]]) -> List[List[int]]:
    """Transpose the grid to process columns as rows."""
    if not grid or not grid[0]:
        return []
    return [list(row) for row in zip(*grid)]

def remove_filled_column_blocks_cut_tail(grid: List[List[int]], min_block: int = 1) -> List[List[int]]:
    """Remove the first block of min_block or more consecutive all-filled columns and everything to the right."""
    if not grid or not grid[0]:
        return grid
    t = transpose(grid)
    n = len(t)
    result_t = []
    i = 0
    found = False
    while i < n and not found:
        if is_all_filled(t[i]):
            start = i
            while i < n and is_all_filled(t[i]):
                i += 1
            block_size = i - start
            if block_size >= min_block:
                found = True
                break
            else:
                result_t.extend(t[j] for j in range(start, i))
        else:
            result_t.append(t[i])
            i += 1
    # If found, result_t has only before start; otherwise all
    return transpose(result_t)

def simplify_blocks(grid: List[List[int]]) -> List[List[int]]:
    """Iteratively simplify by removing large filled row blocks and cutting tail at first filled column block."""
    current = [row[:] for row in grid]
    while True:
        old_h = len(current)
        old_w = len(current[0]) if current else 0
        current = remove_large_filled_row_blocks(current)
        current = remove_filled_column_blocks_cut_tail(current)
        new_h = len(current)
        new_w = len(current[0]) if current else 0
        if new_h == old_h and new_w == old_w:
            break
    return current

def clean_and_collect_blocks(grid: List[List[int]]) -> List[Tuple[int, int, int]]:
    """Clean 7 blocks and following 1s to 4s in each row, collect (row, start, end) of each cleared segment."""
    blocks: List[Tuple[int, int, int]] = []
    for r in range(len(grid)):
        row = grid[r]
        i = 0
        while i < len(row):
            if row[i] == 7:
                start = i
                # Clear consecutive 7s
                while i < len(row) and row[i] == 7:
                    row[i] = 4
                    i += 1
                # Clear up to 2 following 1s
                follow = 0
                while i < len(row) and row[i] == 1 and follow < 2:
                    row[i] = 4
                    i += 1
                    follow += 1
                end = i - 1 if i > start else start
                blocks.append((r, start, end))
            else:
                i += 1
    return blocks

def propagate(blocks: List[Tuple[int, int, int]], grid: List[List[int]]):
    """Propagate 4s down from cleared blocks and up if bottom row."""
    h = len(grid)
    if h == 0:
        return
    w = len(grid[0])
    for r, s, e in blocks:
        if s > e or e >= w:
            continue
        width = e - s + 1
        # Down propagation: ends for first 2 levels
        for d in range(1, 3):
            nr = r + d
            if nr < h:
                if grid[nr][s] == 1:
                    grid[nr][s] = 4
                if width > 1 and grid[nr][e] == 1:
                    grid[nr][e] = 4
        # Inner at level 3 if width >= 4
        if width >= 4:
            d = 3
            nr = r + d
            if nr < h:
                for c in range(s + 1, e):
                    if c < w and grid[nr][c] == 1:
                        grid[nr][c] = 4
        # Up propagation only if this is the bottom row
        if r == h - 1 and width >= 2:
            d = 1
            nr = r - d
            if nr >= 0:
                if grid[nr][s] == 1:
                    grid[nr][s] = 4
                if grid[nr][e] == 1:
                    grid[nr][e] = 4

def remove_bottom_rows(grid: List[List[int]]) -> Tuple[List[List[int]], int]:
    """Iteratively remove bottom rows where num4 > num1 and not all 4s, return updated grid and M removed."""
    M = 0
    while grid and len(grid) > 0:
        last_row = grid[-1]
        num1 = sum(1 for cell in last_row if cell == 1)
        num4 = len(last_row) - num1
        is_all4 = num1 == 0
        if num4 > num1 and not is_all4:
            grid.pop()
            M += 1
        else:
            break
    return grid, M

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program to solve the puzzle."""
    if not g:
        return []
    original = [row[:] for row in g]
    h0 = len(original)
    w0 = len(original[0]) if h0 > 0 else 0
    # Simplify blocks
    grid = simplify_blocks(g)
    # Clean and collect cleared blocks
    blocks = clean_and_collect_blocks(grid)
    # Propagate
    propagate(blocks, grid)
    # Remove bottom rows
    grid, M = remove_bottom_rows(grid)
    # Pad right if M > 0
    if M > 0:
        add_num = M + 1
        current_h = len(grid)
        if current_h > 0:
            current_w = len(grid[0])
            pad_start = w0 - add_num
            if pad_start < 0:
                pad_start = 0
            for k in range(current_h):
                source_r = k + M
                pad = [4] * add_num  # default 4s
                if source_r < h0:
                    source_row = original[source_r]
                    pad_start_clamp = max(0, min(pad_start, w0))
                    pad_end = min(w0, pad_start_clamp + add_num)
                    pad = source_row[pad_start_clamp:pad_end] + [4] * (add_num - (pad_end - pad_start_clamp))
                grid[k].extend(pad)
    return grid
```