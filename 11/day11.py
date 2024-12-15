import os
from collections import Counter, defaultdict

def parse(input):
    with open(input, 'r') as f:
        return list(map(int, f.readline().strip().split()))

def transform_stone(stone):
    if stone == 0:
        yield 1
    else:
        stone_txt = str(stone)
        l = len(stone_txt)
        if l % 2 == 0:
            yield int(stone_txt[:(l // 2)])
            yield int(stone_txt[(l // 2):])
        else:
            yield stone * 2024

def blink(stones, singles):
    for s in stones:
        for ns in transform_stone(s):
            if ns <= 9 or power_of_two(len(str(ns))):
                singles[ns] += 1
            # else:
            else:
                yield ns


def power_of_two(n):
    return (n & (n - 1)) == 0

def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    stones = parse(day_path)
    counts = Counter(stones)
    for _ in range(75):
        new_counts = defaultdict(int)
        for k, v in counts.items():
            if k == 0:
                new_counts[1] += v
            else:
                k_txt = str(k)
                l = len(str(k))
                if l % 2 == 0:
                    h1, h2 = int(k_txt[:(l // 2)]), int(k_txt[(l // 2):])
                    new_counts[h1] += v
                    new_counts[h2] += v
                else:
                    new_counts[k * 2024] += v
        counts = new_counts

    print(sum(v for _, v in counts.items()))

    return len(list(stones))
    
print(solve('input.txt'))