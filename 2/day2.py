import os

def parse(input):
    with open(input, 'r') as f:
        return [list(map(int, l.split())) for l in f.readlines()]

# 7 6 4 2 1
def is_decreasing(report, dampener=False):
    for i in range(1, len(report)):
        if report[i - 1] <= report[i]:
            if not dampener:
                return is_decreasing(report[0:i] + report[i+1:], True)
            return False
        elif abs(report[i - 1] - report[i]) > 3:
            if not dampener:
                return is_decreasing(report[0:i] + report[i+1:], True)
            return False
    return True

# 1 3 6 7 9
def is_increasing(report, dampener=False):
    for i in range(1, len(report)):
        if report[i - 1] >= report[i]:
            if not dampener:
                return is_increasing(report[0:i] + report[i+1:], True)
            return False
        elif abs(report[i - 1] - report[i]) > 3:
            if not dampener:
                return is_increasing(report[0:i] + report[i+1:], True)
            return False
    return True

def is_valid(report):
    return is_decreasing(report) or is_increasing(report)

def is_dec(diffs):
    return all([d < 0 for _, _, d in diffs])

def is_inc(diffs):
    return all([d > 0 for _, _, d in diffs])

def has_valid_diffs(diffs):
    return all([1 <= abs(d) <= 3 for _, _, d in diffs])

def fixable(diffs):
    return sum([1 for _, _, d in diffs if d == 0]) == 1

def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    reports = parse(day_path)

    for r in reports:
        diffs = [(i, i - 1, r[i] - r[i - 1]) for i in range(1, len(r))]

        correct = ((is_inc(diffs) or is_dec(diffs)) and has_valid_diffs(diffs))

        if not correct:
            print(r, [d for _, _, d in diffs], "fixable", fixable(diffs))
        else:
            print(correct)

    return sum([1 for r in reports if is_valid(r)])

print(solve('test.txt'))