import os
from functools import cmp_to_key

def parse(input):
    with open(input, 'r') as f:
        rules, pages = f.read().split("\n\n")

        rules = [r.split("|") for r in rules.split("\n")]
        rules = [tuple(map(int, r)) for r in rules]
        
        pages = [p.split(",") for p in pages.split("\n")]
        pages = [list(map(int, p)) for p in pages]

        return rules, pages
    
# def less_than(a, b, graph, pages):
#     if a not in graph:
#         return False
#     if b in graph[a]:
#         return True
#     return any([less_than(n, b, graph, pages) for n in graph[a] if n in pages])

# def compare(a, b, graph, pages):
#     if less_than(a, b, graph, pages):
#         return -1
#     return 1

# def is_sorted(pages, graph):
#     for i in range(len(pages) - 1):
#         if not less_than(pages[i], pages[i + 1], graph, set(pages)):
#             return False
#         else:
#             graph[pages[i]].add(pages[i + 1])
#     return True

# def part2(pages, graph):
#     incorrect = [p for p in pages if not is_sorted(p, graph)]

#     for i in incorrect:
#         corrected = sorted(i, key=cmp_to_key(lambda a, b: compare(a, b, graph, set(i))))
#         yield corrected[len(corrected) // 2]

def is_correct(page, graph):
    nodes = set(page)

    sorted_order = []
    indeg = { n : 0 for n in nodes }

    for node in nodes:
        for ne in graph.get(node, []):
            if ne in nodes:
                indeg[ne] += 1

    no_indeg = [n for n, v in indeg.items() if v == 0]

    while no_indeg:
        n = no_indeg.pop()
        sorted_order.append(n)
        for ne in [nn for nn in graph.get(n, []) if nn in nodes]:
            indeg[ne] -= 1
            if indeg[ne] == 0:
                no_indeg.append(ne)

    return page == sorted_order, sorted_order

def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    rules, pages = parse(day_path)

    graph = {}
    for a, b in rules:
        if a not in graph:
            graph[a] = set()
        graph[a].add(b)

    evaluated = [is_correct(p, graph) for p in pages]

    # part 1
    print(sum([sort_p[len(sort_p) // 2] for correct, sort_p in evaluated if correct]))

    # part 2
    print(sum([sort_p[len(sort_p) // 2] for correct, sort_p in evaluated if not correct]))


solve("input.txt")