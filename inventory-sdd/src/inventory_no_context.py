class Product:
    def __init__(self, name: str, category: str, quantity: int, unit_price: float, threshold: int):
        self.name = name
        self.category = category
        self.quantity = quantity
        self.unit_price = unit_price
        self.threshold = threshold

class InventorySystem:
    def __init__(self):
        self.products = {}
        self.notification_channels = ["Email"]  # Default channel

    def add_product(self, product: Product):
        self.products[product.name] = product

    def set_threshold(self, product_name: str, new_threshold: int):
        if product_name in self.products:
            self.products[product_name].threshold = new_threshold

    def set_notification_channels(self, channels: list):
        self.notification_channels = channels

    def record_stock_in(self, product_name: str, quantity: int):
        if product_name in self.products:
            self.products[product_name].quantity += quantity

    def record_stock_out(self, product_name: str, quantity: int):
        if product_name not in self.products:
            raise ValueError("ไม่พบสินค้าในระบบ")

        product = self.products[product_name]
        
        # ตรวจสอบสต็อกก่อนจ่าย
        if product.quantity < quantity:
            raise ValueError("สต็อกไม่เพียงพอ")

        # ตัดสต็อก
        product.quantity -= quantity

        # ตรวจสอบแจ้งเตือนสต็อกต่ำ (ต้องต่ำกว่า threshold เท่านั้น)
        if product.quantity < product.threshold:
            self._send_notification(product)

    def _send_notification(self, product: Product):
        message = f"แจ้งเตือน: สินค้า {product.name} สต็อกต่ำกว่า threshold (เหลือ {product.quantity})"
        for channel in self.notification_channels:
            if channel.lower() == "email":
                print(f"[Email Notification] ถึง ผู้จัดการ: {message}")
            elif channel.lower() == "sms":
                print(f"[SMS Notification] ถึง ผู้จัดการ: {message}")

    def generate_value_report(self):
        report = {}
        total_value = 0.0

        for product in self.products.values():
            category_value = product.quantity * product.unit_price
            if product.category in report:
                report[product.category] += category_value
            else:
                report[product.category] = category_value
            total_value += category_value

        return {"categories": report, "total_value": total_value}


# --- ตัวอย่างการใช้งานตาม Scenario ใน Spec ---
if __name__ == "__main__":
    system = InventorySystem()

    # Setup สินค้าตัวอย่าง
    product1 = Product("สายไฟ 2.5 sq.mm", "ไฟฟ้า", 20, 5000.0, 15)
    system.add_product(product1)

    print("=== ทดสอบจ่ายสินค้าแล้วสต็อกต่ำกว่า threshold ===")
    system.record_stock_out("สายไฟ 2.5 sq.mm", 8)  # เหลือ 12 (ต่ำกว่า 15) -> ต้องส่งเตือน

    print("\n=== ทดสอบรายงานมูลค่าสต็อก ===")
    product2 = Product("ท่อ PVC", "ประปา", 100, 300.0, 10)
    system.add_product(product2)
    
    report = system.generate_value_report()
    print("รายงาน:", report)