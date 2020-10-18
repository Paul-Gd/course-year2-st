"""
Create a program that generates all possible valid transactions. A transaction is composed from
a series of read/write operations on multiple variables.

Each operation can read and write from/to a variable only once. A write operation on a variable
cannot be follow  by a read operation.

Example of transaction:
read(x), write(y), read(z), write(u)

Task: Create a program that generates all transaction where each transaction has M read
operations and N write operations.
-------------------------------------
Test at: `repl.it <https://repl.it/@Paulg2/DelayedAmusedOutliers>`_
"""
import argparse
from dataclasses import dataclass
from itertools import combinations, permutations, product
from typing import List, Set, Iterator


@dataclass(eq=True, frozen=True)
class op:
    variable: str
    op_type: str

    def __repr__(self):
        return f'{self.op_type}({self.variable})'


def generate_operations(variables: List[str], op_type: str) -> Set[op]:
    return set(op(var, op_type) for var in variables)


def generate_combinations(ops: Set[op], size: int) -> Iterator[List[op]]:
    yield from (list(el) for el in combinations(ops, size))


def generate_all_transactions(variables: List[str], reads_no: int, writes_no: int) -> Iterator[List[op]]:
    """
    All the transactions with :param reads_no reads and :param writes_no writes are generated
    by using the cartesian product of all possible reads ops ( combination of reads taken by :param reads_no)
    and all possibles writes (combinations of writes taken by :param writes_no).

    :param variables: a list of variables like ['x','y','z']
    :param reads_no: number of read operations in the generated transaction
    :param writes_no: number of write operations in the generated transaction
    :return: a generator that yields all the possible transactions
    """
    all_write_ops = generate_operations(variables, 'write')
    all_read_ops = generate_operations(variables, 'read')

    write_combinations = generate_combinations(all_write_ops, writes_no)
    read_combinations = generate_combinations(all_read_ops, reads_no)

    for (write_ops, read_ops) in product(write_combinations, read_combinations):
        print(f"possible operations= {write_ops + read_ops}")
        yield from permutations(write_ops + read_ops)


def is_valid_transaction(transaction: List[op]) -> bool:
    """
    A transaction is valid if a write operation was not encountered before on that variable.

    :param transaction: a transaction to be validated
    :return: true if the transaction is valid and false if it is not valid
    """
    previous_written_variables = set()
    for operation in transaction:
        if operation.variable in previous_written_variables:
            return False
        if operation.op_type == 'write':
            previous_written_variables.add(operation.variable)
    return True


def generate_all_valid_transactions(variables: List[str], reads: int, writes: int) -> List[op]:
    for possible_transaction in generate_all_transactions(variables, reads, writes):
        if is_valid_transaction(possible_transaction):
            yield possible_transaction


parser = argparse.ArgumentParser(description='Generate read and write transactions '
                                             'on the provided variables based '
                                             'on the number of reads and writes provided.')
requiredNamed = parser.add_argument_group('Required named arguments:')
requiredNamed.add_argument('-r', '--reads', type=int, required=True,
                           help='Set the number of read operations used in transaction')
requiredNamed.add_argument('-w', '--writes', type=int, required=True,
                           help='Set the number of write operations used in transaction')
requiredNamed.add_argument('-v', '--variables', nargs='+', required=True,
                           help='Set the variables used in transaction')
args = parser.parse_args()

for index, transaction in enumerate(generate_all_valid_transactions(**vars(args)), 1):
    print(f'#{index} -> {transaction}')

"""
python transactions.py --variables n m l --reads 2 --writes 2
possible operations= [write(n), write(l), read(l), read(n)]
#1 -> (read(l), write(l), read(n), write(n))
#2 -> (read(l), read(n), write(n), write(l))
#3 -> (read(l), read(n), write(l), write(n))
#4 -> (read(n), write(n), read(l), write(l))
#5 -> (read(n), read(l), write(n), write(l))
#6 -> (read(n), read(l), write(l), write(n))
possible operations= [write(n), write(l), read(l), read(m)]
#7 -> (write(n), read(l), write(l), read(m))
#8 -> (write(n), read(l), read(m), write(l))
#9 -> (write(n), read(m), read(l), write(l))
#10 -> (read(l), write(n), write(l), read(m))
#11 -> (read(l), write(n), read(m), write(l))
#12 -> (read(l), write(l), write(n), read(m))
#13 -> (read(l), write(l), read(m), write(n))
#14 -> (read(l), read(m), write(n), write(l))
#15 -> (read(l), read(m), write(l), write(n))
#16 -> (read(m), write(n), read(l), write(l))
#17 -> (read(m), read(l), write(n), write(l))
#18 -> (read(m), read(l), write(l), write(n))
possible operations= [write(n), write(l), read(n), read(m)]
#19 -> (write(l), read(n), write(n), read(m))
#20 -> (write(l), read(n), read(m), write(n))
#21 -> (write(l), read(m), read(n), write(n))
#22 -> (read(n), write(n), write(l), read(m))
#23 -> (read(n), write(n), read(m), write(l))
#24 -> (read(n), write(l), write(n), read(m))
#25 -> (read(n), write(l), read(m), write(n))
#26 -> (read(n), read(m), write(n), write(l))
#27 -> (read(n), read(m), write(l), write(n))
#28 -> (read(m), write(l), read(n), write(n))
#29 -> (read(m), read(n), write(n), write(l))
#30 -> (read(m), read(n), write(l), write(n))
possible operations= [write(n), write(m), read(l), read(n)]
#31 -> (write(m), read(l), read(n), write(n))
#32 -> (write(m), read(n), write(n), read(l))
#33 -> (write(m), read(n), read(l), write(n))
#34 -> (read(l), write(m), read(n), write(n))
#35 -> (read(l), read(n), write(n), write(m))
#36 -> (read(l), read(n), write(m), write(n))
#37 -> (read(n), write(n), write(m), read(l))
#38 -> (read(n), write(n), read(l), write(m))
#39 -> (read(n), write(m), write(n), read(l))
#40 -> (read(n), write(m), read(l), write(n))
#41 -> (read(n), read(l), write(n), write(m))
#42 -> (read(n), read(l), write(m), write(n))
possible operations= [write(n), write(m), read(l), read(m)]
#43 -> (write(n), read(l), read(m), write(m))
#44 -> (write(n), read(m), write(m), read(l))
#45 -> (write(n), read(m), read(l), write(m))
#46 -> (read(l), write(n), read(m), write(m))
#47 -> (read(l), read(m), write(n), write(m))
#48 -> (read(l), read(m), write(m), write(n))
#49 -> (read(m), write(n), write(m), read(l))
#50 -> (read(m), write(n), read(l), write(m))
#51 -> (read(m), write(m), write(n), read(l))
#52 -> (read(m), write(m), read(l), write(n))
#53 -> (read(m), read(l), write(n), write(m))
#54 -> (read(m), read(l), write(m), write(n))
possible operations= [write(n), write(m), read(n), read(m)]
#55 -> (read(n), write(n), read(m), write(m))
#56 -> (read(n), read(m), write(n), write(m))
#57 -> (read(n), read(m), write(m), write(n))
#58 -> (read(m), write(m), read(n), write(n))
#59 -> (read(m), read(n), write(n), write(m))
#60 -> (read(m), read(n), write(m), write(n))
possible operations= [write(l), write(m), read(l), read(n)]
#61 -> (write(m), read(l), write(l), read(n))
#62 -> (write(m), read(l), read(n), write(l))
#63 -> (write(m), read(n), read(l), write(l))
#64 -> (read(l), write(l), write(m), read(n))
#65 -> (read(l), write(l), read(n), write(m))
#66 -> (read(l), write(m), write(l), read(n))
#67 -> (read(l), write(m), read(n), write(l))
#68 -> (read(l), read(n), write(l), write(m))
#69 -> (read(l), read(n), write(m), write(l))
#70 -> (read(n), write(m), read(l), write(l))
#71 -> (read(n), read(l), write(l), write(m))
#72 -> (read(n), read(l), write(m), write(l))
possible operations= [write(l), write(m), read(l), read(m)]
#73 -> (read(l), write(l), read(m), write(m))
#74 -> (read(l), read(m), write(l), write(m))
#75 -> (read(l), read(m), write(m), write(l))
#76 -> (read(m), write(m), read(l), write(l))
#77 -> (read(m), read(l), write(l), write(m))
#78 -> (read(m), read(l), write(m), write(l))
possible operations= [write(l), write(m), read(n), read(m)]
#79 -> (write(l), read(n), read(m), write(m))
#80 -> (write(l), read(m), write(m), read(n))
#81 -> (write(l), read(m), read(n), write(m))
#82 -> (read(n), write(l), read(m), write(m))
#83 -> (read(n), read(m), write(l), write(m))
#84 -> (read(n), read(m), write(m), write(l))
#85 -> (read(m), write(l), write(m), read(n))
#86 -> (read(m), write(l), read(n), write(m))
#87 -> (read(m), write(m), write(l), read(n))
#88 -> (read(m), write(m), read(n), write(l))
#89 -> (read(m), read(n), write(l), write(m))
#90 -> (read(m), read(n), write(m), write(l))
"""

"""
python transactions.py --variables n m l --reads 3 --writes 3
possible operations= [write(l), write(m), write(n), read(n), read(l), read(m)]
#1 -> (read(n), write(n), read(l), write(l), read(m), write(m))
#2 -> (read(n), write(n), read(l), read(m), write(l), write(m))
#3 -> (read(n), write(n), read(l), read(m), write(m), write(l))
#4 -> (read(n), write(n), read(m), write(m), read(l), write(l))
#5 -> (read(n), write(n), read(m), read(l), write(l), write(m))
#6 -> (read(n), write(n), read(m), read(l), write(m), write(l))
#7 -> (read(n), read(l), write(l), write(n), read(m), write(m))
#8 -> (read(n), read(l), write(l), read(m), write(m), write(n))
#9 -> (read(n), read(l), write(l), read(m), write(n), write(m))
#10 -> (read(n), read(l), write(n), write(l), read(m), write(m))
#11 -> (read(n), read(l), write(n), read(m), write(l), write(m))
#12 -> (read(n), read(l), write(n), read(m), write(m), write(l))
#13 -> (read(n), read(l), read(m), write(l), write(m), write(n))
#14 -> (read(n), read(l), read(m), write(l), write(n), write(m))
#15 -> (read(n), read(l), read(m), write(m), write(l), write(n))
#16 -> (read(n), read(l), read(m), write(m), write(n), write(l))
#17 -> (read(n), read(l), read(m), write(n), write(l), write(m))
#18 -> (read(n), read(l), read(m), write(n), write(m), write(l))
#19 -> (read(n), read(m), write(m), write(n), read(l), write(l))
#20 -> (read(n), read(m), write(m), read(l), write(l), write(n))
#21 -> (read(n), read(m), write(m), read(l), write(n), write(l))
#22 -> (read(n), read(m), write(n), write(m), read(l), write(l))
#23 -> (read(n), read(m), write(n), read(l), write(l), write(m))
#24 -> (read(n), read(m), write(n), read(l), write(m), write(l))
#25 -> (read(n), read(m), read(l), write(l), write(m), write(n))
#26 -> (read(n), read(m), read(l), write(l), write(n), write(m))
#27 -> (read(n), read(m), read(l), write(m), write(l), write(n))
#28 -> (read(n), read(m), read(l), write(m), write(n), write(l))
#29 -> (read(n), read(m), read(l), write(n), write(l), write(m))
#30 -> (read(n), read(m), read(l), write(n), write(m), write(l))
#31 -> (read(l), write(l), read(n), write(n), read(m), write(m))
#32 -> (read(l), write(l), read(n), read(m), write(m), write(n))
#33 -> (read(l), write(l), read(n), read(m), write(n), write(m))
#34 -> (read(l), write(l), read(m), write(m), read(n), write(n))
#35 -> (read(l), write(l), read(m), read(n), write(m), write(n))
#36 -> (read(l), write(l), read(m), read(n), write(n), write(m))
#37 -> (read(l), read(n), write(l), write(n), read(m), write(m))
#38 -> (read(l), read(n), write(l), read(m), write(m), write(n))
#39 -> (read(l), read(n), write(l), read(m), write(n), write(m))
#40 -> (read(l), read(n), write(n), write(l), read(m), write(m))
#41 -> (read(l), read(n), write(n), read(m), write(l), write(m))
#42 -> (read(l), read(n), write(n), read(m), write(m), write(l))
#43 -> (read(l), read(n), read(m), write(l), write(m), write(n))
#44 -> (read(l), read(n), read(m), write(l), write(n), write(m))
#45 -> (read(l), read(n), read(m), write(m), write(l), write(n))
#46 -> (read(l), read(n), read(m), write(m), write(n), write(l))
#47 -> (read(l), read(n), read(m), write(n), write(l), write(m))
#48 -> (read(l), read(n), read(m), write(n), write(m), write(l))
#49 -> (read(l), read(m), write(l), write(m), read(n), write(n))
#50 -> (read(l), read(m), write(l), read(n), write(m), write(n))
#51 -> (read(l), read(m), write(l), read(n), write(n), write(m))
#52 -> (read(l), read(m), write(m), write(l), read(n), write(n))
#53 -> (read(l), read(m), write(m), read(n), write(l), write(n))
#54 -> (read(l), read(m), write(m), read(n), write(n), write(l))
#55 -> (read(l), read(m), read(n), write(l), write(m), write(n))
#56 -> (read(l), read(m), read(n), write(l), write(n), write(m))
#57 -> (read(l), read(m), read(n), write(m), write(l), write(n))
#58 -> (read(l), read(m), read(n), write(m), write(n), write(l))
#59 -> (read(l), read(m), read(n), write(n), write(l), write(m))
#60 -> (read(l), read(m), read(n), write(n), write(m), write(l))
#61 -> (read(m), write(m), read(n), write(n), read(l), write(l))
#62 -> (read(m), write(m), read(n), read(l), write(l), write(n))
#63 -> (read(m), write(m), read(n), read(l), write(n), write(l))
#64 -> (read(m), write(m), read(l), write(l), read(n), write(n))
#65 -> (read(m), write(m), read(l), read(n), write(l), write(n))
#66 -> (read(m), write(m), read(l), read(n), write(n), write(l))
#67 -> (read(m), read(n), write(m), write(n), read(l), write(l))
#68 -> (read(m), read(n), write(m), read(l), write(l), write(n))
#69 -> (read(m), read(n), write(m), read(l), write(n), write(l))
#70 -> (read(m), read(n), write(n), write(m), read(l), write(l))
#71 -> (read(m), read(n), write(n), read(l), write(l), write(m))
#72 -> (read(m), read(n), write(n), read(l), write(m), write(l))
#73 -> (read(m), read(n), read(l), write(l), write(m), write(n))
#74 -> (read(m), read(n), read(l), write(l), write(n), write(m))
#75 -> (read(m), read(n), read(l), write(m), write(l), write(n))
#76 -> (read(m), read(n), read(l), write(m), write(n), write(l))
#77 -> (read(m), read(n), read(l), write(n), write(l), write(m))
#78 -> (read(m), read(n), read(l), write(n), write(m), write(l))
#79 -> (read(m), read(l), write(l), write(m), read(n), write(n))
#80 -> (read(m), read(l), write(l), read(n), write(m), write(n))
#81 -> (read(m), read(l), write(l), read(n), write(n), write(m))
#82 -> (read(m), read(l), write(m), write(l), read(n), write(n))
#83 -> (read(m), read(l), write(m), read(n), write(l), write(n))
#84 -> (read(m), read(l), write(m), read(n), write(n), write(l))
#85 -> (read(m), read(l), read(n), write(l), write(m), write(n))
#86 -> (read(m), read(l), read(n), write(l), write(n), write(m))
#87 -> (read(m), read(l), read(n), write(m), write(l), write(n))
#88 -> (read(m), read(l), read(n), write(m), write(n), write(l))
#89 -> (read(m), read(l), read(n), write(n), write(l), write(m))
#90 -> (read(m), read(l), read(n), write(n), write(m), write(l))
"""
