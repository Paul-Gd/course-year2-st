"""
Compute the Herbrand semantics of the steps of a given schedule.

Notation: Hs[ri(x)] - Herbrand semantics of the read operation
                    of transaction i on variable x

* For a read operation, the Herbarnd semantics is equal to the Herbrand
semantics of the last write operation for that variable.
Formal definition:
Hs[ri(x)]=Hs[wj(x)] where wj(x) is the last write operation on x

* For a write operation of transaction i, the Herbrand semantics depends
on all the read operations of the transaction i until the write operation
Formal definition:
Hs[ri(x)]=Fix(Hs[ri(v1)],Hs[ri(v2), ... , Hs[ri(vn)]])
where
    * Fix represents that the transaction depends on multiple Herbrand transactions
    * v1, v2, ... , vn are all the previous read variables by the transaction i
-------------------------------------
Example:
Schedule: w0(x) w0(y) r1(x) r2(y) w2(x) w1(y)
Herbrand semantics of the steps of the given schedule:
Hs[w0(x)] = f0x( )
Hs[w0(y)] = f0y( )
Hs[r1(x)] = Hs[w0(x)] = f0x( )
Hs[r2(y)] = Hs[w0(y)] = f0y( )
Hs[w2(x)] = f2x(Hs[r2(y)]) = f2x(f0y( ))
Hs[w1(y)] = f1y(Hs[r1(x)]) = f1y(f0x( ))
-------------------------------------
Test at: `repl.it <https://repl.it/@Paulg2/AmusingIllustriousCopyleft>`_
-------------------------------------
usage:
$ python herbrand-semantics w0(x) w0(y) r1(x) r2(y) w2(x) w1(y)
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass(eq=True, frozen=True)
class Op:
    op_type: str
    tr: str
    variable: str

    def __repr__(self):
        return f'{self.op_type}{self.tr}({self.variable})'


@dataclass(eq=True, frozen=True)
class F:
    tr: str
    variable: str
    elements: List[F]

    def __repr__(self):
        elements = ','.join((str(e) for e in self.elements)) if self.elements else ''
        return f'f{self.tr}{self.variable}({elements})'


def get_read_herbrand_semantic(variable: str, previous_ops: List[Op], hs: Dict[Op, F]) -> F:
    """Get the Herbarnd semantic for a read operation. See the formal definition.
    """
    last_write_op = (next((op for op in reversed(previous_ops) if op.op_type == 'w' and op.variable == variable), None))
    if last_write_op:
        return hs.get(last_write_op)
    # no previous write operation was found. We can assume that the variable was written sometime, hence transaction 0
    return F('0', variable,[])


def get_write_herbrand_semantic(op: Op, previous_ops: List[Op], hs: Dict[Op, F]) -> F:
    """Get the Herbarnd semantic for a write operation. See the formal definition.
    """
    depends_on = [hs.get(prev_op) for prev_op in previous_ops if prev_op.tr == op.tr and prev_op.op_type == 'r']
    return F(op.tr, op.variable, depends_on)


def get_el_herbrand_semantic(op: Op, previous_ops: List[Op], hs: Dict[Op, F]) -> F:
    if op.op_type == 'r':
        return get_read_herbrand_semantic(op.variable, previous_ops, hs)
    return get_write_herbrand_semantic(op, previous_ops, hs)


def compute_herbrand_semantics(s: List[Op]) -> Dict[Op, F]:
    hs: Dict[Op, F] = {}
    for i, op in enumerate(s):
        hs[op] = get_el_herbrand_semantic(op, s[:i], hs)
    return hs


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('schedule', metavar='Schedule', type=str, nargs='+', help='schedule')
args = parser.parse_args()

pattern = re.compile(r'((?P<op>[rw])(?P<tr>\d+)\((?P<var>[a-zA-Z]+)\))')  # https://regex101.com/r/Nq0GpK/4


def get_schedule_from_string(schedule: str) -> List[Op]:
    return [Op(op_type, transaction, variable) for (_, op_type, transaction, variable) in pattern.findall(schedule)]


schedule = get_schedule_from_string(' '.join(args.schedule))
print(f's={schedule}')
for el, sem in compute_herbrand_semantics(schedule).items():
    print(f'Hs[{el}]={sem}')
