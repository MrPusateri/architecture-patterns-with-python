from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLine:
    order_reference: str
    sku: str
    qty: int
