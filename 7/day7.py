import os
from itertools import permutations, product
from operator import add, mul

def parse(input):
    with open(input, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        lines = [l.split(":") for l in lines]
        lines = [(int(t), list(map(int, nn.split()))) for t, nn in lines]

        return lines

def valid_ops(t, nn, p):
    result = p[0](nn[0], nn[1])
    for i in range(2, len(nn)):
        result = p[i - 1](result, nn[i])
        if result > t:
            return False
    return result == t

def comb(n1, n2):
    return int(''.join([str(n1), str(n2)]))

def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    lines = parse(day_path)

    # print(sum(set([t for t, nn in lines for p in product([add, mul], repeat=len(nn)-1) if valid_ops(t, nn, p)])))
    result = 0
    for t, nn in lines:
        for p in product([add, mul, comb], repeat=len(nn)-1):
            if valid_ops(t, nn, p):
                result += t
                break

    print(result)

import cProfile
cProfile.run('solve("input.txt")')