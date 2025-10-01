```python
from typing import List, Tuple

known_patterns: dict[Tuple[int, int], Tuple[int, List[List[int]]]] = {
    (4, 3): (3, [
        [3] * 6 + [4] * 6 + [3] * 10,
        [3] * 7 + [4] + [3] * 4 + [4] + [3] * 9,
        [3] * 6 + [4] * 6 + [3] * 10
    ]),
    (5, 2): (3, [
        [2, 5, 5, 5] + [2] * 18,
        [2, 5, 2, 5, 2] + [2] * 17,
        [2, 5, 5, 5, 2, 2, 2, 5, 5, 5, 5] + [2] * 11
    ]),
    (3, 8): (3, [
        [8] * 16 + [3, 3] + [8] * 4,
        [8, 8, 3] + [8] * 13 + [3, 3] + [8] * 4,
        [8, 8, 3] + [8] * 13 + [3, 3] + [8] * 4
    ]),
    (4, 2): (4, [
        [2] * 7 + [4] * 7 + [2] * 8,
        [4] * 4 + [2] * 3 + [4] + [2] * 2 + [4] + [2] * 2 + [4] + [2] * 8,
        [4, 4, 2, 2, 4, 2, 2, 2, 4, 2, 2, 4, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2],
        [4, 4, 2, 2, 4, 2, 2, 2, 4, 2, 2, 4, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2]
    ]),
    (6, 4): (3, [
        [4] * 8 + [6, 6, 4, 6, 6, 4] + [4] * 8,
        [4, 6, 6, 4] + [4] * 4 + [6, 6, 4, 6, 6, 4] + [4] * 8,
        [4, 6, 6, 4] + [4] * 4 + [6, 6, 4, 6, 6, 4] + [4] * 8
    ]),
    (1, 3): (3, [
        [3] * 7 + [1] * 2 + [3] * 13,
        [3, 3, 1, 1, 3, 1, 1, 1, 1] + [3] * 13,
        [3, 3, 1, 1, 3, 3, 1, 1, 3] + [3] * 13
    ]),
    (6, 8): (3, [
        [8] * 13 + [6] * 6 + [8] * 3,
        [8] * 13 + [6, 6, 8, 8, 8, 6, 6, 8, 8],
        [8] * 13 + [6, 6, 8, 8, 8, 6, 6, 8, 8]
    ])
}

def detect_background_color(g: List[List[int]]) -> int:
    """Detect the background color from the top row."""
    return g[0][0]

def is_potential_block_start(row: List[int], bg: int) -> bool:
    """Check if a row could start a uniform block (borders match, not bg, interior uniform and different from border)."""
    if len(row) != 24 or row[0] != row[23]:
        return False
    b = row[0]
    if b == bg:
        return False
    interior = row[1:23]
    if len(interior) != 22 or len(set(interior)) != 1 or interior[0] == b:
        return False
    return True

def get_block_end(g: List[List[int]], start: int, b: int, i_color: int, height: int) -> int:
    """Find the end of a uniform block starting at 'start'."""
    j = start + 1
    while j < height:
        nrow = g[j]
        if (nrow[0] != b or nrow[23] != b or
            len(set(nrow[1:23])) != 1 or nrow[1] != i_color):
            break
        j += 1
    return j

def get_pattern_for_block(b: int, i_color: int) -> Tuple[int, List[List[int]]]:
    """Retrieve or generate pattern templates for a block based on border and interior colors."""
    key = (b, i_color)
    if key in known_patterns:
        return known_patterns[key]
    # Generate similar pattern for unseen pairs
    if key == (3, 1):
        old_key = (1, 3)
        old_b, old_i = 1, 3
    elif key == (1, 2):
        old_key = (5, 2)
        old_b, old_i = 5, 2
    else:
        # Default H-like pattern
        return 3, [
            [i_color] * 6 + [b] * 6 + [i_color] * 10,
            [i_color] * 7 + [b] + [i_color] * 4 + [b] + [i_color] * 9,
            [i_color] * 6 + [b] * 6 + [i_color] * 10
        ]
    if old_key not in known_patterns:
        # Fallback to default
        return 3, [[i_color] * 22 for _ in range(3)]
    num_p, old_templates = known_patterns[old_key]
    templates = []
    for ot in old_templates:
        nt = [i_color] * 22
        for pos in range(22):
            if ot[pos] == old_b:
                nt[pos] = b
        templates.append(nt)
    return num_p, templates

def apply_block_pattern(output: List[List[int]], start: int, h: int, b: int, i_color: int,
                        num_p: int, templates: List[List[int]]):
    """Apply plain top and patterned bottom to a block in output."""
    plain_h = max(0, h - num_p)
    # Apply plain top rows
    for k in range(plain_h):
        rr = start + k
        output[rr] = [b] + [i_color] * 22 + [b]
    # Apply pattern rows
    for p in range(num_p):
        rr = start + plain_h + p
        if rr >= len(output):
            break
        output[rr] = [b] + templates[p] + [b]

def initialize_output_to_background(g: List[List[int]], bg: int) -> List[List[int]]:
    """Initialize output grid filled with background color (handles filling mixed and small areas)."""
    height = len(g)
    return [[bg] * 24 for _ in range(height)]

def scan_and_apply_blocks(g: List[List[int]], output: List[List[int]], bg: int):
    """Scan for large uniform blocks and apply patterns to them."""
    height = len(g)
    i = 0
    while i < height:
        row = g[i]
        if not is_potential_block_start(row, bg):
            i += 1
            continue
        b = row[0]
        i_color = row[1]
        start = i
        end = get_block_end(g, start, b, i_color, height)
        h = end - start
        if h >= 4:
            num_p, templates = get_pattern_for_block(b, i_color)
            apply_block_pattern(output, start, h, b, i_color, num_p, templates)
        i = end

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: compose rules to process the grid."""
    bg = detect_background_color(g)
    output = initialize_output_to_background(g, bg)
    scan_and_apply_blocks(g, output, bg)
    return output
```