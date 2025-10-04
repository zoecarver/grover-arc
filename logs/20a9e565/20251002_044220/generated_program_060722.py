```python
from typing import List
import sys

def remove_orange(g: List[List[int]]) -> List[List[int]]:
    # Rule: Ignore orange components (color 5), set them to 0 as they are consistent markers with no effect on output
    return [[0 if cell == 5 else cell for cell in row] for row in g]

def get_colors_present(g: List[List[int]]) -> set:
    # Observation: Output colors are subset of input colors excluding 0 and 5
    colors = set()
    for row in g:
        for cell in row:
            if cell > 0 and cell != 5:
                colors.add(cell)
    return colors

def find_main_color(g: List[List[int]]) -> int:
    # Rule: Select the color with the most pixels as the primary color for output (consistent with train examples where dominant color is used)
    color_counts = {c: 0 for c in get_colors_present(g)}
    for row in g:
        for cell in row:
            if cell in color_counts:
                color_counts[cell] += 1
    if not color_counts:
        return 0
    return max(color_counts, key=color_counts.get)

def normalize_position(g: List[List[int]]) -> List[List[int]]:
    # Observation: All output components are normalized to start at [0,0]
    # Find min row and min col with non-zero (excluding 5, already removed)
    non_zero_rows = [i for i, row in enumerate(g) if any(cell != 0 for cell in row)]
    if not non_zero_rows:
        return []
    min_r = min(non_zero_rows)
    min_cs = [min(j for j, cell in enumerate(row) if cell != 0) for row in g[min_r:] if any(cell != 0 for cell in row)]
    min_c = min(min_cs) if min_cs else 0
    # Crop and shift
    height = len(g) - min_r
    width = len(g[0]) - min_c if g else 0
    new_g = [[0] * width for _ in range(height)]
    for i in range(min_r, len(g)):
        for j in range(min_c, len(g[0])):
            if i - min_r < height and j - min_c < width:
                new_g[i - min_r][j - min_c] = g[i][j]
    return new_g

def preserve_zero_holes(g: List[List[int]]) -> List[List[int]]:
    # Observation: If input has zero holes across components, output has zero holes (no filling or adding holes)
    # This function ensures no artificial holes are introduced; return as is (simple identity for zero case)
    # Note: Full hole detection is complex, so assume zero input implies zero output by not modifying
    return g

def generate_output_from_main(g: List[List[int]], main_color: int) -> List[List[int]]:
    # Rule: Create output using main color in normalized position; for simplicity, fill the normalized grid with main color where non-zero
    # This is a basic composition; refine based on pattern type in future iterations
    normalized = normalize_position(g)
    if not normalized:
        return []
    h, w = len(normalized), len(normalized[0])
    output = [[0] * w for _ in range(h)]
    for i in range(h):
        for j in range(w):
            if normalized[i][j] == main_color:
                output[i][j] = main_color
            elif normalized[i][j] != 0:
                output[i][j] = main_color  # Merge other colors to main for silhouette
    # Crop to tight bbox for output
    non_zero_rows_out = [i for i in range(h) if any(cell != 0 for cell in output[i])]
    if not non_zero_rows_out:
        return []
    min_r_out = min(non_zero_rows_out)
    max_r_out = max(non_zero_rows_out)
    min_cs_out = [min(j for j, cell in enumerate(row) if cell != 0) for row in output[min_r_out:max_r_out + 1] if any(cell != 0 for cell in row)]
    min_c_out = min(min_cs_out) if min_cs_out else 0
    max_cs_out = [max(j for j, cell in enumerate(row) if cell != 0) for row in output[min_r_out:max_r_out + 1] if any(cell != 0 for cell in row)]
    max_c_out = max(max_cs_out) if max_cs_out else 0
    out_h = max_r_out - min_r_out + 1
    out_w = max_c_out - min_c_out + 1
    final_out = [[0] * out_w for _ in range(out_h)]
    for i in range(min_r_out, max_r_out + 1):
        for j in range(min_c_out, max_c_out + 1):
            final_out[i - min_r_out][j - min_c_out] = output[i][j]
    return final_out

def program(g: List[List[int]]) -> List[List[int]]:
    # Compose all rules: remove orange, find main color, normalize, preserve zero holes, generate output
    cleaned = remove_orange(g)
    main_c = find_main_color(cleaned)
    normalized = normalize_position(cleaned)
    preserved = preserve_zero_holes(normalized)
    output = generate_output_from_main(preserved, main_c)
    if not output:
        # Fallback for empty: return empty grid
        return []
    # Ensure rectangular
    w = len(output[0]) if output else 0
    return output
```