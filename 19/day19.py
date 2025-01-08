import os
from functools import cache

def parse(input):
    with open(input, 'r') as f:
        patterns, goals = f.read().split("\n\n")

        patterns = patterns.split(", ")
        goals = goals.split("\n")
        return patterns, goals
    
@cache
def possible(goal, patts):
    print(goal)
    if not goal:
        return 1
    success = 0
    for pat in patts:
        if goal.startswith(pat):
            print("djes", pat)
            success += possible(goal[len(pat):], patts)
            # if success > 0:
            #     break
    return success
    
def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    patts, goals = parse(day_path)
    
    return sum([possible(g, tuple(patts)) for g in goals])

print(solve("input.txt"))