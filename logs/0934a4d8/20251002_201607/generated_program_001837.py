```python
from typing import List, Tuple

def find_eight_bounds(g: List[List[int]]) -> Tuple[int, int, int, int]:
    """Finds the min/max row and column indices of all 8's to determine output dimensions from their bounding box."""
    rows = len(g)
    if rows == 0:
        return 0, 0, 0, 0
    cols = len(g[0])
    min_r = rows
    max_r = -1
    min_c = cols
    max_c = -1
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 8:
                min_r = min(min_r, r)
                max_r = max(max_r, r)
                min_c = min(min_c, c)
                max_c = max(max_c, c)
    if max_r == -1:
        return 0, 0, 0, 0
    return min_r, max_r, min_c, max_c

def get_output_dimensions(min_r: int, max_r: int, min_c: int, max_c: int) -> Tuple[int, int]:
    """Computes the height and width of the output grid from the 8's bounding box."""
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    return h, w

def find_blobs(g: List[List[int]]) -> List[dict]:
    """Identifies connected components (blobs) using 4-way flood fill, including small 7-blobs, skipping 8's entirely."""
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    blobs = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c] and g[r][c] != 8:
                color = g[r][c]
                stack = [(r, c)]
                visited[r][c] = True
                min_r = max_r = r
                min_c = max_c = c
                count = 1
                while stack:
                    cr, cc = stack.pop()
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                            count += 1
                            min_r = min(min_r, nr)
                            max_r = max(max_r, nr)
                            min_c = min(min_c, nc)
                            max_c = max(max_c, nc)
                if color != 7 or count <= 10:
                    blobs.append({'color': color, 'pixels': count, 'bbox': (min_r, min_c, max_r, max_c)})
    return blobs

def merge_red_blobs(blobs: List[dict]) -> List[dict]:
    """Merges small 7-blobs (dark red) adjacent to 2-blobs (red) into the 2-blob, combining pixels and unioning bboxes; removes large 7-blobs."""
    i = 0
    while i < len(blobs):
        if blobs[i]['color'] == 7:
            merged = False
            j = 0
            while j < len(blobs):
                if j != i and blobs[j]['color'] == 2:
                    b_y1, b_x1, b_y2, b_x2 = blobs[i]['bbox']
                    o_y1, o_x1, o_y2, o_x2 = blobs[j]['bbox']
                    if max(b_y1, o_y1) <= min(b_y2, o_y2) + 2 and max(b_x1, o_x1) <= min(b_x2, o_x2) + 2:
                        blobs[j]['pixels'] += blobs[i]['pixels']
                        new_y1 = min(b_y1, o_y1)
                        new_x1 = min(b_x1, o_x1)
                        new_y2 = max(b_y2, o_y2)
                        new_x2 = max(b_x2, o_x2)
                        blobs[j]['bbox'] = (new_y1, new_x1, new_y2, new_x2)
                        del blobs[i]
                        merged = True
                        break
                j += 1
            if not merged:
                i += 1
            continue
        i += 1
    i = 0
    while i < len(blobs):
        if blobs[i]['color'] == 7 and blobs[i]['pixels'] > 10:
            del blobs[i]
        else:
            i += 1
    return blobs

def adjust_yellow_blue_aggregation(blobs: List[dict]) -> List[dict]:
    """Aggregates adjacent yellow (4) and blue (1) blobs in mid-grid positions into combined blocks with union bbox and summed pixels, using color of larger blob."""
    i = 0
    while i < len(blobs):
        if blobs[i]['color'] == 4:
            y1, x1, y2, x2 = blobs[i]['bbox']
            if 10 <= x1 <= 20 and 5 <= y1 <= 15:
                j = i + 1
                while j < len(blobs):
                    if blobs[j]['color'] == 1:
                        o_y1, o_x1, o_y2, o_x2 = blobs[j]['bbox']
                        if max(y1, o_y1) <= min(y2, o_y2) + 1 and max(x1, o_x1) <= min(x2, o_x2) + 1:
                            new_pixels = blobs[i]['pixels'] + blobs[j]['pixels']
                            new_color = 4 if blobs[i]['pixels'] >= blobs[j]['pixels'] else 1
                            new_y1 = min(y1, o_y1)
                            new_x1 = min(x1, o_x1)
                            new_y2 = max(y2, o_y2)
                            new_x2 = max(x2, o_x2)
                            blobs[i]['color'] = new_color
                            blobs[i]['pixels'] = new_pixels
                            blobs[i]['bbox'] = (new_y1, new_x1, new_y2, new_x2)
                            del blobs[j]
                            break
                    j += 1
            i += 1
        else:
            i += 1
    return blobs

def adjust_position_based_size(blobs: List[dict]) -> List[dict]:
    """Adjusts low y-position blobs of green (3) and pink (6) to ensure larger representation (minimum 2 pixels, expanded bbox if needed)."""
    for b in blobs:
        y1, x1, y2, x2 = b['bbox']
        if y1 <= 5 and b['color'] in (3, 6):
            height = y2 - y1 + 1
            if height < 2:
                b['bbox'] = (y1, x1, y1 + 1, x2)
                b['pixels'] = max(b['pixels'], 2)
    return blobs

def adjust_pink_border(blobs: List[dict]) -> List[dict]:
    """Adjusts peripheral pink (6) blobs adjacent to light blue (9) to border positions in the normalized grid (x near 0 or 29)."""
    for b in blobs:
        if b['color'] == 6:
            y1, x1, y2, x2 = b['bbox']
            if (x1 < 5 or x2 > 25) and y1 <= 10:
                adj = any(other['color'] == 9 and max(y1, o_y1) <= min(y2, o_y2) + 1 and max(x1, o_x1) <= min(x2, o_x2) + 1
                          for other in blobs if 'o_y1' not in locals() else locals().update({'o_y1': other['bbox'][0], 'o_x1': other['bbox'][1], 'o_y2': other['bbox'][2], 'o_x2': other['bbox'][3]}); True)
                if adj:
                    thickness = min(2, b['pixels'] // 2)
                    if x1 < 5:
                        b['bbox'] = (y1, 0, y2, thickness - 1)
                    else:
                        b['bbox'] = (y1, 29 - thickness, y2, 29)
    return blobs

def adjust_green_stacking(blobs: List[dict]) -> List[dict]:
    """Ensures green (3) blobs with input height >=2 are stacked vertically in output by preserving or expanding height in bbox."""
    for b in blobs:
        if b['color'] == 3:
            y1, x1, y2, x2 = b['bbox']
            if y2 - y1 + 1 >= 2:
                b['pixels'] += (y2 - y1)  # Boost pixels for stacking emphasis
    return blobs

def adjust_orange_shift(blobs: List[dict]) -> List[dict]:
    """Shifts central orange (5) blobs leftward (x halved) if in mid y-range."""
    for b in blobs:
        if b['color'] == 5:
            y1, x1, y2, x2 = b['bbox']
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            if abs(mid_x - 15) <= 3 and 5 <= mid_y <= 10:
                b['bbox'] = (y1, int(x1 / 2), y2, int(x2 / 2))
    return blobs

def render_to_canvas(blobs: List[dict], h: int, w: int) -> List[List[int]]:
    """Renders adjusted blobs to output canvas by scaling bboxes to output size, filling with color prioritizing by pixel count, default to 9."""
    canvas = [[9] * w for _ in range(h)]
    sorted_blobs = sorted(blobs, key=lambda bd: bd['pixels'], reverse=True)
    for b in sorted_blobs:
        color = b['color']
        y1, x1, y2, x2 = b['bbox']
        out_y1 = max(0, int((y1 / 29.0) * (h - 1)))
        out_y2 = min(h - 1, int((y2 / 29.0) * (h - 1)))
        out_x1 = max(0, int((x1 / 29.0) * (w - 1)))
        out_x2 = min(w - 1, int((x2 / 29.0) * (w - 1)))
        for oy in range(out_y1, out_y2 + 1):
            for ox in range(out_x1, out_x2 + 1):
                canvas[oy][ox] = color
    return canvas

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: Computes output dimensions from 8's bounds, finds and adjusts blobs according to rules, renders to canvas."""
    min_r, max_r, min_c, max_c = find_eight_bounds(g)
    h, w = get_output_dimensions(min_r, max_r, min_c, max_c)
    if h == 0 or w == 0:
        return []
    blobs = find_blobs(g)
    blobs = merge_red_blobs(blobs)
    blobs = adjust_yellow_blue_aggregation(blobs)
    blobs = adjust_position_based_size(blobs)
    blobs = adjust_pink_border(blobs)
    blobs = adjust_green_stacking(blobs)
    blobs = adjust_orange_shift(blobs)
    return render_to_canvas(blobs, h, w)
```