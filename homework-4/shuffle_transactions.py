"""
Create a program that generates all possible histories of a transaction.
See `wikipedia entry for shuffle product <https://en.wikipedia.org/wiki/Shuffle_algebra#Shuffle_product>`_

Example of shuffle for 2 transactions:
T1 = w(a), r(b) - w(a) is write variable a; r(b) is read variable b
T2 = r(c), w(d)
Shuffle product:
w(a), r(b), r(c), w(d)
w(a), r(c), r(b), w(d)
...
r(c), w(d), w(a), r(b)

Note that the relative order of each transaction is kept the same: w(a) is always before r(b)
and r(c) is always before w(d) in the shuffled transaction.
-------------------------------------
Test at: `repl.it <https://repl.it/@Paulg2/VisibleWateryWordprocessing>`_
"""
import argparse
import re
from dataclasses import dataclass
from typing import List, Iterator


@dataclass(eq=True, frozen=True)
class op:
    variable: str
    op_type: str
    tr: str

    def __repr__(self):
        return f'{self.tr}-{self.op_type}({self.variable})'


def shuffle_transactions(shuffled_transaction: List[op], *unshufled_transactions: List[op]) -> Iterator[List[op]]:
    """
    Uses forward recursion. Each call takes the first operation from the all transactions, adds it to the already
    shuffled transaction list then generates the remaining unshufled transactions by excluding the selected operation.
    :param shuffled_transaction: a list of already shuffled transactions
    :param unshufled_transactions: a list of unsufled transactions
    :return: a generator that generates all the possible shuffle transactions
    """
    for tr in unshufled_transactions:
        if tr:
            yield from shuffle_transactions(shuffled_transaction + tr[:1],
                                            *(tr[1:] if tr == trans else trans for trans in unshufled_transactions))
    if not any(unshufled_transactions):
        yield shuffled_transaction


parser = argparse.ArgumentParser(description='Generate shuffle of transactions')
requiredNamed = parser.add_argument_group('Required named arguments:')
requiredNamed.add_argument('--transaction', '-t', type=str, nargs='+', action='append', help='a list of transactions')
args = parser.parse_args()
pattern = re.compile(r'((?P<op>[rw])\((?P<var>\S)\))+')  # https://regex101.com/r/Lj9HG4/1


def get_transaction_fom_string(trans_idx, unparsed_trans):
    return [op(variable, op_type, f't{trans_idx}') for (_, op_type, variable) in pattern.findall(unparsed_trans)]


transactions = [get_transaction_fom_string(i, *t) for (i, t) in enumerate(args.transaction)]

for (i, shuffled_transaction) in enumerate(shuffle_transactions([], *transactions), 1):
    print(f'#{i} {shuffled_transaction}')
