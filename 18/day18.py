import os
import heapq
from collections import defaultdict

def parse(input):
    with open(input, 'r') as f:
        return [tuple(map(int, c.split(","))) for c in f.readlines()]
    
def print_grid(max_x, max_y, pos):
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in pos:
                print('#', end='')
            else:
                print('.', end='')
        print()

    print()


def in_bounds(p, max_x, max_y):
    x, y = p

    return 0 <= x <= max_x and 0 <= y <= max_y

def next_moves(p, bytes, max_x, max_y):
    x, y = p

    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        if in_bounds((nx, ny), max_x, max_y) and (nx, ny) not in bytes:
            yield (nx, ny)

def shortest_path(source, bytes, max_x, max_y):
    pq = [(0, source)]
    heapq.heapify(pq)

    distances = { (x, y): float("inf") for y in range(max_y + 1) for x in range(max_x + 1) if (x, y) not in bytes }
    pred = defaultdict(tuple)

    visited = set()
    while pq:
        dist, node = heapq.heappop(pq)

        if node in visited:
            continue

        visited.add(node)

        for n in next_moves(node, bytes, max_x, max_y):
            tentative_dist = dist + 1
            if tentative_dist < distances[n]:
                distances[n] = tentative_dist
                pred[n] = node
                heapq.heappush(pq, (tentative_dist, n))

    return distances, pred


def shortest_path_better(source, bytes, max_x, max_y):
    pq = [(0, source)]
    heapq.heapify(pq)

    visited = set()
    while pq:
        dist, node = heapq.heappop(pq)

        if node == (max_x, max_y):
            return dist

        if node in visited:
            continue

        visited.add(node)

        for n in next_moves(node, bytes, max_x, max_y):
            heapq.heappush(pq, (dist + 1, n))

    return None

def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    coords = parse(day_path)
    # max_x, max_y = 6, 6
    # nbytes = 12
    max_x, max_y = 70, 70
    nbytes = 3032

    part1 = shortest_path_better((0, 0), coords[:nbytes], max_x, max_y)

    
    lo = 0
    hi = len(coords)

    while lo <= hi:
        mid = (hi + lo) // 2
        dist = shortest_path_better((0, 0), coords[:mid + 1], max_x, max_y)

        if dist is not None:
            lo = mid + 1
        else:
            hi = mid - 1

    return part1, coords[lo]

print(solve("input.txt"))