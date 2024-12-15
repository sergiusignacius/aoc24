import os
from collections import defaultdict
from itertools import combinations

def parse(input):
    with open(input, 'r') as f:
        line = f.read().strip()

        return list(map(int, line))

def expand_block_list(block_list, should_print=False):
    disk = []
    for filled, free in block_list:
        for id, size in filled:
            for _ in range(size):
                if should_print:
                    print(id, end='')
                disk.append(id)
        for _ in range(free):
            print('.', end='')
            disk.append(0)
    print()
    return disk

def part1(disk):
    size = len(disk)
    new_disk = []
    block_to_move = size - 2 if size % 2 == 0 else size - 1
    remaining = disk[block_to_move]
    for i, c in enumerate(disk):
        if i >= block_to_move:
            break
        if i % 2 == 0:
            for _ in range(c):
                new_disk.append(i//2)
        else:
            free_space = c
            while free_space > 0:
                new_disk.append(block_to_move // 2)
                remaining -= 1
                free_space -= 1
                if remaining == 0:
                    block_to_move -= 2
                    remaining = disk[block_to_move]

    for _ in range(remaining):
        new_disk.append(block_to_move // 2)

    return new_disk

def part2(disk):
    size = len(disk)
    block_to_move = size - 2 if size % 2 == 0 else size - 1

    block_list = []
    for i, d in enumerate(disk):
        if i % 2 == 0:
            block_list.append(([(i // 2, d)], 0))
        else:
            block_list.append(([], d))

    expand_block_list(block_list, should_print=True)

    for file in range(block_to_move, 1, -2):
        file_size = disk[file]
        for i, block in enumerate(block_list):
            if i < file:
                filled, free = block
                if free >= file_size:
                    pf, pfree = block_list[file - 1]
                    filled.append((file // 2, file_size))
                    block_list[i] = (filled, free - file_size)
                    if file - 1 != i:
                        block_list[file - 1] = (pf, pfree + file_size)
                        block_list[file] = ([], 0)
                    else:
                        block_list[file] = ([], file_size)
                    break
    
    return expand_block_list(block_list, should_print=True)

def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    disk = parse(day_path)
    new_disk = part1(disk)
    print(sum([(i * id) for i, id in enumerate(new_disk)]))

    new_disk = part2(disk)
    print(sum([(i * id) for i, id in enumerate(new_disk)]))
        
solve('test.txt')