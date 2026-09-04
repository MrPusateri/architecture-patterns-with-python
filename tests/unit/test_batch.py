from arch_with_py.domain.batch import Batch
from arch_with_py.domain.order_line import OrderLine
from datetime import date


def make_batch_and_line(sku: str, batch_qty: int, line_qty: int):
    return (
        Batch("batch-001", sku, batch_qty, date.today()),
        OrderLine("order-123", sku, line_qty)
    )


def test_allocate_order_line_reduces_batch_quantity():
    batch, order_line = make_batch_and_line(sku="SMALL-TABLE", batch_qty=20, line_qty=2)

    batch.allocate(order_line)

    assert batch.available_quantity == 18


def test_cannot_allocate_if_available_smaller_than_required():
    batch, order_line = make_batch_and_line(sku="BLUE-CUSHION", batch_qty=1, line_qty=2)

    assert batch.can_allocate(order_line) == False


def test_can_allocate_if_available_qty_equals_to_required_qty():
    batch, order_line = make_batch_and_line(sku="BLUE-CUSHION", batch_qty=1, line_qty=1)

    assert batch.can_allocate(order_line) == True


def test_cannot_allocate_if_sku_are_different():
    batch = Batch("batch-001", "BLUE-CUSHION", 2, date.today())
    order_line = OrderLine("order-123", "SMALL-TABLE", 1)

    assert batch.can_allocate(order_line) == False


def test_allocated_quantity_equals_to_required():
    batch, order_line = make_batch_and_line(sku="BLUE-VASE", batch_qty=10, line_qty=2)

    batch.allocate(order_line)

    assert batch.allocated_quantity == 2


def test_that_allocation_is_idempotent():
    batch, order_line = make_batch_and_line(sku="BLUE-VASE", batch_qty=10, line_qty=2)

    batch.allocate(order_line)
    batch.allocate(order_line)

    assert batch.available_quantity == 8
