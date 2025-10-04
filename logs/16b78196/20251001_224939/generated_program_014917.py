```python
from typing import List, Tuple

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    """Rule: Create a mutable copy of the input grid to avoid modifying the original."""
    return [row[:] for row in g]

def get_connected_components(g: List[List[int]]) -> List[Tuple[int, List[Tuple[int, int]]]]:
    """Rule: Extract 4-connected components of the same color (non-zero integers 1-8) using DFS flood-fill."""
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    visited = [[False] * 30 for _ in range(30)]
    components = []
    for i in range(30):
        for j in range(30):
            if g[i][j] > 0 and not visited[i][j]:
                color = g[i][j]
                comp = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    comp.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 30 and 0 <= ny < 30 and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((color, comp))
    return components

def select_base(components: List[Tuple[int, List[Tuple[int, int]]]]) -> Tuple[int, List[Tuple[int, int]]]:
    """Rule: Select the largest component by cell count, tie-broken by highest color value as the fixed base."""
    if not components:
        return (0, [])
    return max(components, key=lambda x: (len(x[1]), x[0]))

def get_anchor(comp: List[Tuple[int, int]]) -> Tuple[int, int]:
    """Rule: Compute the top-left anchor point of a component for translation reference."""
    if not comp:
        return (0, 0)
    min_r = min(r for r, c in comp)
    min_c = min(c for r, c in comp if r == min_r)
    return (min_r, min_c)

def get_bbox(pos: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """Rule: Compute the bounding box (min_r, max_r, min_c, max_c) of a component's positions."""
    if not pos:
        return (0, 0, 0, 0)
    min_r = min(r for r, c in pos)
    max_r = max(r for r, c in pos)
    min_c = min(c for r, c in pos)
    max_c = max(c for r, c in pos)
    return (min_r, max_r, min_c, max_c)

def clear_non_base(out: List[List[int]], base_pos: List[Tuple[int, int]]) -> None:
    """Rule: Clear all cells not part of the base component to 0, preserving the base structure."""
    base_set = set(base_pos)
    for i in range(30):
        for j in range(30):
            if (i, j) not in base_set:
                out[i][j] = 0

def sort_smalls_by_original_position(smalls: List[Tuple[int, List[Tuple[int, int]]]]) -> List[Tuple[int, List[Tuple[int, int]]]]:
    """Rule: Sort small components by their original minimum row (top-to-bottom order) to process upper blobs first."""
    return sorted(smalls, key=lambda x: min(r for r, c in x[1]))

def find_best_translation(out: List[List[int]], color: int, pos: List[Tuple[int, int]], base_min_r: int, base_max_r: int, base_min_c: int, base_max_c: int, base_center_r: float, base_center_c: float) -> Tuple[int, int]:
    """Rule: Search for the best rigid translation (dr, dc) for a small component: valid if in bounds, no overlap with non-zero cells, at least one adjacency; score by fill in base bbox, adjacency count, proximity to base center, top-left bias."""
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    anchor_r, anchor_c = get_anchor(pos)
    best_score = (-float('inf'), -float('inf'), float('inf'), float('inf'), float('inf'))
    best_dr, best_dc = 0, 0
    for dr in range(-29, 30):
        for dc in range(-29, 30):
            new_pos = [(r + dr, c + dc) for r, c in pos]
            if not all(0 <= nr < 30 and 0 <= nc < 30 for nr, nc in new_pos):
                continue
            if any(out[nr][nc] != 0 for nr, nc in new_pos):
                continue
            adj = 0
            for nr, nc in new_pos:
                for dx, dy in directions:
                    nnr = nr + dx
                    nnc = nc + dy
                    if 0 <= nnr < 30 and 0 <= nnc < 30 and out[nnr][nnc] != 0:
                        adj += 1
            if adj == 0:
                continue
            fill = sum(base_min_r <= nr <= base_max_r and base_min_c <= nc <= base_max_c for nr, nc in new_pos)
            comp_center_r = sum(r for r, c in pos) / len(pos) + dr
            comp_center_c = sum(c for r, c in pos) / len(pos) + dc
            dist = abs(comp_center_r - base_center_r) + abs(comp_center_c - base_center_c)
            min_nr = min(nr for nr, nc in new_pos)
            min_nc = min(nc for nr, nc in new_pos)
            score = (fill, adj, -dist, -min_nr, -min_nc)
            if score > best_score:
                best_score = score
                best_dr = dr
                best_dc = dc
    return best_dr, best_dc

def place_component(out: List[List[int]], color: int, pos: List[Tuple[int, int]], dr: int, dc: int) -> None:
    """Rule: Place a component at the computed translation (dr, dc) by setting the output cells to the component color."""
    for r, c in pos:
        out[r + dr][c + dc] = color

def program(g: List[List[int]]) -> List[List[int]]:
    """Main rule: Compose extraction, base preservation, clearing, sorted placement of smalls via best translation search to reconstruct the puzzle."""
    out = copy_grid(g)
    components = get_connected_components(g)
    if not components:
        return out
    base = select_base(components)
    base_color, base_pos = base
    clear_non_base(out, base_pos)
    smalls = [c for c in components if c != base]
    smalls = sort_smalls_by_original_position(smalls)
    if not base_pos:
        return out
    base_min_r, base_max_r, base_min_c, base_max_c = get_bbox(base_pos)
    base_center_r = sum(r for r, _ in base_pos) / len(base_pos)
    base_center_c = sum(c for _, c in base_pos) / len(base_pos)
    for color, pos in smalls:
        if not pos:
            continue
        dr, dc = find_best_translation(out, color, pos, base_min_r, base_max_r, base_min_c, base_max_c, base_center_r, base_center_c)
        place_component(out, color, pos, dr, dc)
    return out
```