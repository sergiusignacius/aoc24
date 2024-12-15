import os
import re

prize_re = re.compile(r"(?:X|Y)\=(\d+)")
increments_re = re.compile(r"(?:X|Y)\+(\d+)")

def parse_prize(p):
    l = increments_re.findall(p)
    l = list(map(int, l))

    pp = prize_re.findall(p)
    pp = list(map(int, pp))

    ax, ay, bx, by = l
    px, py = pp

    return (ax, ay), (bx, by), (px, py)

def parse(input):
    with open(input, 'r') as f:
        prizes = f.read().split("\n\n")

        return map(parse_prize, prizes)
    
def calc(a, b, p, part2=False):
    ax, ay = a
    bx, by = b
    px, py = p
    if part2:
        px += 10000000000000
        py += 10000000000000

    n = (py * bx - by * px) // (ay*bx - ax*by)
    m = (px - ax * n) // bx

    ppx = n * ax + m * bx
    ppy = n * ay + m * by

    return n * 3 + m if (ppx, ppy) == (px, py) else 0

def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    prizes = list(parse(day_path))
    part2 = True
    return sum([calc(a, b, p, part2) for (a, b, p) in prizes])

print(solve("input.txt"))