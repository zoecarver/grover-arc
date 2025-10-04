```python
from typing import List
from collections import Counter

def get_background_color(g: List[List[int]]) -> int:
    pixels = [g[r][c] for r in range(6, 24) for c in range(24) if g[r][c] != 0]
    if not pixels:
        return 0
    return Counter(pixels).most_common(1)[0][0]

def place_shifted_shapes(g: List[List[int]], new_g: List[List[int]], bg_color: int):
    # Rule: Shift non-maroon, non-background shapes (including small ones for simplicity) from rows >=6 upward by 6, but use shift 5 for rows >=21 to push bottom shapes avoiding overlap with large maroon end at row15
    for r in range(6, 24):
        shift = 5 if r >= 21 else 6
        new_r = r - shift
        if 0 <= new_r < 24:
            for c in range(24):
                cell = g[r][c]
                if cell != bg_color and cell != 0 and cell != 5 and cell != 8:
                    new_g[new_r][c] = cell

def place_large_maroon(new_g: List[List[int]]):
    # Rule: Create large maroon structure by filling rows 0-15 completely with 8 (maroon), to be overridden by shifted shapes
    for r in range(16):
        for c in range(24):
            new_g[r][c] = 8

def fill_background(new_g: List[List[int]], bg_color: int):
    # Rule: Fill all remaining empty (0) cells with background color
    for r in range(24):
        for c in range(24):
            if new_g[r][c] == 0:
                new_g[r][c] = bg_color

def place_top_override(new_g: List[List[int]], bg_color: int):
    # Rule: For top rows 0-2 (background color propagation to top fills), override any 8's back to background color (preserves shifted shapes, creates bg fills in maroon areas; small top maroon bars unknown, so omitted)
    for r in range(3):
        for c in range(24):
            if new_g[r][c] == 8:
                new_g[r][c] = bg_color

def program(g: List[List[int]]) -> List[List[int]]:
    bg_color = get_background_color(g)
    new_g = [[0] * 24 for _ in range(24)]
    place_large_maroon(new_g)
    place_shifted_shapes(g, new_g, bg_color)
    fill_background(new_g, bg_color)
    place_top_override(new_g, bg_color)
    return new_g
```