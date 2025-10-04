```python
from typing import List, Set
import sys

def find_centers(row: List[int], n: int) -> Set[int]:
    centers: Set[int] = set()
    i = 0
    while i < n - 2:
        if row[i] == 7 and row[i + 1] == 7 and row[i + 2] == 7:
            centers.add(i + 1)
            i += 3
        else:
            i += 1
    return centers

def process_odd_row(input_row: List[int], n: int) -> List[int]:
    new_row = input_row[:]
    i = 0
    while i < n:
        if i + 2 < n and input_row[i] == 7 and input_row[i + 1] == 7 and input_row[i + 2] == 7:
            new_row[i] = 8
            new_row[i + 1] = 6
            new_row[i + 2] = 8
            i += 3
        else:
            i += 1
    return new_row

def compute_base_even(row_input: List[int], adj_centers: Set[int], n: int) -> List[int]:
    new_row = [0] * n
    for j in range(n):
        if row_input[j] == 0:
            new_row[j] = 0
        elif j in adj_centers:
            new_row[j] = 6
        else:
            new_row[j] = 8
    return new_row

def apply_internal_even_overlays(base_row: List[int], row_input: List[int], place_left: bool, place_right: bool, has_zero: bool, n: int) -> List[int]:
    new_row = base_row[:]
    # Add 3 before each 0 if base was 8
    for j in range(1, n):
        if row_input[j] == 0 and new_row[j - 1] == 8:
            new_row[j - 1] = 3
    # Sides
    if place_left:
        if not has_zero:
            new_row[0] = 3
            if n > 1 and new_row[1] == 8:
                new_row[1] = 3
        else:
            new_row[0] = 3
    else:
        new_row[0] = 8
    if place_right:
        if not has_zero:
            new_row[n - 1] = 3
            if n > 1 and new_row[n - 2] == 8:
                new_row[n - 2] = 3
        else:
            new_row[n - 1] = 3
    else:
        new_row[n - 1] = 8
    return new_row

def apply_top_overlays(base_row: List[int], n: int) -> List[int]:
    # No overlays for top, just base
    return base_row[:]

def apply_bottom_overlays(base_row: List[int], row_input: List[int], n: int) -> List[int]:
    new_row = base_row[:]
    # Segments
    i = 0
    while i < n:
        if row_input[i] != 0:
            seg_start = i
            while i < n and row_input[i] != 0:
                i += 1
            seg_len = i - seg_start
            if seg_len >= 3 and new_row[seg_start] == 8:
                new_row[seg_start] = 3
        else:
            i += 1
    # End
    if n > 0 and new_row[n - 1] == 8:
        new_row[n - 1] = 3
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    m = len(g)
    n = len(g[0])
    # Compute centers for odd rows
    centers = [set() for _ in range(m)]
    for r in range(1, m, 2):
        centers[r] = find_centers(g[r], n)
    # New grid starts as copy
    new_g: List[List[int]] = [row[:] for row in g]
    # Process odd rows
    for r in range(1, m, 2):
        new_g[r] = process_odd_row(g[r], n)
    # Process even rows
    for k in range(0, m, 2):
        row_input = g[k]
        has_zero = any(x == 0 for x in row_input)
        # Adjacent centers
        adj_centers: Set[int] = set()
        if k > 0:
            adj_centers |= centers[k - 1]
        if k < m - 1:
            adj_centers |= centers[k + 1]
        # Base
        base_row = compute_base_even(row_input, adj_centers, n)
        # Overlays depending on type
        if k == 0:
            # Top
            new_g[k] = apply_top_overlays(base_row, n)
        elif k == m - 1:
            # Bottom
            new_g[k] = apply_bottom_overlays(base_row, row_input, n)
        else:
            # Internal
            has_upper = bool(centers[k - 1])
            has_lower = bool(centers[k + 1])
            # Left
            place_left = False
            if not has_lower:
                place_left = True
            elif has_upper:
                upper_l = min(centers[k - 1])
                lower_l = min(centers[k + 1])
                place_left = upper_l < lower_l
            # Right
            place_right = False
            if not has_lower:
                place_right = True
            elif has_upper:
                upper_r = max(centers[k - 1])
                lower_r = max(centers[k + 1])
                place_right = upper_r > lower_r
            # Apply
            new_g[k] = apply_internal_even_overlays(base_row, row_input, place_left, place_right, has_zero, n)
    return new_g
```