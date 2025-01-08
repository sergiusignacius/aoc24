import os
from collections import defaultdict

def parse(input):
    with open(input, 'r') as f:
        return map(int, f.readlines())
    
def mix(n, v):
    return n ^ v

def prune(v):
    return v % 16777216

def evolve(n):
    n = mix(n*64, n)
    n %= 16777216

    n = mix(n // 32, n)
    n %= 16777216

    n = mix(n * 2048, n)
    n %= 16777216

    return n


def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    numbers = parse(day_path)

    part1 = 0
    seqs = []
    all = set()
    for n in numbers:
        nn = n
        nseq = defaultdict(int)
        prices = []
        prices.append(nn % 10)
        for i in range(2000):
            nn = evolve(nn)
            if i <= 1998:
                price = nn % 10
                prices.append(price)

        changes = [-1 if i == 0 else prices[i] - prices[i-1] for i in range(len(prices))]
        for i in range(1, len(changes)-3):
            ch = tuple(changes[i:i+4])
            best_price = prices[i+3]
            if ch not in nseq:
                nseq[ch] = best_price
            all.add(ch)

        seqs.append(nseq)

        part1 += nn

    part2 = 0   
    for a in all:
        part2 = max(part2, sum([ns.get(a, 0) for ns in seqs]))
    return part1, part2
    
print(solve("input.txt"))