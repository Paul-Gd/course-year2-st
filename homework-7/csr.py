"""
1. Build the conflict graph for a history
2. Check if the history is in CSR. This should check if the graph is acyclic.
3. Find the conflict serializable history equivalent to the given history by using topological sort.
--------------------------
Usage:
1. Install requirements
    $ pip install -r requirements.txt
2. Run csr.py and pass the history
    $ python csr.py 'r3(z)r1(y)w3(z)w1(y)r1(x)r2(y)w2(y)w1(x)r2(x)w2(x)c1c2c3
"""
import argparse
import re
from dataclasses import dataclass
from typing import List, Dict

import matplotlib.pyplot as plt
import networkx
from networkx import is_directed_acyclic_graph


@dataclass(eq=True, frozen=True)
class Op:
    op_type: str
    tr: str
    variable: str

    def __repr__(self):
        return f'{self.op_type}{self.tr}({self.variable})'


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
            else:
                dg.add_edges_from(
                    [(prev_op.tr, op.tr, 0, {'label': f'{prev_op}->{op}'}) for prev_op in ops[:i] if
                     prev_op.tr != op.tr])
    return dg


def draw_graph(filename):
    edge_labels = {(u, v): a.get('label') for u, v, a in dg.edges(data=True)}
    pos = networkx.nx.circular_layout(dg)
    networkx.nx.draw(dg, pos, with_labels=True, font_weight='bold')
    networkx.nx.draw_networkx_edge_labels(dg, pos, font_weight='bold', edge_labels=edge_labels)
    plt.savefig(filename)


def print_topological_order(dg):
    print('Topological order')
    print('\n'.join([str(s) for s in networkx.all_topological_sorts(dg)]))


parser = argparse.ArgumentParser(description='Builds the confilct graph of a history, check if in CSR and shows the '
                                             'possible equivalent serial histories.')
parser.add_argument('schedule', metavar='Schedule', type=str, nargs='+', help='schedule')

args = parser.parse_args()

pattern = re.compile(r'((?P<op>[rw])(?P<tr>\d+)\((?P<var>[a-zA-Z]+)\))')  # https://regex101.com/r/Nq0GpK/4


def get_schedule_from_string(s: str) -> List[Op]:
    return [Op(op_type, transaction, variable) for (_, op_type, transaction, variable) in pattern.findall(s)]


schedule = get_schedule_from_string(' '.join(args.schedule))

print(f's={schedule}')

dg = build_conflict_graph(schedule)

draw_graph(f'{"".join(str(s) for s in schedule)}.jpg')
if is_directed_acyclic_graph(dg):
    print('H in CSR')
    print_topological_order(dg)
else:
    print('H not in CSR')
