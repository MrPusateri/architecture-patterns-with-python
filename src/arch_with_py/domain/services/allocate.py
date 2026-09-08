from typing import List

from arch_with_py.domain.order_line import OrderLine
from arch_with_py.domain.batch import Batch
from arch_with_py.domain.exeptions.out_of_stock import OutOfStock


def allocate(order_line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(order_line))
        batch.allocate(order_line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {order_line.sku}")
