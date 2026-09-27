def apply_discount(price: float, discount_percent: float) -> float:
    """คำนวณราคาสินค้าหลังหักส่วนลดเป็นเปอร์เซ็นต์"""
    if price < 0 or discount_percent < 0:
        raise ValueError("Price and discount must be non-negative")
    # แก้ไข: คำนวณส่วนลดแบบเปอร์เซ็นต์ที่ถูกต้อง (discount_percent / 100)
    return price * (1 - discount_percent / 100.0)


def bulk_total(prices: list[float], discount_percent: float) -> float:
    """คำนวณราคารวมของสินค้าหลายชิ้นหลังหักส่วนลด"""
    total = sum(prices)
    return apply_discount(total, discount_percent)


def average_price(prices: list[float]) -> float:
    """คืนราคาเฉลี่ยของรายการสินค้า"""
    # แก้ไข: เช็คถ้าลิสต์ว่าง ให้คืนค่า 0.0 ป้องกัน ZeroDivisionError
    if not prices:
        return 0.0
    return sum(prices) / len(prices)


def cheapest_n(prices: list[float], n: int) -> list[float]:
    """คืนรายการราคาที่ถูกที่สุด N รายการแรก"""
    if n <= 0:
        return []
    # แก้ไข: เรียงลำดับราคาจากน้อยไปมาก แล้วเลือกเอา N รายการแรก
    sorted_prices = sorted(prices)
    return sorted_prices[:n]