import pytest
from discount import calculate_discount, calculate_bulk_discount, apply_coupon

# ==========================================
# 1. Test Cases สำหรับ calculate_discount
# ==========================================

def test_calculate_discount_below_threshold():
    """ยอดซื้อน้อยกว่า 1,000 ไม่ได้ส่วนลด"""
    assert calculate_discount(500) == 0.0

def test_calculate_discount_boundary_1000():
    """ยอดซื้อครบ 1,000 บาทพอดี ได้ส่วนลด 5% (50 บาท)"""
    assert calculate_discount(1000) == 50.0

def test_calculate_discount_above_1000():
    """ยอดซื้อ 1,500 บาท ได้ส่วนลด 5% (75 บาท)"""
    assert calculate_discount(1500) == 75.0

def test_calculate_discount_boundary_5000():
    """ยอดซื้อครบ 5,000 บาทพอดี ได้ส่วนลด 10% (500 บาท)"""
    assert calculate_discount(5000) == 500.0

def test_calculate_discount_negative_amount():
    """ยอดซื้อติดลบ ต้องเกิด ValueError"""
    with pytest.raises(ValueError):
        calculate_discount(-100)


# ==========================================
# 2. Test Cases สำหรับ calculate_bulk_discount
# ==========================================

def test_calculate_bulk_discount_empty_list():
    """กรณีไม่มีรายการสินค้า (รายการว่าง) ต้องคืนค่า 0.0 ไม่พังด้วย ZeroDivisionError"""
    assert calculate_bulk_discount([]) == 0.0

def test_calculate_bulk_discount_normal_items():
    """คำนวณส่วนลดรวมสำหรับสินค้าหลายชิ้น"""
    prices = [100.0, 200.0, 300.0]
    # รวม 600 ไม่ถึง 1000 ได้ส่วนลด 0
    assert calculate_bulk_discount(prices) == 0.0

def test_calculate_bulk_discount_high_value_items():
    """รวมแล้วเกิน 1000 ได้ส่วนลดตามเกณฑ์"""
    prices = [500.0, 600.0] # รวม 1100 ได้ 5% = 55
    assert calculate_bulk_discount(prices) == 55.0


# ==========================================
# 3. Test Cases สำหรับ apply_coupon
# ==========================================

def test_apply_coupon_valid_SAVE10():
    """คูปอง SAVE10 ลดเพิ่ม 10% จากราคาสุทธิ"""
    # ราคา 1000 -> ส่วนลดขั้นต่ำ 50 -> เหลือ 950 -> คูปองลดอีก 10% (95) -> รวมลด 145
    assert apply_coupon(1000, "SAVE10") == 145.0

def test_apply_coupon_invalid_code():
    """คูปองไม่ถูกต้อง ไม่ได้ส่วนลดเพิ่ม"""
    assert apply_coupon(1000, "INVALID_CODE") == 50.0

def test_apply_coupon_empty_code():
    """ไม่ใส่คูปอง (None หรือ "") ได้ส่วนลดปกติ"""
    assert apply_coupon(1000, None) == 50.0