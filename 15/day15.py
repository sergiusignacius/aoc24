import os

def expand(c):
    if c == "@":
        return "@."
    elif c == "#":
        return "##"
    elif c == "O":
        return "[]"
    else:
        return ".."

def parse(input, part2=True):
    with open(input, 'r') as f:
        warehouse, moves = f.read().split("\n\n")
        moves = ''.join(moves.split("\n"))

        warehouse = warehouse.split("\n")
        if part2:
            warehouse = [''.join(map(expand, l)) for l in warehouse]
        
        blocked = set()
        boxes = set()
        robot = None
        for y in range(len(warehouse)):
            for x in range(len(warehouse[0])):
                if warehouse[y][x] == "@":
                    robot = (x, y)
                if warehouse[y][x] == "#":
                    blocked.add((x, y))
                if part2:
                    if warehouse[y][x] == "[":
                        boxes.add((x, y))
                else:
                    if warehouse[y][x] == "O":
                        boxes.add((x, y))

        return moves, robot, blocked, boxes

def box_at(p, boxes):
    if p in boxes:
        return p
    
    px, py = p

    return (px - 1, py) if (px - 1, py) in boxes else None

def boxes_at_vert(min_x, max_x, y, boxes):
    boxes = [box_at((i, y), boxes) for i in range(min_x, max_x + 1)]

    return [b for b in boxes if b is not None]

def box_can_move_v(box, boxes, blocked, delta):
    bx, by = box_at(box, boxes)

    return (bx, by + delta) not in blocked and (bx + 1, by + delta) not in blocked

def is_free(p, boxes, blocked):
    return box_at(p, boxes) is None and p not in blocked

def move_vert(rx, ry, boxes, blocked, delta, part2=False):
    can_move = True
    j = delta
    boxes_to_move = set()
    min_x = rx
    max_x = rx

    while len(boxes_at_vert(min_x, max_x, ry + j, boxes)) > 0:
        nboxes = boxes_at_vert(min_x, max_x, ry + j, boxes)
        boxes_to_move |= set(nboxes)
        if part2:
            min_x = min([x for x, _ in nboxes])
            max_x = max([x for x, _ in nboxes]) + 1
        j += delta

    if len(boxes_to_move) > 0:
        can_move = all([box_can_move_v(b, boxes, blocked, delta) for b in boxes_to_move])
        if can_move:
            for (bx, by) in boxes_to_move:
                boxes.remove((bx, by))
            for (bx, by) in boxes_to_move:
                boxes.add((bx, by + delta))
    else:
        can_move = is_free((rx, ry + delta), boxes, blocked)
    
    return can_move
    # else:
    #     while (rx, ry + j) in boxes:
    #         j += delta
    
    #     can_move = (rx, ry + j) not in blocked

    #     if can_move:
    #         if (rx, ry + delta) in boxes:
    #             boxes.remove((rx, ry + delta))
    #             boxes.add((rx, ry + j))

def move_horz(rx, ry, boxes, blocked, delta, part2=False):
    can_move = True
    i = delta
    if delta > 0:
        i -= 1
    while (rx + i, ry) in boxes:
        i += delta
    
    if part2:
        d = delta
        if delta > 0:
            d -= 1
        can_move = (rx + i + (1 if delta < 0 else 0), ry) not in blocked
        if can_move:
            while d != i:
                assert (rx + d, ry) in boxes
                boxes.remove((rx + d, ry))
                boxes.add((rx + d + delta // 2, ry))
                d += delta
        return can_move
    else:
        can_move = (rx + i, ry) not in blocked
        if can_move:
            if (rx + delta, ry) in boxes:
                boxes.remove((rx + delta, ry))
                boxes.add((rx + i, ry))

        return can_move

deltas = {
    "^": -1,
    "v": 1,
    "<": -1,
    ">": 1
}

def solve(input, part2):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    moves, robot, blocked, boxes = parse(day_path)
    rx, ry = robot
    for m in moves:
        if m in "v^":
            if move_vert(rx, ry, boxes, blocked, deltas[m], part2):
                ry += deltas[m]
        else:
            if move_horz(rx, ry, boxes, blocked, (2 if part2 else 1) * deltas[m], part2):
                rx += deltas[m]
    
    return sum([bx + by * 100 for (bx, by) in boxes])

print(solve("test.txt", False), solve("test.txt", True))