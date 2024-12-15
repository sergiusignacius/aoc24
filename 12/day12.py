import os
from collections import defaultdict
from itertools import combinations

def parse(input):
    with open(input, 'r') as f:
        return [l.strip() for l in f.readlines()]
    
def in_bounds(pos, grid):
    x, y = pos
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

def neighbors_of_region(pos, grid, reverse=False):
    x, y = pos
    value_at = grid[y][x]
    candidates = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    if reverse:
        return [(xx, yy) for (xx, yy) in candidates if in_bounds((xx, yy), grid) and grid[yy][xx] != value_at]
    else:
        return [(xx, yy) for (xx, yy) in candidates if in_bounds((xx, yy), grid) and grid[yy][xx] == value_at]

def bfs(start, grid, visited):
    queue = [start]
    region = []
    while queue:
        plot = queue.pop(0)

        if plot in visited:
            continue

        n_plots = neighbors_of_region(plot, grid)
        region.append((plot, len(n_plots)))
                      
        for nn in n_plots:
            queue.append(nn)
        
        visited.add(plot)

    return region

def colinear(s1, s2):
    x1, y1 = s1
    x2, y2 = s2

    return x1 == x2 or y1 == y2

def diagonal(p, n1, n2, m=-1):
    px, py = p
    n1x, n1y = n1
    n2x, n2y = n2

    return (px + m * (n1x - px) + m * (n2x - px), py + m * (n1y - py) + m * (n2y - py))

def region_of(p, region_map):
    if not in_bounds(p, region_map):
        return -1
    return region_map[p[1]][p[0]]

def check_corner(p, n1, n2, region_map):
    if not colinear(n1, n2):
        px, py = p
        pregion = region_of(p, region_map)

        A = p
        # ? B ?
        # C A N2
        # ? N1 D

        X = diagonal(p, n1, n2)
        D = diagonal(p, n1, n2, 1)

        vert = n1 if n1[0] == p[0] else n2
        horz = n1 if n1[1] == p[1] else n2

        vx, vy = vert
        hx, hy = horz

        B = (vx, py + 1) if vy < py else (vx, py - 1)
        C = (px + 1, hy) if hx < px else (px - 1, hy)

        result = 0

        candidate = False
        if region_of(n1, region_map) == region_of(n2, region_map) == pregion:
            candidate = True

            if region_of(A, region_map) not in [region_of(B, region_map), region_of(C, region_map)]:
                result += 1
            if region_of(D, region_map) != region_of(A, region_map):
                result += 1
        if candidate:
            pass
        return result
    return 0

def all_neighbors(p):
    x, y = p
    candidates = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    return [(xx, yy) for (xx, yy) in candidates]

def sides_of(p, region_map):
    if len(neighbors_of_region(p, region_map)) == 0:
        return 4
    if len(neighbors_of_region(p, region_map)) == 1:
        return 2
    nn = all_neighbors(p)

    result = 0
    for p1, p2 in list(combinations(nn, 2)):
        result += check_corner(p, p1, p2, region_map)

    return result

def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    grid = parse(day_path)
    visited = set()

    regions = defaultdict(list)
    region_map = [["N" for _ in range(len(grid[0]))] for _ in range(len(grid))]

    region_id = 0
    areas = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) not in visited:
                region = bfs((x, y), grid, visited)
                pr = [p for p, _ in region]
                areas.append(len(region))
                for p in pr:
                    region_map[p[1]][p[0]] = region_id
                regions[grid[y][x]].append(region)
                region_id += 1

    sides = [0] * region_id
    
    for _, rs in regions.items():
        for r in rs:
            pr = [p for p, _ in r]
            r_sides = 0
            for p in pr:
                r_sides += sides_of(p, region_map)
            sides[region_of(pr[0], region_map)] = r_sides
    
    part1 = sum([areas[region_of(r[0][0], region_map)] * sum([4 - taken_sides for _, taken_sides in r]) for _, rs in regions.items() for r in rs])
    part2 = sum([sides[r] * areas[r] for r in range(len(sides))])
    
    return part1, part2, grid
    
p1, p2, grid = solve('input.txt')
print(p1, p2)