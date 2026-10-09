from inventory import Inventory


def test_low_stock_empty_inventory():
    inv = Inventory()
    result = inv.low_stock_items(5)
    assert result == []

def test_low_stock_all_greater():
    inv = Inventory()
    inv.add_item("Apple", 10, 20.0)
    inv.add_item("Banana", 15, 10.0)
    result = inv.low_stock_items(5)
    assert result == []

def test_low_stock_equal_threshold():
    inv = Inventory()
    inv.add_item("Apple", 5, 20.0)
    result = inv.low_stock_items(5)
    assert result == ["Apple"]

def test_low_stock_multiple_sorted():
    inv = Inventory()
    inv.add_item("Zebra", 2, 10.0)
    inv.add_item("Apple", 3, 20.0)
    inv.add_item("Mango", 1, 15.0)
    result = inv.low_stock_items(5)
    # ต้องเรียงตามชื่อ: Apple, Mango, Zebra
    assert result == ["Apple", "Mango", "Zebra"]

def test_low_stock_zero_threshold():
    inv = Inventory()
    inv.add_item("Apple", 0, 20.0)
    inv.add_item("Banana", 5, 10.0)
    result = inv.low_stock_items(0)
    assert result == ["Apple"]

def test_low_stock_negative_threshold():
    inv = Inventory()
    inv.add_item("Apple", 0, 20.0)
    inv.add_item("Banana", 5, 10.0)
    result = inv.low_stock_items(-1)
    assert result == []

def test_sell_exact_all():
    inv = Inventory()
    inv.add_item("Pen", 10, 5.0)
    remaining = inv.sell("Pen", 10)
    assert remaining == 0

def test_sell_zero_or_negative():
    inv = Inventory()
    inv.add_item("Pen", 10, 5.0)
    import pytest
    with pytest.raises(ValueError):
        inv.sell("Pen", 0)
    with pytest.raises(ValueError):
        inv.sell("Pen", -2)

def test_sell_exceed_stock():
    inv = Inventory()
    inv.add_item("Pen", 5, 5.0)
    import pytest
    with pytest.raises(ValueError):
        inv.sell("Pen", 500000000000)


def test_sell_item_not_found():
    inv = Inventory()
    import pytest
    with pytest.raises(KeyError):
        inv.sell("NonExistent", 2)

def test_sell_invalid_type():
    inv = Inventory()
    inv.add_item("Pen", 10, 5.0)
    import pytest
    with pytest.raises(TypeError):
        inv.sell("Pen", "two")