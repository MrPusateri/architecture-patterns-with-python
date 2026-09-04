from arch_with_py.domain.order_line import OrderLine
from typing import Optional, Set
from datetime import date


class Batch:

    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_qty = qty
        self._allocated_lines: Set[OrderLine] = set()


    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocated_lines)


    @property
    def available_quantity(self) -> int:
        return self._purchased_qty - self.allocated_quantity


    def can_allocate(self, order_line: OrderLine) -> bool:
        return self.available_quantity >= order_line.qty and self.sku == order_line.sku


    def allocate(self, order_line: OrderLine) -> None:
        if self.can_allocate(order_line):
            self._allocated_lines.add(order_line)


    def can_deallocate(self, order_line: OrderLine) -> bool:
        return order_line in self._allocated_lines


    def deallocate(self, order_line: OrderLine) -> None:
        if self.can_deallocate(order_line):
            self._allocated_lines.remove(order_line)
