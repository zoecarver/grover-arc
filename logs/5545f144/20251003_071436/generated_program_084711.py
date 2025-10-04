```python
from collections import Counter
from typing import List

def find_background(g: List[List[int]]) -> int:
    # Rule: background is the most frequent value in the grid
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def get_num_distinct(g: List[List[int]]) -> int:
    # Observation: number of distinct values affects threshold for separator detection
    flat = [cell for row in g for cell in row]
    return len(set(flat))

def get_separator_threshold(h: int, distinct: int) -> int:
    # Rule: adaptive threshold based on grid complexity (distinct values)
    # For simple grids (binary-like, <=2 distinct), low threshold to detect partial separators
    # For complex grids (>2 distinct), high threshold to avoid false positives from content
    if distinct <= 2:
        return h // 5
    else:
        return h // 2

def find_separator_columns(g: List[List[int]], b: int, thresh: int) -> List[int]:
    # Rule: a column is a separator if it has at least 'thresh' non-background cells
    # This handles full and partial vertical separators by density
    h = len(g)
    w = len(g[0]) if g and g[0] else 0
    seps = []
    for j in range(w):
        non_b_count = sum(1 for i in range(h) if g[i][j] != b)
        if non_b_count >= thresh:
            seps.append(j)
    return seps

def calculate_panel_width(w: int, seps: List[int]) -> int:
    # Rule: panels are equal width, excluding separator columns
    m = len(seps)
    if m == 0:
        return w
    return (w - m) // (m + 1)

def extract_first_panel(g: List[List[int]], s: int) -> List[List[int]]:
    # Rule: the output is the leftmost panel, cropped to panel width s, preserving content within it
    return [row[:s] for row in g]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    b = find_background(g)
    distinct = get_num_distinct(g)
    h = len(g)
    thresh = get_separator_threshold(h, distinct)
    seps = find_separator_columns(g, b, thresh)
    w = len(g[0])
    s = calculate_panel_width(w, seps)
    return extract_first_panel(g, s)
```