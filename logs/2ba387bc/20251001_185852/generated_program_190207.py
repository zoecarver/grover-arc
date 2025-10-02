```python
from typing import List, Dict, Tuple

def extract_color_regions(g: List[List[int]]) -> Dict[int, List[Tuple[int, int]]]:
    color_pos: Dict[int, List[Tuple[int, int]]] = {}
    rows = len(g)
    if rows == 0:
        return color_pos
    cols = len(g[0])
    for r in range(rows):
        for c in range(cols):
            color = g[r][c]
            if color > 0:
                if color not in color_pos:
                    color_pos[color] = []
                color_pos[color].append((r, c))
    return color_pos

def classify_shape(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, color: int) -> str:
    # Check if solid
    is_solid = True
    for rr in range(min_r, max_r + 1):
        for cc in range(min_c, max_c + 1):
            if g[rr][cc] != color:
                is_solid = False
                break
        if not is_solid:
            break
    if is_solid:
        return 'solid'
    # Check if frame
    # Top row
    if any(g[min_r][cc] != color for cc in range(min_c, max_c + 1)):
        return None
    # Bottom row
    if any(g[max_r][cc] != color for cc in range(min_c, max_c + 1)):
        return None
    # Left side
    if any(g[rr][min_c] != color for rr in range(min_r + 1, max_r)):
        return None
    # Right side
    if any(g[rr][max_c] != color for rr in range(min_r + 1, max_r)):
        return None
    # Inner 2x2 empty
    if any(g[rr][cc] != 0 for rr in range(min_r + 1, max_r) for cc in range(min_c + 1, max_c)):
        return None
    return 'frame'

def sort_shapes(shapes: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    return sorted(shapes, key=lambda x: (x[0], x[1]))

def build_pair_rows(left_color: int, left_is_frame: bool, right_color: int) -> List[List[int]]:
    rows: List[List[int]] = []
    for ro in range(4):
        row = [0] * 8
        # Left side (columns 0-3)
        if left_is_frame and left_color != 0:
            if ro == 0 or ro == 3:
                row[0:4] = [left_color] * 4
            else:
                row[0] = left_color
                row[3] = left_color
        else:
            row[0:4] = [left_color] * 4
        # Right side (columns 4-7), always full
        row[4:8] = [right_color] * 4
        rows.append(row)
    return rows

def program(g: List[List[int]]) -> List[List[int]]:
    color_pos = extract_color_regions(g)
    frames: List[Tuple[int, int, int]] = []
    solids: List[Tuple[int, int, int]] = []
    for color, positions in color_pos.items():
        if not positions:
            continue
        min_r = min(r for r, c in positions)
        max_r = max(r for r, c in positions)
        min_c = min(c for r, c in positions)
        max_c = max(c for r, c in positions)
        if max_r - min_r != 3 or max_c - min_c != 3:
            continue
        shape_type = classify_shape(g, min_r, max_r, min_c, max_c, color)
        if shape_type == 'solid':
            solids.append((min_r, min_c, color))
        elif shape_type == 'frame':
            frames.append((min_r, min_c, color))
    frames = sort_shapes(frames)
    solids = sort_shapes(solids)
    num_pairs = max(len(frames), len(solids))
    output: List[List[int]] = []
    for i in range(num_pairs):
        left_color = frames[i][2] if i < len(frames) else 0
        left_is_frame = i < len(frames)
        right_color = solids[i][2] if i < len(solids) else 0
        if left_color == 0:
            left_is_frame = False
        pair_rows = build_pair_rows(left_color, left_is_frame, right_color)
        output.extend(pair_rows)
    return output
```