from arch_with_py.domain.order_line import OrderLine
from typing import Optional
from datetime import date


class Batch:

    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = qty


    def allocate(self, order_line: OrderLine) -> None:
        self.available_quantity -= order_line.qty


    def can_allocate(self, order_line: OrderLine) -> bool:
        return self.available_quantity >= order_line.qty and self.sku == order_line.sku
