import os
import re
from collections import Counter

rg = re.compile(r"(\d+)\s+(\d+)")

def parse(input):
    with open(input, 'r') as f:
        matches = map(rg.match, f.readlines())
        lists = [tuple(map(int, m.groups())) for m in matches]

        return [l[0] for l in lists], [l[1] for l in lists]

def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    l1, l2 = parse(day_path)
    l1, l2 = map(sorted, [l1, l2])

    c2 = Counter(l2)

    part1 = sum(abs(e1 - e2) for (e1, e2) in zip(l1, l2))
    part2 = sum([v * c2[v] for v in l1])

    return part1, part2

print(solve('input.txt'))