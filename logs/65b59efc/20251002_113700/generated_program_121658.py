```python
from typing import List

def parse_sections(top_row: list[int]) -> list[tuple[int, int]]:
    """Parse top row into sections of consecutive non-5 values, returning list of (start, length)."""
    sections = []
    i = 0
    n = len(top_row)
    while i < n:
        if top_row[i] == 5:
            i += 1
            continue
        start = i
        while i < n and top_row[i] != 5:
            i += 1
        length = i - start
        if length > 0:
            sections.append((start, length))
    return sections

def compute_s_and_starts(section_tuples: list[tuple[int, int]]) -> tuple[int, list[int]]:
    """Compute s from first section length, and list of starts; assumes at least one section."""
    if not section_tuples:
        return 0, []
    s = section_tuples[0][1]
    starts = [st for st, _ in section_tuples]
    return s, starts

def build_type_data(g: list[list[int]], section_tuples: list[tuple[int, int]], s: int, h: int, w: int
                     ) -> tuple[dict[int, int], list[list[list[int]]], list[int]]:
    """Build id_to_type mapping, masks (s x s each), and colors for each type based on top s rows and bottom centers."""
    id_to_type: dict[int, int] = {}
    masks: list[list[list[int]]] = []
    colors: list[int] = []
    starts = [st for st, _ in section_tuples]
    lengths = [ln for _, ln in section_tuples]
    num_types = len(section_tuples)
    for k in range(num_types):
        start = starts[k]
        sec_len = lengths[k]
        num_cols = min(s, sec_len)
        center_offset = min(s // 2, sec_len - 1)
        center = start + center_offset
        color = g[h - 1][center] if 0 <= center < w else 0
        colors.append(color)
        # Extract subgrid rows 0 to min(s, h-1), cols start to start+num_cols-1
        actual_rows = min(s, h)
        temp_mask = [[0] * num_cols for _ in range(actual_rows)]
        id_val = 0
        consistent = True
        for r in range(actual_rows):
            for cc in range(num_cols):
                c = start + cc
                val = g[r][c] if 0 <= c < w else 0
                if val != 0:
                    if id_val == 0:
                        id_val = val
                    elif val != id_val:
                        consistent = False
                    temp_mask[r][cc] = 1
        # Pad rows to s if fewer
        while len(temp_mask) < s:
            temp_mask.append([0] * num_cols)
        if consistent and id_val != 0:
            id_to_type[id_val] = k
        else:
            id_val = -1  # Invalid, but proceed
        # Pad columns to s
        mask = [row + [0] * (s - num_cols) for row in temp_mask]
        masks.append(mask)
    return id_to_type, masks, colors

def is_non_separator_row(row: list[int], w: int) -> bool:
    """Check if row is not a separator (has <= w/2 fives)."""
    return sum(1 for x in row if x == 5) <= w / 2

def get_non_separator_middle_rows(g: list[list[int]], s: int, h: int, w: int) -> list[int]:
    """Get indices of non-separator rows from s to h-2 inclusive."""
    middle_non_sep = []
    for i in range(s, h - 1):
        if is_non_separator_row(g[i], w):
            middle_non_sep.append(i)
    return middle_non_sep

def compute_section_eff_ends(starts: list[int], lengths: list[int], s: int) -> list[int]:
    """Compute effective end = start + min(s, length) for each section."""
    return [starts[k] + min(s, lengths[k]) for k in range(len(starts))]

def update_placement_for_row(placement: list[list[int]], row_i: int, g_row: list[int], starts: list[int],
                             eff_ends: list[int], id_to_type: dict[int, int], s: int, w: int) -> None:
    """Update placement for one middle row: set placement[row_i][local_col] = type_k for valid val positions."""
    for j in range(w):
        val = g_row[j]
        if val == 0 or val == 5:
            continue
        type_k = id_to_type.get(val, None)
        if type_k is None:
            continue
        found = False
        for k in range(len(starts)):
            start = starts[k]
            eff_end = eff_ends[k]
            if start <= j < eff_end:
                local_col = j - start
                placement[row_i][local_col] = type_k
                found = True
                break
        # If not in any effective section range, skip

def compute_placement(g: list[list[int]], middle_non_sep: list[int], starts: list[int], lengths: list[int],
                      id_to_type: dict[int, int], s: int, w: int) -> list[list[int]]:
    """Compute s x s placement grid from middle non-separator rows, assigning sequential p=0 to s-1."""
    eff_ends = compute_section_eff_ends(starts, lengths, s)
    placement = [[-1] * s for _ in range(s)]
    for p in range(len(middle_non_sep)):
        if p >= s:
            break
        i = middle_non_sep[p]
        update_placement_for_row(placement, p, g[i], starts, eff_ends, id_to_type, s, w)
    return placement

def build_output_grid(placement: list[list[int]], masks: list[list[list[int]]], colors: list[int],
                      s: int) -> list[list[int]]:
    """Build s*s x s*s output grid by placing masks with colors according to placement."""
    out_h = s * s
    out_w = s * s
    out = [[0] * out_w for _ in range(out_h)]
    num_types = len(masks)
    for place_r in range(s):
        for place_c in range(s):
            type_k = placement[place_r][place_c]
            if type_k == -1 or type_k >= num_types:
                continue
            mask = masks[type_k]
            colr = colors[type_k]
            for local_r in range(s):
                for local_c in range(s):
                    if mask[local_r][local_c] != 0:
                        out_r = place_r * s + local_r
                        out_c = place_c * s + local_c
                        out[out_r][out_c] = colr
    return out

def trim_trailing_zeros(g: List[List[int]]) -> List[List[int]]:
    """Trim trailing all-zero rows from the grid."""
    g = [row[:] for row in g]
    while g and all(x == 0 for x in g[-1]):
        g.pop()
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program to solve the puzzle by parsing sections, building masks and placements, and generating output grid."""
    if not g:
        return []
    g = trim_trailing_zeros(g)
    h = len(g)
    if h == 0:
        return []
    w = len(g[0]) if g else 0
    top_row = g[0]
    section_tuples = parse_sections(top_row)
    if not section_tuples:
        return []
    s, starts = compute_s_and_starts(section_tuples)
    if s == 0:
        return []
    lengths = [ln for _, ln in section_tuples]
    id_to_type, masks, colors = build_type_data(g, section_tuples, s, h, w)
    middle_non_sep = get_non_separator_middle_rows(g, s, h, w)
    placement = compute_placement(g, middle_non_sep, starts, lengths, id_to_type, s, w)
    out = build_output_grid(placement, masks, colors, s)
    return out
```