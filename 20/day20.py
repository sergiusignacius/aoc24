import os
import heapq
from collections import defaultdict

def manhattan_dist(start, end):
    sx, sy = start
    ex, ey = end

    return (abs(sx - ex) + abs(sy - ey))

def can_warp_to(start, end, path, max_dist=2):
    warp_dist = manhattan_dist(start, end)
    return 1 < warp_dist <= max_dist
    #     # is there actually a point to start the cheat now?
    #     return abs(path.index(end) - path.index(start)) > warp_dist

    # return False

def warp_points(path, walls):
    for px, py in path:
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            s = px + dx, py + dy
            if s in walls:
                for p in [p for p in path if p != (px, py) and can_warp_to(s, p, path, 19)]:
                    yield (px, py), p

def warpable(n = 1):
    for s in ['.', 'S', 'E']:
        for e in ['.', 'S', 'E']:
            yield "{}#{}".format(s, e)

def parse(input):
    with open(input, 'r') as f:
        grid = [l.strip() for l in f.readlines()]

        walls = set()
        start = None
        end = None
        warps = defaultdict(set)
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == "S":
                    start = (x, y)
                elif grid[y][x] == "E":
                    end = (x, y)
                elif grid[y][x] == "#":
                    if x > 1 and x < len(grid[0]) - 1:
                        if grid[y][x - 1:x + 2] in warpable():
                            warps[(x - 1, y)].add((x + 1, y))
                            warps[(x + 1, y)].add((x - 1, y))

                    if y > 1 and y < len(grid) - 1:
                        if ''.join([grid[yy][x] for yy in range(y - 1, y + 2)]) in warpable():
                            warps[(x, y - 1)].add((x, y + 1))
                            warps[(x, y + 1)].add((x, y - 1))
                    walls.add((x, y))

        return walls, start, end, len(grid[0]), len(grid), warps
    
def print_grid(max_x, max_y, walls, pos):
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) == pos:
                print('*', end='')
            elif (x, y) in pos:
                print("*", end='')
            elif (x, y) in walls:
                print("#", end='')
            else:
                print('.', end='')
        print()

    print()


def in_bounds(p, max_x, max_y):
    x, y = p

    return 0 <= x <= max_x and 0 <= y <= max_y

def next_moves(p, max_x, max_y, walls, can_cheat=False):
    x, y = p

    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        if in_bounds((nx, ny), max_x, max_y):
            if can_cheat:
                yield (nx, ny)
            elif (nx, ny) not in walls:
                yield (nx, ny)

def shortest_path_better(source, target, walls, max_x, max_y, path):
    pq = [(0, source)]
    heapq.heapify(pq)

    visited = set()
    while pq:
        dist, node = heapq.heappop(pq)

        if node == target:
            return dist

        if node in visited:
            continue

        visited.add(node)
        path.append(node)

        for n in next_moves(node, max_x, max_y, walls):
            heapq.heappush(pq, (dist + 1, n))

    return None

def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    walls, start, end, max_x, max_y, warps = parse(day_path)

    dists = {}
    path = []
    legit_dist = shortest_path_better(start, end, walls, max_x, max_y, path)
    path.append(end)
    dists = { n: i for (i, n) in enumerate(path) }

    savings = defaultdict(int)

    warps = [(p1, p2) for i, p1 in enumerate(path) for j, p2 in enumerate(path) if i < j and can_warp_to(p1, p2, path, 20)]


    good_warps = set()
    for fr, to in warps:
        from_index = dists[fr]
        to_index = dists[to]
        assert to_index > from_index

        new_cost = manhattan_dist(fr, to) - 1 + len(path) - (to_index - from_index)
        good_warps.add((fr, to))
        savings[legit_dist - new_cost] += 1
    
    return sum([v for k, v in savings.items() if k >= 100])

print(solve("input.txt"))