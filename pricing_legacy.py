# pricing_legacy.py
# โมดูลคำนวณราคาและส่วนลดของระบบ Inventory
# รีแฟกเตอร์ใหม่ให้สะอาดขึ้น อ่านง่ายขึ้น และคงพฤติกรรมเดิมครบถ้วน

from __future__ import annotations
import datetime

TAX = 0.07
member_points = {}
LOG = []

# ค่าคงที่ (Constants) อธิบายความหมายแทน Magic Numbers
BULK_DISCOUNT_TIER_1 = 50
BULK_DISCOUNT_TIER_2 = 100
BULK_RATE_TIER_1 = 0.95
BULK_RATE_TIER_2 = 0.90
MEMBER_DISCOUNT_RATE = 0.05
POINTS_PER_100_BAHT = 100


def calculate_item_subtotal(quantity: int, unit_price: float) -> float:
    """คำนวณราคารวมสินค้าแต่ละรายการ พร้อมส่วนลดตามจำนวน"""
    if quantity <= 0:
        return 0.0

    subtotal = quantity * unit_price

    if quantity >= BULK_DISCOUNT_TIER_2:
        subtotal *= BULK_RATE_TIER_2
    elif quantity >= BULK_DISCOUNT_TIER_1:
        subtotal *= BULK_RATE_TIER_1

    return subtotal


def apply_membership_and_coupons(
    subtotal_price: float, member: str | None, coupon: str | None, today: datetime.date
) -> float:
    """จัดการส่วนลดสมาชิก, การสะสมแต้ม และส่วนลดจากคูปอง"""
    t = subtotal_price

    # ส่วนลดสมาชิก
    if member is not None:
        if member not in member_points:
            member_points[member] = 0
        t *= 1.0 - MEMBER_DISCOUNT_RATE
        member_points[member] += int(t / POINTS_PER_100_BAHT)

    # ส่วนลดจากคูปอง
    if coupon is not None:
        if coupon == "SAVE50":
            t -= 50.0
        elif coupon == "HALF":
            t *= 0.5
        elif coupon == "NEWYEAR" and today.month == 1:
            t *= 0.8

    if t < 0:
        t = 0.0

    return t


def calc(items, member=None, coupon=None, today=None):
    """ฟังก์ชันหลักสำหรับคำนวณราคาสินค้า"""
    if today is None:
        today = datetime.date.today()

    # 1. คำนวณราคารวมสินค้าโดยใช้การ Unpack ตัวแปร (แก้ปัญหา Magic Index)
    total_price = 0.0
    for item_name, quantity, unit_price in items:
        total_price += calculate_item_subtotal(quantity, unit_price)

    # 2. จัดการส่วนลดและสมาชิก
    total_price = apply_membership_and_coupons(total_price, member, coupon, today)

    # 3. บวกภาษีมูลค่าเพิ่มและปัดเศษ
    total_price += total_price * TAX
    total_price = round(total_price, 2)

    # 4. บันทึกประวัติ (คงรูปแบบ Tuple 2 ค่าตามเดิม: member และ t)
    LOG.append((member, total_price))

    return total_price