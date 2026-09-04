from dataclasses import dataclass

@dataclass
class OrderLine:
    order_reference: str
    sku: str
    qty: int