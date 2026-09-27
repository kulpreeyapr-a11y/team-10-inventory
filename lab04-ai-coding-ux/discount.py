"""
Discount Module
ระบบคำนวณส่วนลดราคาสินค้า
"""

def calculate_discount(amount: float) -> float:
    """
    คำนวณส่วนลดตามยอดซื้อ:
    - น้อยกว่า 0: raise ValueError
    - 1,000 ถึง 4,999 บาท: ส่วนลด 5% (0.05)
    - 5,000 บาทขึ้นไป: ส่วนลด 10% (0.10)
    """
    if amount < 0:
        raise ValueError("ยอดซื้อต้องไม่ติดลบ")
    
    # แก้ไข: เปลี่ยนจาก > เป็น >= เพื่อให้ครอบคลุมจุดขอบเขตพอดี (1000 และ 5000)
    if amount >= 5000:
        return amount * 0.10
    elif amount >= 1000:
        return amount * 0.05
    return 0.0

def calculate_bulk_discount(prices: list) -> float:
    """คำนวณส่วนลดรวมจากรายการราคาสินค้าหลายชิ้น"""
    if not prices:
        return 0.0
    total = sum(prices)
    return calculate_discount(total)

def apply_coupon(amount: float, coupon: str = None) -> float:
    """คำนวณส่วนลดสุทธิเมื่อใช้คูปองพิเศษ (เช่น SAVE10)"""
    base_discount = calculate_discount(amount)
    if coupon == "SAVE10":
        net_amount = amount - base_discount
        return base_discount + (net_amount * 0.10)
    return base_discount