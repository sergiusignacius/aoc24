
import os
import re
from collections import defaultdict
import graphlib
from itertools import combinations

gate = re.compile("([a-z0-9]+) (AND|OR|XOR) ([a-z0-9]+) -> ([a-z0-9]+)")

def parse(input):
    with open(input, 'r') as f:
        init, circuit = [s.split("\n") for s in f.read().split("\n\n")]

        init = [i.split(": ") for i in init]
        init = dict([(i, int(v)) for i, v in init])

        circuit = [tuple(gate.match(c).groups()) for c in circuit]
        return init, circuit
    
def to_binary(digits):
    return ''.join([str(d) for d in digits])
    
def to_dot_name(n):
    if isinstance(n, tuple):
        return "_".join(n)
    return n

def to_dot(graph, folder, i):
    nodes = graph.keys()

    with open(os.path.join(folder, "output{}.dot".format(i)), "w") as f:
        lines = []
        lines.append('graph {\n')
        for node in nodes:
            lines.append(f'  {to_dot_name(node)}\n')
        for node in nodes:
            for target in graph[node]:
                lines.append(f'  {to_dot_name(node)} -- {to_dot_name(target)} [tooltip="{to_dot_name(node)} -- {to_dot_name(target)}"]\n')
        lines.append('}\n')
        f.writelines(lines)

def find_circuit(circuits, input_choices, input_exclusions, operand, output):
    if operand:
        circuits = [c for c in circuits if c[1] == operand]
    if input_exclusions:
        circuits = [c for c in circuits if c[0] not in input_exclusions and c[2] not in input_exclusions]
    if input_choices:
        circuits = [c for c in circuits if c[0] in input_choices or c[2] in input_choices]
    if output:
        circuits = [c for c in circuits if c[3] == output]
    
    assert len(circuits) <= 1
    return None if len(circuits) == 0 else circuits[0]

def inputs(circuit):
    return [circuit[0], circuit[1]] if circuit else None

def output(circuit):
    return circuit[3] if circuit else None

def cout(out_line, cin, graph):
    x = "x" + out_line[1:]
    y = "y" + out_line[1:]
    circuits = [g for g in graph.keys() if isinstance(g, tuple)]

    xy_and = find_circuit(circuits, {x, y}, None, 'AND', None)

    if out_line == "z00":
        return output(xy_and)
    else:
        cout_circuit = find_circuit(circuits, {output(xy_and)}, None, 'OR', None)

        if cout_circuit is not None:
            return output(cout_circuit)
        else:
            where_cin = find_circuit(circuits, {cin}, None, 'AND', None)
            # where is xy_and output used
            ccout = find_circuit(circuits, {output(where_cin)}, None, 'OR', None)
            wrong_inp = find_circuit(circuits, None, None, None, ccout[0] if ccout[2] == cin else ccout[2])

            return (wrong_inp, xy_and)


def whats_wrong(out_line, cin, graph):
    x = "x" + out_line[1:]
    y = "y" + out_line[1:]

    if out_line == "z00":
        return []
    circuits = [g for g in graph.keys() if isinstance(g, tuple)]

    incorrect = []
    out_xor = find_circuit(circuits, [cin], None, 'XOR', None)

    if output(out_xor) != out_line:
        swappable = find_circuit(circuits, None, None, None, out_line)
        incorrect.append((out_xor, swappable))
    
    return incorrect

def run_graph(graph, init, outputs):
    topo = graphlib.TopologicalSorter(graph)

    for t in list(topo.static_order()):
        if isinstance(t, tuple):
            in1, op, in2, out = t
            if op == "AND":
                init[out] = init[in1] & init[in2]
            elif op == "OR":
                init[out] = init[in1] | init[in2]
            elif op == "XOR":
                init[out] = init[in1] ^ init[in2]

    return int(''.join([str(init[k]) for k in outputs]), 2)

def swap_outputs(fr, to, graph):
    print(output(fr), output(to))
    print()
    # for fr, to in incorrect:
    fi1, fop, fi2, fout = fr
    ti1, top, ti2, tout = to

    del graph[fr]
    del graph[to]

    nfr = (fi1, fop, fi2, tout)
    nto = (ti1, top, ti2, fout)
    graph[nfr] = {fi1, fi2}
    graph[nto] = {ti1, ti2}

    graph[fout].remove(fr)
    graph[tout].remove(to)
    graph[tout].add(nfr)
    graph[fout].add(nto)

def solve(input):
    day_path = '/'.join(__file__.split('/')[:-1])
    folder = day_path
    day_path = os.path.join(day_path, input)

    init, circuit = parse(day_path)

    graph = {}
    n1 = set()
    n2 = set()
    outputs = set()
    for c in circuit:
        if c not in graph:
            graph[c] = set()
        in1, op, in2, out = c
        graph[(in1, op, in2, out)].add(in1)
        graph[(in1, op, in2, out)].add(in2)
        if out not in graph:
            graph[out] = set()
        graph[(out)].add((in1, op, in2, out))
        for nn in [n for n in [in1, in2, out] if n.startswith('z')]:
            outputs.add(nn)
        for nn in [n for n in [in1, in2, out] if n.startswith('x')]:
            n1.add(nn)
        for nn in [n for n in [in1, in2, out] if n.startswith('y')]:
            n2.add(nn)

    outputs = sorted(outputs, reverse=True)
    n1 = sorted(n1, reverse=True)
    n2 = sorted(n2, reverse=True)

    for i in init:
        graph[i] = set()

    init_c = dict(init)
    part1 = run_graph(graph, init_c, outputs)

    xx = to_binary([init_c[xd] for xd in n1])
    yy = to_binary([init_c[yd] for yd in n2])
    zz = to_binary([init_c[zd] for zd in outputs])

    expected = bin(int(xx, 2) + int(yy, 2))[2:]

    i = 0
    while True:
        init_c = dict(init)
        run_graph(graph, init_c, outputs)
        zz = to_binary([init_c[zd] for zd in outputs])
        print(expected)
        print(zz)
        
        wrong_wires = set(reversed([len(zz) - i - 1 for i, (a, b) in enumerate(zip(zz, expected)) if a != b]))

        if not wrong_wires:
            break

        to_dot(graph, folder, i)
        i += 1
        curr_cout = None
        for ww in range(len(xx)):
            z = "z" + ("0" if ww <= 9 else "") + str(ww)
            if ww in wrong_wires:
                fr, to = whats_wrong(z, curr_cout, graph)[0]
                swap_outputs(fr, to, graph)
                break
            else:
                curr_cout = cout(z, curr_cout, graph)
                if isinstance(curr_cout, tuple):
                    swap_outputs(*curr_cout, graph)
                    curr_cout = cout(z, curr_cout, graph)
                    break
                

    return part1

# z09, nnf   
    
print(solve("input.txt"))