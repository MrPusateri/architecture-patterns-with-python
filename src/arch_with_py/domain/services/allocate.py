from typing import List

from arch_with_py.domain.order_line import OrderLine
from arch_with_py.domain.batch import Batch


def allocate(order_line: OrderLine, batches: List[Batch]) -> str:
    batch = next(b for b in sorted(batches) if b.can_allocate(order_line))
    batch.allocate(order_line)
    return batch.reference
