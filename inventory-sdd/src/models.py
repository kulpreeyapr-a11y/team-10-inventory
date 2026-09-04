from dataclasses import dataclass


@dataclass
class Category:
    """ข้อมูลหมวดหมู่สินค้า"""
    name: str


@dataclass
class Product:
    """ข้อมูลสินค้าในคลัง"""
    name: str
    category: Category
    quantity: int
    unit_price: float
    threshold: int