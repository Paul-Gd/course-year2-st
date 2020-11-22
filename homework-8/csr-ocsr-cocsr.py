"""
1. Check if the history is in CSR. See homework 7.
2. Check if the history is in OCSR.
3. Check if the history is in COCSR
--------------------------
Usage:
1. Install requirements
    $ pip install -r requirements.txt
2. Run csr-ocsr-cocsr.py and pass the history
    $ python csr-ocsr-cocsr.py 'r3(z)r1(y)w3(z)w1(y)r1(x)r2(y)w2(y)w1(x)r2(x)w2(x)c1c2c3'
"""
import argparse
import re
from dataclasses import dataclass
from typing import List, Dict

import matplotlib.pyplot as plt
import networkx
from more_itertools import pairwise, unique_everseen
from networkx import is_directed_acyclic_graph


@dataclass(eq=True, frozen=True)
class Op:
    op_type: str
    tr: str
    variable: str

    def __repr__(self):
        if self.variable:
            return f'{self.op_type}{self.tr}({self.variable})'
        return f'{self.op_type}{self.tr}'


def build_conflict_graph(sch: List[Op]) -> networkx.MultiDiGraph:
    variable_transactions: Dict[str, List[Op]] = {}
    for op in sch:
        prev_variable_ops = variable_transactions.get(op.variable, [])
        prev_variable_ops.append(op)
        variable_transactions[op.variable] = prev_variable_ops

    dg = networkx.nx.MultiDiGraph()
    dg.add_nodes_from(op.tr for op in sch)

    for var, ops in variable_transactions.items():
        for i, op in enumerate(ops):
            if op.op_type == 'r':
                dg.add_edges_from(
                    [(prev_op.tr, op.tr, 0, {'label': f'{prev_op}->{op}'}) for prev_op in ops[:i] if
                     prev_op.op_type == 'w'])
            elif op.op_type == 'w':
                dg.add_edges_from(
                    [(prev_op.tr, op.tr, 0, {'label': f'{prev_op}->{op}'}) for prev_op in ops[:i] if
                     prev_op.tr != op.tr])
    return dg


def get_equivalent_histories(dg: networkx.MultiDiGraph) -> List[List[str]]:
    return [h for h in networkx.all_topological_sorts(dg)]


def is_in_ocsr(h: List[Op], eq: List[List[str]]) -> bool:
    # List unique elements, preserving order. Modified to keep commits and first op
    first_ops = list(unique_everseen(h, lambda op: ('c', op.tr) if op.op_type == 'c' else ('rw', op.tr)))

    deps = {}
    for i, e in enumerate(first_ops):
        if e.op_type == 'c':
            ops = [op.tr for op in first_ops[i + 1:] if op.op_type != 'c']
            if ops:
                deps[e.tr] = ops

    for eq_h in eq:
        for i, tr in enumerate(eq_h):
            tr_deps = deps.get(tr, None)
            if tr_deps and not set(tr_deps).issubset(eq_h[i + 1:]):
                break
        else:
            return True
    return False


def is_in_cocsr(h: List[Op], eq: List[List[str]]) -> bool:
    tr_order = [op.tr for op in h if op.op_type == 'c']
    return any(tr_order == eq_tr for eq_tr in eq)


parser = argparse.ArgumentParser(description='Builds the confilct graph of a history, check if in CSR and shows the '
                                             'possible equivalent serial histories.')
parser.add_argument('schedule', metavar='Schedule', type=str, nargs='+', help='schedule')

args = parser.parse_args()

pattern = re.compile(r'((?P<op>[rwc])(?P<transaction>\d)(\((?P<var>[a-zA-Z])\))?)')  # https://regex101.com/r/Nq0GpK/5


def get_schedule_from_string(s: str) -> List[Op]:
    return [Op(op_type, transaction, variable) for (_, op_type, transaction, _, variable) in pattern.findall(s)]


schedule = get_schedule_from_string(' '.join(args.schedule))

print(f's={schedule}')

dg = build_conflict_graph(schedule)

if is_directed_acyclic_graph(dg):
    print('H in CSR')
    eq = get_equivalent_histories(dg)
    print('Equivalent histories\n' + '\n'.join(str(eq_h) for eq_h in eq))

    if is_in_ocsr(schedule, eq):
        print('In OCSR')
        if is_in_cocsr(schedule, eq):
            print('In COCSR')
        else:
            print('Not in COCSR')
    else:
        print('Not in OCSR')
        print('Not in COCSR')
else:
    print('H not in CSR')
    print('Not in OCSR')
    print('Not in COCSR')
