from typing import List, Dict
from src.models import Product
from src.notifiers import Notifier


class InventoryService:
    """จัดการระบบคลังสินค้า และการแจ้งเตือนแบบ Observer Pattern"""
    def __init__(self) -> None:
        self.products: Dict[str, Product] = {}
        self._observers: List[Notifier] = []  # List ของ Observer (Notifier)

    def attach_observer(self, notifier: Notifier) -> None:
        """ลงทะเบียน Observer ใหม่"""
        if notifier not in self._observers:
            self._observers.append(notifier)

    def detach_observer(self, notifier: Notifier) -> None:
        """ยกเลิก Observer"""
        if notifier in self._observers:
            self._observers.remove(notifier)

    def _notify_observers(self, message: str) -> None:
        """เรียก notify ทุกตัวเมื่อเกิด event"""
        for observer in self._observers:
            observer.send(message)

    def add_product(self, product: Product) -> None:
        """เพิ่มสินค้าใหม่เข้าคลัง"""
        self.products[product.name] = product

    def record_stock_in(self, product_name: str, quantity: int) -> None:
        """บันทึกการรับสินค้าเข้าคลัง"""
        if product_name not in self.products:
            raise ValueError("ไม่พบรายการสินค้าในระบบ")
        self.products[product_name].quantity += quantity

    def record_stock_out(self, product_name: str, quantity: int) -> None:
        """บันทึกการจ่ายสินค้าออก และตรวจเช็กสต็อกต่ำกว่า threshold"""
        if product_name not in self.products:
            raise ValueError("ไม่พบรายการสินค้าในระบบ")

        product = self.products[product_name]
        if product.quantity < quantity:
            raise ValueError("สต็อกไม่เพียงพอ")

        product.quantity -= quantity

        # เช็กเงื่อนไขสต็อกต่ำ (< threshold) แล้วแจ้งเตือน Observers
        if product.quantity < product.threshold:
            msg = f"เตือนภัย: สินค้า {product.name} คงเหลือ {product.quantity} ต่ำกว่า Threshold ({product.threshold})"
            self._notify_observers(msg)

    def generate_value_report(self) -> Dict[str, float]:
        """รายงานมูลค่าสินค้าแยกตามหมวดหมู่"""
        report: Dict[str, float] = {}
        for product in self.products.values():
            category_name = product.category.name
            val = product.quantity * product.unit_price
            report[category_name] = report.get(category_name, 0.0) + val
        return report