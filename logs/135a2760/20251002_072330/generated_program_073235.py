```python
from typing import List, Optional
import collections

def get_background(grid_row: List[int]) -> int:
    """Extract the background color B from the first cell of the row."""
    return grid_row[0]

def get_pattern_range(left: int, right: int, width: int) -> tuple[int, int]:
    """Determine the start and end indices for pattern cells based on side values."""
    if left == 2 and right == 2:
        return 2, width - 3
    return 1, width - 2

def get_main_color(grid_row: List[int], start: int, end: int, B: int) -> Optional[int]:
    """Find the main color C: most frequent non-B, non-2 color in the range."""
    freq = collections.Counter()
    for c in range(start, end + 1):
        val = grid_row[c]
        if val != B and val != 2:
            freq[val] += 1
    if not freq:
        return None
    return max(freq, key=freq.get)

def get_group_size(grid_row: List[int], start: int, end: int, C: int) -> int:
    """Compute the mode group size K for consecutive runs of C in the range. In case of tie, choose the maximum K."""
    runs = []
    i = start
    while i <= end:
        if grid_row[i] == C:
            length = 0
            while i <= end and grid_row[i] == C:
                length += 1
                i += 1
            runs.append(length)
        else:
            i += 1
    if not runs:
        return 1  # Fallback, though shouldn't occur
    run_freq = collections.Counter(runs)
    max_f = run_freq.most_common(1)[0][1]
    possible_ks = [k for k, v in run_freq.items() if v == max_f]
    return max(possible_ks)

def generate_pattern(unit: List[int], period: int, num: int, phase: int) -> List[int]:
    """Generate the pattern list for given unit, period, length, and phase."""
    return [unit[(j + phase) % period] for j in range(num)]

def find_best_phase(grid_row: List[int], start: int, unit: List[int], period: int, num: int) -> int:
    """Find the phase with the maximum matches to the input row segment."""
    best_phase = 0
    best_count = -1
    for p in range(period):
        count = 0
        for j in range(num):
            pat = unit[(j + p) % period]
            if pat == grid_row[start + j]:
                count += 1
        if count > best_count or (count == best_count and p < best_phase):
            best_count = count
            best_phase = p
    return best_phase

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: process each row to apply the pattern completion rule."""
    if not g:
        return []
    h = len(g)
    w = len(g[0])
    out = [row[:] for row in g]
    for r in range(h):
        B = get_background(g[r])
        left = g[r][1]
        right = g[r][w - 2]
        start, end = get_pattern_range(left, right, w)
        num = end - start + 1
        if num <= 0:
            continue
        C = get_main_color(g[r], start, end, B)
        if C is None:
            continue
        K = get_group_size(g[r], start, end, C)
        unit = [C] * K + [B]
        period = len(unit)
        best_p = find_best_phase(g[r], start, unit, period, num)
        pattern = generate_pattern(unit, period, num, best_p)
        for j in range(num):
            out[r][start + j] = pattern[j]
    return out
```