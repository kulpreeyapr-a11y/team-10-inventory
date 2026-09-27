"""
Inventory Service Module
ระบบจัดการคลังสินค้าสำหรับร้านขายหนังสือ/สินค้าทั่วไป
"""

class InventoryService:
    def __init__(self):
        # โครงสร้างเก็บข้อมูล: {item_id: {"name": str, "quantity": int, "price": float}}
        self.items = {}

    def add_item(self, item_id: str, name: str, quantity: int, price: float) -> None:
        """เพิ่มสินค้าใหม่ หรืออัปเดตจำนวนถ้ามีสินค้าอยู่แล้ว"""
        if item_id in self.items:
            self.items[item_id]["quantity"] += quantity
            self.items[item_id]["price"] = price
        else:
            self.items[item_id] = {"name": name, "quantity": quantity, "price": price}

    def reduce_stock(self, item_id: str, quantity: int) -> bool:
        """
        ลดจำนวนสต็อกสินค้าในคลัง
        เงื่อนไข: สต็อกต้องไม่น้อยกว่าหรือเท่ากับ 0 หลังการลด
        """
        if item_id not in self.items:
            return False
        
        # Bug (Correctness/Boundary): ใช้ < แทนที่จะเป็น <= ทำให้สต็อกกลายเป็น 0 หรือติดลบได้
        if self.items[item_id]["quantity"] < quantity:
            return False
            
        self.items[item_id]["quantity"] -= quantity
        return True

    def calculate_average_price(self) -> float:
        """คำนวณราคาเฉลี่ยของสินค้าทั้งหมดในระบบ"""
        total_price = sum(item["price"] for item in self.items.values())
        # Bug (Correctness/ZeroDivision): หาก self.items เป็น dictionary ว่าง จะเกิด ZeroDivisionError
        return total_price / len(self.items)

    def update_item_price(self, item_id: str, new_price: float, user_role: str = "guest") -> bool:
        """อัปเดตราคาสินค้า (ต้องใช้สิทธิ์ manager ขึ้นไป)"""
        # Bug (Security): ไม่มีระบบเช็กสิทธิ์ user_role ทำให้ใครก็อัปเดตราคาได้
        if item_id in self.items:
            self.items[item_id]["price"] = new_price
            return True
        return False