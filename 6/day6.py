import os
from functools import cmp_to_key

def parse(input):
    with open(input, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        max_y = len(lines) - 1
        max_x = len(lines[0]) - 1

        obstacles = [(x, y) for y, row in enumerate(lines) for x, c in enumerate(row) if c == "#"]
        start = [(x, y) for y, row in enumerate(lines) for x, c in enumerate(row) if c == "^"][0]
        return obstacles, start, max_x, max_y

UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)

DIRS = [UP, RIGHT, DOWN, LEFT]

def turn(dir):
    return DIRS[(DIRS.index(dir) + 1) % len(DIRS)]

def next_obstacle(pos, dir, obstacles):
    px, py = pos
    if dir == UP:
        ox, oy = px, max([oy for ox, oy in obstacles if ox == px and oy < py], default=None)
    elif dir == DOWN:
        ox, oy = px, min([oy for ox, oy in obstacles if ox == px and oy > py], default=None)
    elif dir == RIGHT:
        ox, oy = min([ox for ox, oy in obstacles if oy == py and ox > px], default=None), py
    else:
        ox, oy = max([ox for ox, oy in obstacles if oy == py and ox < px], default=None), py

    return (ox, oy)

def cycles(pos, obstacles, dir):
    visited = set()

    while True:
        ox, oy = next_obstacle(pos, dir, obstacles)
        if (ox, oy, dir) in visited:
            return True
        visited.add((ox, oy, dir))
        if ox is None or oy is None:
            return False
        if dir == UP:
            pos = (ox, oy + 1)
        elif dir == DOWN:
            pos = (ox, oy - 1)
        elif dir == RIGHT:
            pos = (ox - 1, oy)
        else:
            pos = (ox + 1, oy)

        dir = turn(dir)

def move(pos, obstacles, dir, max_x, max_y):
    count = 0
    new_obstacles = set()
    keep_going = True
    while keep_going:
        px, py = pos
        ox, oy = next_obstacle(pos, dir, obstacles)
        if ox is None or oy is None:
            if ox is None:
                ox = max_x if dir == RIGHT else 0
            if oy is None:
                oy = max_y if dir == DOWN else 0
            keep_going = False

        sx, ex = min(px, ox), max(px, ox)
        sy, ey = min(py, oy), max(py, oy)

        for y in range(sy, ey + 1):
            for x in range(sx, ex + 1):
                if (x, y) in new_obstacles:
                    continue
                else:
                    obstacles.append((x, y))
                    new_obstacles.add((x, y))
                    count += 1 if cycles(pos, obstacles, dir) else 0
                    obstacles.pop()

        if dir == UP:
            pos = (ox, oy + 1)
        elif dir == DOWN:
            pos = (ox, oy - 1)
        elif dir == RIGHT:
            pos = (ox - 1, oy)
        else:
            pos = (ox + 1, oy)

        dir = turn(dir)
    print(count)

def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    obstacles, pos, max_x, max_y = parse(day_path)

    move(pos, obstacles, UP, max_x, max_y)

solve("input.txt")