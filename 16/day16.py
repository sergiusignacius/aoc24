import os
import heapq
from collections import defaultdict

def parse(input):
    with open(input, 'r') as f:
        maze = [l.strip() for l in f.readlines()]

        start = None
        end = None
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == "S":
                    start = (x, y)
                elif maze[y][x] == "E":
                    end = (x, y)

        return start, end, maze
    
RIGHT = (1, 0)
UP = (0, -1)
LEFT = (-1, 0)
DOWN = (0, 1)

def turn_counter(dir):
    if dir == RIGHT:
        return UP
    elif dir == UP:
        return LEFT
    elif dir == LEFT:
        return DOWN
    else:
        return RIGHT
    
def turn(dir):
    if dir == RIGHT:
        return DOWN
    elif dir == DOWN:
        return LEFT
    elif dir == LEFT:
        return UP
    else:
        return RIGHT

def next_move(p, dir, maze):
    px, py = p
    dx, dy = dir

    return ((px + dx, py + dy), dir) if maze[py + dy][px + dx] != "#" else None

def next_moves(p, dir, maze):
    t = turn(dir)
    ct = turn_counter(dir)
    
    moves = [(next_move(p, ct, maze), 1000), (next_move(p, t, maze), 1000), (next_move(p, dir, maze), 0)]

    return [m for m in moves if m[0] is not None and maze[m[0][0][1]][m[0][0][0]] != "#"]

def shortest_path(source, goal, maze):
    pq = [(0, (source, RIGHT))]
    heapq.heapify(pq)

    distances = { ((x, y), d): float("inf") for y in range(len(maze)) for x in range(len(maze[0])) for d in [RIGHT, UP, LEFT, DOWN] if maze[y][x] != "#" }
    pred = defaultdict(set)

    visited = set()
    while pq:
        dist, (node, dir) = heapq.heappop(pq)

        if (node, dir) in visited:
            continue
        visited.add((node, dir))

        for (n, nd), c in next_moves(node, dir, maze):
            tentative_dist = dist + c + 1
            if tentative_dist < distances[(n, nd)]:
                distances[(n, nd)] = tentative_dist
                pred[(n, nd)] = set([(node, dir)])
                heapq.heappush(pq, (tentative_dist, (n, nd)))
            elif tentative_dist == distances[(n, nd)]:
                pred[(n, nd)].add((node, dir))

    return distances, pred

def print_grid(maze, path):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == "#":
                print("#", end="")
            elif (x, y) in path:
                print("O", end="")
            else:
                print(".", end="")
        print()
    print()

def aggregate_nodes(node, coll, pred):
    nn, _ = node
    coll.add(nn)
    for nn in pred[node]:
        aggregate_nodes(nn, coll, pred)

def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    start, end, maze = parse(day_path)

    dists, pred = shortest_path(start, end, maze)

    best_dist = min([dists[(end, d)] for d in [DOWN, RIGHT, LEFT, UP]])

    nodes_in_paths = set()
    for d in [DOWN, RIGHT, UP, LEFT]:
        nn = (end, d)
        if dists[nn] == best_dist:
            aggregate_nodes(nn, nodes_in_paths, pred)

    return best_dist, len(nodes_in_paths)

print(solve("input.txt"))