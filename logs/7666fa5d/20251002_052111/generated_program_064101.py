```python
from typing import List
from copy import deepcopy

def get_active_color(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    s = set(flat) - {8}
    return s.pop() if s else None

def keep_single_pixels(g: List[List[int]], c: int) -> List[List[int]]:
    # Single-pixel components of color C remain unchanged
    return deepcopy(g)

def create_red_components(g: List[List[int]], c: int) -> List[List[int]]:
    # Create new red (2) components near dense/aligned groups of 2+ C pixels
    # Implementation: Set 8 to 2 if >=2 C in 3x3 neighborhood (approximation for density)
    new_g = deepcopy(g)
    for r in range(16):
        for col in range(16):
            if new_g[r][col] == 8:
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr = r + dr
                        nc = col + dc
                        if 0 <= nr < 16 and 0 <= nc < 16 and new_g[nr][nc] == c:
                            count += 1
                if count >= 2:
                    new_g[r][col] = 2
    return new_g

def create_small_maroon(g: List[List[int]], c: int) -> List[List[int]]:
    # For isolated/top-peripheral C, create small maroon (8) fills adjacent (no change since background is 8)
    # Implementation: No change for isolated, as gaps are already 8
    return deepcopy(g)

def conserve_pixels(g: List[List[int]], c: int) -> List[List[int]]:
    # Ensure total maroon + red pixels conserved (recoloring only, already satisfied by replacement)
    # Implementation: No op, as rule is followed by other functions
    return deepcopy(g)

def keep_preexisting_maroon(g: List[List[int]]) -> List[List[int]]:
    # Pre-existing small maroon components remain unchanged
    # Implementation: No change
    return deepcopy(g)

def program(g: List[List[int]]) -> List[List[int]]:
    c = get_active_color(g)
    if c is None:
        return g
    grid = keep_single_pixels(g, c)
    grid = create_red_components(grid, c)
    grid = create_small_maroon(grid, c)
    grid = conserve_pixels(grid, c)
    grid = keep_preexisting_maroon(grid)
    return grid
```