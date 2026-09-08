from datetime import date, timedelta
import pytest

from arch_with_py.domain.batch import Batch
from arch_with_py.domain.order_line import OrderLine
from arch_with_py.domain.services.allocate import allocate
from arch_with_py.domain.exeptions.out_of_stock import OutOfStock

today = date.today()
tomorrow = date.today() + timedelta(days=1)
later = date.today() + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, tomorrow)
    order_line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(order_line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest = Batch("earliest", "RETRO-CLOCK", 100, None)
    medium = Batch("medium", "RETRO-CLOCK", 100, tomorrow)
    latest = Batch("latest", "RETRO-CLOCK", 100, later)
    batches = [earliest, latest, medium]

    line_1 = OrderLine("order-001", "RETRO-CLOCK", 90)
    line_2 = OrderLine("order-001", "RETRO-CLOCK", 50)

    allocate(line_1, batches)
    allocate(line_2, batches)

    assert earliest.available_quantity==10
    assert medium.available_quantity==50
    assert latest.available_quantity==100


def test_returns_allocated_reference():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, tomorrow)
    order_line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocation = allocate(order_line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.reference


def test_raise_out_of_stock_exception_if_cannot_allocate():
    batch = Batch("batch-001", "SMALL-FORK", 10, eta=today)
    line1 = OrderLine("order-002", "SMALL-FORK", 10)
    line2 = OrderLine("order-001", "SMALL-FORK", 1)

    allocate(line1, [batch])

    with pytest.raises(OutOfStock, match="SMALL-FORK"):
        allocate(line2, [batch])
