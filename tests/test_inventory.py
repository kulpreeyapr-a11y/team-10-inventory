from inventory import Inventory, InventoryItem

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