"""
Create a program that generates transactions. A transaction is composed from a series of read/write
operations on multiple variables.

Each operation can read and write from/to a variable only once. A write operation on a variable
cannot be follow  by a read operation.

Example of transaction:
read(x), write(y), read(z), write(u)

Task: Create a program that generates K random transaction where each transaction has M read
operations and N write operations.
-------------------------------------
Test at: `repl.it <https://repl.it/@Paulg2/DelayedAmusedOutliers>`_
"""

from dataclasses import dataclass
from random import sample, shuffle
from typing import List, Set


@dataclass(eq=True, frozen=True)
class op:
    variable: str
    op_type: str

    def __repr__(self):
        return f'{self.op_type}({self.variable})'


def generate_operations(variables: List[str], op_type: str) -> Set[op]:
    return set(op(var, op_type) for var in variables)


def generate_possible_transaction(variables: List[str], reads: int, writes: int):
    read_ops = sample(generate_operations(variables, 'read'), reads)
    write_ops = sample(generate_operations(variables, 'write'), writes)
    transaction = read_ops + write_ops
    shuffle(transaction)
    return transaction


def is_valid_transaction(transaction: List[op]) -> bool:
    previous_written_variables = set()
    for op in transaction:
        if op.variable in previous_written_variables:
            return False
        if op.op_type == 'write':
            previous_written_variables.add(op.variable)
    return True


def generate_transaction(variables: List[str], reads: int, writes: int) -> List[op]:
    while True:
        possible_transaction = generate_possible_transaction(variables, reads, writes)
        if is_valid_transaction(possible_transaction):
            return possible_transaction


variables = ['x', 'y', 'z']
transactions = 12
reads = 2
writes = 2
for _ in range(transactions):
    print(generate_transaction(variables, reads, writes))

"""
Output: $ python transactions.py
[read(x), write(y), read(z), write(x)]
[read(z), write(x), read(y), write(z)]
[read(y), read(x), write(x), write(z)]
[read(z), write(z), read(x), write(x)]
[write(x), read(y), read(z), write(y)]
[read(x), read(z), write(y), write(x)]
[read(z), write(x), read(y), write(z)]
[write(y), read(z), write(z), read(x)]
[read(y), write(x), write(y), read(z)]
[read(z), read(x), write(x), write(y)]
[read(y), read(x), write(z), write(y)]
[read(z), read(y), write(x), write(y)]
"""
