```python
from typing import List, Dict, Tuple
from collections import defaultdict, Counter

def find_left_stem(g: List[List[int]]) -> Tuple[int, int]:
    """Find the leftmost uniform non-zero column across all rows, representing the left support stem."""
    H = len(g)
    if H == 0:
        return -1, 0
    W = len(g[0])
    for col in range(W):
        colors = [row[col] for row in g]
        first = colors[0]
        if first != 0 and all(c == first for c in colors):
            return col, first
    return -1, 0

def find_stem_col(g: List[List[int]], left_stem_col: int) -> Tuple[int, int]:
    """Find the leftmost column after left stem with a dominant non-zero mode color matching top and bottom, appearing more than H//2 times, representing the main stem."""
    H = len(g)
    if H == 0:
        raise ValueError("Empty grid")
    W = len(g[0])
    start_col = left_stem_col + 1 if left_stem_col >= 0 else 0
    for col in range(start_col, W):
        col_colors = [row[col] for row in g]
        counter = Counter(col_colors)
        mode, count = counter.most_common(1)[0]
        if mode != 0 and g[0][col] == mode == g[H - 1][col] and count > H // 2:
            return col, mode
    raise ValueError("No stem column found")

def is_stem_uniform(g: List[List[int]], stem_col: int, frame_color: int, H: int) -> bool:
    """Check if the stem column is entirely uniform with the frame color."""
    col_colors = [row[stem_col] for row in g]
    return all(c == frame_color for c in col_colors)

def compute_key_col(stem_col: int, is_uniform: bool) -> int:
    """Determine the key column for branch colors: stem_col if not uniform, else stem_col + 1."""
    return stem_col if not is_uniform else stem_col + 1

def compute_base_colors(g: List[List[int]], stem_col: int) -> set[int]:
    """Compute base colors: non-zero colors unique to left of stem (not appearing right of stem)."""
    H = len(g)
    W = len(g[0])
    left_colors = set()
    right_colors = set()
    for i in range(H):
        for c in range(stem_col):
            val = g[i][c]
            if val != 0:
                left_colors.add(val)
        for c in range(stem_col, W):
            val = g[i][c]
            if val != 0:
                right_colors.add(val)
    return left_colors - right_colors

def clean_left_middle_rows(g: List[List[int]], base_colors: set[int], stem_col: int, H: int) -> List[List[int]]:
    """Clean non-base colors in left columns (0 to stem_col-1) for middle rows (1 to H-2)."""
    out = [row[:] for row in g]
    for i in range(1, H - 1):
        for c in range(stem_col):
            if out[i][c] not in base_colors:
                out[i][c] = 0
    return out

def set_mirror_column(out: List[List[int]], key_col: int, W: int, H: int) -> List[List[int]]:
    """Set the rightmost column (W-1) to mirror the key column value for all rows."""
    for i in range(H):
        out[i][W - 1] = out[i][key_col]
    return out

def zero_inner_right_middle(out: List[List[int]], key_col: int, W: int, H: int) -> List[List[int]]:
    """Zero the inner right columns (key_col+1 to W-2) for middle rows (1 to H-2)."""
    for i in range(1, H - 1):
        for c in range(key_col + 1, W - 1):
            out[i][c] = 0
    return out

def extract_anchors(out: List[List[int]], key_col: int, frame_color: int, H: int) -> Dict[int, List[int]]:
    """Extract anchor rows (middle rows) per color C != frame_color where key_col == C."""
    anchors = defaultdict(list)
    for i in range(1, H - 1):
        c = out[i][key_col]
        if c != 0 and c != frame_color:
            anchors[c].append(i)
    return dict(anchors)

def extract_clues(g: List[List[int]], key_col: int, frame_color: int, W: int) -> Dict[int, List[int]]:
    """Extract clue positions in top row (row 0, columns key_col to W-2) per color C != frame_color."""
    clues = defaultdict(list)
    for p in range(key_col, W - 1):
        c = g[0][p]
        if c != 0 and c != frame_color:
            clues[c].append(p)
    return dict(clues)

def compute_mid_col(stem_col: int) -> int:
    """Compute the mid column for shape relative deltas: (stem_col - 1) // 2."""
    return (stem_col - 1) // 2

def extract_shape(g: List[List[int]], C: int, stem_col: int, mid_col: int, H: int, W: int) -> Tuple[defaultdict, int]:
    """Extract relative shape (delta_r to set of delta_c) and orig_center for color C from left columns in all rows."""
    left_cells = [(r, cc) for r in range(H) for cc in range(stem_col) if g[r][cc] == C]
    if not left_cells:
        return defaultdict(set), 0  # Empty shape indicator
    min_r = min(r for r, _ in left_cells)
    max_r = max(r for r, _ in left_cells)
    orig_center = min_r + (max_r - min_r) // 2
    shape = defaultdict(set)
    for r, cc in left_cells:
        delta_r = r - orig_center
        delta_c = cc - mid_col
        shape[delta_r].add(delta_c)
    return shape, orig_center

def place_primary_shape(out: List[List[int]], C: int, primary_a: int, clues_list: List[int], shape: defaultdict, orig_center: int, key_col: int, W: int, H: int, frame_color: int) -> List[List[int]]:
    """Place the shape for primary anchor at each clue position, aligning center to primary_a, skipping positive delta_r if orig_center > primary_a, set if empty."""
    include_positive = orig_center <= primary_a
    for p in clues_list:
        for delta_r in list(shape.keys()):
            if delta_r > 0 and not include_positive:
                continue
            tr = primary_a + delta_r
            if 1 <= tr < H - 1:
                for delta_c in shape[delta_r]:
                    tc = p + delta_c
                    if key_col + 1 <= tc < W - 1 and out[tr][tc] == 0:
                        out[tr][tc] = C
    return out

def place_secondary_fills(out: List[List[int]], C: int, secondary_as: List[int], clues_list: List[int], key_col: int, W: int) -> List[List[int]]:
    """For each secondary anchor row, place horizontal adjacent fills (p-1 to p+1) at each clue p if empty."""
    for a_r in secondary_as:
        for p in clues_list:
            for dc in [-1, 0, 1]:
                tc = p + dc
                if key_col + 1 <= tc < W - 1 and out[a_r][tc] == 0:
                    out[a_r][tc] = C
    return out

def place_shapes(out: List[List[int]], anchors: Dict[int, List[int]], clues: Dict[int, List[int]], shapes: Dict[int, Tuple[defaultdict, int]], key_col: int, W: int, H: int, frame_color: int) -> List[List[int]]:
    """Place shapes for primary anchors and adjacent fills for secondary anchors per color, skipping empty shapes."""
    for C in anchors:
        if C not in clues or C == frame_color:
            continue
        anchor_list = anchors[C]
        clues_list = clues[C]
        shape_info = shapes.get(C, (defaultdict(set), 0))
        shape, orig_center = shape_info
        if not shape:  # Empty shape, skip all placements for this C
            continue
        # Find primary anchor closest to orig_center
        primary_a = min(anchor_list, key=lambda ar: abs(ar - orig_center))
        secondary_as = [ar for ar in anchor_list if ar != primary_a]
        # Place primary shape
        out = place_primary_shape(out, C, primary_a, clues_list, shape, orig_center, key_col, W, H, frame_color)
        # Place secondary fills
        out = place_secondary_fills(out, C, secondary_as, clues_list, key_col, W)
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: compose all rules to transform the input grid according to puzzle semantics."""
    H = len(g)
    if H == 0:
        return []
    W = len(g[0])
    # Find structural columns
    left_stem_col, _ = find_left_stem(g)
    stem_col, frame_color = find_stem_col(g, left_stem_col)
    is_uniform = is_stem_uniform(g, stem_col, frame_color, H)
    key_col = compute_key_col(stem_col, is_uniform)
    # Compute colors and clean
    base_colors = compute_base_colors(g, stem_col)
    out = clean_left_middle_rows(g, base_colors, stem_col, H)
    # Set mirror and zero inner
    out = set_mirror_column(out, key_col, W, H)
    out = zero_inner_right_middle(out, key_col, W, H)
    # Extract placements data
    anchors = extract_anchors(out, key_col, frame_color, H)
    clues = extract_clues(g, key_col, frame_color, W)
    mid_col = compute_mid_col(stem_col)
    shapes = {}
    for C in set(anchors.keys()) | set(clues.keys()):
        shape, orig_center = extract_shape(g, C, stem_col, mid_col, H, W)
        shapes[C] = (shape, orig_center)
    # Place shapes and fills
    out = place_shapes(out, anchors, clues, shapes, key_col, W, H, frame_color)
    return out
```