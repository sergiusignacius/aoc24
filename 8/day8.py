import os
from collections import defaultdict
from itertools import combinations

def parse(input):
    with open(input, 'r') as f:
        lines = [l.strip() for l in f.readlines()]

        antennas = defaultdict(list)
        for y in range(len(lines)):
            for x in range(len(lines[0])):
                if lines[y][x] != '.':
                    antennas[lines[y][x]].append((x, y))

        return antennas, lines

def in_bounds(p, max_x, max_y):
    x, y = p
    return 0 <= x < max_x and 0 <= y < max_y

def anti(f1, f2, max_x, max_y):
    x1, y1 = f1
    x2, y2 = f2

    d = 1
    while True:
        np_x, np_y = (x2 + d * (x1 - x2), y2 + d * (y1 - y2))

        if in_bounds((np_x, np_y), max_x, max_y):
            yield np_x, np_y
            d += 1
        else:
            break

def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    antennas, lines = parse(day_path)
    antinodes = set()
    max_x = len(lines[0])
    max_y = len(lines)

    for freq, positions in antennas.items():
        print(freq, positions)
        for f1, f2 in combinations(positions, 2):
            antinodes |= set(anti(f1, f2, max_x, max_y))
            antinodes |= set(anti(f2, f1, max_x, max_y))

    print(sum([1 for p in antinodes if in_bounds(p, max_x, max_y)]))

solve('input.txt')