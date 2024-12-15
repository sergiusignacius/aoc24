import os
from collections import defaultdict, Counter

def parse(input):
    with open(input, 'r') as f:
        robots = [l.strip().split(" ") for l in f.readlines()]
        robots = [tuple([tuple(map(int, p.split("=")[1].split(","))) for p in pv]) for pv in robots]

        return robots
    
def print_robots(w, h, robots):
    for y in range(h):
        for x in range(w):
            if (x, y) in robots:
                print("*", end="")

            else:
                print(".", end="")
        print()
    print()

def part2(w, h, robots):
    duration = 7000
    while True:
        positions = set()
        for r in robots:
            rp, rv = r
            x, y = rp
            vx, vy = rv

            fx = (x + vx * duration) % w
            fy = (y + vy * duration) % h

            positions.add((fx, fy))

        duration += 1

        most_x = Counter([x for x, _ in positions]).most_common()[0][0]
        lines = sorted([r for r in positions if r[0] == most_x])
        y_diff = [lines[i][1] - lines[i - 1][1] for i in range(1, len(lines))]

        max_streak = 0
        streak = 0
        for i in range(1, len(y_diff)):
            if y_diff[i] == 1:
                streak += 1
            else:
                max_streak = max(max_streak, streak)
                streak = 0

        max_streak = max(max_streak, streak)

        if max_streak >= 15:
            return duration - 1
    
def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    robots = list(parse(day_path))

    w = 101
    h = 103
    duration = 100
    q1, q2, q3, q4 = 0, 0, 0, 0
    for rp, rv in robots:
        x, y = rp
        vx, vy = rv
        
        fx = (x + vx * duration) % w
        fy = (y + vy * duration) % h

        mid_y = h // 2
        mid_x = w // 2

        if fx < mid_x and fy < mid_y:
            q1 += 1
        elif fx > mid_x and fy < mid_y:
            q2 += 1
        elif fx < mid_x and fy > mid_y:
            q3 += 1
        elif fx > mid_x and fy > mid_y:
            q4 += 1
            
    return q1 * q2 * q3 * q4, part2(w, h, robots)

print(solve("input.txt"))