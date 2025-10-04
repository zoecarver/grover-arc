```python
from typing import List, Tuple

def find_seeds(g: List[List[int]]) -> List[Tuple[int, int]]:
    last = g[-1]
    return [(last[j], j) for j in range(len(last)) if last[j] != 0 and last[j] != 5]

def find_separators(seeds: List[Tuple[int, int]]) -> List[int]:
    xs = [x for _, x in seeds]
    return [(xs[i] + xs[i + 1]) // 2 for i in range(len(xs) - 1)]

def extract_sections(g: List[List[int]], seps: List[int], width: int) -> List[List[List[int]]]:
    bounds = [0] + seps + [width]
    sections = []
    for i in range(len(bounds) - 1):
        start, end = bounds[i], bounds[i + 1]
        sec = [row[start:end] for row in g[:-1]]
        sections.append(sec)
    return sections

def colorize(section: List[List[int]], color: int) -> List[List[int]]:
    return [[color if c != 0 and c != 5 else 0 for c in row] for row in section]

def concatenate_sections(colored_sections: List[List[List[int]]]) -> List[List[int]]:
    if not colored_sections:
        return []
    num_rows = len(colored_sections[0])
    return [sum((sec[r] for sec in colored_sections), []) for r in range(num_rows)]

def program(g: List[List[int]]) -> List[List[int]]:
    seeds = find_seeds(g)
    seps = find_separators(seeds)
    width = len(g[0]) if g else 0
    sections = extract_sections(g, seps, width)
    colored_sections = [colorize(sec, seeds[i][0]) for i, sec in enumerate(sections)]
    concat = concatenate_sections(colored_sections)
    h = len(concat)
    w = len(concat[0]) if concat else 0
    s = max(h, w)
    padded_concat = [row + [0] * (s - w) for row in concat]
    out = padded_concat + [[0] * s for _ in range(s - h)]
    return out
```