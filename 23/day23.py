
import os
from collections import defaultdict

def parse(input):
    with open(input, 'r') as f:
        return [l.strip().split("-") for l in f.readlines()]
    
def dfs(start, visited, graph):
    stack = [start]

    connected_comp = []
    while stack:
        n = stack.pop()

        if n in visited:
            continue

        visited.add(n)
        connected_comp.append(n)
        for nn in graph[n]:
            stack.append(nn)
    
    return connected_comp
    
def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    day_path = os.path.join(day_path, input)

    connections = parse(day_path)
    graph = defaultdict(set)

    index = 0
    nodes = set([a for a, _ in connections] + [b for _, b in connections])
    nodes = { n: i for i, n in enumerate(nodes)}
    for (a, b) in connections:
        graph[a].add(b)
        graph[b].add(a)

    connected = set()
    for a in graph.keys():
        for b in graph[a]:
            for c in graph[b]:
                if a in graph[c] and c in graph[a]:
                    connected.add(frozenset([a, b, c]))
    
    part1 = sum([1 if any([ss.startswith('t') for ss in s]) else 0 for s in connected])

    cliques = []

    for a in graph.keys():
        clique = [a]
        for b in graph.keys():
            if b != a:
                if all([b in graph[c] for c in clique]):
                    clique.append(b)
        cliques.append(clique)
        

    part2 = ','.join(sorted(max(cliques, key=lambda s:len(s))))

    return part1, part2
    
    
print(solve("input.txt"))