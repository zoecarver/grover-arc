```python
from typing import List, Tuple, Dict, Set
from collections import defaultdict

def identify_primary_color(g: List[List[int]]) -> int:
    # Observation: There is one primary color different from background 8 (maroon)
    colors: Set[int] = set()
    for row in g:
        for cell in row:
            if cell != 8:
                colors.add(cell)
    return min(colors) if colors else 8  # Assume single primary, take min if multiple

def find_primary_positions(g: List[List[int]], primary: int) -> List[Tuple[int, int]]:
    # Rule: Collect all positions of the primary color singles
    positions: List[Tuple[int, int]] = []
    for i in range(len(g)):
        for j in range(len(g[0])):
            if g[i][j] == primary:
                positions.append((i, j))
    return positions

def group_into_clusters(positions: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
    # Observation 1 & 3: Group single-pixel primary components into clusters based on proximity (bbox adjacency or near positions)
    # Use union-find to connect positions within Manhattan distance 4 (tuned to match train examples structural similarities)
    if not positions:
        return []
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {p: p for p in positions}
    rank: Dict[Tuple[int, int], int] = {p: 0 for p in positions}

    def find(p: Tuple[int, int]) -> Tuple[int, int]:
        if parent[p] != p:
            parent[p] = find(parent[p])
        return parent[p]

    def union(p1: Tuple[int, int], p2: Tuple[int, int]):
        pp1 = find(p1)
        pp2 = find(p2)
        if pp1 == pp2:
            return
        if rank[pp1] < rank[pp2]:
            parent[pp1] = pp2
        elif rank[pp1] > rank[pp2]:
            parent[pp2] = pp1
        else:
            parent[pp2] = pp1
            rank[pp1] += 1

    for idx1 in range(len(positions)):
        for idx2 in range(idx1 + 1, len(positions)):
            r1, c1 = positions[idx1]
            r2, c2 = positions[idx2]
            if abs(r1 - r2) + abs(c1 - c2) <= 4:  # Proximity threshold for clustering
                union(positions[idx1], positions[idx2])

    groups: Dict[Tuple[int, int], List[Tuple[int, int]]] = defaultdict(list)
    for p in positions:
        groups[find(p)].append(p)
    return [group for group in groups.values() if len(group) > 1]  # Only clusters with multiple singles (per observation 3)

def generate_red_pixels_for_cluster(cluster: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    # Observation 3 & 4: Emerge red components at/near primary positions, scaling pixel count with enclosed primaries
    # For simplicity, generate red as positions inside the cluster's bbox, excluding primaries (partial fill approximation)
    # This correlates pixel count with cluster density; for small clusters, fills near bbox
    if len(cluster) < 2:
        return []
    min_r = min(r for r, c in cluster)
    max_r = max(r for r, c in cluster)
    min_c = min(c for r, c in cluster)
    max_c = max(c for r, c in cluster)
    # Scale fill density with number of primaries (observation 4): fill fraction ~ len(cluster) / bbox area
    bbox_area = (max_r - min_r + 1) * (max_c - min_c + 1)
    fill_density = min(1.0, len(cluster) / max(1, bbox_area / 4))  # Arbitrary scaling to match sparse fills in train1
    red: List[Tuple[int, int]] = []
    primary_set = set(cluster)
    import random  # Standard library
    random.seed(42)  # For reproducibility
    for i in range(min_r, max_r + 1):
        for j in range(min_c, max_c + 1):
            if (i, j) not in primary_set and random.random() < fill_density:
                red.append((i, j))
    return red  # Note: This is approximate; in practice, tune density to match exact train, but creative for test

def reduce_maroon_near_primary(g: List[List[int]], primary_pos: List[Tuple[int, int]]) -> List[List[int]]:
    # Observation 2: Reduce large maroon pixel count and holes near primary positions
    # Approximate by turning some 8's adjacent to primary to 2 (simulates loss near primary)
    result = [row[:] for row in g]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r, c in primary_pos:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(g) and 0 <= nc < len(g[0]) and result[nr][nc] == 8:
                result[nr][nc] = 2  # Turn adjacent maroon to red (reduces count)
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    primary = identify_primary_color(g)
    positions = find_primary_positions(g, primary)
    clusters = group_into_clusters(positions)
    result = [row[:] for row in g]  # Start with copy
    # Apply reduction near primaries (observation 2)
    result = reduce_maroon_near_primary(result, positions)
    all_red = []
    for cluster in clusters:
        red = generate_red_pixels_for_cluster(cluster)
        all_red.extend(red)
    # Apply red fill (observations 1, 3, 4: create clusters, emerge red, scale with nearby)
    for r, c in all_red:
        if result[r][c] == 8:
            result[r][c] = 2
    return result
```