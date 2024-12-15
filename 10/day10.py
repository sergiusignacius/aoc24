import os
from collections import defaultdict
from itertools import combinations

def parse(input):
    with open(input, 'r') as f:
        grid = [list(map(int, l.strip())) for l in f.readlines()]

        trailheads = [(x, y) for y in range(len(grid)) for x in range(len(grid[0])) if grid[y][x] == 0]

        return grid, trailheads

def in_bounds(pos, grid):
    x, y = pos
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

def neighbors(pos, grid):
    x, y = pos
    value_at = grid[y][x]
    candidates = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    return [(xx, yy) for (xx, yy) in candidates if in_bounds((xx, yy), grid) and grid[yy][xx] == value_at + 1]

def print_grid(grid, pos):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) in pos:
                print('*', end='')
            else:
                print(grid[y][x], end='')
        print()

    print()

def bfs(grid, trailhead, target, allow_dups=False):
    queue = [trailhead]
    score = 0
    visited = set()
    while queue:
        # print_grid(grid, queue)
        x, y = queue.pop(0)

        if (x, y) in visited and allow_dups:
            continue

        visited.add((x, y))
        if grid[y][x] == target:
            score += 1
        for n in neighbors((x, y), grid):
            queue.append(n)

    return score
        

def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    grid, trailheads = parse(day_path)
    part2 = True
    print(sum([bfs(grid, t, 9, allow_dups=not part2) for t in trailheads]))
    
        
solve('input.txt')