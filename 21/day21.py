import os
from collections import Counter
from functools import cache

DELTAS = {
    '^' : (0, -1),
    'v' : (0, 1),
    '<' : (-1, 0),
    '>' : (1, 0),
}

NUMP = [
    "789",
    "456",
    "123",
    "X0A"
]

NUMP_IDX = { NUMP[y][x]: (x, y) for y in range(len(NUMP)) for x in range(len(NUMP[0]))}

DIRP = [
    "X^A",
    "<v>"
]

DIRP_IDX = { DIRP[y][x]: (x, y) for y in range(len(DIRP)) for x in range(len(DIRP[0]))}

def parse(input):
    with open(input, 'r') as f:
        return [l.strip() for l in f.readlines()]
    
def manhattan_dist(s, t, pad_idx):
    sx, sy = pad_idx[s]
    tx, ty = pad_idx[t]

    return abs(sx - tx) + abs(sy - ty)

def move_to(source, target, pad_idx):
    sx, sy = pad_idx[source]
    tx, ty = pad_idx[target]

    disp_x = tx - sx 
    disp_y = ty - sy

    moves_y = ("^" if disp_y < 0 else "v") * abs(disp_y)
    moves_x = ("<" if disp_x < 0 else ">") * abs(disp_x)

    if not moves_x:
        return moves_y
    elif not moves_y:
        return moves_x
    elif (sx + disp_x, sy) == pad_idx['X']:
        return moves_y + moves_x
    elif (sx, sy + disp_y) == pad_idx['X']:
        return moves_x + moves_y
    else:
        moveset = set(moves_x + moves_y)
        assert len(moveset) == 2

        if '^' in moveset and '<' in moveset:
            return moves_x + moves_y
        elif '^' in moveset and '>' in moveset:
            return moves_y + moves_x
        elif 'v' in moveset and '>' in moveset:
            return moves_y + moves_x
        else:
            return moves_x + moves_y

def moves(seq, start, pad, memo):
    moves = []
    for n in seq:
        nm = move_to(start, n, pad)
        moves.append(nm + "A")
        start = n

    return ''.join(moves)

def test(seq, st):
    init = moves(seq, st, DIRP_IDX, None)
    for _ in range(20):
        init = moves(init, 'A', DIRP_IDX, None)

    return len(init)

shortest_path_num = { (fr, to): move_to(fr, to, NUMP_IDX) + "A" for fr in NUMP_IDX.keys() for to in NUMP_IDX.keys() if fr != 'X' and to != 'X' }
shortest_path_dir = { (fr, to): move_to(fr, to, DIRP_IDX) + "A" for fr in DIRP_IDX.keys() for to in DIRP_IDX.keys() if fr != 'X' and to != 'X' }

@cache
def rec(start, target, depth):
    # if depth == 2:
    if depth == 25:
        return len(shortest_path_dir[start, target])
    
    presses = shortest_path_dir[(start, target)]
    ns = 'A'
    result = 0
    for p in presses:
        result += rec(ns, p, depth + 1)
        ns = p
    return result

def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    numbers = parse(day_path)

    part1 = 0
    for n in numbers:
        presses = moves(n, 'A', NUMP_IDX, None)
        s = 'A'
        result = 0
        for p in presses:
            result += rec(s, p, 1)
            s = p

        part1 += result * int(n[:-1])
    
    
    # for n in numbers:
    #     # print(n)
    #     init = moves(n, 'A', NUMP_IDX, None)
    #     for _ in range(5):
    #         init = moves(init, 'A', DIRP_IDX, None)
    #     #     print(len(init))
    #     # print()
        
    #     part1 += len(init) * int(n[:-1])
        
    return part1
    

print(solve("input.txt"))