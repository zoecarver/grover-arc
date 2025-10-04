```python
import typing as tp
from itertools import groupby
from collections import Counter

def identify_stripe_positions(g: tp.List[tp.List[int]]) -> tp.List[tp.Tuple[int, str]]:
    """
    Rule 1: Stripe Position → Color Assignment (Background Interaction)
    Identifies vertical or horizontal stripe positions based on repeating patterns in uniform rows/columns.
    Returns list of (position, color) for stripes; ignored in final rendering as base layer is superseded.
    """
    stripes = []
    # Flatten and detect repeating patterns without nested loops; simplistic for 30x30
    flat = [cell for row in g for cell in row]
    counts = Counter(flat)
    # Assume repeating if count > threshold; return empty as stripes are ignored
    return stripes  # No-op for output generation

def identify_frames(g: tp.List[tp.List[int]]) -> tp.List[tp.Tuple[int, int, int, int, int]]:
    """
    Rule 2: Frame Position → Enclosed Blob Formation (Border-to-Inner Interaction)
    Identifies rectangular frames by finding large consecutive same-color blocks and their bbox.
    Returns list of (color, min_col, min_row, max_col, max_row) for frames.
    Uses groupby to avoid explicit nested loops.
    """
    frames = []
    all_groups = []
    for i, row in enumerate(g):
        pos = 0
        for k, grp in groupby(row):
            length = sum(1 for _ in grp)
            if length > 10:  # Threshold for "large" frame block
                all_groups.append((int(k), length, i, pos, pos + length - 1))
            pos += length
    # Simple aggregation to bbox per color (flat, no nesting)
    frame_dict = {}
    for c, l, r, start, end in all_groups:
        if c not in frame_dict:
            frame_dict[c] = [float('inf'), r, float('-inf'), float('inf'), float('-inf')]
        frame_dict[c][0] = min(frame_dict[c][0], start)
        frame_dict[c][1] = min(frame_dict[c][1], r)
        frame_dict[c][2] = max(frame_dict[c][2], end)
        frame_dict[c][3] = max(frame_dict[c][3], r)
        frame_dict[c][4] = max(frame_dict[c][4], start)  # Dummy for col span
    for c, bbox in frame_dict.items():
        if bbox[2] - bbox[0] + 1 > 15:  # Large enough frame
            frames.append((c, int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])))
    return frames[:1]  # Main frame only

def identify_small_dots(g: tp.List[tp.List[int]]) -> tp.List[tp.Tuple[int, int, int]]:
    """
    Rule 3: Small Dot Position → Larger Blob Hole Creation (Dot-to-Blob Interaction)
    Identifies single-pixel dots (color 1 or 8, isolated).
    Returns list of (row, col, color); simplistic isolation check via neighbors count (flat).
    """
    dots = []
    for i in range(len(g)):
        for j in range(len(g[0])):
            if g[i][j] in (1, 8):
                # Flat neighbor count (up, down, left, right)
                neighbors = 0
                if i > 0 and g[i-1][j] == g[i][j]: neighbors += 1
                if i < len(g)-1 and g[i+1][j] == g[i][j]: neighbors += 1
                if j > 0 and g[i][j-1] == g[i][j]: neighbors += 1
                if j < len(g[0])-1 and g[i][j+1] == g[i][j]: neighbors += 1
                if neighbors == 0:  # Isolated dot
                    dots.append((i, j, g[i][j]))
    return dots

def identify_small_polyominoes(g: tp.List[tp.List[int]]) -> tp.List[tp.Tuple[int, int, int, int, int]]:
    """
    Rule 4: Small Polyomino Position → Blob Color/Edge Modification (Shape-to-Blob Interaction)
    Identifies small connected groups (2-5 pixels, color 2 primarily, bbox width/height 2-3).
    Returns list of (min_row, min_col, max_row, max_col, color); simplistic bbox per color group.
    """
    poly = []
    # Use groupby per row for horizontal, simple vertical check (flat)
    for i in range(len(g)):
        row = g[i]
        pos = 0
        for k, grp in groupby(row):
            length = sum(1 for _ in grp)
            if 2 <= length <= 5 and int(k) == 2:  # Small red polyomino
                # Simple vertical extent check (adjacent rows same color group)
                vspan = 1
                vmin = i
                vmax = i
                for di in [-1, 1]:
                    ni = i + di
                    if 0 <= ni < len(g) and any(g[ni][j] == 2 for j in range(pos, pos+length)):
                        vspan += 1
                        if di < 0: vmin = ni
                        else: vmax = ni
                if 2 <= vspan <= 3:  # Small height
                    poly.append((vmin, pos, vmax, pos + length - 1, 2))
            pos += length
    return poly

def compute_hole_counts_and_density(frames: tp.List[tp.Tuple[int, int, int, int, int]], 
                                    dots: tp.List[tp.Tuple[int, int, int]]) -> tp.Dict:
    """
    Rule 5: Hole Count → Blob Pixel Density (Internal Property Interaction)
    Computes holes per frame from enclosed dots, determines density reduction (~10-20% per hole).
    Returns dict of frame -> (holes, density_factor); factor = 1 - 0.15 * holes
    """
    results = {}
    for frame in frames:
        c, minc, minr, maxc, maxr = frame
        enclosed = [d for d in dots if minr < d[0] < maxr and minc < d[1] < maxc]
        holes = len(enclosed)
        density = max(0.5, 1 - 0.15 * holes)  # Min 50% density
        results[frame] = (holes, density)
    return results

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    """
    Main program: Composes rules to generate output.
    Identifies components using rules 1-5, renders main frame as bordered grid with fill (mode inside color),
    places dots/polyominoes inside at relative positions, reduces density by randomly removing some fill pixels
    (flat list comp), ignores stripes.
    For simplicity, assumes single main frame; relative placement scales to inside dims.
    """
    stripes = identify_stripe_positions(g)  # Ignored
    frames = identify_frames(g)
    if not frames:
        return [[]]  # Empty if no frame
    frame = frames[0]  # Main frame
    c, minc, minr, maxc, maxr = frame
    width = maxc - minc + 3  # +2 borders, +1 adjust
    height = maxr - minr + 3
    inside_w = width - 2
    inside_h = height - 2
    # Fill color: mode of cells near frame (simple flat sample)
    near_cells = []
    for i in range(max(0, minr-1), min(len(g), maxr+2)):
        for j in range(max(0, minc-1), min(len(g[0]), maxc+2)):
            if (i == minr or i == maxr or j == minc or j == maxc) and minr <= i <= maxr and minc <= j <= maxc:
                near_cells.append(g[i][j])
    fill = Counter(near_cells).most_common(1)[0][0] if near_cells else 1
    # Create empty grid
    output = [[0] * width for _ in range(height)]
    # Set borders to frame color
    for row in output[:1] + output[-1:]:
        row[:] = [c] * width
    for r in range(1, height-1):
        output[r][0] = c
        output[r][-1] = c
    # Fill inside with fill color
    for r in range(1, height-1):
        for col in range(1, width-1):
            output[r][col] = fill
    # Place dots (holes) at relative positions, scaled to inside
    dots = identify_small_dots(g)
    holes_dict = compute_hole_counts_and_density(frames, dots)
    holes, density = holes_dict.get(frame, (0, 1.0))
    for dr, dc, dot_c in dots:
        rel_r = (dr - minr) / (maxr - minr) * inside_h
        rel_c = (dc - minc) / (maxc - minc) * inside_w
        out_r = 1 + round(rel_r)
        out_c = 1 + round(rel_c)
        if 1 <= out_r < height-1 and 1 <= out_c < width-1:
            output[out_r][out_c] = dot_c
    # Place polyominoes, modify edges (place near border if outside)
    polys = identify_small_polyominoes(g)
    for pminr, pminc, pmaxr, pmaxc, pcol in polys:
        rel_r = (pminr - minr) / (maxr - minr) * inside_h if pminr >= minr else 1  # Clamp outside to edge
        rel_c = (pminc - minc) / (maxc - minc) * inside_w
        out_r = 1 + round(rel_r)
        out_c = 1 + round(rel_c)
        # Place small block (flat, limited size)
        for pr in range(pmaxr - pminr + 1):
            for pc in range(pmaxc - pminc + 1):
                orr = out_r + pr
                occ = out_c + pc
                if 1 <= orr < height-1 and 1 <= occ < width-1:
                    output[orr][occ] = pcol
    # Reduce density: remove ~ (1-density) fraction of fill cells (flat random sample, but deterministic via hash for repro)
    inside_cells = [(r, col) for r in range(1, height-1) for col in range(1, width-1) if output[r][col] == fill]
    num_remove = int(len(inside_cells) * (1 - density))
    # Deterministic "random" removal (use positions mod)
    to_remove = sorted(inside_cells, key=lambda x: (x[0]*31 + x[1]) % len(inside_cells))[:num_remove]
    for r, col in to_remove:
        output[r][col] = c  # Set to frame color for "hole" effect
    return output
```