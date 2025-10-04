```python
from typing import List, Tuple, Set
from copy import deepcopy

def program(g: List[List[int]]) -> List[List[int]]:
    field = get_base_field(g)
    field = replace_fives_to_threes(field)
    active: Set[int] = get_active_colors(g)
    patch_infos: List[Tuple[int, int, int]] = find_maroon_patches(field)
    # Assume single patch for simplicity; take the first one
    if not patch_infos:
        return field[:19]
    patch_r, min_c, max_c = patch_infos[0]
    field = deepcopy(field)
    field = apply_horizontal_fills(field, active, [(patch_r, min_c, max_c)])
    left_pillar_start, right_pillar_start = compute_pillar_positions(field, patch_r, min_c, max_c)
    width = len(field[0]) if field else 0
    patch_width = max_c - min_c + 1
    field = apply_upper_pillars(field, active, patch_r, min_c, max_c, left_pillar_start, right_pillar_start, patch_width, width)
    field = apply_lower_pillars(field, active, patch_r, min_c, max_c, left_pillar_start, right_pillar_start, patch_width, width)
    # Simple clearing for rows below patch: set active colors to 3 if not 8
    field = clear_active_below_patch(field, active, patch_r + 1)
    # Add full connection below if all background
    field = add_full_connections_below(field, active, patch_r, left_pillar_start, min_c, width)
    return field[:19]

def get_base_field(g: List[List[int]]) -> List[List[int]]:
    """Extract the lower 19 rows as the base field."""
    return [row[:] for row in g[5:24]]

def replace_fives_to_threes(field: List[List[int]]) -> List[List[int]]:
    """Replace all 5's (borders) with 3's (background)."""
    for row in field:
        for j in range(len(row)):
            if row[j] == 5:
                row[j] = 3
    return field

def get_active_colors(g: List[List[int]]) -> Set[int]:
    """Extract unique non-0, non-5 colors from top 4 pattern rows as active colors."""
    active = set()
    for r in range(1, 5):
        for val in g[r]:
            if val not in (0, 5):
                active.add(val)
    return active

def find_maroon_patches(field: List[List[int]]) -> List[Tuple[int, int, int]]:
    """Find rows with 8 (maroon) patches, return (row, min_col, max_col) for each."""
    patches = []
    for r in range(len(field)):
        cols = [c for c in range(len(field[r])) if field[r][c] == 8]
        if cols:
            patches.append((r, min(cols), max(cols)))
    return patches

def apply_horizontal_fills(field: List[List[int]], active: Set[int], patch_infos: List[Tuple[int, int, int]]) -> List[List[int]]:
    """Apply horizontal fills at patch rows, overwriting background and non-active."""
    field = [row[:] for row in field]
    for patch_r, min_c, max_c in patch_infos:
        row = field[patch_r]
        # Left fill
        c = min_c - 1
        while c >= 0 and row[c] not in active:
            row[c] = 8
            c -= 1
        # Right fill
        c = max_c + 1
        while c < len(row) and row[c] not in active:
            row[c] = 8
            c += 1
    return field

def compute_pillar_positions(field: List[List[int]], patch_r: int, orig_min_c: int, orig_max_c: int) -> Tuple[int, int]:
    """Compute left and right pillar start columns based on filled row at patch_r."""
    row = field[patch_r]
    left_start = min(c for c in range(len(row)) if row[c] == 8)
    right_end = max(c for c in range(len(row)) if row[c] == 8)
    return left_start, right_end

def apply_upper_pillars(field: List[List[int]], active: Set[int], patch_r: int, patch_min_c: int, patch_max_c: int, left_start: int, right_end: int, patch_width: int, grid_width: int) -> List[List[int]]:
    """Apply upper pillars: patch and right for all upper rows, left + full fill for immediate above."""
    field = [row[:] for row in field]
    patch_left = patch_min_c
    patch_right = patch_max_c
    right_pillar_left = right_end - patch_width + 1
    left_pillar_left = left_start
    immediate_above = patch_r - 1
    for r in range(immediate_above + 1):
        row = field[r]
        # Set patch and right pillars
        for c in range(patch_left, patch_right + 1):
            if row[c] == 3 or row[c] not in active:
                row[c] = 8
        for c in range(right_pillar_left, right_end + 1):
            if row[c] == 3 or row[c] not in active:
                row[c] = 8
        # For immediate above, set left pillar and fill between all pillars if background
        if r == immediate_above:
            for c in range(left_pillar_left, left_start + patch_width - 1 + 1):
                if row[c] == 3 or row[c] not in active:
                    row[c] = 8
            # Fill between leftmost to rightmost if 3
            min_fill = min(left_pillar_left, patch_left, right_pillar_left)
            max_fill = max(left_start + patch_width - 1, patch_right, right_end)
            for c in range(min_fill + 1, max_fill):
                if row[c] == 3:
                    row[c] = 8
    return field

def apply_lower_pillars(field: List[List[int]], active: Set[int], patch_r: int, patch_min_c: int, patch_max_c: int, left_start: int, right_end: int, patch_width: int, grid_width: int) -> List[List[int]]:
    """Apply lower pillars: left and patch for all lower rows, no full fill."""
    field = [row[:] for row in field]
    patch_left = patch_min_c
    patch_right = patch_max_c
    left_pillar_left = left_start
    for r in range(patch_r + 1, len(field)):
        row = field[r]
        # Set left pillar
        for c in range(left_pillar_left, left_start + patch_width - 1 + 1):
            if row[c] == 3 or row[c] not in active:
                row[c] = 8
        # Set patch pillar
        for c in range(patch_left, patch_right + 1):
            if row[c] == 3 or row[c] not in active:
                row[c] = 8
    return field

def clear_active_below_patch(field: List[List[int]], active: Set[int], start_r: int) -> List[List[int]]:
    """Clear active colors to 3 in rows below patch, keeping connector and background."""
    field = [row[:] for row in field]
    for r in range(start_r, len(field)):
        row = field[r]
        for j in range(len(row)):
            if row[j] in active and row[j] != 8:
                row[j] = 3
    return field

def add_full_connections_below(field: List[List[int]], active: Set[int], patch_r: int, left_start: int, patch_min_c: int, grid_width: int) -> List[List[int]]:
    """Add full horizontal connections in all-background rows below patch to connect to bottom."""
    field = [row[:] for row in field]
    start_fill_r = patch_r + 3  # Arbitrary, based on train: start after some pillars
    for r in range(start_fill_r, len(field) - 3):  # Leave room for bottom
        row = field[r]
        is_background = all(row[j] == 3 for j in range(left_start, grid_width - 3))
        if is_background:
            for j in range(left_start, grid_width - 3):
                row[j] = 8
    return field
```