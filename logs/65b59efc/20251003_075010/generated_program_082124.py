```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    n_rows = len(g)
    n_cols = len(g[0])
    bottom = g[-1]

    # Find centers: group consecutive non-0 in bottom
    centers = []
    i = 0
    while i < n_cols:
        if bottom[i] == 0:
            i += 1
            continue
        # find group
        start = i
        while i < n_cols and bottom[i] != 0:
            i += 1
        # average position
        avg = (start + i - 1) / 2
        centers.append(round(avg))
    g_num = len(centers)

    if g_num == 0:
        return [[0] * n_cols for _ in range(n_rows)]

    # diffs
    diffs = [centers[i+1] - centers[i] for i in range(g_num - 1)]
    w = min(diffs) - 1

    # take up to 3 groups
    centers = centers[:3]
    g_num = len(centers)
    if g_num < 3:
        # pad with dummy
        centers += [centers[-1]] * (3 - g_num)
        # dummy colors 0
        bottom += [0] * (3 - g_num)

    left_c = centers[0]
    mid_c = centers[1]
    right_c = centers[2]

    left_color = bottom[left_c]
    mid_color = bottom[mid_c]
    right_color = bottom[right_c]

    # first section
    sep_rows = [i for i in range(n_rows - 1) if sum(1 for v in g[i] if v == 5) > n_cols // 2]
    first_end = sep_rows[0] if sep_rows else n_rows - 1
    first_h = first_end
    # assume first_h == w

    # used
    used = set()
    for i in range(first_h):
        for j in range(n_cols):
            val = g[i][j]
            if val != 0 and val != 5:
                used.add(val)
    right_used = right_color in used

    # swap mode
    left_top = [g[0][j] != 0 and g[0][j] != 5 for j in range(left_c - w // 2, left_c + w // 2 + 1)]
    swap_mode = len(left_top) > 0 and left_top[0] == 0 and left_top[-1] == 0

    # patterns
    left_pats = []
    mid_pats = []
    right_pats = []
    for r in range(first_h):
        l_start = max(0, left_c - w // 2)
        l_end = min(n_cols, left_c + w // 2 + 1)
        l_pat = [1 if g[r][j] != 0 and g[r][j] != 5 else 0 for j in range(l_start, l_end)]
        l_pat = l_pat[:w]  # pad or truncate if needed, assume correct

        m_start = max(0, mid_c - w // 2)
        m_end = min(n_cols, mid_c + w // 2 + 1)
        m_pat = [1 if g[r][j] != 0 and g[r][j] != 5 else 0 for j in range(m_start, m_end)]
        m_pat = m_pat[:w]

        r_start = max(0, right_c - w // 2)
        r_end = min(n_cols, right_c + w // 2 + 1)
        r_pat = [1 if g[r][j] != 0 and g[r][j] != 5 else 0 for j in range(r_start, r_end)]
        r_pat = r_pat[:w]

        left_pats.append(l_pat)
        mid_pats.append(m_pat)
        right_pats.append(r_pat)

    # output
    size = w * w
    output = [[0] * size for _ in range(size)]

    for out_r in range(size):
        local_r = out_r % first_h

        # left block
        source = ''
        block_pat = []
        block_c = 0
        if swap_mode:
            block_pat = right_pats[local_r][:]
            block_c = right_color
            source = 'right'
        else:
            if right_used:
                block_pat = mid_pats[local_r][:]
                block_c = mid_color
                source = 'mid'
            else:
                block_pat = right_pats[local_r][:]
                block_c = right_color
                source = 'right'

        if source == 'right':
            is_middle_r = local_r == first_h // 2
            only_center = is_middle_r and sum(block_pat) == 1 and block_pat[w // 2] == 1
            if only_center:
                block_pat = [1 - x for x in block_pat]

        for j in range(w):
            if block_pat[j]:
                output[out_r][j] = block_c

        # tiling
        if swap_mode:
            num_empty = max(0, w - 2)
            start = w + num_empty * w
            tile_pat = left_pats[local_r]
            tile_c = left_color
            for k in range(w):
                if tile_pat[k]:
                    if start + k < size:
                        output[out_r][start + k] = tile_c
        else:
            if right_used:
                tile_pat = right_pats[local_r]
                tile_c = right_color
            else:
                tile_pat = mid_pats[local_r]
                tile_c = mid_color
            start = w
            for tile_idx in range(w - 1):
                for k in range(w):
                    pos = start + tile_idx * w + k
                    if pos < size and tile_pat[k]:
                        output[out_r][pos] = tile_c

    return output
```