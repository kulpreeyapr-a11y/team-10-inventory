from typing import Dict, List, Optional
from src.models import Product
from src.notifiers import Notifier


class InventoryService:
    """Business Logic จัดการคลังสินค้า"""

    def __init__(self, notifiers: Optional[List[Notifier]] = None) -> None:
        """รับ Notifiers ผ่าน Constructor Injection"""
        self.products: Dict[str, Product] = {}
        self.notifiers: List[Notifier] = notifiers if notifiers is not None else []

    def add_product(self, product: Product) -> None:
        """เพิ่มสินค้าใหม่เข้าสู่ระบบ"""
        self.products[product.name] = product

    def record_stock_in(self, product_name: str, quantity: int) -> None:
        """บันทึกการรับสินค้าเข้าคลัง"""
        if product_name in self.products:
            self.products[product_name].quantity += quantity

    def record_stock_out(self, product_name: str, quantity: int) -> None:
        """บันทึกการจ่ายสินค้าออก และตรวจการแจ้งเตือนสต็อกต่ำ"""
        if product_name not in self.products:
            raise ValueError("ไม่พบสินค้าในระบบ")

        product = self.products[product_name]
        if product.quantity < quantity:
            raise ValueError("จำนวนสินค้าในสต็อกไม่เพียงพอ")

        product.quantity -= quantity

        # ส่งแจ้งเตือนเมื่อสต็อกหลังจ่าย ต่ำกว่า threshold เท่านั้น
        if product.quantity < product.threshold:
            self._notify_managers(product)

    def _notify_managers(self, product: Product) -> None:
        """แจ้งเตือนไปยังทุก Notifier"""
        message = f"สินค้า {product.name} สต็อกต่ำกว่า threshold (เหลือ {product.quantity})"
        for notifier in self.notifiers:
            notifier.send(message)

    def generate_value_report(self) -> dict:
        """รายงานมูลค่าสต็อกรวม แยกตามหมวดหมู่สินค้า"""
        categories_report: Dict[str, float] = {}
        total_value: float = 0.0

        for product in self.products.values():
            cat_name = product.category.name
            value = product.quantity * product.unit_price

            categories_report[cat_name] = categories_report.get(cat_name, 0.0) + value
            total_value += value

        return {
            "categories": categories_report,
            "total_value": total_value
        }