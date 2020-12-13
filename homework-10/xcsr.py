"""
Check if the history is in XCSR.
--------------------------
Usage:
1. Install requirements
    $ pip install -r requirements.txt
2. Run xcsr.py and pass the history
    $ python xcsr.py 'r3(z)r1(y)w3(z)w1(y)r1(x)r2(y)w2(y)w1(x)r2(x)w2(x)c1a2c3'
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from typing import List, Dict

import networkx
from networkx import is_directed_acyclic_graph


@dataclass(eq=True, frozen=True)
class Op:
    op_type: str
    tr: str
    variable: str
    revert: bool = False

    def __repr__(self):
        if self.variable:
            revert_op = '^-1' if self.revert else ''
            return f'{self.op_type}{self.tr}{revert_op}({self.variable})'
        return f'{self.op_type}{self.tr}'

    def reverted_op(self) -> Op:
        return Op(self.op_type, self.tr, self.variable, True)


def build_expanded_schedule(sch: List[Op]) -> List[Op]:
    expanded_sch = []
    for i, op in enumerate(sch):
        if op.op_type != 'a':
            expanded_sch.append(op)
        else:
            expanded_sch.extend(prev_op.reverted_op() for prev_op in sch[i::-1] if
                                prev_op.tr == op.tr and prev_op.op_type == 'w')
            expanded_sch.append(Op('c', op.tr, ''))
    return expanded_sch


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
                     prev_op.tr != op.tr and prev_op.op_type == 'w'])
            elif op.op_type == 'w':
                dg.add_edges_from(
                    [(prev_op.tr, op.tr, 0, {'label': f'{prev_op}->{op}'}) for prev_op in ops[:i] if
                     prev_op.tr != op.tr and prev_op.op_type in ['r', 'w']])
    return dg


parser = argparse.ArgumentParser(description='Checks if a hostory is in XCSR.')
parser.add_argument('schedule', metavar='Schedule', type=str, nargs='+', help='schedule')

args = parser.parse_args()

pattern = re.compile(r'((?P<op>[rwca])(?P<transaction>\d)(\((?P<var>[a-zA-Z])\))?)')  # https://regex101.com/r/Nq0GpK/6


def get_schedule_from_string(s: str) -> List[Op]:
    return [Op(op_type, transaction, variable) for (_, op_type, transaction, _, variable) in pattern.findall(s)]


schedule = get_schedule_from_string(' '.join(args.schedule))

print(f's={schedule}')

dg = build_conflict_graph(schedule)

if is_directed_acyclic_graph(dg):
    exp_s = build_expanded_schedule(schedule)
    print(f'exp(s)={exp_s}')
    print('H in CSR')
    if is_directed_acyclic_graph(build_conflict_graph(exp_s)):
        print('H is in XCSR!')
    else:
        print('H not in XCSR!')
else:
    print('H not in CSR')
