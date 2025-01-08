
import os
import re
from collections import defaultdict
import graphlib
from itertools import combinations

gate = re.compile("([a-z0-9]+) (AND|OR|XOR) ([a-z0-9]+) -> ([a-z0-9]+)")

def parse(input):
    with open(input, 'r') as f:
        schematics = f.read().split("\n\n")

        schematics = [s.split("\n") for s in schematics]

        locks = []
        keys = []

        for s in schematics:
            item = []
            is_lock = s[0] == "#####"
            for col in range(len(s[0])):
                height = sum([1 if s[row][col] == '#' else 0 for row in range(len(s))])
                if is_lock:        
                    item.append(height - 1)
                else:
                    item.append(len(s) - height)
            if is_lock:
                locks.append(item)
            else:
                keys.append(item)

        return locks, keys

def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    locks, keys = parse(day_path)

    height = 7


    part1 = 0
    for l in locks:
        for k in keys:
            fits = True
            for (h1, h2) in zip(l, k):
                if h1 >= h2:
                    fits = False
                    print("Can't fit", h1, h2)
                    print(l)
                    print(k)
                    print()
                    break
            if fits:
                part1 += 1
            
    return part1

print(solve("input.txt"))