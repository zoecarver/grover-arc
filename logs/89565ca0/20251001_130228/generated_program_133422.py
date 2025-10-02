```python
from typing import List

def flatten_grid(g: List[List[int]]) -> List[int]:
    """Flatten the grid into a 1D list of cell values."""
    return [cell for row in g for cell in row]

def extract_nonzero_colors(flat: List[int]) -> List[int]:
    """Extract unique non-zero colors from the flattened grid, sorted ascending."""
    return sorted({c for c in flat if c != 0})

def select_filler_colors(distinct: List[int]) -> int:
    """Select the smallest color >=5 as the filler; return 0 if none exist."""
    candidates = [c for c in distinct if c >= 5]
    return min(candidates) if candidates else 0

def extract_high_extras(distinct: List[int], filler: int) -> List[int]:
    """Extract high colors (>4 excluding filler) sorted in descending order."""
    extras = [c for c in distinct if c > 4 and c != filler]
    return sorted(extras, reverse=True)

def build_low_set(distinct: List[int]) -> set:
    """Build the set of low colors (1-4) present in distinct colors."""
    return {c for c in distinct if 1 <= c <= 4}

def compute_max_low(low_set: set) -> int:
    """Compute the maximum low color value if low set is non-empty, else 0."""
    return max(low_set) if low_set else 0

def order_lows_with_priority_1(low_set: set) -> List[int]:
    """Start low order with 1 if present."""
    order = []
    if 1 in low_set:
        order.append(1)
    return order

def order_lows_max_le_3(low_base: List[int], low_set: set, max_low: int) -> List[int]:
    """Append descending from max_low to 2 (skipping 1) if max_low <=3."""
    for c in range(max_low, 1, -1):
        if c in low_set:
            low_base.append(c)
    return low_base

def order_lows_max_gt_3(low_base: List[int], low_set: set) -> List[int]:
    """Append 2 if present, then descending from 4 to 3 if max_low >3."""
    if 2 in low_set:
        low_base.append(2)
    for c in range(4, 2, -1):
        if c in low_set:
            low_base.append(c)
    return low_base

def get_low_order(distinct: List[int]) -> List[int]:
    """Order low colors (1-4): prioritize 1, then conditional descending based on max_low."""
    low_set = build_low_set(distinct)
    if not low_set:
        return []
    max_low = compute_max_low(low_set)
    low_order = order_lows_with_priority_1(low_set)
    if max_low <= 3:
        low_order = order_lows_max_le_3(low_order, low_set, max_low)
    else:
        low_order = order_lows_max_gt_3(low_order, low_set)
    return low_order

def combine_bar_colors(extras: List[int], lows: List[int]) -> List[int]:
    """Combine extra high colors and ordered low colors into the bar sequence."""
    return extras + lows

def compute_bar_count(bar_colors: List[int]) -> int:
    """Compute the number of bars (k) from the bar colors sequence."""
    return len(bar_colors)

def generate_length_first() -> int:
    """Length for the first bar: always 1."""
    return 1

def generate_length_second() -> int:
    """Length for the second bar: always 2."""
    return 2

def generate_length_middle() -> int:
    """Length for middle bars (positions 3 to k-1): always 3."""
    return 3

def generate_length_last(k: int) -> int:
    """Length for the last bar: always 4 if k >=1."""
    return 4

def get_bar_lengths(k: int) -> List[int]:
    """Generate bar lengths based on position: 1 for first, 2 for second, 3 for middles, 4 for last."""
    if k == 0:
        return []
    lengths = []
    lengths.append(generate_length_first())
    if k > 1:
        lengths.append(generate_length_second())
    for _ in range(2, k):
        lengths.append(generate_length_middle())
    if k > 0:
        lengths[-1] = generate_length_last(k) if len(lengths) == k else lengths.append(generate_length_last(k))
    if k == 1:
        lengths = [generate_length_first()]
    elif k == 2:
        lengths = [generate_length_first(), generate_length_second()]
    else:
        lengths = [generate_length_first(), generate_length_second()] + [generate_length_middle() for _ in range(k - 2)]
        lengths[-1] = generate_length_last(k)
    return lengths

def build_single_bar(color: int, length: int, filler: int) -> List[int]:
    """Build a single bar row: repeat color for length, pad with filler to 4 cells."""
    return [color] * length + [filler] * (4 - length)

def assemble_output_grid(bar_colors: List[int], lengths: List[int], filler: int) -> List[List[int]]:
    """Assemble the output grid from bar colors, lengths, and filler."""
    return [build_single_bar(color, length, filler) for color, length in zip(bar_colors, lengths)]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: compose all rules to transform input grid to output barcode."""
    flat = flatten_grid(g)
    distinct = extract_nonzero_colors(flat)
    filler = select_filler_colors(distinct)
    extras = extract_high_extras(distinct, filler)
    lows = get_low_order(distinct)
    bar_colors = combine_bar_colors(extras, lows)
    k = compute_bar_count(bar_colors)
    lengths = get_bar_lengths(k)
    return assemble_output_grid(bar_colors, lengths, filler)
```