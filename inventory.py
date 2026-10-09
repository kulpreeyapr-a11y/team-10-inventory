import json
import os

# ชื่อไฟล์สำหรับเก็บข้อมูลสตร็อกสินค้า
DATA_FILE = "inventory.json"

def load_data():
    """ฟังก์ชันโหลดข้อมูลจากไฟล์ JSON"""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    """ฟังก์ชันบันทึกข้อมูลลงไฟล์ JSON"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_item_json(item_id, name, quantity, price):
    """ฟังก์ชันสำหรับเพิ่มสินค้าใหม่เข้าระบบ (US-02)"""
    items = load_data()
    
    for item in items:
        if item["id"] == item_id:
            print(f"Error: รหัสสินค้า {item_id} มีอยู่ในระบบแล้ว!")
            return False

    new_item = {
        "id": item_id,
        "name": name,
        "quantity": int(quantity),
        "price": float(price)
    }
    
    items.append(new_item)
    save_data(items)
    print(f"เพิ่มสินค้า '{name}' เข้าระบบเรียบร้อยแล้ว!")
    return True


# --- เพิ่มคลาส InventoryItem และ Inventory สำหรับใช้กับ Test ของ Lab 5 ---

class InventoryItem:
    def __init__(self, name: str, quantity: int, price: float):
        if not name or not name.strip():
            raise ValueError("ชื่อสินค้าต้องไม่ว่างเปล่า")
        if quantity < 0:
            raise ValueError("จำนวนสินค้าต้องไม่ติดลบ")
        if price <= 0:
            raise ValueError("ราคาต้องมากกว่าศูนย์")
        self.name = name.strip()
        self.quantity = quantity
        self.price = price


class Inventory:
    def __init__(self):
        self._items: dict[str, InventoryItem] = {}

    def add_item(self, name: str, quantity: int, price: float) -> InventoryItem:
        if name in self._items:
            raise ValueError(f"สินค้า '{name}' มีอยู่ในระบบแล้ว")
        item = InventoryItem(name, quantity, price)
        self._items[name] = item
        return item

    def restock(self, name: str, amount: int) -> int:
        if name not in self._items:
            raise KeyError(f"ไม่พบสินค้า '{name}' ในระบบ")
        if amount <= 0:
            raise ValueError("จำนวนที่เติมต้องมากกว่าศูนย์")
        self._items[name].quantity += amount
        return self._items[name].quantity

    def sell(self, name: str, amount: int) -> int:
        if name not in self._items:
            raise KeyError(f"ไม่พบสินค้า '{name}' ในระบบ")
        if amount <= 0:
            raise ValueError("จำนวนที่ขายต้องมากกว่าศูนย์")
        if self._items[name].quantity < amount:
            raise ValueError(
                f"สินค้า '{name}' คงเหลือ {self._items[name].quantity} ชิ้น "
                f"ไม่เพียงพอสำหรับการขาย {amount} ชิ้น"
            )
        self._items[name].quantity -= amount
        return self._items[name].quantity

    def get_total_value(self) -> float:
        return sum(
            item.quantity * item.price for item in self._items.values()
        )

    def low_stock_items(self, threshold: int) -> list[str]:
        """คืนรายชื่อสินค้าที่มีจำนวนคงเหลือ น้อยกว่าหรือเท่ากับ threshold โดยเรียงตามชื่อ"""
        filtered_items = [
            item.name for item in self._items.values() if item.quantity <= threshold
        ]
        return sorted(filtered_items)