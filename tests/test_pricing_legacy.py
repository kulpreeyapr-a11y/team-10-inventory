import datetime

import pytest

from pricing_legacy import LOG, calc, member_points


@pytest.fixture(autouse=True)
def clear_globals():
    """ล้างค่า Global state ก่อนรัน Test ทุกครั้ง เพื่อป้องกันข้อมูลชนกัน"""
    member_points.clear()
    LOG.clear()


def test_calc_normal_price():
    # กรณีราคาปกติ: สินค้า 1 รายการ จำนวนน้อย ไม่ใช้สิทธิ์
    items = [("Apple", 5, 10.0)]
    result = calc(items)
    # 5 * 10 = 50 + vat 7% (53.5) -> round(53.5, 2) = 53.5
    assert result == 53.5


def test_calc_bulk_discount():
    # กรณีซื้อจำนวนมาก (>= 50 และ >= 100)
    items_50 = [("Book", 50, 10.0)]  # 50 * 10 * 0.95 = 475 + vat 7% = 508.25
    assert calc(items_50) == 508.25

    items_100 = [("Pen", 100, 10.0)]  # 100 * 10 * 0.9 = 900 + vat 7% = 963.0
    assert calc(items_100) == 963.0


def test_calc_zero_quantity():
    # กรณีจำนวนสินค้าเป็นศูนย์
    items = [("Ghost Item", 0, 100.0)]
    result = calc(items)
    # จำนวน <= 0 จะถูกข้าม ยอดรวมเป็น 0 + vat 0 = 0.0
    assert result == 0.0


def test_calc_with_member():
    # กรณีมีสมาชิก (ลด 5% และสะสมแต้ม 1 แต้มต่อ 100 บาท)
    items = [("Shirt", 2, 1000.0)]  # 2000 - 5% member = 1900 + vat 7% = 2033.0
    result = calc(items, member="John")
    assert result == 2033.0
    # ตรวจสอบแต้มสะสม (คำนวณจาก t ก่อน vat: 1900 / 100 = 19 แต้ม)
    assert member_points.get("John") == 19


def test_calc_coupons():
    # ทดสอบคูปอง SAVE50
    items = [("Bag", 1, 200.0)]  # 200 - 50 = 150 + vat 7% = 160.5
    assert calc(items, coupon="SAVE50") == 160.5

    # ทดสอบคูปอง HALF
    items_half = [("Shoes", 1, 200.0)]  # 200 * 0.5 = 100 + vat 7% = 107.0
    assert calc(items_half, coupon="HALF") == 107.0

    # ทดสอบคูปอง NEWYEAR ในเดือนมกราคม
    jan_date = datetime.date(2026, 1, 15)
    items_ny = [("Gift", 1, 100.0)]  # 100 * 0.8 = 80 + vat 7% = 85.6
    assert calc(items_ny, coupon="NEWYEAR", today=jan_date) == 85.6

    # ทดสอบคูปอง NEWYEAR นอกเดือนมกราคม (จะไม่ลด 20%)
    feb_date = datetime.date(2026, 2, 15)
    assert calc(items_ny, coupon="NEWYEAR", today=feb_date) == 107.0


def test_calc_negative_total_clamping():
    # ยอดติดลบ (ส่วนลดมากกว่าราคาสินค้า ให้ t ต่ำสุดที่ 0 ก่อนบวกภาษี)
    items = [("Item", 1, 10.0)]
    result = calc(items, coupon="SAVE50")  # 10 - 50 = -40 -> ปรับเป็น 0 + vat 0 = 0.0
    assert result == 0.0


def test_calc_logs_history():
    # ตรวจสอบว่าฟังก์ชันบันทึก Log และ Global State ถูกต้อง
    items = [("Box", 2, 50.0)]
    calc(items, member="Alice")
    assert len(LOG) == 1
    assert LOG[0][0] == "Alice"